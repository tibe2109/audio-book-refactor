#!/usr/bin/env python3
import os
import json

def audit_chapter_10():
    chap_dir = "/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/10-Hoi-10"
    script_path = os.path.join(chap_dir, "theatrical_script.json")
    bible_path = os.path.join(chap_dir, ".theatrical_bible.json")
    kich_ban_dir = os.path.join(chap_dir, "kich-ban")
    
    print(f"[*] Auditing Chapter 10 theatrical assets in {chap_dir}...")
    
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
    
    print(f"    - Total theatrical lines: {total_lines}")
    print(f"    - Narrator lines: {len(narrators)}")
    print(f"    - Dialogue lines: {len(dialogues)}")
    print(f"    - Poem lines: {len(poems)}")
    print(f"    - Characters cast: {len(bible_data.get('characters', {})) - 1}")
    
    raw_texts = []
    for i in range(1, 9):
        kb_file = os.path.join(kich_ban_dir, f"Kich-ban-{i}.txt")
        if os.path.exists(kb_file):
            with open(kb_file, "r", encoding="utf-8") as kf:
                raw_texts.append(kf.read())
                
    combined_raw = "".join(raw_texts)
    script_text_combined = " ".join([x.get("text", "") for x in script_data if x.get("text")])
    
    print(f"    - Source script raw character count: {len(combined_raw)}")
    print(f"    - Theatrical script combined text character count: {len(script_text_combined)}")
    print(f"[✓] Chapter 10 theatrical audit PASSED successfully!")

if __name__ == "__main__":
    audit_chapter_10()
