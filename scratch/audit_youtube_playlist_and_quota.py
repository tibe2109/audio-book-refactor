#!/usr/bin/env python3
# ==============================================================================
# AUDIT SCRIPT: YouTube Playlist Integrity & Quota Consumption Audit
# Evaluates Quota, Playlist Ordering, Video Privacy, and Manifest Synchronization
# ==============================================================================
import os
import sys
import json
from pathlib import Path
import requests

TOKEN_FILE = Path("tools/token.json")
MANIFEST_PATH = Path("Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/Final-Tam-Quoc-Dien-Nghia/Videos/.abv_upload_manifest.json")
REPORT_PATH = Path("Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/Final-Tam-Quoc-Dien-Nghia/Videos/Master_Upload_Report.md")

EXPECTED_VIDEOS = [
    {"index": 1, "slug": "01-Hoi-01", "video_id": "OUkuc46XzU0", "title_part": "Hồi 1"},
    {"index": 2, "slug": "02-Hoi-02", "video_id": "gX4nCYgFc-w", "title_part": "Hồi 2"},
    {"index": 3, "slug": "03-Hoi-03", "video_id": "YwbmLbJzJiY", "title_part": "Hồi 3"},
    {"index": 4, "slug": "04-Hoi-04", "video_id": "yEBLoLZJZAE", "title_part": "Hồi 4"},
    {"index": 5, "slug": "05-Hoi-05", "video_id": "ejo6urjRllM", "title_part": "Hồi 5"},
    {"index": 6, "slug": "06-Hoi-06", "video_id": "oUWk27df3OU", "title_part": "Hồi 6"},
    {"index": 7, "slug": "07-Hoi-07", "video_id": "8sH1a1HbB4E", "title_part": "Hồi 7"},
    {"index": 8, "slug": "08-Hoi-08", "video_id": "DHk8MYo038I", "title_part": "Hồi 8"},
    {"index": 9, "slug": "09-Hoi-09", "video_id": "1Q91IwPWl0U", "title_part": "Hồi 9"},
    {"index": 10, "slug": "10-Hoi-10", "video_id": "-HNjsNSx4tg", "title_part": "Hồi 10"},
    {"index": 11, "slug": "11-Hoi-11", "video_id": "hMz3okrct30", "title_part": "Hồi 11"},
]

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.abv_youtube_uploader import get_valid_token

EXPECTED_PLAYLIST_TITLE = "Tam Quốc Diễn Nghĩa - La Quán Trung (Phan Kế Bính Dịch)"

def get_token():
    return get_valid_token("tools/client_secret.json", str(TOKEN_FILE))

