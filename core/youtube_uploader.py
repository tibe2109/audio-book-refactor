#!/usr/bin/env python3
# ==============================================================================
# YouTube Automated Uploader & SEO Publisher
# Native Requests-based Resumable Uploader (Corporate Proxy & High Speed Compatible)
# ==============================================================================
import os
import sys
import json
import argparse
import time
from pathlib import Path

import requests
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube"
]

def get_valid_token(client_secrets_file: str, token_file: str) -> str:
    """Get a valid OAuth access token, refreshing or authenticating if needed."""
    creds = None
    if os.path.exists(token_file):
        try:
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        except Exception as e:
            print(f"[WARN] Failed to load existing token file: {e}")
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("[INFO] Refreshing access token via proxy...")
            try:
                # Use requests-backed transport for proxy compatibility
                req = Request()
                creds.refresh(req)
                with open(token_file, "w", encoding="utf-8") as f:
                    f.write(creds.to_json())
                print("[INFO] Token refreshed successfully.")
            except Exception as e:
                print(f"[WARN] Token refresh failed: {e}. Re-authenticating...")
                creds = None

        if not creds or not creds.valid:
            if not os.path.exists(client_secrets_file):
                raise FileNotFoundError(f"Client secret file not found: {client_secrets_file}")
            print(f"[INFO] Initiating OAuth authentication using {client_secrets_file}...")
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
            creds = flow.run_local_server(port=0, open_browser=True)
            os.makedirs(os.path.dirname(os.path.abspath(token_file)), exist_ok=True)
            with open(token_file, "w", encoding="utf-8") as f:
                f.write(creds.to_json())
            print(f"[INFO] Token saved to: {token_file}")

    return creds.token

