#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRATCH_DIR = os.path.join(PROJECT_ROOT, "scratch", "safe_bgm_dl")
BGM_LIB_DIR = os.path.join(PROJECT_ROOT, "bgm_audio_library")
TOOLS_DIR = os.path.join(PROJECT_ROOT, "tools")
YT_DLP = os.path.join(TOOLS_DIR, "yt-dlp")
FFMPEG = os.path.join(TOOLS_DIR, "ffmpeg", "ffmpeg")

os.makedirs(SCRATCH_DIR, exist_ok=True)

TRACKS = [
    {
        "id": "05_dan_tranh_co_cam_truyen_thong",
        "url": "https://www.youtube.com/watch?v=IrbWRLUBY2w",
        "filename": "05_dan_tranh_co_cam_truyen_thong.mp3",
        "title": "Lau Tzu Ehru (Doug Maxwell) - 1hr Loop",
        "genre": "Classical Chinese / Asian Erhu & Strings (YouTube Audio Library - No Attribution)",
    },
    {
        "id": "06_epic_three_kingdoms_shu_theme",
        "url": "https://www.youtube.com/watch?v=jJTABmGUCbo",
        "filename": "06_epic_three_kingdoms_shu_theme.mp3",
        "title": "Koto San (Ofshane) - 1hr Loop",
        "genre": "Classical East Asian Zither / Guzheng & Koto (YouTube Audio Library - No Attribution)",
    },
    {
        "id": "04_tam_quoc_epic_theme",
        "url": "https://www.youtube.com/watch?v=ojA8-akwFoA",
        "filename": "04_tam_quoc_epic_theme.mp3",
        "title": "Beneath the Moonlight (Aaron Kenny)",
        "genre": "Traditional Asian Flute & Strings (YouTube Audio Library - No Attribution)",
    },
    {
        "id": "01_baroque_focus",
        "url": "https://www.youtube.com/watch?v=fSLnffmDbME",
        "filename": "01_baroque_focus.mp3",
        "title": "C Major Prelude (J.S. Bach)",
        "genre": "Classical Baroque Focus (YouTube Audio Library - No Attribution)",
    },
    {
        "id": "02_deep_focus_ambient",
        "url": "https://www.youtube.com/watch?v=JlOEFv8CkLY",
        "filename": "02_deep_focus_ambient.mp3",
        "title": "The Sleeping Prophet (Jesse Gallagher)",
        "genre": "Deep Ambient Focus (YouTube Audio Library - No Attribution)",
    },
    {
        "id": "03_piano_outro",
        "url": "https://www.youtube.com/watch?v=0NqxwZI5lwg",
        "filename": "03_piano_outro.mp3",
        "title": "Gymnopedie no1 (Erik Satie)",
        "genre": "Solo Piano Classical (YouTube Audio Library - No Attribution)",
    }
]

def download_and_standardize(track):
    print(f"\n=======================================================")
    print(f"[*] Processing {track['filename']} : {track['title']}")
    print(f"    URL: {track['url']}")
    
    raw_target_template = os.path.join(SCRATCH_DIR, f"{track['id']}_raw.%(ext)s")
    final_output = os.path.join(BGM_LIB_DIR, track['filename'])
    
    # Download raw audio
    dl_cmd = [
        YT_DLP,
        "--js-runtimes", "node:/home/hoanganh/.nvm/versions/node/v24.18.0/bin/node",
        "--ffmpeg-location", os.path.dirname(FFMPEG),
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "192K",
        "-o", raw_target_template,
        "--no-playlist",
        track['url']
    ]
    
    res = subprocess.run(dl_cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[!] Error downloading {track['filename']}: {res.stderr[:300]}")
        return False
        
    raw_file = os.path.join(SCRATCH_DIR, f"{track['id']}_raw.mp3")
    if not os.path.exists(raw_file):
        for f in os.listdir(SCRATCH_DIR):
            if f.startswith(f"{track['id']}_raw"):
                raw_file = os.path.join(SCRATCH_DIR, f)
                break
                
    if not os.path.exists(raw_file):
        print(f"[!] Could not locate downloaded file for {track['id']}")
        return False
        
    print(f"    Raw downloaded: {os.path.basename(raw_file)} ({os.path.getsize(raw_file)} bytes)")
    
    # Standardize to 48000Hz, stereo, 192k MP3
    norm_cmd = [
        FFMPEG, "-y",
        "-i", raw_file,
        "-ar", "48000",
        "-ac", "2",
        "-b:a", "192k",
        final_output
    ]
    res_norm = subprocess.run(norm_cmd, capture_output=True, text=True)
    if res_norm.returncode != 0:
        print(f"[!] Error standardizing {track['filename']}: {res_norm.stderr[:300]}")
        return False
        
    print(f"[✓] Successfully standardized: {final_output}")
    print(f"    File size: {os.path.getsize(final_output) / (1024*1024):.2f} MB")
    return True

if __name__ == "__main__":
    success = 0
    for t in TRACKS:
        if download_and_standardize(t):
            success += 1
    print(f"\n[✓] Completed: {success}/{len(TRACKS)} tracks updated with 100% safe YouTube Audio Library music.")
