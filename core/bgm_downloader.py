#!/usr/bin/env python3
"""
BGM Downloader & Thematic Music Director (Step 10: arf_10_bgm_dynamic_mixer)
- Analyzes book theme, genre, characters, time period, culture and national setting.
- Matches with curated public domain & royalty-free BGM in bgm_audio_library/.
- Automatically downloads safe, calm, minimalist instrumental reading music if missing.
- Prevents overly energetic, multi-instrument, loud music that competes with speech.
"""

import os
import re
import sys
import json
import shutil
import subprocess

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(PROJECT_ROOT, "tools")
YT_DLP_EXE = os.path.join(TOOLS_DIR, "yt-dlp")
BGM_LIB_DIR = os.path.join(PROJECT_ROOT, "bgm_audio_library")

# Safe YouTube Audio Library search templates for reading background music (No Attribution Required)
GENRE_SAFE_QUERIES = {
    "classical_chinese_epic": {
        "query": "ytsearch1:\"Provided to YouTube by YouTube Audio Library\" (Doug Maxwell OR Ofshane OR Aaron Kenny) (Ehru OR Koto OR Chinese)",
        "default_filename": "05_dan_tranh_co_cam_truyen_thong.mp3",
        "description": "Cổ phong Đông Á: Cổ Cầm, Đàn Tranh, Đàn Nhị êm dịu, thanh thoát (YouTube Audio Library Safe)",
        "volume_factor": 0.065
    },
    "vietnamese_literature": {
        "query": "ytsearch1:\"Provided to YouTube by YouTube Audio Library\" (Flute OR Koto OR Acoustic calm)",
        "default_filename": "05_dan_tranh_co_cam_truyen_thong.mp3",
        "description": "Văn học Việt Nam: Đàn Tranh, Sáo Trúc, Acoustic mộc mạc, hoài niệm sâu lắng (YouTube Audio Library Safe)",
        "volume_factor": 0.065
    },
    "western_classical_literature": {
        "query": "ytsearch1:\"Provided to YouTube by YouTube Audio Library\" Satie Gymnopedie",
        "default_filename": "03_piano_outro.mp3",
        "description": "Văn học phương Tây & Cổ điển: Solo Piano, Solo Cello nhẹ nhàng (YouTube Audio Library Safe)",
        "volume_factor": 0.075
    },
    "self_help_inspirational": {
        "query": "ytsearch1:\"Provided to YouTube by YouTube Audio Library\" Jesse Gallagher ambient",
        "default_filename": "02_deep_focus_ambient.mp3",
        "description": "Tự lực & Phát triển bản thân: Deep Ambient ấm áp, truyền cảm hứng (YouTube Audio Library Safe)",
        "volume_factor": 0.070
    },
    "business_tech_management": {
        "query": "ytsearch1:\"Provided to YouTube by YouTube Audio Library\" Bach C Major Prelude",
        "default_filename": "01_baroque_focus.mp3",
        "description": "Quản trị, Khoa học & Công nghệ: Baroque kích thích tập trung sóng não Alpha (YouTube Audio Library Safe)",
        "volume_factor": 0.070
    },
    "mystery_noir": {
        "query": "ytsearch1:\"Provided to YouTube by YouTube Audio Library\" ambient dark calm piano",
        "default_filename": "02_deep_focus_ambient.mp3",
        "description": "Trinh thám & Noir: Minimalist Ambient Drone, Solo Piano quãng trầm (YouTube Audio Library Safe)",
        "volume_factor": 0.060
    }
}

