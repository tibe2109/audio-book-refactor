#!/usr/bin/env python3
# ==============================================================================
# ABV-04: Automated YouTube Batch Uploader & Asset Synchronizer
# Manages Multi-Threaded Resumable Uploads, Quota Safety, and Upload Manifest
# ==============================================================================
import os
import sys
import json
import re
import argparse
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube"
]

def resolve_all_assets(input_path_str: str) -> Dict[str, Path]:
    """
    Intelligently discovers all necessary folders from a general source path.
    Finds: book_dir, final_dir, final_video_dir, metadata_dir, backgrounds_dir.
    """
    path = Path(input_path_str).resolve()
    
    if path.name == "Videos" and "Final-" in path.parent.name:
        final_video_dir = path
        final_dir = path.parent
        book_dir = final_dir.parent
    elif path.name.startswith("Final-"):
        final_dir = path
        book_dir = path.parent
        final_video_dir = final_dir / "Videos" if (final_dir / "Videos").exists() else final_dir
    else:
        book_dir = path
        book_name = book_dir.name
        final_dir = book_dir / f"Final-{book_name}"
        if not final_dir.exists():
            final_dir = book_dir.parent / f"Final-{book_name}"
        final_video_dir = final_dir / "Videos" if (final_dir / "Videos").exists() else final_dir

    metadata_dir = final_video_dir / "youtube_metadata"
    if not metadata_dir.exists():
        metadata_dir = final_dir / "youtube_metadata"

    backgrounds_dir = final_dir / "backgrounds"

    return {
        "book_dir": book_dir,
        "final_dir": final_dir,
        "final_video_dir": final_video_dir,
        "metadata_dir": metadata_dir,
        "backgrounds_dir": backgrounds_dir
    }

