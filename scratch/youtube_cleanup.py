#!/usr/bin/env python3
import os
import sys
import json
import time
from pathlib import Path
import requests

# Add core to sys.path to use existing helpers
sys.path.insert(0, os.path.abspath("core"))
from abv_youtube_uploader import get_valid_token, get_playlist_items, update_video_thumbnail

CLIENT_SECRETS_FILE = "tools/client_secret.json"
TOKEN_FILE = "tools/token.json"
PLAYLIST_ID = "PLW4YT639QMO4"

DUPLICATE_VIDEOS = [
    ("Hồi 12", "eEfzvZB5z2M"),
    ("Hồi 13", "sosx0YX7XmI"),
    ("Hồi 14", "ahvbukDuLuo"),
    ("Hồi 15", "jOJ2gThvyrY"),
    ("Hồi 16", "piYwAT5O0aA"),
    ("Hồi 17", "SdAHucFWVP8"),
    ("Hồi 18", "0bvKMZ_fjxk"),
    ("Hồi 19", "hddmnhxGDHw"),
    ("Hồi 20", "qbMELip0zmw"),
    ("Hồi 21", "ZWsxhFdaZQI"),
    ("Hồi 22", "Pm6CkqNKhb8"),
]

ORIGINAL_VIDEOS = [
    ("Hồi 1", "OUkuc46XzU0"),
    ("Hồi 2", "gX4nCYgFc-w"),
    ("Hồi 3", "YwbmLbJzJiY"),
    ("Hồi 4", "yEBLoLZJZAE"),
    ("Hồi 5", "ejo6urjRllM"),
    ("Hồi 6", "oUWk27df3OU"),
    ("Hồi 7", "8sH1a1HbB4E"),
    ("Hồi 8", "DHk8MYo038I"),
    ("Hồi 9", "1Q91IwPWl0U"),
    ("Hồi 10", "-HNjsNSx4tg"),
    ("Hồi 11", "hMz3okrct30"),
    ("Hồi 12", "CebpnLdUByA"),
    ("Hồi 13", "Pr_wb0ukXGI"),
    ("Hồi 14", "pRmfCr6A4SU"),
    ("Hồi 15", "JZBs0nKY4vA"),
    ("Hồi 16", "5ZDR2J30jUA"),
    ("Hồi 17", "pnSMHBp25X4"),
    ("Hồi 18", "poLwSb-5-T8"),
    ("Hồi 19", "HJ9eeJ63xzI"),
    ("Hồi 20", "LjlkKBpW1wU"),
    ("Hồi 21", "szR2rNFv_Z0"),
    ("Hồi 22", "DAlwoCgBMHc"),
]

THUMBNAIL_HOI_19 = Path("/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/Final-Tam-Quoc-Dien-Nghia/backgrounds/Background-1_thumb.jpg")
HOI_19_VIDEO_ID = "HJ9eeJ63xzI"

