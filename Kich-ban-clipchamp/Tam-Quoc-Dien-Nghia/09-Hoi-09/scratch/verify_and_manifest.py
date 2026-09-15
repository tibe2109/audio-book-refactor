import os
import json
import glob

chapter_dir = "/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/09-Hoi-09"
kich_ban_dir = os.path.join(chapter_dir, "kich-ban")
script_path = os.path.join(chapter_dir, "theatrical_script.json")
bible_path = os.path.join(chapter_dir, ".theatrical_bible.json")
manifest_path = os.path.join(chapter_dir, ".session_manifest.json")

print("Reading script files from:", kich_ban_dir)
kb_files = sorted(glob.glob(os.path.join(kich_ban_dir, "Kich-ban-*.txt")), key=lambda x: int(os.path.basename(x).split('-')[2].split('.')[0]))

total_kb_text = ""
for fpath in kb_files:
    with open(fpath, "r", encoding="utf-8") as f:
        total_kb_text += f.read() + "\n"

print(f"Loaded {len(kb_files)} Kich-ban files. Total characters in source chunks: {len(total_kb_text)}")

if os.path.exists(script_path):
    with open(script_path, "r", encoding="utf-8") as f:
        script_data = json.load(f)
    print(f"Loaded theatrical_script.json with {len(script_data)} entries.")
else:
    print("WARNING: theatrical_script.json not found!")
    script_data = []

if os.path.exists(bible_path):
    with open(bible_path, "r", encoding="utf-8") as f:
        bible_data = json.load(f)
    print(f"Loaded .theatrical_bible.json successfully.")
else:
    print("WARNING: .theatrical_bible.json not found!")
    bible_data = {}

total_theatrical_lines = len(script_data)
total_poem_lines = sum(1 for item in script_data if item.get('type') == 'poem')
total_dialogue_lines = sum(1 for item in script_data if item.get('type') == 'dialogue')
narrator_lines = sum(1 for item in script_data if item.get('type') == 'narrator')

characters_cast = set()
for item in script_data:
    if item.get('type') == 'dialogue':
        speaker = item.get('speaker', 'Unknown')
        characters_cast.add(speaker)

print(f"Stats:")
print(f"  - Total Theatrical Lines: {total_theatrical_lines}")
print(f"  - Total Poem Lines: {total_poem_lines}")
print(f"  - Total Dialogue Lines: {total_dialogue_lines}")
print(f"  - Total Narrator Lines: {narrator_lines}")
print(f"  - Total Characters Cast: {len(characters_cast)} ({sorted(list(characters_cast))})")

manifest_data = {
    "chapter": "09-Hoi-09",
    "step_8a_status": "completed",
    "total_theatrical_lines": total_theatrical_lines,
    "total_poem_lines": total_poem_lines,
    "total_dialogue_lines": total_dialogue_lines,
    "total_narrator_lines": narrator_lines,
    "total_characters_cast": len(characters_cast),
    "characters_list": sorted(list(characters_cast)),
    "source_chunks_count": len(kb_files)
}

with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest_data, f, ensure_ascii=False, indent=2)

print("Successfully generated/updated .session_manifest.json at:", manifest_path)
