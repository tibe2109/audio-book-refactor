import json
import os
import glob

chapter_dir = "/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/20-Hoi-20"
script_path = os.path.join(chapter_dir, "theatrical_script.json")
bible_path = os.path.join(chapter_dir, ".theatrical_bible.json")
manifest_path = "/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/.session_manifest.json"

print("--- Verifying theatrical_script.json ---")
with open(script_path, "r", encoding="utf-8") as f:
    script_data = json.load(f)

total_lines = len(script_data)
dialogue_lines = sum(1 for x in script_data if x.get("type") == "dialogue")
poem_lines = sum(1 for x in script_data if x.get("type") == "poem")
narrator_lines = sum(1 for x in script_data if x.get("type") == "narrator")

speakers = set(x.get("speaker") for x in script_data if x.get("speaker"))
print(f"Total theatrical lines: {total_lines}")
print(f"Dialogue lines: {dialogue_lines}")
print(f"Poem lines: {poem_lines}")
print(f"Narrator lines: {narrator_lines}")
print(f"Unique speakers/characters cast: {list(speakers)}")
print(f"Total characters cast count: {len(speakers)}")

print("--- Verifying .theatrical_bible.json ---")
if os.path.exists(bible_path):
    with open(bible_path, "r", encoding="utf-8") as f:
        bible_data = json.load(f)
    print("Bible loaded successfully. Type:", type(bible_data))
else:
    print(".theatrical_bible.json not found!")

# Update session manifest
with open(manifest_path, "r", encoding="utf-8") as f:
    manifest = json.load(f)

updated = False
chapters_list = manifest.get("chapters", [])
for ch in chapters_list:
    if isinstance(ch, dict) and (ch.get("chapter_id") == "20-Hoi-20" or ch.get("slug") == "20-Hoi-20" or ch.get("id") == "20-Hoi-20" or ch.get("chapter_slug") == "20-Hoi-20" or ch.get("title", "").startswith("Hồi 20")):
        ch["step_8a_status"] = "completed"
        ch["total_theatrical_lines"] = total_lines
        ch["total_poem_lines"] = poem_lines
        ch["total_dialogue_lines"] = dialogue_lines
        ch["total_characters_cast"] = len(speakers)
        updated = True
        print("Updated manifest entry for 20-Hoi-20:", ch)

if not updated:
    # If not found by chapter_id, let's search by index or add/update
    for i, ch in enumerate(chapters_list):
        if isinstance(ch, dict) and ("20" in str(ch.get("chapter_id", "")) or "20" in str(ch.get("slug", ""))):
            print(f"Found chapter at index {i}: {ch}")
            ch["step_8a_status"] = "completed"
            ch["total_theatrical_lines"] = total_lines
            ch["total_poem_lines"] = poem_lines
            ch["total_dialogue_lines"] = dialogue_lines
            ch["total_characters_cast"] = len(speakers)
            updated = True
            break

if not updated:
    # Create or append chapter entry if missing
    new_entry = {
        "chapter_id": "20-Hoi-20",
        "slug": "20-Hoi-20",
        "title": "Hồi 20",
        "step_8a_status": "completed",
        "total_theatrical_lines": total_lines,
        "total_poem_lines": poem_lines,
        "total_dialogue_lines": dialogue_lines,
        "total_characters_cast": len(speakers)
    }
    chapters_list.append(new_entry)
    print("Added new chapter entry for 20-Hoi-20 to manifest.")

manifest["step_8a_status"] = "completed"
manifest["theatrical_characters_total"] = len(speakers)
manifest["theatrical_dialogues_total"] = dialogue_lines
manifest["theatrical_poems_total"] = poem_lines

with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)
print("Session manifest saved successfully.")
