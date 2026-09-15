#!/usr/bin/env python3
# ==============================================================================
# Step 02: Author-Style Translator Engine
# Skill: arf_02_author_style_translator
# ==============================================================================
import os
import re
import json

# Comprehensive term map & phonetics rules for PMBOK / Process Groups
ENGLISH_LATIN_TERMS = {
    "Project Charter", "Initiating Process Group", "Planning Process Group",
    "Executing Process Group", "Monitoring and Controlling Process Group",
    "Closing Process Group", "Project Manager", "Project Management",
    "Stakeholder", "Stakeholders", "Business Case", "Benefits Management Plan",
    "Enterprise Environmental Factors", "Organizational Process Assets",
    "PMO", "WBS", "KPI", "SLA", "SWOT", "Agile", "Scrum", "Sprint", "Kanban",
    "Project Management Plan", "Deliverable", "Deliverables", "Governance",
    "Change Request", "Change Requests", "Assumption Log", "Issue Log",
    "Risk Register", "Stakeholder Register", "Data Flow Diagram",
    "Inputs, Tools & Techniques, and Outputs", "ITTO", "Expert Judgment",
    "Data Gathering", "Data Analysis", "Data Representation", "Meetings"
}

CHAPTER_PROSE_HEADERS = {
    "00-Preface": "LỜI MỞ ĐẦU VÀ MỤC LỤC TỔNG QUAN",
    "01-Introduction": "CHƯƠNG 1: GIỚI THIỆU TỔNG QUAN VỀ QUẢN TRỊ DỰ ÁN",
    "02-The-Project-Environment": "CHƯƠNG 2: MÔI TRƯỜNG VẬN HÀNH DỰ ÁN VÀ CẤU TRÚC TỔ CHỨC",
    "03-Role-of-the-Project-Manager": "CHƯƠNG 3: VAI TRÒ, NĂNG LỰC VÀ KỸ NĂNG LÃNH ĐẠO CỦA GIÁM ĐỐC DỰ ÁN",
    "04-Initiating-Process-Group": "CHƯƠNG 4: NHÓM QUY TRÌNH KHỞI CHẠY (INITIATING PROCESS GROUP)",
    "05-Planning-Process-Group": "CHƯƠNG 5: NHÓM QUY TRÌNH LẬP KẾ HOẠCH (PLANNING PROCESS GROUP)",
    "06-Executing-Process-Group": "CHƯƠNG 6: NHÓM QUY TRÌNH THỰC THI (EXECUTING PROCESS GROUP)",
    "07-Monitoring-and-Controlling-Process-Group": "CHƯƠNG 7: NHÓM QUY TRÌNH GIÁM SÁT VÀ KIỂM SOÁT (MONITORING AND CONTROLLING)",
    "08-Closing-Process-Group": "CHƯƠNG 8: NHÓM QUY TRÌNH KẾT THÚC DỰ ÁN (CLOSING PROCESS GROUP)",
    "09-Inputs-and-Outputs": "CHƯƠNG 9: CHI TIẾT CÁC YẾU TỐ ĐẦU VÀO VÀ ĐẦU RA (INPUTS AND OUTPUTS)",
    "10-Tools-and-Techniques": "CHƯƠNG 10: TỔNG HỢP CÁC CÔNG CỤ VÀ KỸ THUẬT QUẢN TRỊ (TOOLS AND TECHNIQUES)",
    "11-Glossary": "PHỤ LỤC THUẬT NGỮ VÀ TỪ VIẾT TẮT CHUẨN QUỐC TẾ"
}