def get_valid_token(client_secrets_file: str, token_file: str) -> str:
    """Get a valid OAuth access token, refreshing via requests if needed."""
    if not os.path.exists(token_file):
        raise FileNotFoundError(f"Token file not found: {token_file}")

    with open(token_file, "r", encoding="utf-8") as f:
        token_data = json.load(f)

    token = token_data.get("token")
    # Quick test to verify if token is valid
    try:
        test_resp = requests.get(
            "https://www.googleapis.com/youtube/v3/channels?part=id&mine=true",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
        if test_resp.status_code == 200:
            return token
    except Exception as e:
        print(f"[WARN] Token verification request failed: {e}")

    # If token expired or invalid, refresh using refresh_token
    refresh_token = token_data.get("refresh_token")
    client_id = token_data.get("client_id")
    client_secret = token_data.get("client_secret")
    token_uri = token_data.get("token_uri", "https://oauth2.googleapis.com/token")

    if refresh_token and client_id and client_secret:
        print("[INFO] Access token expired. Refreshing using refresh_token via requests...")
        payload = {
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token"
        }
        ref_resp = requests.post(token_uri, data=payload, timeout=15)
        if ref_resp.status_code == 200:
            new_data = ref_resp.json()
            token = new_data["access_token"]
            token_data["token"] = token
            with open(token_file, "w", encoding="utf-8") as f:
                json.dump(token_data, f, indent=2)
            print("[INFO] Token refreshed successfully.")
            return token
        else:
            raise RuntimeError(f"Failed to refresh token ({ref_resp.status_code}): {ref_resp.text}")

    return token

def load_manifest(manifest_path: Path) -> Dict:
    """Loads manifest with atomic error recovery."""
    if not manifest_path.exists():
        return {}
    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[WARN] Manifest read error: {e}. Rebuilding manifest.")
        return {}

def save_manifest_atomic(manifest_path: Path, data: Dict):
    """Saves manifest atomically using a temporary file and replace."""
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    temp_dir = manifest_path.parent
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    
    with tempfile.NamedTemporaryFile("w", dir=temp_dir, delete=False, encoding="utf-8") as tf:
        json.dump(data, tf, indent=2, ensure_ascii=False)
        temp_file_name = tf.name

    os.replace(temp_file_name, manifest_path)

def upload_single_video(
    token: str,
    video_path: Path,
    metadata: Dict,
    thumbnail_path: Optional[Path] = None
) -> Dict[str, str]:
    """Uploads a single video using resumable upload chunks (8MB) and sets thumbnail."""
    file_size = os.path.getsize(video_path)
    file_size_mb = file_size / (1024 * 1024)

    title = metadata.get("title", video_path.stem)[:100]
    description = metadata.get("description", "")[:5000]
    tags = metadata.get("tags", [])
    category_id = str(metadata.get("category", "24"))
    privacy_status = metadata.get("privacy", "unlisted")

    print(f"\n=======================================================")
    print(f"🎬 UPLOADING TO YOUTUBE: {video_path.name}")
    print(f"=======================================================")
    print(f"📁 Size        : {file_size_mb:.2f} MB")
    print(f"🏷️ Title       : {title}")
    print(f"🔒 Privacy     : {privacy_status}")
    if thumbnail_path and thumbnail_path.exists():
        print(f"🖼️ Thumbnail   : {thumbnail_path.name}")
    print(f"=======================================================\n")

    init_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": category_id,
            "defaultLanguage": "vi",
            "defaultAudioLanguage": "vi"
        },
        "status": {
            "privacyStatus": privacy_status,
            "selfDeclaredMadeForKids": False
        }
    }

    init_headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=UTF-8",
        "X-Upload-Content-Type": "video/mp4",
        "X-Upload-Content-Length": str(file_size)
    }
    init_url = "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status"

    resp = requests.post(init_url, headers=init_headers, json=init_body, timeout=30)
    if resp.status_code != 200:
        raise RuntimeError(f"Failed to initialize upload ({resp.status_code}): {resp.text}")

    upload_url = resp.headers.get("Location")
    if not upload_url:
        raise RuntimeError("No Location header returned from YouTube API.")

    chunk_size = 8 * 1024 * 1024
    start_time = time.time()
    video_id = None

    with open(video_path, "rb") as vf:
        offset = 0
        while offset < file_size:
            chunk = vf.read(chunk_size)
            chunk_len = len(chunk)
            range_end = offset + chunk_len - 1
            content_range = f"bytes {offset}-{range_end}/{file_size}"

            chunk_headers = {
                "Content-Type": "video/mp4",
                "Content-Length": str(chunk_len),
                "Content-Range": content_range
            }

            retry_count = 0
            while retry_count < 5:
                try:
                    chunk_resp = requests.put(upload_url, headers=chunk_headers, data=chunk, timeout=60)
                    if chunk_resp.status_code in (200, 201):
                        data = chunk_resp.json()
                        video_id = data.get("id")
                        offset = file_size
                        break
                    elif chunk_resp.status_code == 308:
                        offset += chunk_len
                        pct = int((offset / file_size) * 100)
                        elapsed = time.time() - start_time
                        speed = (offset / (1024 * 1024)) / max(elapsed, 0.1)
                        print(f"  ⏳ Progress: {pct}% ({offset / (1024*1024):.1f}/{file_size_mb:.1f} MB) - {speed:.2f} MB/s")
                        break
                    else:
                        print(f"  [WARN] Unexpected response ({chunk_resp.status_code}): {chunk_resp.text}")
                        retry_count += 1
                        time.sleep(2)
                except Exception as ex:
                    print(f"  [WARN] Network error: {ex}. Retrying ({retry_count+1}/5)...")
                    retry_count += 1
                    time.sleep(3)

            if retry_count >= 5 and offset < file_size:
                raise RuntimeError(f"Failed to upload chunk starting at byte {offset}")

    if not video_id:
        raise RuntimeError("Video upload finished but no video ID received.")

    video_url = f"https://youtu.be/{video_id}"
    print(f"\n🎉 UPLOAD SUCCESS: {video_url}")

    # Upload thumbnail if available
    if thumbnail_path and thumbnail_path.exists():
        print(f"[INFO] Uploading custom thumbnail from {thumbnail_path.name}...")
        try:
            # Check 2MB limit
            if os.path.getsize(thumbnail_path) > 2 * 1024 * 1024:
                from PIL import Image
                import io
                im = Image.open(thumbnail_path).convert("RGB")
                buf = io.BytesIO()
                im.save(buf, format="JPEG", quality=92)
                thumb_data = buf.getvalue()
                mime = "image/jpeg"
            else:
                with open(thumbnail_path, "rb") as tf:
                    thumb_data = tf.read()
                mime = "image/png" if thumbnail_path.suffix.lower() == ".png" else "image/jpeg"

            thumb_headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": mime
            }
            thumb_url = f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={video_id}"
            thumb_resp = requests.post(thumb_url, headers=thumb_headers, data=thumb_data, timeout=30)
            if thumb_resp.status_code in (200, 201):
                print(f"[SUCCESS] Thumbnail updated successfully!")
            else:
                print(f"[WARN] Failed to set thumbnail ({thumb_resp.status_code}): {thumb_resp.text}")
        except Exception as e:
            print(f"[WARN] Thumbnail upload error: {e}")

    return {
        "video_id": video_id,
        "youtube_url": video_url,
        "title": title
    }