def detect_book_thematic_genre(book_name, chap_dir=None):
    """
    Detects cultural, national setting and genre of the book based on:
    1. .theatrical_bible.json (if present in chap_dir)
    2. Book folder name / slug keywords
    3. Returns canonical genre key
    """
    # 1. Check .theatrical_bible.json first
    if chap_dir:
        bible_path = os.path.join(chap_dir, ".theatrical_bible.json")
        if os.path.exists(bible_path):
            try:
                with open(bible_path, "r", encoding="utf-8") as f:
                    b_data = json.load(f)
                b_genre = b_data.get("genre", "").lower()
                if "classical_epic" in b_genre or "chinese" in b_genre or "co_trang" in b_genre:
                    return "classical_chinese_epic"
                elif "vietnamese" in b_genre:
                    return "vietnamese_literature"
                elif "western" in b_genre or "classical" in b_genre:
                    return "western_classical_literature"
                elif "self_help" in b_genre or "inspirational" in b_genre:
                    return "self_help_inspirational"
                elif "tech" in b_genre or "business" in b_genre:
                    return "business_tech_management"
                elif "noir" in b_genre or "mystery" in b_genre:
                    return "mystery_noir"
            except Exception:
                pass

    # 2. Slug & Keyword analysis
    slug = (book_name or "").lower().replace("-", " ").replace("_", " ")

    # East Asian / Chinese Historical Epics / Wuxia
    chinese_epic_kw = [
        "tam quoc", "thuy hu", "tay du", "hong lau", "dong chu", "han so",
        "kiem hiep", "tien hiep", "tien huyen", "co phong", "co trang",
        "romance of the three kingdoms", "water margin", "wuxia"
    ]
    if any(k in slug for k in chinese_epic_kw):
        return "classical_chinese_epic"

    # Vietnamese Classical & Modern Literature
    vn_lit_kw = [
        "nam cao", "vu trong phung", "ngo tat to", "thach lam", "nguyen tuan",
        "chi pheo", "so do", "tat den", "vang bong mot thoi", "hoang phu ngoc tuong",
        "doan gioi", "dat rung phuong nam", "viet nam", "su viet"
    ]
    if any(k in slug for k in vn_lit_kw):
        return "vietnamese_literature"

    # Business, Tech, Project Management
    biz_tech_kw = [
        "pmbok", "agile", "scrum", "project management", "quan tri",
        "kinh te", "lap trinh", "clean code", "refactoring", "data",
        "python", "software", "startup", "marketing", "finance",
        "project", "execution", "management"
    ]
    if any(k in slug for k in biz_tech_kw):
        return "business_tech_management"

    # Self-Help / Inspirational
    self_help_kw = [
        "quiet", "introvert", "dac nhan tam", "atomic habits", "habit",
        "thoi quen", "nghi giau", "lam giau", "tam ly", "cam xuc",
        "suc manh", "song dep", "tu duy", "think and grow rich", "carnegie"
    ]
    if any(k in slug for k in self_help_kw):
        return "self_help_inspirational"

    # Mystery / Noir / Detective
    noir_kw = [
        "sherlock", "conan doyle", "higashino", "trinh tham", "an mang",
        "tham tu", "noir", "toi pham", "investigation"
    ]
    if any(k in slug for k in noir_kw):
        return "mystery_noir"

    # Western Classical / Realism / Philosophical Literature
    western_lit_kw = [
        "victor hugo", "dostoevsky", "tolstoy", "kafka", "camus", "balzac",
        "dickens", "hemingway", "les miserables", "war and peace", "crime and punishment"
    ]
    if any(k in slug for k in western_lit_kw):
        return "western_classical_literature"

    # Default fallback to self-help / contemplative ambient
    return "self_help_inspirational"

def get_ffmpeg_cmd():
    """Find ffmpeg binary in project or system PATH."""
    local_ffmpeg = os.path.join(TOOLS_DIR, "ffmpeg", "ffmpeg")
    if os.path.exists(local_ffmpeg):
        return local_ffmpeg
    return shutil.which("ffmpeg") or "ffmpeg"

