#!/usr/bin/env python3
import os
import re
import json
import glob
import datetime
from collections import defaultdict, Counter

# Import previous rules
from build_theatrical_bible import (
    LIFECYCLE_RULES, TEMPERAMENT_REGISTRY, AGE_BASE_PITCH, AGE_BASE_RATE,
    TEMPERAMENT_DELTAS, TEMPERAMENT_NAMES_VI, AGE_NAMES_VI, ATSE_DESCRIPTIONS,
    resolve_character_age_stage, resolve_character_temperament,
    resolve_character_timbre, calculate_base_acoustic
)

BASE_DIR = "Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia"
chapter_dirs = sorted(glob.glob(os.path.join(BASE_DIR, "*-Hoi-*")))
print(f"Found {len(chapter_dirs)} chapter directories.")

# 1. Collect all characters across 120 chapters
all_characters = {}
chapter_data = {}

for c_dir in chapter_dirs:
    c_folder = os.path.basename(c_dir)
    bible_file = os.path.join(c_dir, ".theatrical_bible.json")
    if not os.path.exists(bible_file):
        continue
    with open(bible_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    c_idx = data.get('chapter_index', int(re.search(r'\d+', c_folder).group()))
    c_title = data.get('chapter_title', '')
    chapter_data[c_idx] = {
        'folder': c_folder,
        'title': c_title,
        'original_bible': data
    }

    for cid, c in data.get('characters', {}).items():
        if cid == 'Narrator':
            continue
        if cid not in all_characters:
            all_characters[cid] = {
                'name': c.get('name', cid),
                'gender': c.get('gender', 'male'),
                'voice': c.get('voice', 'vi-VN-NamMinhNeural'),
                'chapters_active': [],
                'dialogue_count_total': 0,
                'sample_emotions': set(),
                'chapter_appearances_data': []
            }
        all_characters[cid]['chapters_active'].append(c_idx)
        all_characters[cid]['dialogue_count_total'] += c.get('dialogue_count', 0)
        for em in c.get('sample_emotions', []):
            all_characters[cid]['sample_emotions'].add(em)
        all_characters[cid]['chapter_appearances_data'].append({
            'chapter_index': c_idx,
            'dialogue_count': c.get('dialogue_count', 0),
            'emotions': c.get('sample_emotions', [])
        })

print(f"Total unique characters collected: {len(all_characters)}")

# 2. Build Master Character Profiles & Arcs
master_bible = {
    "work_title": "Tam Quốc Diễn Nghĩa",
    "total_chapters": 120,
    "directed_at": datetime.datetime.now().isoformat(),
    "master_theatrical_profiler": "Character Arc & Bible Profiler (Step 08A - arf_08a_theatrical_voice_director)",
    "total_unique_characters": len(all_characters),
    "acoustic_specification": {
        "pitch_scale": {
            "min_pitch": "-8Hz",
            "max_pitch": "+12Hz",
            "contrast_range_hz": 20,
            "formula": "Base Pitch = Age Acoustic Core + Temperament Delta"
        },
        "five_age_stages": {
            "au_tho": {"name_vi": "Ấu thơ (0-13 tuổi)", "base_pitch": "+9Hz", "range": "+8Hz đến +12Hz"},
            "nien_thieu": {"name_vi": "Niên thiếu / Vỡ giọng (14-18 tuổi)", "base_pitch": "+5Hz", "range": "+4Hz đến +7Hz"},
            "thanh_xuan": {"name_vi": "Thanh xuân (19-35 tuổi)", "base_pitch": "+1Hz", "range": "0Hz đến +3Hz"},
            "trung_nien": {"name_vi": "Trung niên (36-55 tuổi)", "base_pitch": "-4Hz", "range": "-3Hz đến -5Hz"},
            "lao_hoa": {"name_vi": "Lão hóa (>55 tuổi)", "base_pitch": "-7Hz", "range": "-6Hz đến -8Hz"}
        },
        "ten_temperaments": TEMPERAMENT_NAMES_VI,
        "five_atse_timbres": ATSE_DESCRIPTIONS
    },
    "narrator_profile": {
        "name": "Người dẫn chuyện",
        "gender": "male",
        "voice": "vi-VN-NamMinhNeural",
        "base_pitch": "+0Hz",
        "base_rate": "-5%",
        "lead_in_pause": "0.20s",
        "narrative_modes": [
            "epic", "elegiac", "suspense", "contemplative", "intimate",
            "melancholic_social", "satirical_ironic", "existential_interior"
        ]
    },
    "characters": {}
}

# Stats counters
stats_age_stages = Counter()
stats_temperaments = Counter()
stats_timbres = Counter()
stats_pitches = Counter()

for cid, info in sorted(all_characters.items(), key=lambda x: -x[1]['dialogue_count_total']):
    cname = info['name']
    gender = info['gender']
    voice = "vi-VN-HoaiMyNeural" if gender == "female" else "vi-VN-NamMinhNeural"
    temp = resolve_character_temperament(cid, cname)
    
    # Character Arc across chapters
    chaps = sorted(info['chapters_active'])
    first_c, last_c = chaps[0], chaps[-1]
    
    # Determine full arc
    arc_stages = []
    if cid in LIFECYCLE_RULES:
        for max_c, st, desc in LIFECYCLE_RULES[cid]:
            # Check if character appeared in this range
            sub_chaps = [c for c in chaps if c <= max_c and (not arc_stages or c > arc_stages[-1]['max_chapter'])]
            p_str, r_str, p_val, r_val = calculate_base_acoustic(st, temp)
            timbre = resolve_character_timbre(cid, gender, st, temp)
            arc_stages.append({
                "max_chapter": max_c,
                "age_stage": st,
                "age_stage_vietnamese": AGE_NAMES_VI[st],
                "base_pitch": p_str,
                "base_rate": r_str,
                "timbre_eq": timbre,
                "context_description": desc,
                "active_chapters": [c for c in chaps if (len(arc_stages) == 1 and c <= max_c) or (len(arc_stages) > 1 and arc_stages[-2]['max_chapter'] < c <= max_c)]
            })
    else:
        # Standard lifecycle based on active chapters
        # Group active chapters by age stage
        stage_groups = defaultdict(list)
        for c_idx in chaps:
            st = resolve_character_age_stage(cid, c_idx, cname)
            stage_groups[st].append(c_idx)
        
        for st in ['au_tho', 'nien_thieu', 'thanh_xuan', 'trung_nien', 'lao_hoa']:
            if st in stage_groups:
                p_str, r_str, p_val, r_val = calculate_base_acoustic(st, temp)
                timbre = resolve_character_timbre(cid, gender, st, temp)
                arc_stages.append({
                    "age_stage": st,
                    "age_stage_vietnamese": AGE_NAMES_VI[st],
                    "base_pitch": p_str,
                    "base_rate": r_str,
                    "timbre_eq": timbre,
                    "active_chapters": stage_groups[st]
                })

    primary_stage = arc_stages[0]['age_stage'] if arc_stages else 'thanh_xuan'
    primary_pitch = arc_stages[0]['base_pitch'] if arc_stages else '+1Hz'
    primary_timbre = arc_stages[0]['timbre_eq'] if arc_stages else 'warm_authority'
    
    # Record stats
    stats_age_stages[primary_stage] += 1
    stats_temperaments[temp] += 1
    stats_timbres[primary_timbre] += 1
    stats_pitches[primary_pitch] += 1

    master_bible["characters"][cid] = {
        "name": cname,
        "gender": gender,
        "voice": voice,
        "temperament": temp,
        "temperament_vietnamese": TEMPERAMENT_NAMES_VI[temp],
        "primary_timbre_eq": primary_timbre,
        "atse_profile": ATSE_DESCRIPTIONS[primary_timbre],
        "character_arc": arc_stages,
        "first_appearance_chapter": first_c,
        "last_appearance_chapter": last_c,
        "appearances_chapter_count": len(chaps),
        "total_dialogue_lines": info['dialogue_count_total'],
        "sample_emotions": sorted(list(info['sample_emotions']))
    }

master_bible["summary_statistics"] = {
    "total_characters": len(all_characters),
    "gender_distribution": {
        "male": sum(1 for c in all_characters.values() if c['gender'] == 'male'),
        "female": sum(1 for c in all_characters.values() if c['gender'] == 'female')
    },
    "age_stages_distribution": dict(stats_age_stages),
    "temperaments_distribution": dict(stats_temperaments),
    "atse_timbre_distribution": dict(stats_timbres),
    "pitch_distribution": dict(stats_pitches)
}

# Write master bible
master_bible_path = os.path.join(BASE_DIR, ".theatrical_bible.json")
with open(master_bible_path, 'w', encoding='utf-8') as f:
    json.dump(master_bible, f, ensure_ascii=False, indent=2)

print(f"Master Theatrical Bible written successfully to: {master_bible_path}")
print(f"Stats summary:")
print("  Age stages:", dict(stats_age_stages))
print("  Temperaments:", dict(stats_temperaments))
print("  Timbres:", dict(stats_timbres))
print("  Pitches:", dict(stats_pitches))
