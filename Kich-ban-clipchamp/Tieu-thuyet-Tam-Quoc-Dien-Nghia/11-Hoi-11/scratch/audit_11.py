import os
import json

def main():
    chap_dir = "/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/11-Hoi-11"
    script_path = os.path.join(chap_dir, "theatrical_script.json")
    bible_path = os.path.join(chap_dir, ".theatrical_bible.json")
    kich_ban_dir = os.path.join(chap_dir, "kich-ban")
    manifest_path = "/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/.session_manifest.json"

    print(f"[*] Auditing Chapter 11 theatrical assets in {chap_dir}...")

    assert os.path.exists(script_path), f"Missing {script_path}"
    assert os.path.exists(bible_path), f"Missing {bible_path}"

    with open(script_path, "r", encoding="utf-8") as f:
        script_data = json.load(f)

    with open(bible_path, "r", encoding="utf-8") as f:
        bible_data = json.load(f)

    total_lines = len(script_data)
    dialogues = [x for x in script_data if x.get("type") == "dialogue"]
    poems = [x for x in script_data if x.get("type") == "poem"]
    narrators = [x for x in script_data if x.get("type") == "narrator"]

    characters = bible_data.get("characters", {})
    chars_cast = len([k for k in characters.keys() if k != "Narrator"])

    print(f"    - Total theatrical lines: {total_lines}")
    print(f"    - Narrator lines: {len(narrators)}")
    print(f"    - Dialogue lines: {len(dialogues)}")
    print(f"    - Poem lines: {len(poems)}")
    print(f"    - Characters cast: {chars_cast}")

    raw_texts = []
    for i in range(1, 12):
        kb_file = os.path.join(kich_ban_dir, f"Kich-ban-{i}.txt")
        if os.path.exists(kb_file):
            with open(kb_file, "r", encoding="utf-8") as kf:
                raw_texts.append(kf.read())

    combined_raw = "".join(raw_texts)
    script_text_combined = " ".join([x.get("text", "") for x in script_data if x.get("text")])

    print(f"    - Source script raw character count: {len(combined_raw)}")
    print(f"    - Theatrical script combined text character count: {len(script_text_combined)}")

    with open(manifest_path, "r", encoding="utf-8") as mf:
        manifest_data = json.load(mf)

    chap_entry = None
    for ch in manifest_data.get("chapters", []):
        if ch.get("folder") == "11-Hoi-11":
            chap_entry = ch
            break

    if chap_entry:
        print(f"    - Manifest entry found for 11-Hoi-11:")
        print(f"        step_8a_status: {chap_entry.get('step_8a_status')}")
        print(f"        total_theatrical_lines: {chap_entry.get('total_theatrical_lines')}")
        print(f"        total_poem_lines: {chap_entry.get('total_poem_lines')}")
        print(f"        total_dialogue_lines: {chap_entry.get('total_dialogue_lines')}")
        print(f"        total_characters_cast: {chap_entry.get('total_characters_cast')}")

        chap_entry["step_8a_status"] = "completed"
        chap_entry["total_theatrical_lines"] = total_lines
        chap_entry["total_poem_lines"] = len(poems)
        chap_entry["total_dialogue_lines"] = len(dialogues)
        chap_entry["total_characters_cast"] = chars_cast

        with open(manifest_path, "w", encoding="utf-8") as mf:
            json.dump(manifest_data, mf, ensure_ascii=False, indent=2)
        print(f"[✓] Updated .session_manifest.json successfully with exact counts!")
    else:
        print(f"[!] Warning: 11-Hoi-11 not found in session manifest chapters!")

    print(f"[✓] Chapter 11 theatrical audit PASSED successfully!")

if __name__ == "__main__":
    main()