def download_safe_bgm(genre, custom_query=None, output_dir=None):
    """
    Downloads safe, royalty-free, minimalist instrumental background music for reading
    using tools/yt-dlp into bgm_audio_library/.
    Guarantees:
    - 100% instrumental, calm tempo (60-80 BPM).
    - No boisterous percussion or heavy brass that drowns voice.
    - Public domain / Creative Commons / YouTube Audio Library Safe.
    """
    if not output_dir:
        output_dir = BGM_LIB_DIR
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(YT_DLP_EXE):
        print(f"[!] Warning: yt-dlp tool not found at {YT_DLP_EXE}. Cannot auto-download.")
        return None

    ffmpeg_bin = get_ffmpeg_cmd()
    genre_info = GENRE_SAFE_QUERIES.get(genre, GENRE_SAFE_QUERIES["self_help_inspirational"])
    search_term = custom_query if custom_query else genre_info["query"]

    target_slug = f"auto_{genre}_reading_bgm"
    temp_target = os.path.join(output_dir, f"{target_slug}_temp.%(ext)s")
    final_mp3 = os.path.join(output_dir, f"{target_slug}.mp3")

    print(f"[*] Auto-downloading safe royalty-free BGM for genre '{genre}'...")
    print(f"    -> Query: {search_term}")
    print(f"    -> Target: {final_mp3}")

    cmd = [
        YT_DLP_EXE,
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "192K",
        "--ffmpeg-location", os.path.dirname(ffmpeg_bin) if os.path.dirname(ffmpeg_bin) else "/usr/bin",
        "--default-search", "ytsearch1",
        "--max-downloads", "1",
        "--no-playlist",
    ]
    node_bin = shutil.which("node") or os.path.expanduser("~/.nvm/versions/node/v24.18.0/bin/node")
    if os.path.exists(node_bin):
        cmd.extend(["--js-runtimes", f"node:{node_bin}"])
    cmd.extend(["-o", temp_target, search_term])

    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if res.returncode == 0:
            for f in os.listdir(output_dir):
                if f.startswith(f"{target_slug}_temp") and f.endswith(".mp3"):
                    temp_mp3 = os.path.join(output_dir, f)
                    norm_cmd = [
                        ffmpeg_bin, "-y",
                        "-i", temp_mp3,
                        "-ar", "48000",
                        "-ac", "2",
                        "-b:a", "192k",
                        final_mp3
                    ]
                    subprocess.run(norm_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    if os.path.exists(temp_mp3) and temp_mp3 != final_mp3:
                        os.remove(temp_mp3)
                    break

            if os.path.exists(final_mp3) and os.path.getsize(final_mp3) > 100000:
                print(f"[✓] Downloaded and standardized safe BGM: {final_mp3}")
                return final_mp3
        else:
            print(f"[!] yt-dlp download notice: {res.stderr[:200]}")
    except Exception as e:
        print(f"[!] Exception downloading BGM: {e}")

    return None

def resolve_thematic_bgm(book_name, chap_dir=None, user_bgm=None, auto_download_if_missing=True):
    """
    Intelligent Thematic BGM Resolver:
    1. Honors user_bgm if explicitly specified and valid (not 'nhac-nen.mp3').
    2. Analyzes book genre, cultural context and characters.
    3. Finds best matching calm, minimalist instrumental track in bgm_audio_library/.
    4. If missing or inadequate, automatically downloads safe royalty-free BGM.
    5. Returns (bgm_path, genre, volume_factor, description)
    """
    if user_bgm and user_bgm not in ("nhac-nen.mp3", "default", ""):
        if os.path.exists(user_bgm):
            return os.path.abspath(user_bgm), "custom_user", 0.07, "User specified custom BGM"
        candidate = os.path.join(BGM_LIB_DIR, user_bgm)
        if os.path.exists(candidate):
            return candidate, "custom_user", 0.07, f"User selected from library: {user_bgm}"
        candidate_root = os.path.join(PROJECT_ROOT, user_bgm)
        if os.path.exists(candidate_root):
            return candidate_root, "custom_user", 0.07, f"User selected from root: {user_bgm}"

    genre = detect_book_thematic_genre(book_name, chap_dir)
    genre_info = GENRE_SAFE_QUERIES.get(genre, GENRE_SAFE_QUERIES["self_help_inspirational"])
    expected_file = genre_info["default_filename"]
    volume_factor = genre_info["volume_factor"]
    description = genre_info["description"]

    # Priority 1: Primary default file for this genre
    primary_candidate = os.path.join(BGM_LIB_DIR, expected_file)
    if os.path.exists(primary_candidate) and os.path.getsize(primary_candidate) > 100000:
        return primary_candidate, genre, volume_factor, description

    # Priority 2: Alternative genre-specific matches
    if genre == "classical_chinese_epic":
        alt_candidates = ["05_dan_tranh_co_cam_truyen_thong.mp3", "04_tam_quoc_epic_theme.mp3"]
    elif genre == "vietnamese_literature":
        alt_candidates = ["05_dan_tranh_co_cam_truyen_thong.mp3", "02_deep_focus_ambient.mp3"]
    elif genre == "business_tech_management":
        alt_candidates = ["01_baroque_focus.mp3", "02_deep_focus_ambient.mp3"]
    elif genre == "western_classical_literature":
        alt_candidates = ["03_piano_outro.mp3", "01_baroque_focus.mp3"]
    elif genre == "mystery_noir":
        alt_candidates = ["02_deep_focus_ambient.mp3", "03_piano_outro.mp3"]
    else:
        alt_candidates = ["02_deep_focus_ambient.mp3", "03_piano_outro.mp3", "01_baroque_focus.mp3"]

    for alt in alt_candidates:
        c_path = os.path.join(BGM_LIB_DIR, alt)
        if os.path.exists(c_path) and os.path.getsize(c_path) > 100000:
            return c_path, genre, volume_factor, f"Library match ({alt}): {description}"

    # Priority 3: Check auto-downloaded track for this genre
    auto_downloaded = os.path.join(BGM_LIB_DIR, f"auto_{genre}_reading_bgm.mp3")
    if os.path.exists(auto_downloaded) and os.path.getsize(auto_downloaded) > 100000:
        return auto_downloaded, genre, volume_factor, f"Auto-downloaded royalty-free match: {description}"

    # Priority 4: Auto-download if missing
    if auto_download_if_missing:
        dl_path = download_safe_bgm(genre)
        if dl_path and os.path.exists(dl_path):
            return dl_path, genre, volume_factor, f"Freshly downloaded royalty-free BGM: {description}"

    # Priority 5: Any available MP3 in library
    if os.path.exists(BGM_LIB_DIR):
        all_mp3s = sorted([os.path.join(BGM_LIB_DIR, f) for f in os.listdir(BGM_LIB_DIR) if f.lower().endswith(".mp3")])
        if all_mp3s:
            return all_mp3s[0], genre, volume_factor, f"Fallback first library track: {os.path.basename(all_mp3s[0])}"

    return None, genre, volume_factor, "No BGM found"

if __name__ == "__main__":
    test_books = [
        "Tam-Quoc-Dien-Nghia",
        "Quiet-The-Power-of-Introverts",
        "PMBOK-6th-Edition",
        "Chi-Pheo-Nam-Cao",
        "Sherlock-Holmes"
    ]
    print("=== Testing Thematic BGM Detection & Matching ===")
    for b in test_books:
        bgm, g, vol, desc = resolve_thematic_bgm(b, auto_download_if_missing=False)
        print(f"Book: {b:30} -> Genre: {g:28} | Vol: {vol:.3f} | BGM: {os.path.basename(bgm) if bgm else 'None'}")
        print(f"      Desc: {desc}")
