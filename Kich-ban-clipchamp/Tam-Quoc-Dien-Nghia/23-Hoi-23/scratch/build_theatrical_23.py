import os
import re
import json
import datetime

chapter_dir = "/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/23-Hoi-23"
kich_ban_dir = os.path.join(chapter_dir, "kich-ban")
script_path = os.path.join(chapter_dir, "theatrical_script.json")
bible_path = os.path.join(chapter_dir, ".theatrical_bible.json")
manifest_path = os.path.join(chapter_dir, ".session_manifest.json")

print("=== BUILDING GRANULAR THEATRICAL SCRIPT & BIBLE FOR CHAPTER 23 (ZERO-LOSS) ===")

theatrical_lines = []
line_id = 1
total_dialogues = 0
total_poems = 0
total_narrators = 0
speakers_set = set()

def add_line(chunk_id, line_type, speaker, text, narrative_mode="contemplative", pitch="-2Hz", rate="-12%", lead_in_pause="0.30s", timbre_eq="intimate_narrator", emotion="binh_than"):
    global line_id, total_dialogues, total_poems, total_narrators
    if not text:
        return
    speakers_set.add(speaker)
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
        "voice": "vi-VN-NamMinhNeural",
        "pitch": pitch,
        "rate": rate,
        "lead_in_pause": lead_in_pause,
        "timbre_eq": timbre_eq,
        "emotion": emotion
    }
    if line_type == "narrator":
        entry["narrative_mode"] = narrative_mode
    theatrical_lines.append(entry)
    line_id += 1

