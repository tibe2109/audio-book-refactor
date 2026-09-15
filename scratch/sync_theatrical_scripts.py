#!/usr/bin/env python3
import os
import re
import json
import glob

# Emotion deltas table from Step 08A spec
EMOTION_DELTAS = {
    'cuong_no': {'pitch': 5, 'rate': 6},
    'dau_don_trang_troi': {'pitch': -4, 'rate': -8},
    'de_doa_tham_hiem': {'pitch': -4, 'rate': -4},
    'ninh_bo_van_xin': {'pitch': 5, 'rate': 5},
    'hoi_hop_thi_thao': {'pitch': 1, 'rate': -4},
    'doc_thoai_dan_vat': {'pitch': -2, 'rate': -3},
    'ghen_tuong_cay_dang': {'pitch': 2, 'rate': 2},
    'nguong_ngung_tinh_dau': {'pitch': 3, 'rate': 0},
    'bang_hoang_chet_lang': {'pitch': 0, 'rate': -8},
    'hoan_ca_dac_thang': {'pitch': 3, 'rate': 4},
    'mia_mai_cham_biem': {'pitch': 2, 'rate': -2},
    'met_moi_buong_xuoi': {'pitch': -4, 'rate': -6},
    'binh_than_tu_nhien': {'pitch': 0, 'rate': 0},
}

BASE_DIR = "Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia"
chapter_dirs = sorted(glob.glob(os.path.join(BASE_DIR, "*-Hoi-*")))
print(f"Synchronizing theatrical_scripts in {len(chapter_dirs)} chapters...")

total_lines_updated = 0
unique_script_pitches = set()

for c_dir in chapter_dirs:
    script_file = os.path.join(c_dir, "theatrical_script.json")
    bible_file = os.path.join(c_dir, ".theatrical_bible.json")
    if not os.path.exists(script_file) or not os.path.exists(bible_file):
        continue
    
    with open(bible_file, 'r', encoding='utf-8') as f:
        b_data = json.load(f)
    chars = b_data.get('characters', {})

    with open(script_file, 'r', encoding='utf-8') as f:
        lines = json.load(f)
    
    dirty = False
    for item in lines:
        if item.get('type') == 'dialogue':
            spk = item.get('speaker')
            if spk in chars:
                c_prof = chars[spk]
                item['age_stage'] = c_prof.get('age_stage', item.get('age_stage'))
                item['temperament'] = c_prof.get('temperament', item.get('temperament'))
                item['timbre_eq'] = c_prof.get('timbre_eq', item.get('timbre_eq'))
                
                # Base acoustic from bible
                base_p_match = re.search(r'[-+]?\d+', c_prof.get('base_pitch', '+0Hz'))
                base_p = int(base_p_match.group()) if base_p_match else 0
                
                base_r_match = re.search(r'[-+]?\d+', c_prof.get('base_rate', '+0%'))
                base_r = int(base_r_match.group()) if base_r_match else 0
                
                # Emotion adjustment
                emo = item.get('emotion', 'binh_than_tu_nhien')
                d_emo = EMOTION_DELTAS.get(emo, {'pitch': 0, 'rate': 0})
                
                final_p = base_p + d_emo['pitch']
                final_r = base_r + d_emo['rate']
                
                # Clamping
                final_p = max(-10, min(12, final_p))
                final_r = max(-25, min(20, final_r))
                
                p_str = f"+{final_p}Hz" if final_p > 0 else (f"{final_p}Hz" if final_p < 0 else "+0Hz")
                r_str = f"+{final_r}%" if final_r > 0 else (f"{final_r}%" if final_r < 0 else "+0%")
                
                item['pitch'] = p_str
                item['rate'] = r_str
                unique_script_pitches.add(p_str)
                total_lines_updated += 1
                dirty = True
        elif 'pitch' in item:
            unique_script_pitches.add(item['pitch'])

    if dirty:
        with open(script_file, 'w', encoding='utf-8') as f:
            json.dump(lines, f, ensure_ascii=False, indent=2)

print(f"Synchronized {total_lines_updated} dialogue lines across all chapters.")
print("Updated Script pitch range:", sorted(list(unique_script_pitches), key=lambda x: int(re.search(r'[-+]?\d+', x).group())))
