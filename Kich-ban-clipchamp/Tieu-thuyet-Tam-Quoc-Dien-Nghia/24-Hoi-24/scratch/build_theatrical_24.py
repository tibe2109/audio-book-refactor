import os
import re
import json
import datetime

chapter_dir = "/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/24-Hoi-24"
kich_ban_dir = os.path.join(chapter_dir, "kich-ban")
script_path = os.path.join(chapter_dir, "theatrical_script.json")
bible_path = os.path.join(chapter_dir, ".theatrical_bible.json")
manifest_path = os.path.join(chapter_dir, "..", ".session_manifest.json")

print("=== BUILDING GRANULAR THEATRICAL SCRIPT & BIBLE FOR CHAPTER 24 (ROBUST MULTI-DIALOGUE PARSER) ===")

theatrical_lines = []
line_id = 1
total_dialogues = 0
total_poems = 0
total_narrators = 0
characters_set = set()

def add_line(chunk_id, line_type, speaker, text, narrative_mode="contemplative", pitch="-2Hz", rate="-12%", lead_in_pause="0.30s", timbre_eq="intimate_narrator", emotion="binh_than", voice="vi-VN-NamMinhNeural", character_name=None, age_stage="thanh_xuan", temperament="binh_thuong"):
    global line_id, total_dialogues, total_poems, total_narrators
    if not text:
        return
    characters_set.add(speaker)
    if line_type == "dialogue":
        total_dialogues += 1
    elif line_type == "poem":
        total_poems += 1
    else:
        total_narrators += 1

    entry = {
        "line_id": line_id,
        "chunk_id": chunk_id,
        "type": line_type,
        "speaker": speaker,
        "text": text,
        "voice": voice,
        "pitch": pitch,
        "rate": rate,
        "lead_in_pause": lead_in_pause,
        "timbre_eq": timbre_eq,
        "emotion": emotion
    }
    if character_name:
        entry["character_name"] = character_name
    if line_type == "dialogue":
        entry["age_stage"] = age_stage
        entry["temperament"] = temperament
    if line_type == "narrator":
        entry["narrative_mode"] = narrative_mode
    theatrical_lines.append(entry)
    line_id += 1

# Load original chunks
chunk_texts = {}
for i in range(1, 6):
    fpath = os.path.join(kich_ban_dir, f"Kich-ban-{i}.txt")
    with open(fpath, "r", encoding="utf-8") as f:
        chunk_texts[i] = f.read()

full_original = "".join([chunk_texts[i] for i in range(1, 6)])

def split_sentences(text):
    pattern = r'(?<=[.?!;:])\s+'
    matches = list(re.finditer(pattern, text))
    if not matches:
        return [text]
    fragments = []
    last = 0
    for m in matches:
        end = m.end()
        fragments.append(text[last:end])
        last = end
    if last < len(text):
        fragments.append(text[last:])
    return fragments