def main():
    print("=== BẮT ĐẦU QUY TRÌNH DỌN DẸP YOUTUBE ===")
    token = get_valid_token(CLIENT_SECRETS_FILE, TOKEN_FILE)
    print(f"Token verified successfully.")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # 1. Kiểm tra playlist hiện tại
    print("\n--- 1. KIỂM TRA PLAYLIST HIỆN TẠI ---")
    current_items = get_playlist_items(token, PLAYLIST_ID)
    print(f"Tổng số video trong playlist {PLAYLIST_ID}: {len(current_items)}")
    for idx, it in enumerate(current_items, 1):
        print(f"  {idx:02d}. [{it['video_id']}] {it['title']} (item_id: {it['item_id']}, pos: {it['position']})")

    # 2. Xóa 11 video trùng lặp
    print("\n--- 2. XÓA 11 VIDEO TRÙNG LẶP ---")
    delete_results = []
    for chapter_name, video_id in DUPLICATE_VIDEOS:
        del_url = f"https://www.googleapis.com/youtube/v3/videos?id={video_id}"
        resp = requests.delete(del_url, headers=headers, timeout=30)
        status_code = resp.status_code
        if status_code in (200, 204):
            print(f"  [SUCCESS] Đã xóa {chapter_name} (video_id: {video_id}) - HTTP {status_code}")
            delete_results.append((chapter_name, video_id, True, f"HTTP {status_code} Deleted"))
        elif status_code == 404:
            print(f"  [ALREADY DELETED/404] {chapter_name} (video_id: {video_id}) không tồn tại hoặc đã xóa trước đó")
            delete_results.append((chapter_name, video_id, True, "404 Not Found (Already deleted)"))
        else:
            print(f"  [ERROR] Lỗi xóa {chapter_name} (video_id: {video_id}) - HTTP {status_code}: {resp.text}")
            delete_results.append((chapter_name, video_id, False, f"HTTP {status_code}: {resp.text}"))
        time.sleep(0.5)

    # 3. Cập nhật thumbnail cho Hồi 19 (HJ9eeJ63xzI)
    print("\n--- 3. CẬP NHẬT THUMBNAIL CHO HỒI 19 ---")
    print(f"Video ID: {HOI_19_VIDEO_ID}")
    print(f"Thumbnail path: {THUMBNAIL_HOI_19}")
    thumb_success = update_video_thumbnail(token, HOI_19_VIDEO_ID, THUMBNAIL_HOI_19)
    if thumb_success:
        print("  [SUCCESS] Đã cập nhật thumbnail thành công cho Hồi 19!")
    else:
        print("  [ERROR] Không thể cập nhật thumbnail cho Hồi 19!")

    # 4. Kiểm tra lại playlist PLW4YT639QMO4
    print("\n--- 4. KIỂM TRA LẠI PLAYLIST SAU KHI XÓA ---")
    time.sleep(2)  # Wait for eventual consistency
    updated_items = get_playlist_items(token, PLAYLIST_ID)
    print(f"Tổng số video trong playlist {PLAYLIST_ID} sau khi xóa: {len(updated_items)}")
    
    # Check if any duplicate videos are still in playlist, or if original videos match
    playlist_video_ids = [it['video_id'] for it in updated_items]
    print("\nDanh sách video hiện tại trong playlist:")
    for idx, it in enumerate(updated_items, 1):
        is_orig = any(it['video_id'] == orig_id for _, orig_id in ORIGINAL_VIDEOS)
        is_dup = any(it['video_id'] == dup_id for _, dup_id in DUPLICATE_VIDEOS)
        mark = "✓ GỐC" if is_orig else ("✗ TRÙNG" if is_dup else "? KHÁC")
        print(f"  {idx:02d}. [{mark}] [{it['video_id']}] {it['title']}")

    # Đối soát với danh sách 22 video gốc
    orig_ids = [vid for _, vid in ORIGINAL_VIDEOS]
    matched_all = (playlist_video_ids == orig_ids)
    print(f"\nĐối soát danh sách: {'HOÀN HẢO (Khớp 100% 22 video gốc theo thứ tự Hồi 1-22)' if matched_all else 'CÓ CHÊNH LỆCH'}")
    if not matched_all:
        print("Chi tiết chênh lệch:")
        print("  Expected:", orig_ids)
        print("  Actual:  ", playlist_video_ids)

    # Xuất báo cáo tóm tắt
    print("\n=== TỔNG KẾT KẾT QUẢ ===")
    print("1. Xóa video trùng lặp:")
    for chap, vid, ok, msg in delete_results:
        print(f"   - {chap} ({vid}): {'THÀNH CÔNG' if ok else 'THẤT BẠI'} ({msg})")
    print(f"2. Cập nhật thumbnail Hồi 19: {'THÀNH CÔNG' if thumb_success else 'THẤT BẠI'}")
    print(f"3. Playlist {PLAYLIST_ID}: {len(updated_items)}/22 video.")

if __name__ == "__main__":
    main()
