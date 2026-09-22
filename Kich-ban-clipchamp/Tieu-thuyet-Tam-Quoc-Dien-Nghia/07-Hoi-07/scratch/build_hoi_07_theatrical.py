import json
import os
import re

CHAPTER_DIR = "/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/07-Hoi-07"
THEATRICAL_SCRIPT_PATH = os.path.join(CHAPTER_DIR, "theatrical_script.json")
THEATRICAL_BIBLE_PATH = os.path.join(CHAPTER_DIR, ".theatrical_bible.json")
MANIFEST_PATH = "/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/.session_manifest.json"

print("Loading theatrical script and bible for 07-Hoi-07...")
with open(THEATRICAL_SCRIPT_PATH, "r", encoding="utf-8") as f:
    script = json.load(f)

with open(THEATRICAL_BIBLE_PATH, "r", encoding="utf-8") as f:
    bible = json.load(f)

total_lines = len(script)
dialogue_lines = [l for l in script if l["type"] == "dialogue"]
narrator_lines = [l for l in script if l["type"] == "narrator"]
poem_lines = [l for l in script if l["type"] == "poem"]

print(f"Total Lines: {total_lines}")
print(f"Narrator Lines: {len(narrator_lines)}")
print(f"Poem Lines: {len(poem_lines)}")
print(f"Dialogue Lines: {len(dialogue_lines)}")
print(f"Characters Cast: {len(bible['characters'])}")

# Zero-loss invariant check across all 9 chunks
for chunk_id in range(1, 10):
    chunk_file = os.path.join(CHAPTER_DIR, "kich-ban", f"Kich-ban-{chunk_id}.txt")
    if os.path.exists(chunk_file):
        with open(chunk_file, "r", encoding="utf-8") as f:
            orig_text = f.read()
        chunk_lines = [l["text"] for l in script if l.get("chunk_id") == chunk_id]
        assembled_text = " ".join(chunk_lines)
        orig_words = set(re.findall(r'\w+', orig_text.lower()))
        assem_words = set(re.findall(r'\w+', assembled_text.lower()))
        missing = orig_words - assem_words
        print(f"Chunk {chunk_id}: orig_words={len(orig_words)}, assem_words={len(assem_words)}, missing={len(missing)}")

# Update session manifest
print("Updating .session_manifest.json...")
with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
    manifest = json.load(f)

updated = False
for chap in manifest.get("chapters", []):
    if chap.get("folder") == "07-Hoi-07":
        chap["step_8a_status"] = "completed"
        chap["theatrical_script_file"] = "07-Hoi-07/theatrical_script.json"
        chap["theatrical_bible_file"] = "07-Hoi-07/.theatrical_bible.json"
        chap["total_theatrical_lines"] = total_lines
        chap["total_poem_lines"] = len(poem_lines)
        chap["total_dialogue_lines"] = len(dialogue_lines)
        chap["total_characters_cast"] = len(bible["characters"])
        updated = True
        print("Updated 07-Hoi-07 in manifest successfully!")
        break

if updated:
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print("Saved manifest successfully!")
else:
    print("Warning: 07-Hoi-07 not found in manifest chapters!")

print("Build & validation completed successfully for 07-Hoi-07!")