# Define all attribution patterns with speaker info
attribution_patterns = [
    ("Trình Dục can rằng,", "Trinh_Duc", "vi-VN-NamMinhNeural", "Trình Dục", "+0Hz", "-2%", "warm_authority", "binh_than_tu_nhien"),
    ("Vua run cầm rập nói,", "Hien_De", "vi-VN-NamMinhNeural", "Hiến Đế", "+1Hz", "+2%", "warm_authority", "so_hai"),
    ("Đổng Quý phi ở bên cạnh đỡ lời,", "Dong_Quy_Phi", "vi-VN-HoaiMyNeural", "Đổng Quý Phi", "+0Hz", "-5%", "gentle_female", "cau_xin"),
    ("Phục hậu khóc lóc can rằng,", "Phuc_Hau", "vi-VN-HoaiMyNeural", "Phục Hậu", "+0Hz", "-5%", "gentle_female", "dau_don"),
    ("Đổng phi khóc nói,", "Dong_Quy_Phi", "vi-VN-HoaiMyNeural", "Đổng Quý Phi", "+0Hz", "-5%", "gentle_female", "tuyet_vong"),
    ("Tháo giận nói,", "Tao_Thao", "vi-VN-NamMinhNeural", "Tào Tháo", "+0Hz", "-5%", "sharp_cunning", "gian_du"),
    ("Dục nói,", "Trinh_Duc", "vi-VN-NamMinhNeural", "Trình Dục", "+0Hz", "-2%", "warm_authority", "binh_than_tu_nhien"),
    ("Quách Gia nói,", "Quach_Gia", "vi-VN-NamMinhNeural", "Quách Gia", "+0Hz", "-5%", "sharp_cunning", "binh_than_tu_nhien"),
    ("Gia nói,", "Quach_Gia", "vi-VN-NamMinhNeural", "Quách Gia", "+0Hz", "-5%", "sharp_cunning", "binh_than_tu_nhien"),
    ("Phong ngạc nhiên quá hỏi,", "Dien_Phong", "vi-VN-NamMinhNeural", "Điền Phong", "+0Hz", "-5%", "warm_authority", "ngac_nhien"),
    ("Phong nói,", "Dien_Phong", "vi-VN-NamMinhNeural", "Điền Phong", "+0Hz", "-5%", "warm_authority", "thuyet_phuc"),
    ("Thiệu nói,", "Yuan_Shao", "vi-VN-NamMinhNeural", "Viên Thiệu", "-1Hz", "-5%", "chest_resonance", "tuyet_vong"),
    ("Trương Phi nói,", "Truong_Phi", "vi-VN-NamMinhNeural", "Trương Phi", "+1Hz", "+2%", "chest_resonance", "hao_sang"),
    ("Huyền Đức nói,", "Luu_Bi", "vi-VN-NamMinhNeural", "Lưu Bị", "+0Hz", "-5%", "warm_authority", "khiêm_nhu"),
    ("Tuân Úc hỏi,", "Tuan_Uc", "vi-VN-NamMinhNeural", "Tuân Úc", "+0Hz", "-5%", "sharp_cunning", "cau_hoi"),
    ("Tuân Úc nói,", "Tuan_Uc", "vi-VN-NamMinhNeural", "Tuân Úc", "+0Hz", "-5%", "sharp_cunning", "lo_lang"),
    ("Mao Giới thưa,", "Mao_Gioi", "vi-VN-NamMinhNeural", "Mao Giới", "+0Hz", "-5%", "warm_authority", "tu_tin"),
    ("đáp lễ, nói,", "Yuan_Shao", "vi-VN-NamMinhNeural", "Viên Thiệu", "-1Hz", "-5%", "chest_resonance", "vui_mung"),
    ("Trình Dục nói,", "Trinh_Duc", "vi-VN-NamMinhNeural", "Trình Dục", "+0Hz", "-2%", "warm_authority", "binh_than_tu_nhien"),
    ("Tháo nói,", "Tao_Thao", "vi-VN-NamMinhNeural", "Tào Tháo", "+0Hz", "-5%", "sharp_cunning", "tu_tin"),
    ("bèn hỏi,", "Dien_Phong", "vi-VN-NamMinhNeural", "Điền Phong", "+0Hz", "-5%", "warm_authority", "lo_lang"),
]

for chunk_id in range(1, 6):
    text = chunk_texts[chunk_id]
    paragraphs = text.split("\n\n")
    for p_idx, p in enumerate(paragraphs):
        p_full = p + ("\n\n" if p_idx < len(paragraphs) - 1 else "")
        if not p.strip():
            add_line(chunk_id, "narrator", "Narrator", p_full, narrative_mode="contemplative", pitch="-2Hz", rate="-12%", lead_in_pause="0.30s", timbre_eq="contemplative_narrator", emotion="binh_than")
            continue
        if p.strip() == ". ......":
            add_line(chunk_id, "narrator", "Narrator", p_full, narrative_mode="contemplative", pitch="-2Hz", rate="-12%", lead_in_pause="1.50s", timbre_eq="contemplative_narrator", emotion="binh_than")
            continue
        if "HỒI HAI MƯƠI BỐN" in p or "QUỐC TẶC HÀNH HUNG" in p:
            add_line(chunk_id, "narrator", "Narrator", p_full, narrative_mode="epic", pitch="+1Hz", rate="+0%", lead_in_pause="0.50s", timbre_eq="epic_narrator", emotion="hao_hung")
            continue
        if "Ngán cho thế Hán, đã cô cùng!" in p or "Cướp trại còn mong một chút công" in p:
            add_line(chunk_id, "poem", "Poet", p_full, pitch="-2Hz", rate="-18%", lead_in_pause="0.85s", timbre_eq="poetic_recitation", emotion="bi_trang", voice="vi-VN-NamMinhNeural", character_name="Người ngâm thơ")
            continue

        # Process paragraph by finding all matching attribution patterns sequentially
        remaining = p_full
        while remaining.strip():
            found_delim = None
            found_idx = 1000000
            for delim, spk, voice, cname, pitch, rate, teq, emo in attribution_patterns:
                idx = remaining.find(delim)
                if idx != -1 and idx < found_idx:
                    found_idx = idx
                    found_delim = (delim, spk, voice, cname, pitch, rate, teq, emo)
            
            if found_delim is not None:
                delim, spk, voice, cname, pitch, rate, teq, emo = found_delim
                narr_part = remaining[:found_idx + len(delim)]
                if narr_part.strip():
                    add_line(chunk_id, "narrator", "Narrator", narr_part, narrative_mode="contemplative", pitch="-2Hz", rate="-12%", lead_in_pause="0.30s", timbre_eq="contemplative_narrator", emotion="binh_than")
                remaining = remaining[found_idx + len(delim):]
                
                # Extract dialogue until next delimiter or end of paragraph
                next_idx = 1000000
                for d, _, _, _, _, _, _, _ in attribution_patterns:
                    idx = remaining.find(d)
                    if idx != -1 and idx < next_idx:
                        next_idx = idx
                
                if next_idx != 1000000:
                    diag_part = remaining[:next_idx]
                    remaining = remaining[next_idx:]
                else:
                    diag_part = remaining
                    remaining = ""
                
                if diag_part.strip():
                    sents = split_sentences(diag_part)
                    for s in sents:
                        add_line(chunk_id, "dialogue", spk, s, pitch=pitch, rate=rate, lead_in_pause="0.35s", timbre_eq=teq, emotion=emo, voice=voice, character_name=cname)
            else:
                # No more delimiters in remaining text, treat as narrator sentences
                sents = split_sentences(remaining)
                for s in sents:
                    add_line(chunk_id, "narrator", "Narrator", s, narrative_mode="contemplative", pitch="-2Hz", rate="-12%", lead_in_pause="0.30s", timbre_eq="contemplative_narrator", emotion="binh_than")
                remaining = ""

