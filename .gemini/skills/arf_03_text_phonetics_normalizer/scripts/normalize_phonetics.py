#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
normalize_phonetics.py - Step 03: Text Phonetics Normalizer Engine
Skill: arf_03_text_phonetics_normalizer

Performs:
1. 100% num2words number normalization (zero raw digits allowed).
2. Spelled-out hyphenated acronyms for dual-voice TTS (P-M-I, W-B-S, K-P-I, C-E-O...).
3. Stripping forbidden TTS characters (markdown #, bullets, quotes, brackets, colons, em-dashes).
4. Preserving Latin/English professional terminology intact for en-US-BrianMultilingualNeural.
5. Updating .session_manifest.json to step_3_status = 'completed'.
"""

import os
import sys
import re
import json
import argparse
from datetime import datetime, timezone

# Number to Vietnamese words helper
UNITS = ["không", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]

def int_to_vietnamese_words(n: int) -> str:
    if n == 0:
        return "không"

    def convert_below_1000(num: int) -> str:
        if num < 10:
            return UNITS[num]
        elif num < 100:
            ten = num // 10
            unit = num % 10
            ten_str = "mười" if ten == 1 else UNITS[ten] + " mươi"
            if unit == 1 and ten > 1:
                unit_str = "mốt"
            elif unit == 5:
                unit_str = "lăm"
            elif unit == 0:
                unit_str = ""
            else:
                unit_str = UNITS[unit]
            return (ten_str + " " + unit_str).strip()
        else:
            hundred = num // 100
            rem = num % 100
            hundred_str = UNITS[hundred] + " trăm"
            if rem == 0:
                return hundred_str
            elif rem < 10:
                return hundred_str + " lẻ " + UNITS[rem]
            else:
                return hundred_str + " " + convert_below_1000(rem)

    parts = []
    if n >= 1000000000:
        billions = n // 1000000000
        n %= 1000000000
        parts.append(convert_below_1000(billions) + " tỷ")
    if n >= 1000000:
        millions = n // 1000000
        n %= 1000000
        parts.append(convert_below_1000(millions) + " triệu")
    if n >= 1000:
        thousands = n // 1000
        n %= 1000
        parts.append(convert_below_1000(thousands) + " nghìn")
    if n > 0:
        parts.append(convert_below_1000(n))

    return " ".join(parts).strip()

def normalize_numbers_vietnamese(text: str) -> str:
    """Converts all numbers in text to Vietnamese words with zero raw digits remaining."""

    # 1. Ratios and common abbreviations with slashes
    text = re.sub(r'\b24/7\b', 'hai mươi tư trên bảy', text, flags=re.IGNORECASE)
    text = re.sub(r'\bkm/h\b', 'ki-lô-mét trên giờ', text, flags=re.IGNORECASE)

    # 2. Fractions: e.g. 1/2, 1/3, 1/4, 2/3, 3/4, 4/5
    def replace_fraction(match):
        num = int(match.group(1))
        den = int(match.group(2))
        num_w = int_to_vietnamese_words(num)
        den_w = int_to_vietnamese_words(den)
        if den == 4:
            den_w = "tư"
        return f"{num_w} phần {den_w}"
    text = re.sub(r'\b(\d+)\s*/\s*(\d+)\b', replace_fraction, text)

    # 3. Ampersands & brand names
    text = re.sub(r'\bAT&T\b', 'A-T và T', text, flags=re.IGNORECASE)
    text = re.sub(r'\s*&\s*', ' và ', text)

    # 4. Currency patterns: e.g. $250.000, $100, $500K, 500$
    def replace_currency(match):
        val = match.group(1).replace('.', '').replace(',', '')
        try:
            return int_to_vietnamese_words(int(val)) + " đô la"
        except:
            return match.group(0)
    text = re.sub(r'\$\s*(\d+(?:[\.,]\d+)?)', replace_currency, text)
    text = re.sub(r'(\d+(?:[\.,]\d+)?)\s*\$', replace_currency, text)

    # 5. Percentage patterns: e.g. 50%, 95.5%, 100%
    def replace_percent(match):
        val = match.group(1)
        if '.' in val or ',' in val:
            p1, p2 = re.split(r'[\.,]', val)
            return f"{int_to_vietnamese_words(int(p1))} phẩy {int_to_vietnamese_words(int(p2))} phần trăm"
        return int_to_vietnamese_words(int(val)) + " phần trăm"
    text = re.sub(r'(\d+(?:[\.,]\d+)?)\s*%', replace_percent, text)

    # Specific common phrases first
    specific_replacements = [
        (r'\b100%\b', 'một trăm phần trăm'),
        (r'\b48%\b', 'bốn mươi tám phần trăm'),
        (r'\b43%\b', 'bốn mươi ba phần trăm'),
        (r'\b31%\b', 'ba mươi mốt phần trăm'),
        (r'\b95%\b', 'chín mươi lăm phần trăm'),
        (r'\b90%\b', 'chín mươi phần trăm'),
        (r'\b85%\b', 'tám mươi lăm phần trăm'),
        (r'\b50%\b', 'năm mươi phần trăm'),
        (r'\b25%\b', 'hai mươi lăm phần trăm'),
        (r'\b24%\b', 'hai mươi tư phần trăm'),
        (r'\b20%\b', 'hai mươi phần trăm'),
        (r'\b10%\b', 'mười phần trăm'),
        (r'\b87,7 triệu\b', 'tám mươi bảy phẩy bảy triệu'),
        (r'\b87\.7 triệu\b', 'tám mươi bảy phẩy bảy triệu'),
        (r'\b10\.000 đô la\b', 'mười nghìn đô la'),
        (r'\b10,000 đô la\b', 'mười nghìn đô la'),
        (r'\b5\.000 đô la\b', 'năm nghìn đô la'),
        (r'\b5,000 đô la\b', 'năm nghìn đô la'),
        (r'\b30 đô la\b', 'ba mươi đô la'),
        (r'\b500 chữ ký\b', 'năm trăm chữ ký'),
        (r'\b300 sinh viên\b', 'ba trăm sinh viên'),
        (r'\b20 bạn sinh viên\b', 'hai mươi bạn sinh viên'),
        (r'\b20 sinh viên\b', 'hai mươi sinh viên'),
        (r'\b29 tuổi\b', 'hai mươi chín tuổi'),
        (r'\b15 năm\b', 'mười lăm năm'),
        (r'\b15 phút\b', 'mười lăm phút'),
        (r'\b12 năm\b', 'mười hai năm'),
        (r'\b8 năm\b', 'tám năm'),
        (r'\b3 năm\b', 'ba năm'),
        (r'\b2 năm\b', 'hai năm'),
        (r'\b10 phút\b', 'mười phút'),
        (r'\b30 phút\b', 'ba mươi phút'),
        (r'\b9 giờ 30\b', 'chín giờ ba mươi phút'),
        (r'\b10 giờ\b', 'mười giờ'),
        (r'\b101\b', 'một trăm linh một'),
        (r'\bnăm 2008\b', 'năm hai nghìn không trăm linh tám'),
        (r'\bnăm 2017\b', 'năm hai nghìn không trăm mười bảy'),
        (r'\bnăm 2027\b', 'năm hai nghìn không trăm hai mươi bảy'),
        (r'\bnăm 2001\b', 'năm hai nghìn không trăm linh một'),
        (r'\bnhững năm 1970\b', 'thập niên một nghìn chín trăm bảy mươi'),
        (r'\bnhững năm 1990\b', 'thập niên một nghìn chín trăm chín mươi'),
        (r'\bHọc phần 1\b', 'Học phần một'),
        (r'\bHọc phần 2\b', 'Học phần hai'),
        (r'\bHọc phần 3\b', 'Học phần ba'),
        (r'\bHọc phần 4\b', 'Học phần bốn'),
        (r'\bKhóa học 3\b', 'Khóa học ba'),
        (r'\bChương 1\b', 'Chương một'),
        (r'\bChương 2\b', 'Chương hai'),
        (r'\bChương 3\b', 'Chương ba'),
        (r'\bChương 4\b', 'Chương bốn'),
        (r'\bChương 5\b', 'Chương năm'),
        (r'\bChương 6\b', 'Chương sáu'),
        (r'\bthứ 1\b', 'thứ nhất'),
        (r'\bthứ 2\b', 'thứ hai'),
        (r'\bthứ 3\b', 'thứ ba'),
        (r'\bthứ 4\b', 'thứ tư'),
        (r'\bthứ 5\b', 'thứ năm'),
    ]
    for pat, rep in specific_replacements:
        text = re.sub(pat, rep, text, flags=re.IGNORECASE)

    # Convert number ranges: e.g. 5-10
    def replace_range(match):
        v1 = int(match.group(1))
        v2 = int(match.group(2))
        return f"{int_to_vietnamese_words(v1)} đến {int_to_vietnamese_words(v2)}"
    text = re.sub(r'\b(\d+)\s*-\s*(\d+)\b', replace_range, text)

    # Convert ordered numbered list headers: "1. ", "2. ", "3. ", "4. ", "5. "
    def replace_order_num(match):
        num = match.group(1)
        mapping = {
            "1": "Thứ nhất", "2": "Thứ hai", "3": "Thứ ba", "4": "Thứ tư",
            "5": "Thứ năm", "6": "Thứ sáu", "7": "Thứ bảy", "8": "Thứ tám"
        }
        return mapping.get(num, f"Thứ {num}") + ", "
    text = re.sub(r'(?m)^(\d+)\.\s+', replace_order_num, text)

    # Convert percentage patterns: e.g. (\d+)%
    def replace_percent(match):
        val = int(match.group(1))
        return int_to_vietnamese_words(val) + " phần trăm"
    text = re.sub(r'(\d+)%', replace_percent, text)

    # Convert decimal patterns: e.g. (\d+)[,\.](\d+)
    def replace_decimal(match):
        int_part = int(match.group(1))
        dec_part = int(match.group(2))
        return f"{int_to_vietnamese_words(int_part)} phẩy {int_to_vietnamese_words(dec_part)}"
    text = re.sub(r'(\d+)[,\.](\d+)', replace_decimal, text)

    # Convert thousand dots: e.g. 250.000, 1.000
    def replace_thousands(match):
        val = int(match.group(0).replace('.', ''))
        return int_to_vietnamese_words(val)
    text = re.sub(r'\b\d{1,3}(?:\.\d{3})+\b', replace_thousands, text)

    # Convert remaining integers
    def replace_int(match):
        val = int(match.group(0))
        return int_to_vietnamese_words(val)
    text = re.sub(r'\b\d+\b', replace_int, text)

    return text

def normalize_acronyms(text: str) -> str:
    """Spells out broadcast acronyms with hyphens for crisp pronunciation."""
    acronyms = [
        (r'\bRACI\b', 'R-A-C-I'),
        (r'\bSMART\b', 'S-M-A-R-T'),
        (r'\bOKRs\b', 'O-K-R'),
        (r'\bOKR\b', 'O-K-R'),
        (r'\bKRs\b', 'K-R'),
        (r'\bKR\b', 'K-R'),
        (r'\bROI\b', 'R-O-I'),
        (r'\bTPM\b', 'T-P-M'),
        (r'\bEPM\b', 'E-P-M'),
        (r'\bALM\b', 'A-L-M'),
        (r'\bJIRA\b', 'J-I-R-A'),
        (r'\bPMI\b', 'P-M-I'),
        (r'\bPMBOK\b', 'P-M-B-O-K'),
        (r'\bWBS\b', 'W-B-S'),
        (r'\bKPI\b', 'K-P-I'),
        (r'\bPMO\b', 'P-M-O'),
        (r'\bPMB\b', 'P-M-B'),
        (r'\bCEO\b', 'C-E-O'),
        (r'\bCFO\b', 'C-F-O'),
        (r'\bCOO\b', 'C-O-O'),
        (r'\bCTO\b', 'C-T-O'),
        (r'\bVPs\b', 'V-P'),
        (r'\bVP\b', 'V-P'),
        (r'\bSRE\b', 'S-R-E'),
        (r'\bUX\b', 'U-X'),
        (r'\bQA\b', 'Q-A'),
        (r'\bPII\b', 'P-I-I'),
        (r'\bSOW\b', 'S-O-W'),
        (r'\bSoW\b', 'S-O-W'),
        (r'\bRFP\b', 'R-F-P'),
        (r'\bNDA\b', 'N-D-A'),
        (r'\bEVM\b', 'E-V-M'),
        (r'\bCPI\b', 'C-P-I'),
        (r'\bCV\b', 'C-V'),
        (r'\bSPI\b', 'S-P-I'),
        (r'\bSV\b', 'S-V'),
        (r'\bTCO\b', 'T-C-O'),
        (r'\bSME\b', 'S-M-E'),
        (r'\bCAPEX\b', 'C-A-P-E-X'),
        (r'\bOPEX\b', 'O-P-E-X'),
        (r'\bFF\b', 'F-F'),
        (r'\bFS\b', 'F-S'),
        (r'\bSS\b', 'S-S'),
        (r'\bSF\b', 'S-F'),
        (r'\bGED\b', 'G-E-D'),
        (r'\bEMT\b', 'E-M-T'),
        (r'\bPMP\b', 'P-M-P'),
        (r'\bCAPM\b', 'C-A-P-M'),
        (r'\bDMAIC\b', 'D-M-A-I-C'),
        (r'\bAI\b', 'A-I'),
        (r'\bGen AI\b', 'Gen A-I'),
        (r'\bT-C-R-E-I\b', 'T-C-R-E-I'),
        (r'\bSLA\b', 'S-L-A'),
        (r'\bSWOT\b', 'S-W-O-T'),
    ]
    for pat, rep in acronyms:
        text = re.sub(pat, rep, text)
    return text

def clean_tts_forbidden_characters(text: str) -> str:
    """Removes all TTS forbidden characters, formats section headings with pauses, and cleans punctuation."""
    # Step 1: Pre-normalize numbers, currency, percentage, fractions, and acronyms FIRST before stripping symbols
    text = normalize_numbers_vietnamese(text)
    text = normalize_acronyms(text)

    lines = text.split('\n')
    processed_lines = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            processed_lines.append("")
            continue

        # Convert markdown headers: #, ##, ###
        if stripped.startswith('#'):
            # Remove leading #
            header_text = re.sub(r'^#+\s*', '', stripped)
            # Remove asterisks and bolding
            header_text = header_text.replace('**', '').replace('*', '')
            # Replace colons in headers
            header_text = header_text.replace(':', ', ')
            # Remove brackets/parentheses in headers to keep clean spoken text
            header_text = header_text.replace('(', ', ').replace(')', '')
            header_text = re.sub(r'\s+,', ',', header_text)
            header_text = re.sub(r'\s+', ' ', header_text).strip()
            header_text = re.sub(r'[,:\s]+$', '', header_text)
            # Standalone spoken heading followed by breathing pause . ......
            processed_lines.append(f"\n{header_text.upper()}\n. ......")
            continue

        # Strip list bullets: -, *, •, ●, ▪, etc.
        line_clean = re.sub(r'^\s*[-*•●▪▶►★▲◆■✓]\s*', '', line)

        # Remove markdown bold/italic
        line_clean = line_clean.replace('**', '').replace('*', '')

        # Remove double quotes and single quotes around words
        line_clean = line_clean.replace('"', '').replace('“', '').replace('”', '').replace('«', '').replace('»', '')

        # Replace parentheses and brackets with comma pause
        line_clean = line_clean.replace('(', ', ').replace(')', ', ')
        line_clean = line_clean.replace('[', ', ').replace(']', ', ')

        # Replace colons and semicolons with commas or periods
        line_clean = line_clean.replace(':', ', ').replace(';', ', ')

        # Replace dashes (em-dash, en-dash) with commas
        line_clean = line_clean.replace('—', ', ').replace('–', ', ')

        # Remove forbidden symbols: @, #, $, %, ^, &, _, ~, |, \, /
        line_clean = re.sub(r'[@#$^&_~|\\/]', ' ', line_clean)

        processed_lines.append(line_clean)

    text_clean = '\n'.join(processed_lines)

    # Secondary sweep for any remaining raw digits uncovered
    text_clean = normalize_numbers_vietnamese(text_clean)
    text_clean = normalize_acronyms(text_clean)

    # Clean double commas and spaces
    text_clean = re.sub(r',\s*,+', ',', text_clean)
    text_clean = re.sub(r'[ \t]+,', ',', text_clean)
    text_clean = re.sub(r',\s*\.', '.', text_clean)
    text_clean = re.sub(r'\.\s*,', '.', text_clean)
    text_clean = re.sub(r'\.{2,}', '......', text_clean)  # preserve audio pauses
    text_clean = re.sub(r'[ \t]+', ' ', text_clean)

    # Insert breathing commas after key transitional conjunctions if missing
    transitions = [
        "Tuy nhiên", "Bởi vì", "Do đó", "Ngoài ra", "Hơn nữa", "Đồng thời",
        "Tóm lại", "Nói cách khác", "Nhìn chung", "Mặt khác", "Vì vậy", "Chính vì thế"
    ]
    for t in transitions:
        text_clean = re.sub(r'\b(' + t + r')\s+(?![\,\.\:\;\!\?])', r'\1, ', text_clean, flags=re.IGNORECASE)

    # Final cleanup of double spaces/commas
    text_clean = re.sub(r',\s*,', ',', text_clean)
    text_clean = re.sub(r'[ \t]+,', ',', text_clean)

    return text_clean.strip()

def process_chapter_normalization(chap_dir: str) -> bool:
    trans_file = os.path.join(chap_dir, "translated.txt")
    norm_file = os.path.join(chap_dir, "normalized.txt")

    if not os.path.exists(trans_file):
        print(f"[!] File not found: {trans_file}")
        return False

    with open(trans_file, "r", encoding="utf-8") as f:
        translated_text = f.read()

    normalized_text = clean_tts_forbidden_characters(translated_text)

    # Quality Gate 2 verification: check for remaining raw digits
    digits_found = re.findall(r'\d+', normalized_text)
    if digits_found:
        print(f"[!] Warning: Raw digits still found in {chap_dir}: {set(digits_found)}")
        # Secondary sweep
        normalized_text = normalize_numbers_vietnamese(normalized_text)
        remaining = re.findall(r'\d+', normalized_text)
        if remaining:
            print(f"[!] CRITICAL: Could not eliminate digits: {set(remaining)}")
            return False

    with open(norm_file, "w", encoding="utf-8") as f:
        f.write(normalized_text)

    word_count = len(normalized_text.split())
    char_count = len(normalized_text)
    print(f"[✓] {os.path.basename(chap_dir)}: normalized.txt written ({word_count:,} words, {char_count:,} chars) [Zero raw digits]")
    return True

def normalize_all_chapters(book_dir: str):
    manifest_path = os.path.join(book_dir, ".session_manifest.json")
    if not os.path.exists(manifest_path):
        print(f"[!] Error: .session_manifest.json not found in {book_dir}")
        return False

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    all_completed = True
    for chap in manifest.get("chapters", []):
        chap_dir = os.path.join(book_dir, chap.get("folder", ""))
        ok = process_chapter_normalization(chap_dir)
        if ok:
            norm_file = os.path.join(chap_dir, "normalized.txt")
            with open(norm_file, "r", encoding="utf-8") as nf:
                content = nf.read()
            chap["step_3_status"] = "completed"
            chap["status"] = "phonetics_normalized"
            chap["normalized_file"] = f"{chap.get('folder')}/normalized.txt"
            chap["normalized_word_count"] = len(content.split())
            chap["normalized_char_count"] = len(content)
        else:
            chap["step_3_status"] = "error"
            all_completed = False

    if all_completed:
        manifest["pipeline_stage"] = "03_phonetics_normalized"
        manifest["step_3_status"] = "completed"
        manifest["step_3_completed_at"] = datetime.now(timezone.utc).isoformat()
        print(f"\n[★] All {len(manifest.get('chapters', []))} chapters successfully normalized for TTS!")

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    return all_completed

def main():
    parser = argparse.ArgumentParser(description="Text Phonetics Normalizer Runner (Step 03)")
    parser.add_argument("--input_dir", required=True, help="Path to book directory containing .session_manifest.json")
    parser.add_argument("--chapter", help="Specific chapter folder name (optional)")
    args = parser.parse_args()

    input_dir = os.path.abspath(args.input_dir)
    print(f"=== Step 03: Text Phonetics Normalizer ===")
    print(f"Directory: {input_dir}")
    if args.chapter:
        chap_dir = os.path.join(input_dir, args.chapter)
        process_chapter_normalization(chap_dir)
    else:
        normalize_all_chapters(input_dir)

if __name__ == "__main__":
    main()
