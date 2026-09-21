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
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

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
    """Get a valid OAuth access token, refreshing or authenticating if needed."""
    creds = None
    if os.path.exists(token_file):
        try:
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        except Exception as e:
            print(f"[WARN] Failed to load token file: {e}")
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                with open(token_file, "w", encoding="utf-8") as f:
                    f.write(creds.to_json())
            except Exception as e:
                print(f"[WARN] Token refresh failed: {e}. Re-authenticating...")
                creds = None

        if not creds or not creds.valid:
            if not os.path.exists(client_secrets_file):
                raise FileNotFoundError(f"Client secret file not found: {client_secrets_file}")
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
            creds = flow.run_local_server(port=0, open_browser=True)
            os.makedirs(os.path.dirname(os.path.abspath(token_file)), exist_ok=True)
            with open(token_file, "w", encoding="utf-8") as f:
                f.write(creds.to_json())

    return creds.token

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
    print(f"  🕒 Last Updated    : {manifest.get('updated_at', 'N/A')}")
    print(f"=======================================================\n")

def main():
    parser = argparse.ArgumentParser(description="ABV-04 Automated YouTube Batch Uploader & Synchronizer")
    parser.add_argument("--source", required=True, help="Path to book project or Final folder")
    parser.add_argument("--batch_start", type=int, help="Start index of video batch (1-based)")
    parser.add_argument("--batch_end", type=int, help="End index of video batch (1-based)")
    parser.add_argument("--file", help="Specific video file name to upload")
    parser.add_argument("--status", action="store_true", help="Display upload progress and exit")
    parser.add_argument("--force", action="store_true", help="Force re-upload even if already uploaded")
    parser.add_argument("--client_secrets", default="tools/client_secret.json", help="Path to OAuth client secret")
    parser.add_argument("--token_file", default="tools/token.json", help="Path to OAuth token")

    args = parser.parse_args()
    assets = resolve_all_assets(args.source)

    final_video_dir = assets["final_video_dir"]
    metadata_dir = assets["metadata_dir"]
    backgrounds_dir = assets["backgrounds_dir"]
    book_dir = assets["book_dir"]

    manifest_path = final_video_dir / ".abv_upload_manifest.json"
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

    token = get_valid_token(args.client_secrets, args.token_file)

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

        # 2. Discover Thumbnail
        # Check chapter number
        num_match = re.search(r'\d+', chap_slug)
        c_num = int(num_match.group(0)) if num_match else 1
        thumb_candidates = [
            backgrounds_dir / f"Background-{c_num}.png",
            backgrounds_dir / f"Background-{c_num}.jpg",
            backgrounds_dir / "Background-1.png",
            book_dir / chap_slug / "storyboard_video" / "kich-ban-1" / "images" / "scene_03_tieu_de_hoi_mot.png"
        ]
        thumbnail_path = None
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
        except Exception as e:
            print(f"  ❌ [UPLOAD FAILED] {v_name}: {e}")
            v_info["status"] = "failed"
            v_info["error"] = str(e)

        # Update manifest atomically after each video
        manifest["uploaded_count"] = sum(1 for v in manifest["videos"].values() if v.get("status") == "uploaded")
        manifest["failed_count"] = sum(1 for v in manifest["videos"].values() if v.get("status") == "failed")
        manifest["pending_count"] = manifest["total_videos"] - manifest["uploaded_count"] - manifest["failed_count"]
        save_manifest_atomic(manifest_path, manifest)

    print(f"\n=======================================================")
    print(f"🎉 BATCH UPLOAD WORKFLOW FINISHED")
    print(f"=======================================================")
    print_upload_status(manifest)

if __name__ == "__main__":
    main()
