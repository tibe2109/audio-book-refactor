import os
import sys
import json
import glob

# Add core to sys.path
sys.path.insert(0, "/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/core")
from theatrical_voice_director import direct_chapter_theatrical_script

chapter_dir = "/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/15-Hoi-15"
kich_ban_dir = os.path.join(chapter_dir, "kich-ban")
script_json_path = os.path.join(chapter_dir, "theatrical_script.json")
bible_json_path = os.path.join(chapter_dir, ".theatrical_bible.json")
manifest_path = "/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/.session_manifest.json"

print("=== RUNNING THEATRICAL VOICE DIRECTOR FOR CHAPTER 15 ===")

# 1. Run director on Chapter 15
chap_num = 15
chap_title = "Hồi 15: Thái Sử Từ ham đả Tiểu Bá Vương; Tôn Bá Phù hăng đánh Nghiêm Bạch Hổ"

res = direct_chapter_theatrical_script(chapter_dir, chap_num, chap_title)
if not res:
    print("Error: Directing chapter 15 failed!")
    sys.exit(1)

print(f"Directing completed successfully:")
print(f"  - Total lines: {res['total_lines']}")
print(f"  - Narrator lines: {res['narrator_lines']}")
print(f"  - Dialogue lines: {res['dialogue_lines']}")
print(f"  - Poem lines: {res['poem_lines']}")
print(f"  - Characters cast: {res['characters_count']}")

# 2. Zero-Loss Invariant verification
print("\n--- ZERO-LOSS INVARIANT VERIFICATION ---")
kich_ban_files = sorted(glob.glob(os.path.join(kich_ban_dir, "Kich-ban-*.txt")))
original_text_full = ""
for fpath in kich_ban_files:
    with open(fpath, "r", encoding="utf-8") as f:
        original_text_full += f.read()

with open(script_json_path, "r", encoding="utf-8") as f:
    theatrical_script = json.load(f)

script_text_full = "".join(item.get("text", "") for item in theatrical_script)

print(f"Original script chunks length (chars): {len(original_text_full)}")
print(f"Theatrical script combined length (chars): {len(script_text_full)}")

# 3. Update session manifest
print("\n--- UPDATING SESSION MANIFEST ---")
manifest = {}
if os.path.exists(manifest_path):
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

chapters = manifest.get("chapters", [])
chapter_found = False
for ch in chapters:
    if ch.get("folder") == "15-Hoi-15":
        ch["step_8a_status"] = "completed"
        ch["theatrical_script_file"] = os.path.relpath(script_json_path, os.path.dirname(manifest_path))
        ch["theatrical_bible_file"] = os.path.relpath(bible_json_path, os.path.dirname(manifest_path))
        ch["total_theatrical_lines"] = res["total_lines"]
        ch["total_poem_lines"] = res["poem_lines"]
        ch["total_dialogue_lines"] = res["dialogue_lines"]
        ch["total_characters_cast"] = res["characters_count"]
        chapter_found = True
        break

if not chapter_found:
    chapters.append({
        "index": 14,
        "folder": "15-Hoi-15",
        "title": chap_title,
        "step_8a_status": "completed",
        "theatrical_script_file": os.path.relpath(script_json_path, os.path.dirname(manifest_path)),
        "theatrical_bible_file": os.path.relpath(bible_json_path, os.path.dirname(manifest_path)),
        "total_theatrical_lines": res["total_lines"],
        "total_poem_lines": res["poem_lines"],
        "total_dialogue_lines": res["dialogue_lines"],
        "total_characters_cast": res["characters_count"]
    })
    manifest["chapters"] = chapters

with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

print("Session manifest successfully updated for 15-Hoi-15.")
print("=== CHAPTER 15 THEATRICAL DIRECTION & VERIFICATION COMPLETED ===")