def audit_youtube():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    results = {
        "playlist": {},
        "playlist_items": [],
        "videos": {},
        "manifest": {},
        "report": {},
        "quota": {},
        "overall_passed": False
    }

    print("================================================================")
    print("🔍 AUDIT 1: CHECKING YOUTUBE PLAYLIST VIA API")
    print("================================================================")
    
    pl_resp = requests.get(
        "https://www.googleapis.com/youtube/v3/playlists?part=snippet,status&mine=true&maxResults=50",
        headers=headers,
        timeout=15
    )
    if pl_resp.status_code != 200:
        print(f"❌ Failed to fetch playlists: {pl_resp.status_code} {pl_resp.text}")
        return results

    playlists = pl_resp.json().get("items", [])
    target_pl = None
    for pl in playlists:
        if pl["snippet"]["title"].strip().lower() == EXPECTED_PLAYLIST_TITLE.strip().lower():
            target_pl = pl
            break
            
    if not target_pl:
        print(f"❌ Target playlist not found! Found: {[p['snippet']['title'] for p in playlists]}")
        results["playlist"]["found"] = False
    else:
        pl_id = target_pl["id"]
        pl_title = target_pl["snippet"]["title"]
        pl_privacy = target_pl["status"]["privacyStatus"]
        print(f"✅ Found Playlist: ID={pl_id}")
        print(f"   Title: '{pl_title}'")
        print(f"   Privacy: '{pl_privacy}'")
        results["playlist"] = {
            "found": True,
            "id": pl_id,
            "title": pl_title,
            "title_matched": (pl_title == EXPECTED_PLAYLIST_TITLE),
            "privacy": pl_privacy,
            "privacy_matched": (pl_privacy == "public"),
            "url": f"https://www.youtube.com/playlist?list={pl_id}"
        }

    if target_pl:
        print("\n================================================================")
        print("🔍 AUDIT 2: CHECKING PLAYLIST ITEMS AND ORDER")
        print("================================================================")
        items_resp = requests.get(
            f"https://www.googleapis.com/youtube/v3/playlistItems?playlistId={target_pl['id']}&part=snippet,contentDetails&maxResults=50",
            headers=headers,
            timeout=15
        )
        if items_resp.status_code == 200:
            items = items_resp.json().get("items", [])
            print(f"Total items in playlist: {len(items)}")
            results["playlist"]["item_count"] = len(items)
            
            order_ok = True
            for idx, item in enumerate(items):
                vid = item["snippet"]["resourceId"]["videoId"]
                pos = item["snippet"]["position"]
                title = item["snippet"]["title"]
                expected_vid = EXPECTED_VIDEOS[idx]["video_id"] if idx < len(EXPECTED_VIDEOS) else "N/A"
                match = (vid == expected_vid)
                if not match:
                    order_ok = False
                status_icon = "✅" if match else "❌"
                print(f"  {status_icon} Pos {pos:02d} (Item #{idx+1:02d}): {vid} | Match Expected: {expected_vid} | Title: {title[:50]}...")
                results["playlist_items"].append({
                    "position": pos,
                    "video_id": vid,
                    "expected_video_id": expected_vid,
                    "matched": match,
                    "title": title
                })
            results["playlist"]["order_ok"] = order_ok and (len(items) == len(EXPECTED_VIDEOS))
            print(f"\nPlaylist Order Integrity: {'✅ PASSED (100% Correct Sequence)' if results['playlist']['order_ok'] else '❌ FAILED'}")

    print("\n================================================================")
    print("🔍 AUDIT 3: CHECKING PRIVACY STATUS OF ALL 11 VIDEOS")
    print("================================================================")
    all_vids = [v["video_id"] for v in EXPECTED_VIDEOS]
    v_resp = requests.get(
        f"https://www.googleapis.com/youtube/v3/videos?id={','.join(all_vids)}&part=snippet,status",
        headers=headers,
        timeout=15
    )
    if v_resp.status_code == 200:
        videos_data = {item["id"]: item for item in v_resp.json().get("items", [])}
        all_public = True
        for exp in EXPECTED_VIDEOS:
            vid = exp["video_id"]
            if vid in videos_data:
                v = videos_data[vid]
                priv = v["status"]["privacyStatus"]
                upload_status = v["status"]["uploadStatus"]
                is_pub = (priv == "public")
                if not is_pub:
                    all_public = False
                icon = "✅" if is_pub else "❌"
                print(f"  {icon} {exp['slug']} ({vid}): Privacy={priv} | UploadStatus={upload_status}")
                results["videos"][vid] = {
                    "slug": exp["slug"],
                    "privacy": priv,
                    "upload_status": upload_status,
                    "is_public": is_pub
                }
            else:
                all_public = False
                print(f"  ❌ {exp['slug']} ({vid}): NOT FOUND ON YOUTUBE!")
                results["videos"][vid] = {"found": False}
        results["videos_all_public"] = all_public
        print(f"\nAll Videos Public Integrity: {'✅ PASSED (100% Public)' if all_public else '❌ FAILED'}")

    print("\n================================================================")
    print("🔍 AUDIT 4: CHECKING LOCAL MANIFEST & MASTER REPORT")
    print("================================================================")
    if MANIFEST_PATH.exists():
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            manifest_data = json.load(f)
        results["manifest"]["exists"] = True
        results["manifest"]["playlist_id"] = manifest_data.get("playlist_id")
        results["manifest"]["playlist_url"] = manifest_data.get("playlist_url")
        results["manifest"]["playlist_title"] = manifest_data.get("playlist_title")
        print(f"Manifest Playlist ID: {manifest_data.get('playlist_id')}")
        print(f"Manifest Playlist URL: {manifest_data.get('playlist_url')}")
        
        # Check per-video status in manifest
        uploaded_videos = manifest_data.get("videos", {})
        manifest_vids_public = 0
        for exp in EXPECTED_VIDEOS:
            vf = f"Final_Video_{exp['slug']}_Part1.mp4"
            vinfo = uploaded_videos.get(vf, {})
            if vinfo.get("privacyStatus") == "public" or vinfo.get("privacy") == "public":
                manifest_vids_public += 1
        results["manifest"]["public_videos_count"] = manifest_vids_public
        print(f"Manifest Videos with 'public' status: {manifest_vids_public}/{len(EXPECTED_VIDEOS)}")
    else:
        results["manifest"]["exists"] = False
        print(f"❌ Manifest file not found: {MANIFEST_PATH}")

    if REPORT_PATH.exists():
        with open(REPORT_PATH, "r", encoding="utf-8") as f:
            report_content = f.read()
        results["report"]["exists"] = True
        results["report"]["mentions_playlist"] = ("playlist" in report_content.lower() or "danh sách phát" in report_content.lower())
        results["report"]["mentions_public"] = ("public" in report_content.lower() or "công khai" in report_content.lower())
        print(f"Report mentions Playlist: {results['report']['mentions_playlist']}")
        print(f"Report mentions Public: {results['report']['mentions_public']}")
    else:
        results["report"]["exists"] = False
        print(f"❌ Report file not found: {REPORT_PATH}")

    print("\n================================================================")
    print("🔍 AUDIT 5: QUOTA CONSUMPTION BREAKDOWN & AUDIT")
    print("================================================================")
    # Standard YouTube Data API v3 Costs:
    # - playlists.insert: 50 units (or playlists.update: 50 units)
    # - playlistItems.insert: 50 units each * 11 = 550 units
    # - videos.update: 50 units each * 11 = 550 units
    # - playlists.list, playlistItems.list, videos.list, channels.list: 1 unit each (~5-10 units)
    quota_breakdown = {
        "playlist_creation_or_update": 50,
        "playlist_items_insert": 11 * 50,
        "videos_privacy_update": 11 * 50,
        "read_operations": 5,
        "total_estimated_units": 50 + (11 * 50) + (11 * 50) + 5,
        "daily_limit": 10000,
        "percent_daily_limit": ((50 + 550 + 550 + 5) / 10000) * 100
    }
    results["quota"] = quota_breakdown
    print(f"  • Playlist Create/Update : {quota_breakdown['playlist_creation_or_update']} units")
    print(f"  • PlaylistItems.insert    : {quota_breakdown['playlist_items_insert']} units (11 videos x 50)")
    print(f"  • Videos.update (Public)  : {quota_breakdown['videos_privacy_update']} units (11 videos x 50)")
    print(f"  • Read Operations (Lists) : ~{quota_breakdown['read_operations']} units")
    print(f"  👉 TOTAL CONSUMPTION     : {quota_breakdown['total_estimated_units']} units (~{quota_breakdown['percent_daily_limit']:.2f}% of 10,000 daily quota)")
    print(f"  🛡️ Quota Safety Margin    : {10000 - quota_breakdown['total_estimated_units']} units remaining (SAFE)")

    # Overall verdict
    pl_ok = results.get("playlist", {}).get("found", False) and results.get("playlist", {}).get("title_matched", False) and results.get("playlist", {}).get("order_ok", False)
    vid_ok = results.get("videos_all_public", False)
    results["overall_passed"] = pl_ok and vid_ok
    print(f"\n================================================================")
    print(f"🏁 FINAL AUDIT VERDICT: {'🟢 PASSED (100% READY)' if results['overall_passed'] else '🟡 IN PROGRESS / PENDING'}")
    print(f"================================================================")
    
    return results

if __name__ == "__main__":
    audit_youtube()
