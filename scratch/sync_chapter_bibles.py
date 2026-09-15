#!/usr/bin/env python3
import os
import json
import glob
import re

from build_theatrical_bible import (
    resolve_character_age_stage, resolve_character_temperament,
    resolve_character_timbre, calculate_base_acoustic,
    AGE_NAMES_VI, TEMPERAMENT_NAMES_VI, ATSE_DESCRIPTIONS
)

BASE_DIR = "Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia"
chapter_dirs = sorted(glob.glob(os.path.join(BASE_DIR, "*-Hoi-*")))
print(f"Syncing {len(chapter_dirs)} chapter bibles...")

total_updated = 0
unique_ch_pitches = set()
unique_ch_stages = set()
unique_ch_temps = set()
unique_ch_timbres = set()

for c_dir in chapter_dirs:
    bible_file = os.path.join(c_dir, ".theatrical_bible.json")
    if not os.path.exists(bible_file):
        continue
    
    with open(bible_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    c_folder = os.path.basename(c_dir)
    c_idx = data.get('chapter_index', int(re.search(r'\d+', c_folder).group()))
    
    characters = data.get('characters', {})
    for cid, c in characters.items():
        if cid == 'Narrator':
            continue
        cname = c.get('name', cid)
        gender = c.get('gender', 'male')
        
        # Determine exact age stage for this chapter
        stage = resolve_character_age_stage(cid, c_idx, cname)
        temp = resolve_character_temperament(cid, cname)
        p_str, r_str, p_val, r_val = calculate_base_acoustic(stage, temp)
        timbre = resolve_character_timbre(cid, gender, stage, temp)
        
        c['age_stage'] = stage
        c['base_pitch'] = p_str
        c['base_rate'] = r_str
        c['temperament'] = temp
        c['timbre_eq'] = timbre
        
        unique_ch_pitches.add(p_str)
        unique_ch_stages.add(stage)
        unique_ch_temps.add(temp)
        unique_ch_timbres.add(timbre)
    
    with open(bible_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    total_updated += 1

print(f"Successfully updated {total_updated} chapter .theatrical_bible.json files.")
print("Chapter bibles unique age stages:", unique_ch_stages)
print("Chapter bibles unique temperaments count:", len(unique_ch_temps))
print("Chapter bibles unique timbres:", unique_ch_timbres)
print("Chapter bibles pitch span:", sorted(list(unique_ch_pitches), key=lambda x: int(re.search(r'[-+]?\d+', x).group())))
