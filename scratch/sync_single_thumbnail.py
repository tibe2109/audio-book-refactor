#!/usr/bin/env python3
# ==============================================================================
# SCRIPT: Sync Single Master Thumbnail to All 11 YouTube Videos
# Enforces User Rule: 100% videos (Hồi 1 - 11) must use Background-1_thumb.jpg
# ==============================================================================
import os
import sys
import json
import io
from pathlib import Path
import requests
from PIL import Image

TOKEN_FILE = Path("tools/token.json")
THUMBNAIL_PATH = Path("/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/Final-Tam-Quoc-Dien-Nghia/backgrounds/Background-1_thumb.jpg")

VIDEOS = [
    {"index": 1, "slug": "01-Hoi-01", "video_id": "OUkuc46XzU0", "title": "Hồi 1"},
    {"index": 2, "slug": "02-Hoi-02", "video_id": "gX4nCYgFc-w", "title": "Hồi 2"},
    {"index": 3, "slug": "03-Hoi-03", "video_id": "YwbmLbJzJiY", "title": "Hồi 3"},
    {"index": 4, "slug": "04-Hoi-04", "video_id": "yEBLoLZJZAE", "title": "Hồi 4"},
    {"index": 5, "slug": "05-Hoi-05", "video_id": "ejo6urjRllM", "title": "Hồi 5"},
    {"index": 6, "slug": "06-Hoi-06", "video_id": "oUWk27df3OU", "title": "Hồi 6"},
    {"index": 7, "slug": "07-Hoi-07", "video_id": "8sH1a1HbB4E", "title": "Hồi 7"},
    {"index": 8, "slug": "08-Hoi-08", "video_id": "DHk8MYo038I", "title": "Hồi 8"},
    {"index": 9, "slug": "09-Hoi-09", "video_id": "1Q91IwPWl0U", "title": "Hồi 9"},
    {"index": 10, "slug": "10-Hoi-10", "video_id": "-HNjsNSx4tg", "title": "Hồi 10"},
    {"index": 11, "slug": "11-Hoi-11", "video_id": "hMz3okrct30", "title": "Hồi 11"},
]

def get_token():
    with open(TOKEN_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("token")

def main():
    if not THUMBNAIL_PATH.exists():
        print(f"❌ Thumbnail not found: {THUMBNAIL_PATH}")
        sys.exit(1)
        
    print(f"🖼️ Target Master Thumbnail: {THUMBNAIL_PATH.name} ({THUMBNAIL_PATH})")
    print(f"   Size: {os.path.getsize(THUMBNAIL_PATH):,} bytes")
    
    # Read & prepare thumbnail binary
    if os.path.getsize(THUMBNAIL_PATH) > 2 * 1024 * 1024:
        im = Image.open(THUMBNAIL_PATH).convert("RGB")
        buf = io.BytesIO()
        im.save(buf, format="JPEG", quality=92)
        thumb_data = buf.getvalue()
        mime = "image/jpeg"
    else:
        with open(THUMBNAIL_PATH, "rb") as tf:
            thumb_data = tf.read()
        mime = "image/png" if THUMBNAIL_PATH.suffix.lower() == ".png" else "image/jpeg"
        
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": mime
    }
    
    print("\n🚀 Starting thumbnail synchronization for 11 videos...")
    success_count = 0
    failed_count = 0
    
    results = []
    for item in VIDEOS:
        vid = item["video_id"]
        slug = item["slug"]
        url = f"https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId={vid}"
        print(f"  📤 Updating thumbnail for {slug} ({vid})...", end=" ", flush=True)
        resp = requests.post(url, headers=headers, data=thumb_data, timeout=30)
        if resp.status_code in (200, 201):
            print(f"✅ SUCCESS ({resp.status_code})")
            success_count += 1
            results.append({"slug": slug, "video_id": vid, "status": "SUCCESS", "code": resp.status_code})
        else:
            print(f"❌ FAILED ({resp.status_code}): {resp.text}")
            failed_count += 1
            results.append({"slug": slug, "video_id": vid, "status": "FAILED", "code": resp.status_code, "error": resp.text})
            
    print(f"\n=======================================================")
    print(f"🏁 THUMBNAIL SYNC SUMMARY:")
    print(f"   Success: {success_count}/{len(VIDEOS)}")
    print(f"   Failed : {failed_count}/{len(VIDEOS)}")
    print(f"   Quota Consumed for thumbnails.set: {success_count * 50} units")
    print(f"=======================================================")
    
    if failed_count > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()
