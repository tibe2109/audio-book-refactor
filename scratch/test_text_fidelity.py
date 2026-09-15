import json
import os
import re

CHAPTER_DIR = "/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/06-Hoi-06"
THEATRICAL_SCRIPT_PATH = os.path.join(CHAPTER_DIR, "theatrical_script.json")

with open(THEATRICAL_SCRIPT_PATH, "r", encoding="utf-8") as f:
    script = json.load(f)

for chunk_id in range(1, 10):
    chunk_file = os.path.join(CHAPTER_DIR, "kich-ban", f"Kich-ban-{chunk_id}.txt")
    with open(chunk_file, "r", encoding="utf-8") as f:
        orig_text = f.read()

    chunk_lines = [l["text"] for l in script if l["chunk_id"] == chunk_id]
    assembled_text = " ".join(chunk_lines)

    # Normalize words for comparison
    orig_words = re.findall(r'\w+', orig_text.lower())
    assem_words = re.findall(r'\w+', assembled_text.lower())

    orig_set = set(orig_words)
    assem_set = set(assem_words)

    missing = orig_set - assem_set
    extra = assem_set - orig_set

    print(f"Chunk {chunk_id}: orig_words={len(orig_words)}, assem_words={len(assem_words)}")
    if missing:
        print(f"  Missing in chunk {chunk_id}: {missing}")
    if extra:
        print(f"  Extra in chunk {chunk_id}: {extra}")
