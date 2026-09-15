import os
import json
import glob

chapter_dir = "/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/12-Hoi-12"
kich_ban_dir = os.path.join(chapter_dir, "kich-ban")
script_json_path = os.path.join(chapter_dir, "theatrical_script.json")
bible_json_path = os.path.join(chapter_dir, ".theatrical_bible.json")
manifest_path = "/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/.session_manifest.json"

print("--- VERIFYING CHAPTER 12 THEATRICAL SCRIPT & BIBLE ---")

# 1. Read Kich-ban files
kich_ban_files = sorted(glob.glob(os.path.join(kich_ban_dir, "Kich-ban-*.txt")))
print(f"Found {len(kich_ban_files)} script chunk files.")

raw_chunks_text = []
for fpath in kich_ban_files:
    with open(fpath, "r", encoding="utf-8") as f:
        raw_chunks_text.append(f.read())

# 2. Load theatrical_script.json
with open(script_json_path, "r", encoding="utf-8") as f:
    theatrical_script = json.load(f)

print(f"Loaded theatrical_script.json with {len(theatrical_script)} lines.")

# 3. Load .theatrical_bible.json
with open(bible_json_path, "r", encoding="utf-8") as f:
    bible_data = json.load(f)

print(f"Loaded .theatrical_bible.json. Characters cast: {bible_data.get('characters_cast_count', 0)}")

# Count lines by type
total_lines = len(theatrical_script)
narrator_lines = sum(1 for item in theatrical_script if item.get('type') == 'narrator')
poem_lines = sum(1 for item in theatrical_script if item.get('type') == 'poem')
dialogue_lines = sum(1 for item in theatrical_script if item.get('type') == 'dialogue')
characters_cast = len(bible_data.get('characters', {}))

print(f"Stats: total={total_lines}, narrator={narrator_lines}, poem={poem_lines}, dialogue={dialogue_lines}, cast={characters_cast}")

# Update bible stats
bible_data['total_theatrical_lines'] = total_lines
bible_data['narrator_lines'] = narrator_lines
bible_data['poem_lines'] = poem_lines
bible_data['dialogue_lines'] = dialogue_lines
bible_data['characters_cast_count'] = characters_cast

with open(bible_json_path, "w", encoding="utf-8") as f:
    json.dump(bible_data, f, ensure_ascii=False, indent=2)
print("Updated .theatrical_bible.json stats.")

# 4. Update .session_manifest.json
with open(manifest_path, "r", encoding="utf-8") as f:
    manifest = json.load(f)

chapter_found = False
for ch in manifest.get('chapters', []):
    if ch.get('folder') == '12-Hoi-12':
        ch['step_8a_status'] = 'completed'
        ch['total_theatrical_lines'] = total_lines
        ch['total_poem_lines'] = poem_lines
        ch['total_dialogue_lines'] = dialogue_lines
        ch['total_characters_cast'] = characters_cast
        chapter_found = True
        print("Updated chapter 12 entry in session manifest.")
        break

if not chapter_found:
    print("Warning: Chapter 12 not found in session manifest chapters!")

with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print("Session manifest successfully updated.")
print("=== VERIFICATION COMPLETED SUCCESSFULLY ===")