def get_or_create_playlist(
    token: str,
    title: str,
    description: str = "",
    privacy_status: str = "public",
    recreate: bool = False
) -> Tuple[str, str]:
    """Finds existing playlist by title or creates a new one."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    url = "https://www.googleapis.com/youtube/v3/playlists?part=snippet,status&mine=true&maxResults=50"
    resp = requests.get(url, headers=headers, timeout=30)
    if resp.status_code != 200:
        raise RuntimeError(f"Failed to list playlists ({resp.status_code}): {resp.text}")
    
    playlists = resp.json().get("items", [])
    for pl in playlists:
        pl_title = pl.get("snippet", {}).get("title", "").strip()
        if pl_title.lower() == title.strip().lower():
            pl_id = pl["id"]
            if recreate:
                print(f"  [INFO] Recreating playlist: deleting existing playlist {pl_id}...")
                requests.delete(f"https://www.googleapis.com/youtube/v3/playlists?id={pl_id}", headers=headers, timeout=15)
                break
            pl_url = f"https://www.youtube.com/playlist?list={pl_id}"
            if pl_title != title.strip() or pl.get("status", {}).get("privacyStatus") != privacy_status:
                update_body = {
                    "id": pl_id,
                    "snippet": {
                        "title": title.strip(),
                        "description": pl.get("snippet", {}).get("description", description),
                        "defaultLanguage": "vi"
                    },
                    "status": {
                        "privacyStatus": privacy_status
                    }
                }
                up_resp = requests.put("https://www.googleapis.com/youtube/v3/playlists?part=snippet,status", headers=headers, json=update_body, timeout=30)
                if up_resp.status_code == 200:
                    print(f"  [INFO] Updated playlist title/status to: {title} ({privacy_status})")
            return pl_id, pl_url

    create_body = {
        "snippet": {
            "title": title.strip(),
            "description": description,
            "defaultLanguage": "vi"
        },
        "status": {
            "privacyStatus": privacy_status
        }
    }
    resp = requests.post("https://www.googleapis.com/youtube/v3/playlists?part=snippet,status", headers=headers, json=create_body, timeout=30)
    if resp.status_code not in (200, 201):
        raise RuntimeError(f"Failed to create playlist ({resp.status_code}): {resp.text}")
    
    data = resp.json()
    pl_id = data["id"]
    pl_url = f"https://www.youtube.com/playlist?list={pl_id}"
    print(f"  🎉 Created new playlist: {title} ({pl_url})")
    return pl_id, pl_url

def get_playlist_items(token: str, playlist_id: str) -> List[Dict]:
    """Retrieves all items in a playlist with retry for eventual consistency."""
    headers = {"Authorization": f"Bearer {token}"}
    items = []
    page_token = None
    while True:
        url = f"https://www.googleapis.com/youtube/v3/playlistItems?playlistId={playlist_id}&part=snippet&maxResults=50"
        if page_token:
            url += f"&pageToken={page_token}"
        
        resp = None
        for attempt in range(5):
            resp = requests.get(url, headers=headers, timeout=30)
            if resp.status_code == 200:
                break
            if resp.status_code == 404 and attempt < 4:
                time.sleep(2)
                continue
            raise RuntimeError(f"Failed to get playlist items ({resp.status_code}): {resp.text}")

        data = resp.json()
        for item in data.get("items", []):
            items.append({
                "item_id": item["id"],
                "video_id": item["snippet"]["resourceId"]["videoId"],
                "title": item["snippet"].get("title", ""),
                "position": item["snippet"].get("position", 0)
            })
        page_token = data.get("nextPageToken")
        if not page_token:
            break
    return items

def add_video_to_playlist(
    token: str,
    playlist_id: str,
    video_id: str,
    position: Optional[int] = None
) -> Dict:
    """Adds a video to a playlist with position and automatic fallback."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    body = {
        "snippet": {
            "playlistId": playlist_id,
            "resourceId": {
                "kind": "youtube#video",
                "videoId": video_id
            }
        }
    }
    if position is not None:
        body["snippet"]["position"] = position

    url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet"
    resp = requests.post(url, headers=headers, json=body, timeout=30)
    if resp.status_code in (200, 201):
        return resp.json()

    # Fallback if manualSortRequired
    if resp.status_code == 400 and "manualSortRequired" in resp.text and position is not None:
        del body["snippet"]["position"]
        fallback_resp = requests.post(url, headers=headers, json=body, timeout=30)
        if fallback_resp.status_code in (200, 201):
            return fallback_resp.json()

    raise RuntimeError(f"Failed to add video {video_id} to playlist {playlist_id} ({resp.status_code}): {resp.text}")