def upload_video(token: str, video_path: str, title: str, description: str, tags: list,
                 category_id: str = "24", privacy_status: str = "unlisted",
                 thumbnail_path: str = None):
    """Uploads video using standard YouTube v3 Resumable Upload protocol via requests."""
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    file_size = os.path.getsize(video_path)
    file_size_mb = file_size / (1024 * 1024)

    print(f"\n=======================================================")
    print(f"🎬 PREPARING YOUTUBE UPLOAD (Proxy Compatible)")
    print(f"=======================================================")
    print(f"📁 Video File  : {video_path} ({file_size_mb:.2f} MB)")
    print(f"🏷️  Title       : {title}")
    print(f"🔒 Privacy     : {privacy_status}")
    print(f"📂 Category ID : {category_id}")
    if thumbnail_path:
        print(f"🖼️  Thumbnail   : {thumbnail_path}")
    print(f"=======================================================\n")

    # Step 1: Initialize Resumable Upload
    metadata = {
        "snippet": {
            "title": title[:100],
            "description": description[:5000],
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

    print("[INFO] Initializing resumable upload session with YouTube API...")
    resp = requests.post(init_url, headers=init_headers, json=metadata)
    if resp.status_code != 200:
        raise RuntimeError(f"Failed to initialize upload ({resp.status_code}): {resp.text}")

    upload_url = resp.headers.get("Location")
    if not upload_url:
        raise RuntimeError("No Location header returned from YouTube API.")

    print(f"[INFO] Upload session initialized successfully.")
    print(f"[INFO] Uploading video data in 8 MB chunks...")

    # Step 2: Upload Chunks (8MB chunks)
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
                        # Upload complete!
                        data = chunk_resp.json()
                        video_id = data.get("id")
                        offset = file_size
                        break
                    elif chunk_resp.status_code == 308:
                        # Resume incomplete, continue next chunk
                        offset += chunk_len
                        pct = int((offset / file_size) * 100)
                        elapsed = time.time() - start_time
                        speed = (offset / (1024 * 1024)) / max(elapsed, 0.1)
                        print(f"  ⏳ Upload Progress: {pct}% ({offset / (1024*1024):.1f}/{file_size_mb:.1f} MB) - {speed:.2f} MB/s")
                        break
                    else:
                        print(f"  [WARN] Unexpected chunk response ({chunk_resp.status_code}): {chunk_resp.text}")
                        retry_count += 1
                        time.sleep(2)
                except Exception as ex:
                    print(f"  [WARN] Network error during chunk upload: {ex}. Retrying ({retry_count+1}/5)...")
                    retry_count += 1
                    time.sleep(3)

            if retry_count >= 5 and offset < file_size:
                raise RuntimeError(f"Failed to upload chunk starting at byte {offset} after 5 retries.")

    if not video_id:
        raise RuntimeError("Video upload finished but no video ID was received.")

    video_url = f"https://youtu.be/{video_id}"
    print(f"\n🎉 VIDEO UPLOADED SUCCESSFULLY!")
    print(f"🔗 Video URL: {video_url}")

    # Step 3: Upload Thumbnail if provided
    if thumbnail_path and os.path.exists(thumbnail_path):
        print(f"\n[INFO] Uploading custom thumbnail from {thumbnail_path}...")
        try:
            # YouTube limit for custom thumbnails is 2MB
            if os.path.getsize(thumbnail_path) > 2 * 1024 * 1024:
                print("[INFO] Thumbnail exceeds 2MB limit, automatically optimizing to JPEG...")
                try:
                    from PIL import Image
                    import io
                    im = Image.open(thumbnail_path).convert("RGB")
                    buf = io.BytesIO()
                    im.save(buf, format="JPEG", quality=92)
                    thumb_data = buf.getvalue()
                    mime = "image/jpeg"
                except Exception as ce:
                    print(f"  [WARN] Thumbnail auto-compression failed: {ce}")
                    with open(thumbnail_path, "rb") as tf:
                        thumb_data = tf.read()
                    mime = "image/png" if thumbnail_path.lower().endswith(".png") else "image/jpeg"
            else:
                with open(thumbnail_path, "rb") as tf:
                    thumb_data = tf.read()
                mime = "image/png" if thumbnail_path.lower().endswith(".png") else "image/jpeg"

            thumb_headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": mime
            }
            thumb_url = f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={video_id}"
            thumb_resp = requests.post(thumb_url, headers=thumb_headers, data=thumb_data)
            if thumb_resp.status_code in (200, 201):
                print(f"[SUCCESS] Thumbnail updated successfully!")
            else:
                print(f"[WARN] Failed to set thumbnail ({thumb_resp.status_code}): {thumb_resp.text}")
        except Exception as e:
            print(f"[WARN] Error uploading thumbnail: {e}")

    return {
        "video_id": video_id,
        "video_url": video_url,
        "title": title,
        "privacy": privacy_status
    }

def main():
    parser = argparse.ArgumentParser(description="Automated YouTube Video Uploader with SEO Metadata")
    parser.add_argument("--video", required=True, help="Path to video MP4 file")
    parser.add_argument("--title", help="YouTube video title (max 100 chars)")
    parser.add_argument("--description", help="Video description text")
    parser.add_argument("--description_file", help="Path to text/markdown file containing description")
    parser.add_argument("--tags", help="Comma-separated tags")
    parser.add_argument("--tags_file", help="Path to file containing tags")
    parser.add_argument("--privacy", choices=["public", "unlisted", "private"], default="unlisted", help="Video privacy status")
    parser.add_argument("--category", default="24", help="YouTube Category ID (24=Entertainment, 27=Education, 22=People)")
    parser.add_argument("--thumbnail", help="Path to thumbnail image file (JPG/PNG)")
    parser.add_argument("--meta_json", help="Path to JSON file containing title, description, tags, etc.")
    parser.add_argument("--client_secrets", default="tools/client_secret.json", help="Path to OAuth client secret JSON")
    parser.add_argument("--token_file", default="tools/token.json", help="Path to save/load OAuth token")

    args = parser.parse_args()

    title = args.title or ""
    description = args.description or ""
    tags = [t.strip() for t in args.tags.split(",")] if args.tags else []
    thumbnail = args.thumbnail
    privacy = args.privacy

    if args.meta_json and os.path.exists(args.meta_json):
        with open(args.meta_json, "r", encoding="utf-8") as f:
            meta = json.load(f)
            title = meta.get("title", title)
            description = meta.get("description", description)
            if "tags" in meta:
                tags = meta["tags"] if isinstance(meta["tags"], list) else [t.strip() for t in meta["tags"].split(",")]
            thumbnail = meta.get("thumbnail", thumbnail)
            privacy = meta.get("privacy", privacy)

    if args.description_file and os.path.exists(args.description_file):
        with open(args.description_file, "r", encoding="utf-8") as f:
            description = f.read()

    if args.tags_file and os.path.exists(args.tags_file):
        with open(args.tags_file, "r", encoding="utf-8") as f:
            tags = [t.strip() for t in f.read().split(",") if t.strip()]

    if not title:
        title = Path(args.video).stem

    token = get_valid_token(args.client_secrets, args.token_file)
    upload_video(
        token=token,
        video_path=args.video,
        title=title,
        description=description,
        tags=tags,
        category_id=args.category,
        privacy_status=privacy,
        thumbnail_path=thumbnail
    )

if __name__ == "__main__":
    main()
