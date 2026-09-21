#!/usr/bin/env python3
import os
import sys
import subprocess

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRATCH_DIR = os.path.join(PROJECT_ROOT, "scratch", "expanded_bgm_dl")
BGM_LIB_DIR = os.path.join(PROJECT_ROOT, "bgm_audio_library")
TOOLS_DIR = os.path.join(PROJECT_ROOT, "tools")
YT_DLP = os.path.join(TOOLS_DIR, "yt-dlp")
FFMPEG = os.path.join(TOOLS_DIR, "ffmpeg", "ffmpeg")

os.makedirs(SCRATCH_DIR, exist_ok=True)
os.makedirs(BGM_LIB_DIR, exist_ok=True)

NEW_TRACKS = [
    {
        "filename": "cophong_quan_doi_chien_tran_hao_hung_aaron_kenny.mp3",
        "url": "https://www.youtube.com/watch?v=D_rmRFu_gII",
        "title": "Imperial Forces (Aaron Kenny)",
        "genre": "Cổ phong dã sử hào hùng / Trận chiến"
    },
    {
        "filename": "cophong_sao_truc_thien_dinh_jr_tundra.mp3",
        "url": "https://www.youtube.com/watch?v=OVJHuVXGxzU",
        "title": "Enochian Magic (JR Tundra)",
        "genre": "Cổ phong Sáo trúc / Thiền định tịch mịch"
    },
    {
        "filename": "vanhoc_vn_guitar_moc_hoai_niem_chris_haugen.mp3",
        "url": "https://www.youtube.com/watch?v=AYKnkuzNPX8",
        "title": "Campfire Song (Chris Haugen)",
        "genre": "Văn học VN: Guitar mộc / Hoài niệm làng quê"
    },
    {
        "filename": "vanhoc_vn_dan_day_dong_que_esther_abrami.mp3",
        "url": "https://www.youtube.com/watch?v=-zslRrtafdo",
        "title": "No.3 Morning Folk Song (Esther Abrami)",
        "genre": "Văn học VN: Dàn dây đồng quê êm đềm"
    },
    {
        "filename": "vanhoc_tay_violin_noi_tam_esther_abrami.mp3",
        "url": "https://www.youtube.com/watch?v=SuN03iyFq9o",
        "title": "No.7 Alone With My Thoughts (Esther Abrami)",
        "genre": "Văn học phương Tây: Solo Violin nội tâm sâu sắc"
    },
    {
        "filename": "tuluc_guitar_am_ap_truyen_cam_hung_chris_haugen.mp3",
        "url": "https://www.youtube.com/watch?v=aWNjSkelbmY",
        "title": "Fresh Fallen Snow (Chris Haugen)",
        "genre": "Tự lực: Acoustic Guitar ấm áp, truyền cảm hứng"
    },
    {
        "filename": "quantri_baroque_quy_toc_aaron_kenny.mp3",
        "url": "https://www.youtube.com/watch?v=PNWcyO79dBU",
        "title": "A Baroque Letter (Aaron Kenny)",
        "genre": "Quản trị: Baroque thính phòng kỷ luật, trang trọng"
    },
    {
        "filename": "trinhtham_noir_dieu_tra_jeremy_blake.mp3",
        "url": "https://www.youtube.com/watch?v=v3Z-lB8kEoI",
        "title": "Missing Persons (Jeremy Blake)",
        "genre": "Trinh thám & Noir: Không gian điều tra, bí ẩn"
    }
]

def download_track(t):
    final_output = os.path.join(BGM_LIB_DIR, t["filename"])
    if os.path.exists(final_output) and os.path.getsize(final_output) > 50000:
        print(f"[✓] Already exists: {t['filename']}")
        return True

    slug = t["filename"].replace(".mp3", "")
    temp_target = os.path.join(SCRATCH_DIR, f"{slug}_raw.%(ext)s")
    
    cmd = [
        YT_DLP,
        "--js-runtimes", "node:/home/hoanganh/.nvm/versions/node/v24.18.0/bin/node",
        "--ffmpeg-location", os.path.dirname(FFMPEG),
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "192K",
        "-o", temp_target,
        "--no-playlist",
        t["url"]
    ]
    
    print(f"[*] Downloading: {t['title']} -> {t['filename']}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[!] Download failed for {t['filename']}: {res.stderr[:250]}")
        return False
        
    raw_mp3 = None
    for f in os.listdir(SCRATCH_DIR):
        if f.startswith(f"{slug}_raw"):
            raw_mp3 = os.path.join(SCRATCH_DIR, f)
            break
            
    if not raw_mp3 or not os.path.exists(raw_mp3):
        print(f"[!] Could not find raw file for {slug}")
        return False
        
    norm_cmd = [
        FFMPEG, "-y",
        "-i", raw_mp3,
        "-ar", "48000",
        "-ac", "2",
        "-b:a", "192k",
        final_output
    ]
    subprocess.run(norm_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.exists(raw_mp3):
        os.remove(raw_mp3)
        
    if os.path.exists(final_output) and os.path.getsize(final_output) > 50000:
        print(f"[✓] Standardized: {t['filename']} ({os.path.getsize(final_output)/(1024*1024):.2f} MB)")
        return True
    return False

if __name__ == "__main__":
    count = 0
    for t in NEW_TRACKS:
        if download_track(t):
            count += 1
    print(f"\n[✓] Finished downloading {count}/{len(NEW_TRACKS)} new safe tracks.")