# Verify Zero-Loss Invariant
reconstructed = "".join([e["text"] for e in theatrical_lines])
print(f"Original full length: {len(full_original)}, Reconstructed length: {len(reconstructed)}")
assert full_original == reconstructed, f"ZERO LOSS INVARIANT FAILED! Diff len: {len(full_original)} vs {len(reconstructed)}"
print("SUCCESS: 100% ZERO LOSS INVARIANT VERIFIED!")

print(f"Total theatrical lines: {len(theatrical_lines)}")
print(f"Total dialogue lines: {total_dialogues}")
print(f"Total poem lines: {total_poems}")
print(f"Total narrator lines: {total_narrators}")
print(f"Total characters cast: {len(characters_set)}")
print(f"Characters set: {characters_set}")

# Save theatrical script
with open(script_path, "w", encoding="utf-8") as f:
    json.dump(theatrical_lines, f, ensure_ascii=False, indent=2)

# Save theatrical bible
character_bible = {
    "chapter_folder": "24-Hoi-24",
    "chapter_index": 24,
    "chapter_title": "Hồi 24: Quốc tặc hành hung giết quý phi; Hoàng Thúc thua chạy sang Viên Thiệu",
    "genre": "classical_epic_literature",
    "total_theatrical_lines": len(theatrical_lines),
    "narrator_lines": total_narrators,
    "poem_lines": total_poems,
    "dialogue_lines": total_dialogues,
    "characters_cast_count": len(characters_set),
    "characters": list(characters_set),
    "directed_at": "vi-VN-NamMinhNeural & vi-VN-HoaiMyNeural",
    "timestamp": datetime.datetime.now().isoformat()
}
with open(bible_path, "w", encoding="utf-8") as f:
    json.dump(character_bible, f, ensure_ascii=False, indent=2)

# Update session manifest
with open(manifest_path, "r", encoding="utf-8") as f:
    manifest = json.load(f)

for chap in manifest.get("chapters", []):
    if chap.get("folder") == "24-Hoi-24":
        chap["step_8a_status"] = "completed"
        chap["total_theatrical_lines"] = len(theatrical_lines)
        chap["total_poem_lines"] = total_poems
        chap["total_dialogue_lines"] = total_dialogues
        chap["total_characters_cast"] = len(characters_set)
        chap["theatrical_script_file"] = "24-Hoi-24/theatrical_script.json"
        chap["theatrical_bible_file"] = "24-Hoi-24/.theatrical_bible.json"
        print("Updated Chapter 24 in manifest successfully.")

manifest["updated_at"] = datetime.datetime.now().isoformat()
with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print("ALL CHAPTER 24 BUILD & MANIFEST UPDATE TASKS COMPLETED SUCCESSFULLY!")