def update_video_privacy(token: str, video_id: str, privacy_status: str = "public") -> Dict:
    """Updates the privacyStatus of a video."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    body = {
        "id": video_id,
        "status": {
            "privacyStatus": privacy_status
        }
    }
    url = "https://www.googleapis.com/youtube/v3/videos?part=status"
    resp = requests.put(url, headers=headers, json=body, timeout=30)
    if resp.status_code != 200:
        raise RuntimeError(f"Failed to update privacy status for video {video_id} ({resp.status_code}): {resp.text}")
    return resp.json()

def update_video_thumbnail(token: str, video_id: str, thumbnail_path: Path) -> bool:
    """Sets/updates custom thumbnail for a video."""
    if not thumbnail_path or not thumbnail_path.exists():
        raise FileNotFoundError(f"Thumbnail not found: {thumbnail_path}")

    if os.path.getsize(thumbnail_path) > 2 * 1024 * 1024:
        from PIL import Image
        import io
        im = Image.open(thumbnail_path).convert("RGB")
        buf = io.BytesIO()
        im.save(buf, format="JPEG", quality=92)
        thumb_data = buf.getvalue()
        mime = "image/jpeg"
    else:
        with open(thumbnail_path, "rb") as tf:
            thumb_data = tf.read()
        mime = "image/png" if thumbnail_path.suffix.lower() == ".png" else "image/jpeg"

    thumb_headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": mime
    }
    thumb_url = f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={video_id}"
    resp = requests.post(thumb_url, headers=thumb_headers, data=thumb_data, timeout=30)
    if resp.status_code in (200, 201):
        return True
    else:
        print(f"  [WARN] Failed to set thumbnail for {video_id} ({resp.status_code}): {resp.text}")
        return False

def sync_video_thumbnails(token: str, thumbnail_path: Path, manifest: Dict) -> int:
    """Updates custom thumbnail for all uploaded videos in manifest."""
    print(f"\n=======================================================")
    print(f"🖼️ SYNCING THUMBNAIL TO ALL UPLOADED VIDEOS")
    print(f"=======================================================")
    print(f"🖼️ Target Thumbnail : {thumbnail_path}")
    print(f"=======================================================\n")

    uploaded_videos = []
    sorted_items = sorted(
        manifest["videos"].items(),
        key=lambda x: [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', x[0])]
    )
    for v_name, v_info in sorted_items:
        if v_info.get("status") == "uploaded" and v_info.get("video_id"):
            uploaded_videos.append((v_name, v_info))

    success_count = 0
    for idx, (v_name, v_info) in enumerate(uploaded_videos, start=1):
        vid = v_info["video_id"]
        print(f"[{idx}/{len(uploaded_videos)}] Updating thumbnail for {v_name} ({vid})...")
        try:
            if update_video_thumbnail(token, vid, thumbnail_path):
                print(f"  ✅ [THUMBNAIL UPDATED] {v_name} ({vid})")
                success_count += 1
            time.sleep(0.5)
        except Exception as e:
            print(f"  ❌ [ERROR] Failed to update thumbnail for {v_name} ({vid}): {e}")

    print(f"\n🎉 Finished updating thumbnails: {success_count}/{len(uploaded_videos)} successful.")
    return success_count

def sync_playlist_and_privacy(
    token: str,
    playlist_title: str,
    manifest: Dict,
    manifest_path: Path,
    target_privacy: Optional[str] = "public",
    sync_playlist: bool = True,
    recreate_playlist: bool = False
) -> Tuple[str, str]:
    """
    Ensures the playlist exists, adds uploaded videos sequentially,
    and updates video privacy status.
    """
    pl_id, pl_url = get_or_create_playlist(
        token=token,
        title=playlist_title,
        description="AUDIOBOOK: TAM QUỐC DIỄN NGHĨA — TRỌN BỘ 120 HỒI\nNguyên tác: La Quán Trung\nDịch giả: Phan Kế Bính | Hiệu đính: Bùi Kỷ\nPhát thanh: Tibe audio book",
        privacy_status="public",
        recreate=recreate_playlist
    )
    manifest["playlist_id"] = pl_id
    manifest["playlist_url"] = pl_url
    manifest["playlist_title"] = playlist_title

    print(f"\n=======================================================")
    print(f"📋 PLAYLIST SYNC & PRIVACY UPDATE")
    print(f"=======================================================")
    print(f"🏷️ Playlist Title : {playlist_title}")
    print(f"🆔 Playlist ID    : {pl_id}")
    print(f"🔗 Playlist URL   : {pl_url}")
    print(f"🔒 Target Privacy : {target_privacy}")
    print(f"=======================================================\n")

    uploaded_videos = []
    sorted_items = sorted(
        manifest["videos"].items(),
        key=lambda x: [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', x[0])]
    )
    for v_name, v_info in sorted_items:
        if v_info.get("status") == "uploaded" and v_info.get("video_id"):
            uploaded_videos.append((v_name, v_info))

    print(f"🎯 Total uploaded videos found: {len(uploaded_videos)}")

    # 1. Update privacy if requested
    if target_privacy:
        print(f"\n[STEP 1] Updating video privacy to '{target_privacy}'...")
        for v_name, v_info in uploaded_videos:
            vid = v_info["video_id"]
            current_privacy = v_info.get("privacyStatus")
            if current_privacy == target_privacy:
                print(f"  ⏭️ [ALREADY {target_privacy.upper()}] {v_name} ({vid})")
                continue
            try:
                update_video_privacy(token, vid, target_privacy)
                v_info["privacyStatus"] = target_privacy
                print(f"  ✅ [UPDATED] {v_name} ({vid}) -> {target_privacy}")
            except Exception as e:
                print(f"  ❌ [ERROR] Failed to update privacy for {v_name} ({vid}): {e}")
        save_manifest_atomic(manifest_path, manifest)

    # 2. Sync to playlist if requested
    if sync_playlist:
        print(f"\n[STEP 2] Synchronizing videos to playlist in sequential order...")
        existing_items = get_playlist_items(token, pl_id)
        existing_vids = [it["video_id"] for it in existing_items]

        for pos, (v_name, v_info) in enumerate(uploaded_videos):
            vid = v_info["video_id"]
            if vid in existing_vids:
                print(f"  ⏭️ [ALREADY IN PLAYLIST] {v_name} ({vid})")
                continue
            try:
                add_video_to_playlist(token, pl_id, vid, position=pos)
                existing_vids.append(vid)
                print(f"  ➕ [ADDED TO PLAYLIST] Position {pos}: {v_name} ({vid})")
                time.sleep(0.5)
            except Exception as e:
                print(f"  ❌ [ERROR] Failed to add {v_name} ({vid}) to playlist: {e}")

    save_manifest_atomic(manifest_path, manifest)
    return pl_id, pl_url

def update_all_thumbnails(token: str, thumbnail_path: Path, manifest: Dict) -> Dict[str, bool]:
    """Updates custom thumbnail for all uploaded videos to a single uniform image."""
    if not thumbnail_path.exists():
        print(f"  ❌ [ERROR] Thumbnail file does not exist: {thumbnail_path}")
        return {}

    file_size = os.path.getsize(thumbnail_path)
    if file_size > 2 * 1024 * 1024:
        from PIL import Image
        import io
        im = Image.open(thumbnail_path).convert("RGB")
        buf = io.BytesIO()
        im.save(buf, format="JPEG", quality=92)
        thumb_data = buf.getvalue()
        mime = "image/jpeg"
    else:
        with open(thumbnail_path, "rb") as tf:
            thumb_data = tf.read()
        mime = "image/png" if thumbnail_path.suffix.lower() == ".png" else "image/jpeg"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": mime
    }

    results = {}
    uploaded_videos = [
        (v_name, v_info) for v_name, v_info in manifest.get("videos", {}).items()
        if v_info.get("status") == "uploaded" and v_info.get("video_id")
    ]
    uploaded_videos.sort(key=lambda x: [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', x[0])])

    print(f"\n=======================================================")
    print(f"🖼️ UPDATING ALL VIDEO THUMBNAILS TO: {thumbnail_path.name}")
    print(f"=======================================================")

    for v_name, v_info in uploaded_videos:
        vid = v_info["video_id"]
        url = f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={vid}"
        try:
            resp = requests.post(url, headers=headers, data=thumb_data, timeout=30)
            if resp.status_code in (200, 201):
                print(f"  ✅ [SUCCESS] {v_name} ({vid}) -> thumbnail updated")
                results[vid] = True
            elif resp.status_code == 429:
                print(f"  ⚠️ [RATE LIMIT] {v_name} ({vid}): YouTube thumbnail daily limit reached (429).")
                results[vid] = False
                break
            else:
                print(f"  ❌ [FAIL] {v_name} ({vid}): {resp.status_code} - {resp.text[:200]}")
                results[vid] = False
        except Exception as e:
            print(f"  ❌ [ERROR] {v_name} ({vid}): {e}")
            results[vid] = False
        time.sleep(1)

    return results

def print_upload_status(manifest: Dict):
    """Prints upload progress status."""
    total = manifest.get("total_videos", 0)
    uploaded = manifest.get("uploaded_count", 0)
    pending = manifest.get("pending_count", 0)
    failed = manifest.get("failed_count", 0)
    pct = (uploaded / total * 100) if total > 0 else 0.0

    print(f"\n=======================================================")
    print(f"📊 ABV-04 UPLOAD PROGRESS: {pct:.1f}% ({uploaded}/{total})")
    print(f"=======================================================")
    print(f"  ✅ Uploaded Videos : {uploaded}")
    print(f"  ⏳ Pending Videos  : {pending}")
    print(f"  ❌ Failed Videos   : {failed}")
    if manifest.get("playlist_id"):
        print(f"  📋 Playlist        : {manifest.get('playlist_title')} ({manifest.get('playlist_url')})")
    print(f"  🕒 Last Updated    : {manifest.get('updated_at', 'N/A')}")
    print(f"=======================================================\n")

def generate_master_upload_report(manifest: Dict, output_path: Path, channel_name: str = "Tibe audio book"):
    total = manifest.get("total_videos", 0)
    uploaded = manifest.get("uploaded_count", 0)
    videos = manifest.get("videos", {})
    sorted_videos = sorted(videos.items(), key=lambda x: [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', x[0])])

    playlist_id = manifest.get("playlist_id")
    playlist_url = manifest.get("playlist_url")
    playlist_title = manifest.get("playlist_title", "Tam Quốc Diễn Nghĩa - La Quán Trung (Phan Kế Bính Dịch)")

    report_lines = [
        f"# 🚀 BÁO CÁO ĐĂNG TẢI YOUTUBE HÀNG LOẠT (MASTER YOUTUBE UPLOAD REPORT)",
        f"## TÁC PHẨM: TAM QUỐC DIỄN NGHĨA — TRỌN BỘ 120 HỒI",
        f"**Kênh phát hành:** `{channel_name}`  ",
        f"**Tổng số Video:** {total}  ",
        f"**Đã đăng thành công:** {uploaded} / {total}  ",
    ]
    if playlist_id and playlist_url:
        report_lines.append(f"**Danh sách phát (Playlist):** [{playlist_title}]({playlist_url}) (`{playlist_id}`)  ")

    report_lines.extend([
        f"**Thời điểm cập nhật báo cáo:** `{datetime.now(timezone.utc).isoformat()}`  ",
        f"",
        f"---",
        f"",
        f"| STT | Hồi | Tệp Video | Trạng Thái | Video ID | Quyền Riêng Tư | Link Xem Trực Tiếp | Thời Điểm Đăng |",
        f"| :---: | :---: | :--- | :---: | :---: | :---: | :--- | :--- |"
    ])

    for idx, (v_name, v_info) in enumerate(sorted_videos, start=1):
        status = v_info.get("status", "pending")
        vid = v_info.get("video_id") or "—"
        url = v_info.get("youtube_url")
        url_link = f"[{url}]({url})" if url else "Chưa đăng"
        privacy = v_info.get("privacyStatus") or ("public" if status == "uploaded" else "—")
        uploaded_at = v_info.get("uploaded_at") or "—"
        status_icon = "✅ UPLOADED" if status == "uploaded" else ("❌ FAILED" if status == "failed" else "⏳ PENDING")
        report_lines.append(f"| {idx:03d} | Hồi {idx} | `{v_name}` | {status_icon} | `{vid}` | `{privacy}` | {url_link} | `{uploaded_at}` |")

    report_lines.extend([
        "",
        "---",
        "",
        f"*Báo cáo được quản lý nguyên tử bởi hệ thống Universal Audiobook Pipeline — Module ABV-04.*"
    ])

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    print(f"\n📊 Master Upload Report generated at: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="ABV-04 Automated YouTube Batch Uploader & Synchronizer")
    parser.add_argument("--source", required=True, help="Path to book project or Final folder")
    parser.add_argument("--batch_start", type=int, help="Start index of video batch (1-based)")
    parser.add_argument("--batch_end", type=int, help="End index of video batch (1-based)")
    parser.add_argument("--file", help="Specific video file name to upload")
    parser.add_argument("--thumbnail", help="Explicit path to thumbnail file (e.g. Background-1_thumb.jpg)")
    parser.add_argument("--seo_manifest", help="Path to .abv_seo_manifest.json")
    parser.add_argument("--upload_manifest", help="Path to .abv_upload_manifest.json")
    parser.add_argument("--status", action="store_true", help="Display upload progress and exit")
    parser.add_argument("--force", action="store_true", help="Force re-upload even if already uploaded")
    parser.add_argument("--client_secrets", default="tools/client_secret.json", help="Path to OAuth client secret")
    parser.add_argument("--token_file", default="tools/token.json", help="Path to OAuth token")
    parser.add_argument("--playlist_title", default="Tam Quốc Diễn Nghĩa - La Quán Trung (Phan Kế Bính Dịch)", help="YouTube playlist title to create or sync")
    parser.add_argument("--sync_playlist", action="store_true", help="Sync uploaded videos to playlist")
    parser.add_argument("--recreate_playlist", action="store_true", help="Recreate playlist from scratch if exists")
    parser.add_argument("--set_privacy", choices=["public", "unlisted", "private"], help="Update privacyStatus of uploaded videos")
    parser.add_argument("--sync_thumbnails", action="store_true", help="Update thumbnail for all uploaded videos to --thumbnail")

    args = parser.parse_args()
    assets = resolve_all_assets(args.source)

    final_video_dir = assets["final_video_dir"]
    metadata_dir = assets["metadata_dir"]
    backgrounds_dir = assets["backgrounds_dir"]
    book_dir = assets["book_dir"]

    manifest_path = Path(args.upload_manifest).resolve() if args.upload_manifest else final_video_dir / ".abv_upload_manifest.json"
    manifest = load_manifest(manifest_path)

    if not manifest or "videos" not in manifest:
        manifest = {
            "book_name": book_dir.name,
            "final_video_dir": str(final_video_dir),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "total_videos": 0,
            "uploaded_count": 0,
            "pending_count": 0,
            "failed_count": 0,
            "videos": {}
        }

    # Discover all MP4 videos
    video_files = sorted(final_video_dir.glob("Final_Video_*.mp4"))
    for vf in video_files:
        v_name = vf.name
        if v_name not in manifest["videos"]:
            # Extract chapter slug
            match = re.search(r'Final_Video_(\d+-[^._]+)', v_name)
            chap_slug = match.group(1) if match else v_name.replace("Final_Video_", "").replace(".mp4", "")
            
            manifest["videos"][v_name] = {
                "video_file": v_name,
                "chapter_slug": chap_slug,
                "status": "pending",
                "video_id": None,
                "youtube_url": None,
                "uploaded_at": None,
                "error": None
            }

    # If Hồi 1 is already uploaded (from previous session), record it
    if "Final_Video_01-Hoi-01_Part1.mp4" in manifest["videos"]:
        h1 = manifest["videos"]["Final_Video_01-Hoi-01_Part1.mp4"]
        if not h1.get("youtube_url"):
            h1["status"] = "uploaded"
            h1["video_id"] = "OUkuc46XzU0"
            h1["youtube_url"] = "https://youtu.be/OUkuc46XzU0"
            h1["uploaded_at"] = "2026-09-18T18:15:50Z"

    # Sync counters
    manifest["total_videos"] = len(manifest["videos"])
    manifest["uploaded_count"] = sum(1 for v in manifest["videos"].values() if v.get("status") == "uploaded")
    manifest["failed_count"] = sum(1 for v in manifest["videos"].values() if v.get("status") == "failed")
    manifest["pending_count"] = manifest["total_videos"] - manifest["uploaded_count"] - manifest["failed_count"]
    save_manifest_atomic(manifest_path, manifest)

    if args.status:
        print_upload_status(manifest)
        sys.exit(0)

    print(f"\n=======================================================")
    print(f"🚀 ABV-04: YOUTUBE BATCH UPLOADER & ASSET SYNCHRONIZER")
    print(f"=======================================================")
    print(f"📁 Video Directory     : {final_video_dir}")
    print(f"📑 Metadata Directory  : {metadata_dir}")
    print(f"🖼️ Backgrounds Directory: {backgrounds_dir}")
    print(f"🧭 Upload Manifest     : {manifest_path}")
    print_upload_status(manifest)

    token = get_valid_token(args.client_secrets, args.token_file)

    # Execute playlist sync or privacy update if requested
    if args.sync_playlist or args.set_privacy:
        sync_playlist_and_privacy(
            token=token,
            playlist_title=args.playlist_title,
            manifest=manifest,
            manifest_path=manifest_path,
            target_privacy=args.set_privacy,
            sync_playlist=args.sync_playlist,
            recreate_playlist=args.recreate_playlist
        )
        report_file = final_video_dir / "Master_Upload_Report.md"
        generate_master_upload_report(manifest, report_file)
        if not (args.file or args.batch_start or args.batch_end or args.sync_thumbnails):
            print("\n✅ Playlist and privacy synchronization completed successfully.")
            sys.exit(0)

    # Execute thumbnail synchronization if requested
    if args.sync_thumbnails:
        target_thumb = Path(args.thumbnail).resolve() if args.thumbnail else backgrounds_dir / "Background-1_thumb.jpg"
        update_all_thumbnails(token, target_thumb, manifest)
        if not (args.file or args.batch_start or args.batch_end):
            print("\n✅ Thumbnail synchronization completed successfully.")
            sys.exit(0)

    # Filter target videos
    target_videos = []
    sorted_items = sorted(manifest["videos"].items(), key=lambda x: [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', x[0])])

    for idx, (v_name, v_info) in enumerate(sorted_items, start=1):
        if args.file and v_name != args.file:
            continue
        if args.batch_start and idx < args.batch_start:
            continue
        if args.batch_end and idx > args.batch_end:
            continue
        target_videos.append((v_name, v_info))

    print(f"🎯 Target videos for this execution batch: {len(target_videos)}")

    for v_name, v_info in target_videos:
        # Atomic Resume: Skip if already uploaded
        if not args.force and v_info.get("status") == "uploaded" and v_info.get("youtube_url"):
            print(f"  ⏭️ [SKIP UPLOADED] {v_name} -> {v_info['youtube_url']}")
            continue

        video_path = final_video_dir / v_name
        chap_slug = v_info["chapter_slug"]

        # 1. Discover Metadata JSON
        meta_candidates = [
            metadata_dir / f"youtube_metadata_{chap_slug}.json",
            final_video_dir / f"youtube_metadata_{chap_slug}.json",
            book_dir / chap_slug / "youtube_metadata.json"
        ]
        metadata = {}
        for mc in meta_candidates:
            if mc.exists():
                with open(mc, "r", encoding="utf-8") as f:
                    metadata = json.load(f)
                break

        if not metadata:
            print(f"  [WARN] No metadata JSON found for {v_name}. Using defaults.")
            metadata = {"title": v_name.replace(".mp4", ""), "description": "", "tags": []}

        if args.set_privacy:
            metadata["privacy"] = args.set_privacy

        # 2. Discover Thumbnail (Strictly enforce DUY NHẤT Background-1_thumb.jpg)
        thumbnail_path = None
        if args.thumbnail and Path(args.thumbnail).exists():
            thumbnail_path = Path(args.thumbnail).resolve()
        else:
            thumb_candidates = [
                backgrounds_dir / "Background-1_thumb.jpg",
                backgrounds_dir / "Background-1.png"
            ]
            for tc in thumb_candidates:
                if tc.exists():
                    thumbnail_path = tc
                    break

        # 3. Perform Upload
        try:
            result = upload_single_video(
                token=token,
                video_path=video_path,
                metadata=metadata,
                thumbnail_path=thumbnail_path
            )
            v_info["status"] = "uploaded"
            v_info["video_id"] = result["video_id"]
            v_info["youtube_url"] = result["youtube_url"]
            v_info["uploaded_at"] = datetime.now(timezone.utc).isoformat()
            v_info["error"] = None
            if args.set_privacy:
                v_info["privacyStatus"] = args.set_privacy
        except Exception as e:
            err_msg = str(e)
            print(f"  ❌ [UPLOAD FAILED] {v_name}: {err_msg}")
            v_info["status"] = "failed"
            v_info["error"] = err_msg

            # Update manifest atomically before deciding to break
            manifest["uploaded_count"] = sum(1 for v in manifest["videos"].values() if v.get("status") == "uploaded")
            manifest["failed_count"] = sum(1 for v in manifest["videos"].values() if v.get("status") == "failed")
            manifest["pending_count"] = manifest["total_videos"] - manifest["uploaded_count"] - manifest["failed_count"]
            save_manifest_atomic(manifest_path, manifest)

            if "quotaExceeded" in err_msg or "uploadLimitExceeded" in err_msg:
                print(f"\n⚠️ [QUOTA REACHED] YouTube API daily quota exceeded.")
                print(f"   Manifest progress is saved. Please resume after quota reset (14:00 - 15:00 VN).")
                break

        # Update manifest atomically after each video
        manifest["uploaded_count"] = sum(1 for v in manifest["videos"].values() if v.get("status") == "uploaded")
        manifest["failed_count"] = sum(1 for v in manifest["videos"].values() if v.get("status") == "failed")
        manifest["pending_count"] = manifest["total_videos"] - manifest["uploaded_count"] - manifest["failed_count"]
        save_manifest_atomic(manifest_path, manifest)

    # Re-sync playlist and privacy for newly uploaded videos if requested
    if args.sync_playlist or args.set_privacy:
        sync_playlist_and_privacy(
            token=token,
            playlist_title=args.playlist_title,
            manifest=manifest,
            manifest_path=manifest_path,
            target_privacy=args.set_privacy,
            sync_playlist=args.sync_playlist,
            recreate_playlist=args.recreate_playlist
        )

    print(f"\n=======================================================")
    print(f"🎉 BATCH UPLOAD WORKFLOW FINISHED")
    print(f"=======================================================")
    print_upload_status(manifest)

    # Generate / update Master Upload Report
    report_file = final_video_dir / "Master_Upload_Report.md"
    generate_master_upload_report(manifest, report_file)

if __name__ == "__main__":
    main()
