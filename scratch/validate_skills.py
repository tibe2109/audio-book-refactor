#!/usr/bin/env python3
import os
import re
import sys
import yaml

SKILLS = [
    "arf_01_pdf_structure_extractor",
    "arf_02_author_style_translator",
    "arf_03_text_phonetics_normalizer",
    "arf_04_smart_audiobook_rechunker",
    "arf_05_script_structure_formatter",
    "arf_06_llm_script_refiner",
    "arf_07_audiobook_qc_auditor",
    "arf_08a_theatrical_voice_director",
    "arf_08_tts_neural_bgm_mixer",
    "arf_09_audio_smart_aggregator",
    "arf_10_bgm_dynamic_mixer",
    "Make-audio-script-process",
    "Make-audio-bgm-process",
    "universal-audiobook",
    "abv_01_thematic_visual_prompter",
    "abv_02_audiobook_video_compiler"
]

REQUIRED_SECTIONS = [
    ("SOP / Đặc tả", re.compile(r"(đặc tả|sop|quy trình thao tác chuẩn)", re.I)),
    ("Trigger / Khi nào dùng", re.compile(r"(trigger|khi nào dùng|điều kiện kích hoạt)", re.I)),
    ("Trình tự từng bước", re.compile(r"(trình tự từng bước|step-by-step|các bước thực thi)", re.I)),
    ("Output Contract", re.compile(r"(output contract|ràng buộc đầu ra|chuẩn đầu ra)", re.I)),
    ("Negative Trigger", re.compile(r"(negative trigger|cơ chế phủ định|không được làm|chống chỉ định)", re.I)),
]

def validate_skill(filepath):
    if not os.path.exists(filepath):
        return False, ["File not found"]
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()
    line_count = len(lines)
    errors = []

    if line_count >= 500:
        errors.append(f"Line count too high: {line_count} >= 500")

    if not content.startswith("---"):
        errors.append("Missing YAML frontmatter")
    else:
        parts = content.split("---", 2)
        if len(parts) < 3:
            errors.append("Malformed YAML frontmatter")
        else:
            try:
                meta = yaml.safe_load(parts[1])
                desc = meta.get("description", "")
                desc_len = len(desc.strip())
                if desc_len < 1024 or desc_len > 1536:
                    errors.append(f"Description length out of bounds: {desc_len} (must be 1024-1536)")
            except Exception as e:
                errors.append(f"YAML parse error: {e}")

    for sec_name, pattern in REQUIRED_SECTIONS:
        if not pattern.search(content):
            errors.append(f"Missing required section: {sec_name}")

    return len(errors) == 0, errors, line_count, desc_len if "desc_len" in locals() else 0

def main():
    base_dir = ".agent/skills"
    all_ok = True
    print("=" * 80)
    print(f"{'SKILL NAME':<35} | {'LINES':<6} | {'DESC LEN':<8} | {'STATUS'}")
    print("=" * 80)

    for skill in SKILLS:
        fp = os.path.join(base_dir, skill, "SKILL.md")
        ok, errs, lines, dlen = validate_skill(fp)
        status = "PASSED" if ok else f"FAILED: {'; '.join(errs)}"
        if not ok:
            all_ok = False
        print(f"{skill:<35} | {lines:<6} | {dlen:<8} | {status}")

    print("=" * 80)
    sys.exit(0 if all_ok else 1)

if __name__ == "__main__":
    main()
