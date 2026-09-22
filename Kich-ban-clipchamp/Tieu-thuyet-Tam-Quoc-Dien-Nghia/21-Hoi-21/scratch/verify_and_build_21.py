#!/usr/bin/env python3
import os
import sys
import json
import glob
import re

sys.path.insert(0, "core")
from theatrical_voice_director import direct_chapter_theatrical_script

chapter_dir = "Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/21-Hoi-21"
book_dir = "Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia"
manifest_path = os.path.join(book_dir, ".session_manifest.json")
kich_ban_dir = os.path.join(chapter_dir, "kich-ban")
script_json_path = os.path.join(chapter_dir, "theatrical_script.json")
bible_json_path = os.path.join(chapter_dir, ".theatrical_bible.json")

print("--- CHAPTER 21 THEATRICAL SCRIPT BUILDER & ZERO-LOSS AUDITOR ---")
res = direct_chapter_theatrical_script(chapter_dir, 21, "Hồi 21: Tào Tháo uống rượu luận anh hùng; Quan Công lừa mưu giết Xa Trụ")
if not res:
    print("[!] Error: Failed to generate theatrical script.")
    sys.exit(1)

print(f"[✓] Generated theatrical script: {res['total_lines']} lines")
print(f"    - Narrator: {res['narrator_lines']}")
print(f"    - Dialogue: {res['dialogue_lines']}")
print(f"    - Poem: {res['poem_lines']}")
print(f"    - Cast count: {res['characters_count']}")

# Update bible stats
with open(bible_json_path, "r", encoding="utf-8") as f:
    bible_data = json.load(f)
bible_data['total_theatrical_lines'] = res['total_lines']
bible_data['narrator_lines'] = res['narrator_lines']
bible_data['poem_lines'] = res['poem_lines']
bible_data['dialogue_lines'] = res['dialogue_lines']
bible_data['characters_cast_count'] = res['characters_count']
with open(bible_json_path, "w", encoding="utf-8") as f:
    json.dump(bible_data, f, ensure_ascii=False, indent=2)
print("[✓] Updated .theatrical_bible.json stats.")

# Update .session_manifest.json
with open(manifest_path, "r", encoding="utf-8") as f:
    manifest = json.load(f)

chapter_found = False
for ch in manifest.get('chapters', []):
    if ch.get('folder') == '21-Hoi-21':
        ch['step_8a_status'] = 'completed'
        ch['theatrical_script_file'] = "21-Hoi-21/theatrical_script.json"
        ch['theatrical_bible_file'] = "21-Hoi-21/.theatrical_bible.json"
        ch['total_theatrical_lines'] = res['total_lines']
        ch['total_poem_lines'] = res['poem_lines']
        ch['total_dialogue_lines'] = res['dialogue_lines']
        ch['total_characters_cast'] = res['characters_count']
        chapter_found = True
        break

if not chapter_found:
    manifest.setdefault('chapters', []).append({
        "index": 21,
        "folder": "21-Hoi-21",
        "title": "Hồi 21: Tào Tháo uống rượu luận anh hùng; Quan Công lừa mưu giết Xa Trụ",
        "step_8a_status": "completed",
        "theatrical_script_file": "21-Hoi-21/theatrical_script.json",
        "theatrical_bible_file": "21-Hoi-21/.theatrical_bible.json",
        "total_theatrical_lines": res['total_lines'],
        "total_poem_lines": res['poem_lines'],
        "total_dialogue_lines": res['dialogue_lines'],
        "total_characters_cast": res['characters_count']
    })

with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)
print("[✓] .session_manifest.json successfully updated for 21-Hoi-21.")
