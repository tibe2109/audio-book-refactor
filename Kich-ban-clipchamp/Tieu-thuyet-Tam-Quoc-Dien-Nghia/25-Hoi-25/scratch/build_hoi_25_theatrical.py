import os
import json
import glob

chapter_dir = "/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/25-Hoi-25"
kich_ban_dir = os.path.join(chapter_dir, "kich-ban")
script_path = os.path.join(chapter_dir, "theatrical_script.json")
bible_path = os.path.join(chapter_dir, ".theatrical_bible.json")
manifest_path = "/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/.session_manifest.json"

print("=== BUILDING & VERIFYING CHAPTER 25 THEATRICAL SCRIPT, BIBLE & MANIFEST ===")

# 1. Verify script and bible exist
if not os.path.exists(script_path):
    raise FileNotFoundError(f"theatrical_script.json not found at {script_path}")
if not os.path.exists(bible_path):
    raise FileNotFoundError(f".theatrical_bible.json not found at {bible_path}")

with open(script_path, "r", encoding="utf-8") as f:
    script = json.load(f)

with open(bible_path, "r", encoding="utf-8") as f:
    bible = json.load(f)

total_lines = len(script)
narrator_lines = sum(1 for x in script if x.get("type") == "narrator")
poem_lines = sum(1 for x in script if x.get("type") == "poem")
dialogue_lines = sum(1 for x in script if x.get("type") == "dialogue")
characters_cast = len(bible.get("characters", {}))

print(f"Stats -> Total lines: {total_lines}, Narrator: {narrator_lines}, Poem: {poem_lines}, Dialogue: {dialogue_lines}, Cast: {characters_cast}")

# Update bible stats
bible["total_theatrical_lines"] = total_lines
bible["narrator_lines"] = narrator_lines
bible["poem_lines"] = poem_lines
bible["dialogue_lines"] = dialogue_lines
bible["characters_cast_count"] = characters_cast

with open(bible_path, "w", encoding="utf-8") as f:
    json.dump(bible, f, ensure_ascii=False, indent=2)
print("Updated .theatrical_bible.json successfully.")

# 2. Update or create .session_manifest.json
manifest = {"chapters": []}
if os.path.exists(manifest_path):
    with open(manifest_path, "r", encoding="utf-8") as f:
        try:
            manifest = json.load(f)
        except Exception:
            manifest = {"chapters": []}

ch_entry = None
for ch in manifest.get("chapters", []):
    if ch.get("folder") == "25-Hoi-25" or ch.get("chapter_index") == 25:
        ch_entry = ch
        break

if not ch_entry:
    ch_entry = {
        "chapter_index": 25,
        "folder": "25-Hoi-25",
        "title": "Hồi 25: Đóng Thổ Sơn, Quan Công giao ước ba việc; Cứu Bạch Mã, Tào Tháo thoát khỏi vòng vây"
    }
    manifest.setdefault("chapters", []).append(ch_entry)

ch_entry["step_8a_status"] = "completed"
ch_entry["total_theatrical_lines"] = total_lines
ch_entry["total_poem_lines"] = poem_lines
ch_entry["total_dialogue_lines"] = dialogue_lines
ch_entry["total_characters_cast"] = characters_cast

with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print("Updated .session_manifest.json successfully with chapter 25 status: completed.")
print("=== CHAPTER 25 BUILD & MANIFEST VERIFICATION COMPLETED ===")
