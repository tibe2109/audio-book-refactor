import os
import json
import glob
import re

chapter_dir = "/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/09-Hoi-09"
kich_ban_dir = os.path.join(chapter_dir, "kich-ban")
script_path = os.path.join(chapter_dir, "theatrical_script.json")

kb_files = sorted(glob.glob(os.path.join(kich_ban_dir, "Kich-ban-*.txt")), key=lambda x: int(os.path.basename(x).split('-')[2].split('.')[0]))

original_chunks_text = {}
for fpath in kb_files:
    fname = os.path.basename(fpath)
    with open(fpath, "r", encoding="utf-8") as f:
        original_chunks_text[fname] = f.read()

with open(script_path, "r", encoding="utf-8") as f:
    script_data = json.load(f)

# Reconstruct text from script entries
script_texts_by_chunk = {}
for item in script_data:
    chunk_id = item.get('chunk_id', 'Kich-ban-1.txt')
    if chunk_id not in script_texts_by_chunk:
        script_texts_by_chunk[chunk_id] = []
    text = item.get('text', '')
    script_texts_by_chunk[chunk_id].append(text)

print("Checking character speaker distribution and properties:")
speakers = set()
for item in script_data:
    if item.get('type') == 'dialogue':
        spk = item.get('speaker')
        speakers.add(spk)
        print(f"  Speaker: {spk}, Voice: {item.get('voice')}, Pitch: {item.get('pitch')}, Emotion: {item.get('emotion')}")

print("\nSpeakers found:", sorted(list(speakers)))
print("Total entries in theatrical_script.json:", len(script_data))
print("Poems count:", sum(1 for i in script_data if i.get('type') == 'poem'))
print("Dialogues count:", sum(1 for i in script_data if i.get('type') == 'dialogue'))
print("Narrators count:", sum(1 for i in script_data if i.get('type') == 'narrator'))