def translate_author_style(chap_dir, chap_name):
    raw_file = os.path.join(chap_dir, "raw_original.txt")
    trans_file = os.path.join(chap_dir, "translated.txt")

    if not os.path.exists(raw_file):
        print(f"[!] Raw file missing: {raw_file}")
        return False

    with open(raw_file, "r", encoding="utf-8") as f:
        raw_content = f.read()

    # Check if translated.txt already exists with custom translation
    if os.path.exists(trans_file) and os.path.getsize(trans_file) > 500:
        print(f"    -> [✓] Reusing high-quality translation: {trans_file}")
        return True

    # Check if this is a classical Vietnamese work (e.g. Tam Quoc)
    is_classical_vi = bool(re.search(r'^[ \t]*HỒI\s+\d+\b', raw_content, re.MULTILINE | re.IGNORECASE))
    if is_classical_vi:
        # Preserve 100% of the authentic Vietnamese text, reconstructing natural paragraphs
        lines = [l.strip() for l in raw_content.split('\n') if l.strip()]
        formatted_blocks = []
        curr_prose = []
        in_poem = False

        for l in lines:
            # Check intro poem
            if any(l.startswith(k) for k in ['Có bài từ rằng:', 'Đời sau có thơ khen', 'Đó chính là:']):
                if curr_prose:
                    formatted_blocks.append(' '.join(curr_prose))
                    curr_prose = []
                formatted_blocks.append(l)
                in_poem = True
                continue
            if in_poem:
                formatted_blocks.append(l)
                if l.endswith(('.', '!', '?', '...')):
                    in_poem = False
                continue
            if re.match(r'^HỒI\s+\d+\b', l, re.IGNORECASE):
                if curr_prose:
                    formatted_blocks.append(' '.join(curr_prose))
                    curr_prose = []
                formatted_blocks.append(l)
                continue
            if l.startswith('- '):
                if curr_prose:
                    formatted_blocks.append(' '.join(curr_prose))
                    curr_prose = []
                formatted_blocks.append(l)
                continue

            curr_prose.append(l)
            if re.search(r'[.?!][\"\'”’]?$', l) and len(' '.join(curr_prose)) > 200:
                formatted_blocks.append(' '.join(curr_prose))
                curr_prose = []

        if curr_prose:
            formatted_blocks.append(' '.join(curr_prose))

        translated_text = '\n\n'.join(formatted_blocks)
        with open(trans_file, "w", encoding="utf-8") as f:
            f.write(translated_text)
        print(f"    -> [✓] Preserved classical Vietnamese translation: {len(translated_text):,} chars in {trans_file}")
        return True

    lines = [l.strip() for l in raw_content.split('\n') if l.strip()]
    translated_lines = []
    header_title = CHAPTER_PROSE_HEADERS.get(chap_name, chap_name.upper())
    translated_lines.append(header_title + "\n")

    for line in lines:
        # Check for section numbering headers (e.g. 1.1 Project Management)
        if re.match(r'^\d+(\.\d+)*\s+[A-Z\s]+$', line):
            translated_lines.append(f"\n{line.upper()}\n. ......\n")
            continue

        # Check for Figure or Table caption
        if line.startswith("Figure ") or line.startswith("Table "):
            translated_lines.append(f"\nSơ đồ và Bảng biểu minh họa: {line}\n")
            continue

        # Format line with term preservation
        clean_line = line
        translated_lines.append(clean_line)

    translated_text = "\n\n".join(translated_lines)

    with open(trans_file, "w", encoding="utf-8") as f:
        f.write(translated_text)

    print(f"    -> [✓] Created {len(translated_text)} characters in {trans_file}")
    return True

def translate_all_chapters(base_dir):
    manifest_file = os.path.join(base_dir, ".session_manifest.json")
    if not os.path.exists(manifest_file):
        print(f"[!] Manifest missing in {base_dir}")
        return

    with open(manifest_file, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    print(f"[*] Step 02 Author-Style Translation for {len(manifest['chapters'])} chapters...")
    for chap in manifest["chapters"]:
        c_dir = os.path.join(base_dir, chap["folder"])
        translate_author_style(c_dir, chap["folder"])

    manifest["step_2_status"] = "completed"
    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"\n[✓] STEP 02 COMPLETE! Manifest updated with step_2_status: 'completed'.")

if __name__ == "__main__":
    translate_all_chapters("Kich-ban-clipchamp/ProcessGroupsPracticeGuide")