def chunk_into_n_parts(text, target_parts=10):
    matches = list(re.finditer(r"(?<=[.?!;:])\s+", text))
    if not matches or len(matches) < target_parts:
        length = len(text)
        step = max(1, length // target_parts)
        indices = [i * step for i in range(1, target_parts)]
    else:
        step = len(matches) // target_parts
        indices = [matches[i * step].end() for i in range(1, target_parts)]
    
    parts = []
    last = 0
    for idx in indices:
        parts.append(text[last:idx])
        last = idx
    parts.append(text[last:])
    return parts

for chunk_id in range(1, 12):
    fpath = os.path.join(kich_ban_dir, f"Kich-ban-{chunk_id}.txt")
    if not os.path.exists(fpath):
        print(f"Warning: {fpath} not found")
        continue
    with open(fpath, "r", encoding="utf-8") as fh:
        content = fh.read()

    parts = chunk_into_n_parts(content, 10)
    for p in parts:
        cleaned = p.strip()
        if not cleaned:
            add_line(chunk_id, "narrator", "Narrator", p, narrative_mode="contemplative", pitch="-2Hz", rate="-12%", lead_in_pause="0.30s", timbre_eq="contemplative_narrator", emotion="binh_than")
            continue

        if cleaned == ". ......":
            add_line(chunk_id, "narrator", "Narrator", p, narrative_mode="contemplative", pitch="-2Hz", rate="-12%", lead_in_pause="1.50s", timbre_eq="contemplative_narrator", emotion="binh_than")
        elif "HỒI" in cleaned or "NỄ CHÍNH BÌNH" in cleaned or "Sử quan" in cleaned or "Chưa biết" in cleaned:
            add_line(chunk_id, "narrator", "Narrator", p, narrative_mode="epic", pitch="+1Hz", rate="+0%", lead_in_pause="0.50s", timbre_eq="epic_narrator", emotion="hao_hung")
        elif "có thơ rằng," in cleaned or "Hán triều," in cleaned or "Hoàng Tổ ra chi" in cleaned or "Mấy hàng chiếu đỏ" in cleaned or any(w in cleaned for w in ["Hán triều, đang vận yếu", "Thầy thuốc, Xưng Bình", "Xin thề, trừ gian đảng", "Liều thân, báo thánh minh"]):
            add_line(chunk_id, "poem", "Poet", p, pitch="-2Hz", rate="-18%", lead_in_pause="0.85s", timbre_eq="poetic_recitation", emotion="bi_trang")
        elif "Nễ Hành" in cleaned or "Hành" in cleaned and ("đáp" in cleaned or "nói" in cleaned or "than" in cleaned or "cười" in cleaned or "mắng" in cleaned):
            add_line(chunk_id, "dialogue", "Ne_Hanh", p, pitch="+3Hz", rate="-5%", lead_in_pause="0.40s", timbre_eq="youth_bright", emotion="ngong_cuong")
        elif "Cát Bình" in cleaned or "Bình" in cleaned and ("nói" in cleaned or "đáp" in cleaned or "mắng" in cleaned):
            add_line(chunk_id, "dialogue", "Cat_Binh", p, pitch="-1Hz", rate="-10%", lead_in_pause="0.40s", timbre_eq="chest_resonance", emotion="bi_trang")
        elif "Khổng Dung" in cleaned:
            add_line(chunk_id, "dialogue", "Khong_Dung", p, pitch="-1Hz", rate="-10%", lead_in_pause="0.35s", timbre_eq="warm_authority", emotion="tri_thuc")
        elif "Giả Hủ" in cleaned:
            add_line(chunk_id, "dialogue", "Jia_Xu", p, pitch="0Hz", rate="-8%", lead_in_pause="0.35s", timbre_eq="sharp_cunning", emotion="muu_mo")
        elif "Trương Tú" in cleaned:
            add_line(chunk_id, "dialogue", "Zhang_Xiu", p, pitch="0Hz", rate="-8%", lead_in_pause="0.35s", timbre_eq="chest_resonance", emotion="lo_lang")
        elif "Tháo" in cleaned:
            add_line(chunk_id, "dialogue", "Tao_Thao", p, pitch="0Hz", rate="-5%", lead_in_pause="0.35s", timbre_eq="sharp_cunning", emotion="giao_hoat")
        elif "Đổng Thừa" in cleaned or "Thừa" in cleaned:
            add_line(chunk_id, "dialogue", "Dong_Thieu", p, pitch="-1Hz", rate="-10%", lead_in_pause="0.35s", timbre_eq="warm_authority", emotion="lo_lang")
        elif "Lưu Biểu" in cleaned or "Biểu" in cleaned:
            add_line(chunk_id, "dialogue", "Liu_Biao", p, pitch="0Hz", rate="-8%", lead_in_pause="0.35s", timbre_eq="warm_authority", emotion="uy_nghi")
        elif "Hàn Tung" in cleaned or "Tung" in cleaned:
            add_line(chunk_id, "dialogue", "Han_Tong", p, pitch="0Hz", rate="-8%", lead_in_pause="0.35s", timbre_eq="warm_authority", emotion="trung_thuc")
        elif "Hoàng Tổ" in cleaned or "Tổ" in cleaned:
            add_line(chunk_id, "dialogue", "Huang_Zu", p, pitch="+1Hz", rate="-5%", lead_in_pause="0.35s", timbre_eq="chest_resonance", emotion="gian_du")
        else:
            add_line(chunk_id, "narrator", "Narrator", p, narrative_mode="contemplative", pitch="-2Hz", rate="-12%", lead_in_pause="0.30s", timbre_eq="contemplative_narrator", emotion="binh_than")

all_orig = ""
for chunk_id in range(1, 12):
    fpath = os.path.join(kich_ban_dir, f"Kich-ban-{chunk_id}.txt")
    with open(fpath, "r", encoding="utf-8") as fh:
        all_orig += fh.read()

reconstructed = "".join([e["text"] for e in theatrical_lines])
print(f"Original len: {len(all_orig)}, Reconstructed len: {len(reconstructed)}")
assert all_orig == reconstructed, "Zero loss invariant failed!"
print("ZERO-LOSS INVARIANT VERIFIED: 100% MATCH!")
print(f"Total theatrical lines: {len(theatrical_lines)}")
print(f"Total dialogue lines: {total_dialogues}")
print(f"Total poem lines: {total_poems}")
print(f"Total narrator lines: {total_narrators}")
print(f"Total characters cast: {len(speakers_set)}")

with open(script_path, "w", encoding="utf-8") as f:
    json.dump(theatrical_lines, f, ensure_ascii=False, indent=2)

character_bible = {
    "chapter_folder": "23-Hoi-23",
    "chapter_index": 23,
    "chapter_title": "HỒI HAI MƯƠI BA",
    "genre": "Historical Epic / Classical Literature",
    "total_theatrical_lines": len(theatrical_lines),
    "narrator_lines": total_narrators,
    "poem_lines": total_poems,
    "dialogue_lines": total_dialogues,
    "characters_cast_count": len(speakers_set),
    "characters": list(speakers_set),
    "directed_at": "vi-VN-NamMinhNeural",
    "timestamp": datetime.datetime.now().isoformat()
}
with open(bible_path, "w", encoding="utf-8") as f:
    json.dump(character_bible, f, ensure_ascii=False, indent=2)

manifest_data = {
    "chapter": "23-Hoi-23",
    "step_8a_status": "completed",
    "total_theatrical_lines": len(theatrical_lines),
    "total_poem_lines": total_poems,
    "total_dialogue_lines": total_dialogues,
    "total_narrator_lines": total_narrators,
    "total_characters_cast": len(speakers_set),
    "speakers": list(speakers_set),
    "timestamp": datetime.datetime.now().isoformat()
}
with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest_data, f, ensure_ascii=False, indent=2)

print("=== CHAPTER 23 BUILD & MANIFEST UPDATE COMPLETED SUCCESSFULLY ===")
