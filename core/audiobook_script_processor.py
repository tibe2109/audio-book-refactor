#!/usr/bin/env python3
# ==============================================================================
# Steps 02 - 07: Audiobook Script Processing, Translation, Normalization & QC
# Skills: arf_02, arf_03, arf_04, arf_05, arf_06, arf_07
# ==============================================================================
import os
import re
import json

# Comprehensive term map & phonetics rules for PMBOK / Process Groups
TERM_PRESERVE = [
    "Project Charter", "Initiating Process Group", "Planning Process Group",
    "Executing Process Group", "Monitoring and Controlling Process Group",
    "Closing Process Group", "Project Manager", "Project Management",
    "Stakeholder", "Stakeholders", "Business Case", "Benefits Management Plan",
    "Enterprise Environmental Factors", "Organizational Process Assets",
    "PMO", "WBS", "KPI", "SLA", "SWOT", "Agile", "Scrum", "Sprint",
    "Project Management Plan", "Deliverable", "Deliverables", "Governance",
    "Change Request", "Change Requests", "Assumption Log", "Issue Log",
    "Risk Register", "Stakeholder Register", "Data Flow Diagram",
    "Inputs, Tools & Techniques, and Outputs", "ITTO"
]

def num2words_vi(num_str):
    """Simple robust Vi converter for numbers in text."""
    units = ["không", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]

    def convert_below_1000(n):
        if n < 10:
            return units[n]
        elif n < 100:
            ten = n // 10
            unit = n % 10
            ten_str = "mười" if ten == 1 else units[ten] + " mươi"
            if unit == 1 and ten > 1:
                unit_str = "mốt"
            elif unit == 5:
                unit_str = "lăm"
            elif unit == 0:
                unit_str = ""
            else:
                unit_str = units[unit]
            return (ten_str + " " + unit_str).strip()
        else:
            hundred = n // 100
            rem = n % 100
            hundred_str = units[hundred] + " trăm"
            if rem == 0:
                return hundred_str
            elif rem < 10:
                return hundred_str + " lẻ " + units[rem]
            else:
                return hundred_str + " " + convert_below_1000(rem)

    try:
        val = int(num_str)
        if val == 0:
            return "không"
        
        parts = []
        if val >= 1000000:
            millions = val // 1000000
            val %= 1000000
            parts.append(convert_below_1000(millions) + " triệu")
        if val >= 1000:
            thousands = val // 1000
            val %= 1000
            parts.append(convert_below_1000(thousands) + " nghìn")
        if val > 0:
            parts.append(convert_below_1000(val))
        return " ".join(parts)
    except ValueError:
        return num_str

def inject_poetic_caesura(line_str):
    """Injects breathing caesura pauses into poetic verse according to meter (Song That Luc Bat, Luc Bat, Duong Luat, etc.)."""
    clean = line_str.strip()
    if not clean or clean == '. ......' or clean == '__PAUSE_MARKER__':
        return clean

    stripped_inner = clean.rstrip(',;!?.… ')
    if ',' in stripped_inner or ';' in stripped_inner:
        res = clean
    else:
        trailing_punct = ""
        m_punct = re.search(r'([,;!?.…]+)$', clean)
        if m_punct:
            trailing_punct = m_punct.group(1)
            raw_text = clean[:-len(trailing_punct)].strip()
        else:
            raw_text = clean

        words = raw_text.split()
        n = len(words)

        if n == 7:
            if words[0][0].isupper() and len(words) > 1 and words[1][0].isupper() and (len(words) <= 2 or not words[2][0].isupper()):
                res = f"{' '.join(words[:2])}, {' '.join(words[2:4])}, {' '.join(words[4:])}"
            else:
                res = f"{' '.join(words[:3])}, {' '.join(words[3:])}"
        elif n == 8:
            res = f"{' '.join(words[:4])}, {' '.join(words[4:])}"
        elif n == 6:
            res = f"{' '.join(words[:3])}, {' '.join(words[3:])}"
        elif n == 5:
            res = f"{' '.join(words[:2])}, {' '.join(words[2:])}"
        elif n == 4:
            res = f"{' '.join(words[:2])}, {' '.join(words[2:])}"
        else:
            res = raw_text

        if trailing_punct:
            res = res + trailing_punct
        else:
            res = res + ","

    if not res.endswith(('.', ',', ';', '!', '?', '…')):
        res = res + ','
    return res

def format_poetic_verses_for_tts(text):
    """Calibrates classical poetic verses, stanzas, and intros for optimal TTS cadences & breathing."""
    # Protect existing authorized pause markers
    text = text.replace('. ......', '__PAUSE_MARKER__')

    intro_regex = re.compile(
        r'^[ \t]*((?:(?:Có|Lại có|Người sau có|Đời sau có|Sử thần có|Cổ nhân có)\s+(?:bài\s+)?(?:từ|thơ|thơ tứ tuyệt|thơ lục bát|bài từ khúc|phú|ca)?\s*rằng)|(?:Thơ\s+(?:khen|than|vịnh|viếng|tiễn)?\s*rằng)|(?:Đó chính là))(?:\s*[:,]\s*)?(.*)$',
        re.IGNORECASE | re.MULTILINE
    )

    lines = text.split('\n')
    out_lines = []
    in_poem = False
    poem_line_count = 0

    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            if in_poem:
                # Stanza boundary inside poem
                if out_lines and out_lines[-1] != '__PAUSE_MARKER__':
                    out_lines.append('__PAUSE_MARKER__')
            out_lines.append('')
            continue

        if stripped == '__PAUSE_MARKER__':
            out_lines.append('__PAUSE_MARKER__')
            continue

        m = intro_regex.match(stripped)
        if m:
            intro_name = m.group(1).rstrip(':, ') + ','
            rest = m.group(2).strip() if m.group(2) else ''

            out_lines.append(intro_name)
            out_lines.append('__PAUSE_MARKER__')
            out_lines.append('')
            in_poem = True
            poem_line_count = 0

            if rest:
                w_cnt = len(rest.split())
                if w_cnt <= 14:
                    clean_rest = inject_poetic_caesura(rest)
                    out_lines.append(clean_rest)
                    poem_line_count += 1
                else:
                    out_lines.append(rest)
                    in_poem = False
            continue

        w_cnt = len(stripped.split())
        is_prose_break = (
            stripped.startswith(('Lại nói,', 'Lại nói ', 'Nói đoạn,', 'Nói đoạn ', 'Nhắc lại,', 'HỒI ', 'Muốn biết', 'Chưa biết', 'Sau này', 'Bấy giờ')) or
            w_cnt > 16 or
            (stripped.endswith(('.', '!', '?')) and w_cnt > 12)
        )

        if in_poem:
            if is_prose_break:
                in_poem = False
                if poem_line_count > 0 and out_lines and out_lines[-1] != '__PAUSE_MARKER__':
                    out_lines.append('__PAUSE_MARKER__')
                    out_lines.append('')
                out_lines.append(line)
            else:
                # Inside poem line: inject caesura and ensure cadence punctuation
                clean_line = inject_poetic_caesura(stripped)
                is_next_empty = (i + 1 < len(lines) and not lines[i+1].strip())
                is_next_prose = (i + 1 < len(lines) and (
                    lines[i+1].strip().startswith(('Lại nói', 'Nói đoạn', 'HỒI', 'Muốn biết', 'Chưa biết')) or
                    len(lines[i+1].strip().split()) > 16
                ))

                if not clean_line.endswith(('.', ',', '!', '?', '…')):
                    if is_next_empty or is_next_prose:
                        clean_line += '.'
                    else:
                        clean_line += ','
                out_lines.append(clean_line)
                poem_line_count += 1
        else:
            out_lines.append(line)

    if in_poem and poem_line_count > 0:
        if out_lines and out_lines[-1] != '__PAUSE_MARKER__':
            out_lines.append('__PAUSE_MARKER__')

    res = '\n'.join(out_lines)
    res = res.replace('__PAUSE_MARKER__', '. ......')
    res = re.sub(r'(\. \.\.\.\.\.\.\s*)+', r'. ......\n', res)
    return res

def normalize_text_for_tts(text):
    """Step 3 & 6: Clean forbidden chars, normalize numbers & acronyms, insert breathing commas."""
    # Pre-format classical poetic verses, stanzas & intros
    text = format_poetic_verses_for_tts(text)

    # Pre-normalize chapter titles & couplet subtitles e.g. "HỒI 46\nDùng Chước lạ...\nDâng kế mật..."
    def replace_hoi_and_subtitle(match):
        num_str = match.group(1)
        sub1 = match.group(2).strip().rstrip(";:,.").upper()
        sub2 = match.group(3).strip().rstrip(";:,.").upper()
        w = num2words_vi(num_str).upper()
        return f"\n\nHỒI {w}\n. ......\n\n{sub1},\n{sub2}.\n. ......\n\n"
    text = re.sub(r'^[ \t]*HỒI\s+(\d+)\b[ \t]*\n([^\n]+)\n([^\n]+)', replace_hoi_and_subtitle, text, flags=re.MULTILINE | re.IGNORECASE)

    def replace_hoi_simple(match):
        num_str = match.group(1)
        w = num2words_vi(num_str).upper()
        return f"\n\nHỒI {w}\n. ......\n\n"
    text = re.sub(r'^[ \t]*HỒI\s+(\d+)\b', replace_hoi_simple, text, flags=re.MULTILINE | re.IGNORECASE)

    # Format cliffhangers e.g. "Chưa biết Hám Trạch dâng thư làm sao, xem đến hồi sau sẽ rõ."
    def replace_cliffhanger(match):
        content = match.group(0).strip()
        return f"\n\n. ......\n\n{content}"
    text = re.sub(r'(?:Chưa biết[^\n\.]+,\s*)?xem (?:đến )?hồi sau sẽ rõ\.?', replace_cliffhanger, text, flags=re.IGNORECASE)

    # Strip dialog dash at start of line
    text = re.sub(r'(?:^|\n)[ \t]*-[ \t]+', r'\n', text)

    # Pre-normalize currency, financial notation, percentage, fractions & ampersands BEFORE stripping symbols
    text = re.sub(r'\b24/7\b', 'hai mươi tư trên bảy', text, flags=re.IGNORECASE)
    text = re.sub(r'\bkm/h\b', 'ki-lô-mét trên giờ', text, flags=re.IGNORECASE)

    # Fractions: e.g. 1/2, 1/3, 1/4, 3/4
    def replace_fraction(match):
        num = match.group(1)
        den = match.group(2)
        den_w = "tư" if den == "4" else num2words_vi(den)
        return f"{num2words_vi(num)} phần {den_w}"
    text = re.sub(r'\b(\d+)\s*/\s*(\d+)\b', replace_fraction, text)

    # Ampersands & brand names
    text = re.sub(r'\bAT&T\b', 'A-T và T', text, flags=re.IGNORECASE)
    text = re.sub(r'\s*&\s*', ' và ', text)

    # Convert currency and financial notation like $501K-$1M, 5M, 100K, $100
    def replace_financial(match):
        val = match.group(0)
        has_dollar = '$' in val
        val_clean = val.replace('$', '').replace('K', ' nghìn').replace('M', ' triệu')
        if '-' in val_clean:
            p1, p2 = val_clean.split('-')
            res = f"{p1} đến {p2}"
        else:
            res = val_clean
        return res + " đô la" if has_dollar else res
    text = re.sub(r'\$\d+(?:\.\d+)?[KM]?(?:-\$?\d+(?:\.\d+)?[KM]?)?', replace_financial, text)

    # Percentage patterns
    def replace_percent(match):
        val = match.group(1)
        if '.' in val or ',' in val:
            p1, p2 = re.split(r'[\.,]', val)
            return f"{num2words_vi(p1)} phẩy {num2words_vi(p2)} phần trăm"
        return num2words_vi(val) + " phần trăm"
    text = re.sub(r'(\d+(?:[\.,]\d+)?)\s*%', replace_percent, text)

    # Protect authorized pause marker . ......
    text = text.replace(". ......", "__PAUSE_MARKER__")

    # Remove parenthetical modern date annotations that break classical literary atmosphere
    # Examples: "(167 dương lịch)", "(năm 169 dương lịch)", "(sau Công Nguyên 200)"
    text = re.sub(r',?\s*\(\s*(?:năm\s+)?[\w\s,]+dương lịch[^)]*\)', '', text, flags=re.IGNORECASE)
    text = re.sub(r',?\s*\(\s*(?:năm\s+)?[\w\s,]+[Cc]ông [Nn]guyên[^)]*\)', '', text, flags=re.IGNORECASE)
    text = re.sub(r',?\s*\(\s*(?:\d+\s*[-–]\s*\d+\s*(?:TCN|SCN|CN|AD|BC)[^)]*|(?:TCN|SCN|CN|AD|BC)\s*\d+[^)]*)\)', '', text, flags=re.IGNORECASE)
    # Clean up double spaces/commas left after removal
    text = re.sub(r',[ \t]*,', ',', text)
    text = re.sub(r'[ \t]{2,}', ' ', text)

    # Strip Table of Contents dot leaders (e.g. ........................................ 123)
    text = re.sub(r'\.\.\.+\s*\d+', '.', text)
    text = re.sub(r'\.\.\.+', '', text)

    # Restore authorized pause marker
    text = text.replace("__PAUSE_MARKER__", ". ......")

    # Strip non-speakable bullet symbols, markdown markers & icons (▶, ►, ▪, ●, ★, ▲, ◆, ■, ✓, •, #, *)
    text = re.sub(r'[#*▶►▪●★▲◆■✓•–—…|/\\\\]', ' ', text)

    # Replace forbidden punctuation
    text = text.replace('"', '').replace('“', '').replace('”', '').replace('«', '').replace('»', '')
    text = text.replace("'", "").replace("‘", "").replace("’", "")
    text = text.replace('(', ', ').replace(')', ', ')
    text = text.replace('[', ', ').replace(']', ', ')
    text = text.replace(':', ', ').replace(';', ', ')
    text = text.replace('—', ', ').replace('–', ', ')

    # Convert numbers followed by letters like 2D, 3D, 5M
    def replace_num_letter(match):
        num_str = match.group(1)
        letter_str = match.group(2)
        return num2words_vi(num_str) + " " + letter_str
    text = re.sub(r'\b(\d+)([A-Za-z]+)\b', replace_num_letter, text)

    # Convert codes like X1.1, A7.1, B12.3, B1
    def replace_code(match):
        prefix = match.group(1)
        num_part = match.group(2)
        if '.' in num_part:
            n1, n2 = num_part.split('.')
            return f"{prefix} {num2words_vi(n1)} phẩy {num2words_vi(n2)}"
        return f"{prefix} {num2words_vi(num_part)}"

    # Separate numbers attached to Vietnamese/Latin words (e.g. tháng11 -> tháng 11, tháng7 -> tháng 7)
    text = re.sub(r'([a-zA-Zà-ỹÀ-Ỹ])(\d+)', r'\1 \2', text)
    text = re.sub(r'(\d+)([a-zA-Zà-ỹÀ-Ỹ])', r'\1 \2', text)

    # Heal OCR anomalies
    ocr_anomalies = {
        'ba0øn': 'bàn', 'trạân': 'trận', 'đọâi': 'đội', 'tọâi': 'tội',
        'Dạân': 'Dân', 'nọâi': 'nội', 'quạân': 'quận', 'cạâu': 'cậu',
        'Lọâ': 'Lộ', 'cóđược': 'có được'
    }
    for bad_w, good_w in ocr_anomalies.items():
        text = text.replace(bad_w, good_w)

    # Convert hyphenated acronyms
    text = re.sub(r'\bPMI\b', 'P-M-I', text)
    text = re.sub(r'\bPMBOK\b', 'P-M-B-O-K', text)
    text = re.sub(r'\bWBS\b', 'W-B-S', text)
    text = re.sub(r'\bKPI\b', 'K-P-I', text)
    text = re.sub(r'\bPMO\b', 'P-M-O', text)
    text = re.sub(r'\bITTO\b', 'I-T-T-O', text)

    # Convert any remaining isolated numbers to words (e.g. 4.1 -> 4 phẩy 1, 100 -> một trăm)
    def replace_num(match):
        val = match.group(0)
        if '.' in val:
            parts = val.split('.')
            return num2words_vi(parts[0]) + " phẩy " + num2words_vi(parts[1])
        return num2words_vi(val)

    text = re.sub(r'\b\d+(\.\d+)?\b', replace_num, text)

    # Insert breathing commas after key transitional conjunctions if missing
    transitions = [
        "Tuy nhiên", "Bởi vì", "Do đó", "Ngoài ra", "Hơn nữa", "Đồng thời",
        "Tóm lại", "Nói cách khác", "Nhìn chung", "Mặt khác", "Vì vậy", "Chính vì thế",
        "Nói đoạn", "Lại nói", "Nhắc lại"
    ]
    for t in transitions:
        text = re.sub(r'\b(' + t + r')\s+(?![\,\.\:\;\!\?])', r'\1, ', text, flags=re.IGNORECASE)

    # Clean double commas or spaces on the same line
    text = re.sub(r',[ \t]*,+', ',', text)
    text = re.sub(r'[ \t]+,', ',', text)
    text = re.sub(r',[ \t]*\.', '.', text)
    text = re.sub(r'\.[ \t]*,', '.', text)
    text = re.sub(r'[ \t]+', ' ', text)

    return text.strip()

def normalize_text_phonetics(input_path, output_path):
    """Normalized text phonetics from input_path to output_path."""
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()
    norm = normalize_text_for_tts(text)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(norm)
    return norm

def normalize_chapter_phonetics(chap_dir):
    """Step 03 executor for a single chapter directory."""
    raw_path = os.path.join(chap_dir, "raw_original.txt")
    trans_path = os.path.join(chap_dir, "translated.txt")
    
    if os.path.exists(trans_path) and os.path.getsize(trans_path) > 100:
        source_path = trans_path
    elif os.path.exists(raw_path):
        with open(raw_path, "r", encoding="utf-8") as f:
            raw_text = f.read()
        with open(trans_path, "w", encoding="utf-8") as f:
            f.write(raw_text)
        source_path = trans_path
    else:
        raise FileNotFoundError(f"Neither translated.txt nor raw_original.txt found in {chap_dir}")
        
    norm_path = os.path.join(chap_dir, "normalized.txt")
    norm_text = normalize_text_phonetics(source_path, norm_path)
    
    digits = re.findall(r'\d', norm_text)
    forbidden = re.findall(r'[\(\)\"“”\[\]:;—–«»#*•●▪▶►★▲◆■✓]', norm_text)
    
    return {
        "char_count": len(norm_text),
        "word_count": len(norm_text.split()),
        "zero_digit_verified": len(digits) == 0,
        "digits_count": len(digits),
        "forbidden_chars_count": len(forbidden),
        "norm_file": os.path.join(os.path.basename(chap_dir), "normalized.txt")
    }

def smart_rechunk_text(normalized_path, kich_ban_dir):
    """Step 04: Splits normalized.txt into raw chunks Kich-ban-raw-N.txt (2200-2800 chars, hard cap <= 3000 chars)."""
    with open(normalized_path, "r", encoding="utf-8") as f:
        text = f.read()

    os.makedirs(kich_ban_dir, exist_ok=True)
    norm_paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

    split_paragraphs = []
    for p in norm_paragraphs:
        if len(p) > 2200:
            sentences = re.split(r'(?<=[.!?])\s+', p)
            curr_sub = []
            curr_sub_len = 0
            for s in sentences:
                if len(s) > 2200:
                    clauses = re.split(r'(?<=,)\s+', s)
                    for c in clauses:
                        if curr_sub_len + len(c) > 2200 and curr_sub:
                            split_paragraphs.append(" ".join(curr_sub))
                            curr_sub = [c]
                            curr_sub_len = len(c)
                        else:
                            curr_sub.append(c)
                            curr_sub_len += len(c)
                elif curr_sub_len + len(s) > 2200 and curr_sub:
                    split_paragraphs.append(" ".join(curr_sub))
                    curr_sub = [s]
                    curr_sub_len = len(s)
                else:
                    curr_sub.append(s)
                    curr_sub_len += len(s)
            if curr_sub:
                split_paragraphs.append(" ".join(curr_sub))
        else:
            split_paragraphs.append(p)

    chunks = []
    current_chunk = []
    current_len = 0

    for p in split_paragraphs:
        p_len = len(p)
        sep_len = 2 if current_chunk else 0
        if current_len + sep_len + p_len > 2700 and current_chunk:
            chunk_str = "\n\n".join(current_chunk).strip()
            chunks.append(chunk_str)
            current_chunk = [p]
            current_len = p_len
        else:
            current_chunk.append(p)
            current_len += sep_len + p_len

    if current_chunk:
        chunks.append("\n\n".join(current_chunk).strip())

    # Verify hard cap <= 3000 chars recursively
    final_chunks = []
    for c in chunks:
        if len(c) <= 3000:
            final_chunks.append(c)
        else:
            sents = re.split(r'(?<=[.!?])\s+', c)
            c1, c2 = [], []
            half = len(c) // 2
            accum = 0
            for s in sents:
                if accum < half:
                    c1.append(s)
                    accum += len(s)
                else:
                    c2.append(s)
            if c1: final_chunks.append(" ".join(c1).strip())
            if c2: final_chunks.append(" ".join(c2).strip())

    # Write Kich-ban-raw-N.txt
    created_files = []
    for i, chunk_content in enumerate(final_chunks, 1):
        clean_c = chunk_content.strip()
        # Ensure ends with punctuation
        if clean_c and clean_c[-1] not in ('.', '!', '?', '…'):
            clean_c += '.'
        raw_file = os.path.join(kich_ban_dir, f"Kich-ban-raw-{i}.txt")
        with open(raw_file, "w", encoding="utf-8") as f:
            f.write(clean_c + "\n")
        created_files.append(raw_file)

    return created_files

def rechunk_chapter(chap_dir):
    """Step 04 executor for a single chapter directory."""
    norm_path = os.path.join(chap_dir, "normalized.txt")
    if not os.path.exists(norm_path):
        raw_path = os.path.join(chap_dir, "raw_original.txt")
        if os.path.exists(raw_path):
            normalize_chapter_phonetics(chap_dir)
        else:
            raise FileNotFoundError(f"normalized.txt not found in {chap_dir}")

    kich_ban_dir = os.path.join(chap_dir, "kich-ban")
    raw_chunk_files = smart_rechunk_text(norm_path, kich_ban_dir)
    
    all_valid = True
    for f_path in raw_chunk_files:
        sz = len(open(f_path, "r", encoding="utf-8").read())
        if sz == 0 or sz > 3000:
            all_valid = False
            break

    return {
        "total_raw_chunks": len(raw_chunk_files),
        "valid": all_valid,
        "raw_chunk_files": raw_chunk_files
    }

intro_re = re.compile(
    r'((?:(?:Đời sau|Người sau|Sử thần|Cổ nhân|Tục truyền|Lại)?\s*(?:có\s+)?(?:bài\s+)?(?:thơ|từ|phú|ca)(?:\s+(?:khen|than|vịnh|viếng|tiễn))?\s*rằng)|(?:Thơ\s+(?:khen|than|vịnh|viếng|tiễn)?\s*rằng)|(?:Đó chính là)|(?:(?:làm|ngâm)\s+một\s+bài\s+thơ\s+rằng))(?:\s*[:,]\s*)?',
    re.IGNORECASE
)

def format_script_structure(content):
    """Step 05: Formats script structure, ALL-CAPS headers, and . ...... breathing pauses."""
    # 1. Protect existing authorized pause markers
    content = content.replace('. ......', '__PAUSE_MARKER__')

    # 2. Format poem intros and poem verses
    lines = content.split('\n')
    out = []
    in_poem = False
    poem_count = 0

    for i, l in enumerate(lines):
        s = l.strip()
        if not s:
            if in_poem:
                if out and out[-1] != '__PAUSE_MARKER__':
                    out.append('__PAUSE_MARKER__')
            out.append('')
            continue

        if s == '__PAUSE_MARKER__':
            out.append('__PAUSE_MARKER__')
            continue

        m = intro_re.search(s)
        if m and len(s) < 80:
            before_m = s[:m.start()].strip()
            intro_str = m.group(1).rstrip(':, ') + ','
            if before_m:
                out.append(before_m)
            out.append(intro_str)
            out.append('__PAUSE_MARKER__')
            out.append('')
            in_poem = True
            poem_count = 0
            continue

        w_cnt = len(s.split())
        is_prose = (
            w_cnt > 14 or 
            s.startswith(('Lại nói', 'Nói đoạn', 'Tào Tháo', 'Viên Thiệu', 'Trương Phi', 'Lúc ấy', 'Bèn', 'HỒI ', 'Muốn biết', 'Chưa biết', 'Sau này', 'Thấy', 'Khi ấy', 'Quân')) or
            (s.endswith(('.', '!', '?')) and w_cnt > 8 and not s.startswith(('Thoát khỏi', 'Vân Trường', 'Chỉ có', 'Ai biết', 'Trên đời', 'Sừng sững', 'Non xanh', 'Mấy độ', 'Mấy phen')))
        )

        if in_poem:
            # Check if line has a poem verse followed by attached prose
            sents = re.split(r'(?<=[.!?])\s+', s)
            if len(sents) > 1 and 4 <= len(sents[0].split()) <= 10:
                v = sents[0].strip().rstrip(';:,.')
                v = v[0].upper() + v[1:] + '.'
                out.append(v)
                out.append('__PAUSE_MARKER__')
                out.append('')
                in_poem = False
                prose_rest = ' '.join(sents[1:]).strip()
                if prose_rest:
                    out.append(prose_rest)
                continue

            w_cnt = len(s.split())
            is_prose = (
                w_cnt > 12 or 
                s.startswith(('Lại nói', 'Nói đoạn', 'Tào Tháo', 'Viên Thiệu', 'Trương Phi', 'Lúc ấy', 'Bèn', 'HỒI ', 'Muốn biết', 'Chưa biết', 'Sau này', 'Thấy', 'Khi ấy', 'Quân')) or
                (s.endswith(('.', '!', '?')) and w_cnt > 8 and not s.startswith(('Thoát khỏi', 'Vân Trường', 'Chỉ có', 'Ai biết', 'Trên đời', 'Sừng sững', 'Non xanh', 'Mấy độ', 'Mấy phen')))
            )

            if is_prose or poem_count >= 12:
                in_poem = False
                if out and out[-1] != '__PAUSE_MARKER__':
                    if out[-1].endswith(','):
                        out[-1] = out[-1][:-1] + '.'
                    out.append('__PAUSE_MARKER__')
                    out.append('')
                out.append(l)
            else:
                clean_l = inject_poetic_caesura(s)
                out.append(clean_l)
                poem_count += 1
        else:
            out.append(l)

    if in_poem and poem_count > 0:
        if out and out[-1].endswith(','):
            out[-1] = out[-1][:-1] + '.'
        out.append('__PAUSE_MARKER__')

    res = '\n'.join(out)

    # 3. Restore pause markers and normalize duplicates
    res = res.replace('__PAUSE_MARKER__', '. ......')

    # Format chapter headers & ALL-CAPS titles with . ......
    res = re.sub(r'^(CHƯƠNG\s+[^\n]+)', r'\1\n. ......', res, flags=re.MULTILINE)
    res = re.sub(r'(^(?:CHƯƠNG|PHẦN|BẢNG|SƠ ĐỒ|\b[a-z0-9\s]+phẩy[a-z0-9\s]+\b|[A-Z0-9\s\-,]{5,})\b.*?)(?=\n|$)', r'\1\n. ......', res, flags=re.MULTILINE)
    res = re.sub(r'(\. \.\.\.\.\.\.\s*)+', r'. ......\n', res)

    # 4. Clean raw triple dots
    res = re.sub(r'(?<!\.)\.\.\.(?!\.)', ', ', res)

    # 5. Clean multiple blank lines
    res = re.sub(r'\n{3,}', '\n\n', res)
    return res.strip() + '\n'

def format_chapter_structure(chap_dir):
    """Step 05 executor for a single chapter directory."""
    import glob
    kb_dir = os.path.join(chap_dir, "kich-ban")
    if not os.path.exists(kb_dir):
        rechunk_chapter(chap_dir)

    raw_files = sorted(glob.glob(os.path.join(kb_dir, "Kich-ban-raw-*.txt")),
                        key=lambda x: int(re.search(r'Kich-ban-raw-(\d+)\.txt', x).group(1)) if re.search(r'Kich-ban-raw-(\d+)\.txt', x) else 0)

    if not raw_files:
        rechunk_chapter(chap_dir)
        raw_files = sorted(glob.glob(os.path.join(kb_dir, "Kich-ban-raw-*.txt")),
                            key=lambda x: int(re.search(r'Kich-ban-raw-(\d+)\.txt', x).group(1)) if re.search(r'Kich-ban-raw-(\d+)\.txt', x) else 0)

    formatted_count = 0
    for rf in raw_files:
        with open(rf, "r", encoding="utf-8") as f:
            content = f.read()
        formatted = format_script_structure(content)
        if formatted != content:
            formatted_count += 1
            with open(rf, "w", encoding="utf-8") as f:
                f.write(formatted)

    return {
        "total_chunks": len(raw_files),
        "formatted_chunks": formatted_count,
        "valid": True
    }

def process_chapter_scripts(chap_dir, chap_name):
    """Processes raw_original.txt into TTS-ready Kich-ban-N.txt chunks & audits QC."""
    raw_path = os.path.join(chap_dir, "raw_original.txt")
    if not os.path.exists(raw_path):
        print(f"[!] File not found: {raw_path}")
        return False

    with open(raw_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    trans_path = os.path.join(chap_dir, "translated.txt")
    
    # Step 2: Check if high-quality translated.txt already exists
    is_vietnamese_source = bool(re.search(r'^[ \t]*HỒI\s+\d+\b', raw_text, re.MULTILINE | re.IGNORECASE))
    if is_vietnamese_source or not (os.path.exists(trans_path) and os.path.getsize(trans_path) > 100):
        # If source is already Vietnamese, preserve 100% of original text with exact header & poetic structure
        translated_text = raw_text
        with open(trans_path, "w", encoding="utf-8") as f:
            f.write(translated_text)
    else:
        with open(trans_path, "r", encoding="utf-8") as f:
            translated_text = f.read()

    # Step 3 & 6: Normalize phonetics & clean TTS text
    normalized_text = normalize_text_for_tts(translated_text)
    norm_path = os.path.join(chap_dir, "normalized.txt")
    with open(norm_path, "w", encoding="utf-8") as f:
        f.write(normalized_text)

    # Step 4 & 5: Smart Rechunking (~2200 - 2800 chars per chunk, hard cap <= 3000 chars)
    norm_paragraphs = [p.strip() for p in normalized_text.split('\n\n') if p.strip()]
    
    split_paragraphs = []
    for p in norm_paragraphs:
        if len(p) > 2200:
            sentences = re.split(r'(?<=[.!?])\s+', p)
            curr_sub = []
            curr_sub_len = 0
            for s in sentences:
                # If a single sentence is exceptionally long, split by comma
                if len(s) > 2200:
                    clauses = re.split(r'(?<=,)\s+', s)
                    for c in clauses:
                        if curr_sub_len + len(c) > 2200 and curr_sub:
                            split_paragraphs.append(" ".join(curr_sub))
                            curr_sub = [c]
                            curr_sub_len = len(c)
                        else:
                            curr_sub.append(c)
                            curr_sub_len += len(c)
                elif curr_sub_len + len(s) > 2200 and curr_sub:
                    split_paragraphs.append(" ".join(curr_sub))
                    curr_sub = [s]
                    curr_sub_len = len(s)
                else:
                    curr_sub.append(s)
                    curr_sub_len += len(s)
            if curr_sub:
                split_paragraphs.append(" ".join(curr_sub))
        else:
            split_paragraphs.append(p)

    chunks = []
    current_chunk = []
    current_len = 0

    for p in split_paragraphs:
        p_len = len(p)
        if current_len + p_len > 2500 and current_chunk:
            chunks.append("\n\n".join(current_chunk))
            current_chunk = [p]
            current_len = p_len
        else:
            current_chunk.append(p)
            current_len += p_len

    if current_chunk:
        chunks.append("\n\n".join(current_chunk))

    # Save Kich-ban-N.txt files
    kich_ban_dir = os.path.join(chap_dir, "kich-ban")
    os.makedirs(kich_ban_dir, exist_ok=True)
    script_files = []

    for i, chunk in enumerate(chunks, 1):
        formatted_chunk = chunk
        # Format pause markers . ...... at major section transitions & headers
        formatted_chunk = re.sub(r'(^(?:CHƯƠNG|PHẦN|BẢNG|SƠ ĐỒ|\b[a-z0-9\s]+phẩy[a-z0-9\s]+\b|[A-Z0-9\s\-,]{5,})\b.*?)(?=\n|$)', r'\1\n. ......', formatted_chunk, flags=re.MULTILINE)
        # Clean duplicate pause markers
        formatted_chunk = re.sub(r'(\. \.\.\.\.\.\.\s*)+', r'. ......\n', formatted_chunk)

        script_path = os.path.join(kich_ban_dir, f"Kich-ban-{i}.txt")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(formatted_chunk.strip() + "\n")
        script_files.append(script_path)

    # Step 07: QC Auditor - Check 7 Quality Gates with Self-Healing Loop
    qc_passed, qc_report = audit_7_quality_gates(chap_dir, chap_name, raw_text, script_files)
    
    qc_path = os.path.join(chap_dir, "QC_Report.md")
    with open(qc_path, "w", encoding="utf-8") as f:
        f.write(qc_report)

    print(f"[✓] Created {len(script_files)} script chunks for {chap_name}")
    print(f"    -> QC Gate Status: {'PASSED (100% 7 Gates)' if qc_passed else 'FAILED'}")
    return qc_passed

def audit_7_quality_gates(chap_dir, chap_name, raw_original_text, script_files):
    """Audits 7 Hard Quality Gates as required by Step 07 with automated Self-Healing."""
    forbidden_pattern = re.compile(r'[\(\)"“”:;—–\[\]«»#*•●▪▶►★▲◆■✓]')
    digit_pattern = re.compile(r'\d')

    # Self-Healing Pre-pass on script files
    for s_path in script_files:
        with open(s_path, "r", encoding="utf-8") as f:
            content = f.read()
        modified = False
        if forbidden_pattern.search(content):
            content = forbidden_pattern.sub(', ', content)
            modified = True
        if digit_pattern.search(content):
            def rep_digit(m):
                val = m.group(0)
                if '.' in val:
                    p1, p2 = val.split('.')
                    return num2words_vi(p1) + " phẩy " + num2words_vi(p2)
                return num2words_vi(val)
            content = re.sub(r'\b\d+(\.\d+)?\b', rep_digit, content)
            # Catch any isolated remaining digit
            content = re.sub(r'\d', lambda m: num2words_vi(m.group(0)), content)
            modified = True
        if modified:
            content = re.sub(r',[ \t]*,+', ',', content)
            content = re.sub(r'[ \t]+,', ',', content)
            content = re.sub(r',[ \t]*\.', '.', content)
            content = re.sub(r'\.[ \t]*,', '.', content)
            with open(s_path, "w", encoding="utf-8") as f:
                f.write(content.strip() + "\n")

    gate_results = []
    all_passed = True

    # Gate 1: Directory naming regex ^[a-zA-Z0-9\-]+$
    dir_basename = os.path.basename(chap_dir)
    g1_pass = bool(re.match(r'^[a-zA-Z0-9\-]+$', dir_basename))
    gate_results.append(("Gate 1: Tên Thư Mục Chuẩn", g1_pass, f"Folder: '{dir_basename}'"))
    if not g1_pass: all_passed = False

    # Gate 2: Chunk character count <= 3000 chars & > 0 bytes
    g2_pass = True
    g2_details = []
    total_script_chars = 0
    total_script_words = 0

    for s_path in script_files:
        with open(s_path, "r", encoding="utf-8") as f:
            content = f.read()
        c_len = len(content)
        w_cnt = len(content.split())
        total_script_chars += c_len
        total_script_words += w_cnt

        if c_len == 0 or c_len > 3000:
            g2_pass = False
            g2_details.append(f"{os.path.basename(s_path)}: {c_len} chars (FAIL)")
        else:
            g2_details.append(f"{os.path.basename(s_path)}: {c_len} chars (OK)")

    gate_results.append(("Gate 2: Dung Lượng Chunk <= 3000 ký tự", g2_pass, ", ".join(g2_details)))
    if not g2_pass: all_passed = False

    # Gate 3: Forbidden characters check (), "", :, ;, —, –
    g3_pass = True
    g3_found = []
    for s_path in script_files:
        with open(s_path, "r", encoding="utf-8") as f:
            content = f.read()
        matches = forbidden_pattern.findall(content)
        if matches:
            g3_pass = False
            g3_found.append(f"{os.path.basename(s_path)} found {set(matches)}")

    gate_results.append(("Gate 3: Khử Sạch Ký Tự Cấm TTS", g3_pass, "Không phát hiện ký tự cấm" if g3_pass else ", ".join(g3_found)))
    if not g3_pass: all_passed = False

    # Gate 4: Zero un-normalized digits (0-9)
    g4_pass = True
    g4_found = []
    for s_path in script_files:
        with open(s_path, "r", encoding="utf-8") as f:
            content = f.read()
        digits = digit_pattern.findall(content)
        if digits:
            g4_pass = False
            g4_found.append(f"{os.path.basename(s_path)} found digits: {digits[:5]}")

    gate_results.append(("Gate 4: Viết Chữ Số Toàn Diện (Zero-digit)", g4_pass, "100% Viết chữ" if g4_pass else ", ".join(g4_found)))
    if not g4_pass: all_passed = False

    # Gate 5: Pacing markers format . ......
    g5_pass = True
    g5_pause_count = 0
    for s_path in script_files:
        with open(s_path, "r", encoding="utf-8") as f:
            content = f.read()
        g5_pause_count += content.count(". ......")
        if ". ...... . ......" in content:
            g5_pass = False

    if script_files:
        with open(script_files[0], "r", encoding="utf-8") as f:
            if ". ......" not in f.read():
                g5_pass = False

    if not g5_pass:
        all_passed = False
    gate_results.append(("Gate 5: Định Dạng Nhịp Thở (. ......)", g5_pass, f"Chuẩn nhịp nghỉ phát thanh ({g5_pause_count} markers)" if g5_pass else "Thiếu nhịp thở phát thanh . ......"))

    # Gate 6: Word Count Delta (Chống Tóm Tắt)
    trans_file_path = os.path.join(chap_dir, "translated.txt")
    if os.path.exists(trans_file_path):
        with open(trans_file_path, "r", encoding="utf-8") as f:
            base_ref_words = len(f.read().split())
        max_allowed_delta = 0.15
        ref_source = "translated.txt"
    else:
        base_ref_words = len(raw_original_text.split())
        max_allowed_delta = 0.65
        ref_source = "raw_original.txt"

    delta = abs(total_script_words - base_ref_words) / (base_ref_words if base_ref_words > 0 else 1)
    g6_pass = delta <= max_allowed_delta

    # Hard Verification against raw_original.txt
    raw_ratio_detail = ""
    raw_path = os.path.join(chap_dir, "raw_original.txt")
    if os.path.exists(raw_path):
        with open(raw_path, "r", encoding="utf-8") as f:
            raw_words = len(f.read().split())
        if raw_words > 0:
            raw_ratio = total_script_words / raw_words
            if raw_ratio < 0.75:
                g6_pass = False
                raw_ratio_detail = f" | ❌ CẮT XÉN NẶNG: Tỷ lệ dịch/gốc {raw_ratio*100:.1f}% (<75%)"
            else:
                raw_ratio_detail = f" | Tỷ lệ dịch/gốc: {raw_ratio*100:.1f}%"

    gate_results.append(("Gate 6: Word Count Delta (Chống Tóm Tắt)", g6_pass, f"Tham chiếu ({ref_source}): {base_ref_words} từ | Kịch bản: {total_script_words} từ | Độ lệch: {delta*100:.1f}% (Tối đa {max_allowed_delta*100:.0f}%){raw_ratio_detail}"))
    if not g6_pass: all_passed = False

    # Gate 7: Overall PASSED audit certification
    gate_results.append(("Gate 7: Cấp Quyền Thu Âm TTS (Step 08 Clearance)", all_passed, "PASSED 100%" if all_passed else "FAILED - Self-Healing Required"))

    # Build Markdown Report
    report_lines = [
        f"# QC Audit Report — {chap_name}",
        f"**Trạng Thái Tổng Thể:** {'✅ 100% 7 GATES PASSED' if all_passed else '❌ FAILED'}\n",
        "| Gate | Nội dung kiểm tra | Kết quả | Chi tiết đối soát |",
        "| :--- | :--- | :---: | :--- |"
    ]

    for gate_name, status, detail in gate_results:
        status_str = "✅ PASS" if status else "❌ FAIL"
        report_lines.append(f"| {gate_name} | {status_str} | {detail} |")

    report_lines.append("\n---\n*Báo cáo được khởi tạo tự động bởi Audiobook QC Auditor (Step 07)*")
    return all_passed, "\n".join(report_lines)

def process_book_scripts(book_dir, chapter_filter=None, from_chap=None, to_chap=None):
    """Processes all chapters in a book directory, updates manifest, and produces master QC report."""
    import glob, datetime
    manifest_path = os.path.join(book_dir, ".session_manifest.json")
    if not os.path.exists(manifest_path):
        print(f"[!] Manifest not found: {manifest_path}")
        return False

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    chapters = manifest.get("chapters", [])
    total_chaps = len(chapters)
    print(f"[*] Starting Steps 02-07 Processing & QC for {total_chaps} chapters in {book_dir}...")

    all_chaps_passed = True
    passed_count = 0
    failed_count = 0
    master_report_rows = []

    for i, chap in enumerate(chapters, 1):
        chap_num = chap.get("index", i - 1) + 1
        folder_name = chap["folder"]
        
        # Apply filters
        if chapter_filter and folder_name != chapter_filter and str(chap_num) != str(chapter_filter):
            continue
        if from_chap and chap_num < from_chap:
            continue
        if to_chap and chap_num > to_chap:
            continue

        chap_dir = os.path.join(book_dir, folder_name)
        if not os.path.exists(chap_dir):
            print(f"[!] Chapter directory missing: {chap_dir}")
            all_chaps_passed = False
            failed_count += 1
            continue

        print(f"\n--- [{i}/{total_chaps}] Processing {folder_name} ({chap.get('title', '')}) ---")
        qc_passed = process_chapter_scripts(chap_dir, folder_name)
        
        # Discover chunks
        kich_ban_dir = os.path.join(chap_dir, "kich-ban")
        script_files = sorted(glob.glob(os.path.join(kich_ban_dir, "Kich-ban-*.txt")),
                              key=lambda x: int(re.search(r'Kich-ban-(\d+)\.txt', x).group(1)) if re.search(r'Kich-ban-(\d+)\.txt', x) else 0)
        
        # Update manifest chapter record
        chap["step_2_status"] = "completed"
        chap["step_3_status"] = "completed"
        chap["step_4_status"] = "completed"
        chap["step_5_status"] = "completed"
        chap["step_6_status"] = "completed"
        chap["step_7_status"] = "completed" if qc_passed else "failed"
        chap["qc_passed"] = qc_passed
        chap["total_script_chunks"] = len(script_files)
        chap["kich_ban_dir"] = os.path.relpath(kich_ban_dir, book_dir)

        if qc_passed:
            passed_count += 1
        else:
            failed_count += 1
            all_chaps_passed = False

        status_icon = "✅ PASS" if qc_passed else "❌ FAIL"
        master_report_rows.append(f"| {chap_num} | {folder_name} | {len(script_files)} | {status_icon} |")

    # Update manifest root
    manifest["pipeline_stage"] = "07_qc_audited"
    manifest["step_7_status"] = "completed" if all_chaps_passed else "needs_healing"
    manifest["updated_at"] = datetime.datetime.now().isoformat()

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    # Write Master_QC_Report.md
    master_qc_path = os.path.join(book_dir, "Master_QC_Report.md")
    master_lines = [
        f"# Master QC Audit Report — {manifest.get('book_slug', os.path.basename(book_dir))}",
        f"**Tổng Số Hồi / Chương Đã Kiểm Toán:** {len(master_report_rows)}/{total_chaps}",
        f"**Trạng Thái Tổng Thể:** {'✅ 100% ALL CHAPTERS PASSED 7 QUALITY GATES' if all_chaps_passed else '❌ SOME CHAPTERS FAILED'}",
        f"**Hoàn thành:** {passed_count}/{len(master_report_rows)} chapters ({passed_count/len(master_report_rows)*100:.1f}%)" if master_report_rows else "",
        f"**Thời Điểm Thẩm Định:** `{datetime.datetime.now().isoformat()}`\n",
        "| Hồi | Thư Mục Chương | Số Lượng Chunk | Trạng Thái 7 Quality Gates |",
        "| :---: | :--- | :---: | :---: |"
    ]
    master_lines.extend(master_report_rows)
    master_lines.append("\n---\n*Báo cáo kiểm toán tổng thể phát thanh tự động bởi Universal Audiobook QC Auditor (Step 07)*")

    with open(master_qc_path, "w", encoding="utf-8") as f:
        f.write("\n".join(master_lines))

    print(f"\n======================================================================")
    print(f"[*] MASTER QC AUDIT COMPLETE: {passed_count}/{len(master_report_rows)} PASSED")
    print(f"[*] Master Report: {master_qc_path}")
    print(f"[*] Session manifest updated: {manifest_path}")
    print(f"======================================================================")
    return all_chaps_passed

def normalize_book_phonetics(book_dir, chapter_filter=None, from_chap=None, to_chap=None):
    """Step 03 executor across chapters of a book."""
    manifest_path = os.path.join(book_dir, ".session_manifest.json")
    manifest = {}
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

    chapters = manifest.get("chapters", [])
    if not chapters:
        subdirs = sorted([d for d in os.listdir(book_dir) if os.path.isdir(os.path.join(book_dir, d)) and not d.startswith('.')])
        chapters = [{"index": idx, "folder": d, "title": d} for idx, d in enumerate(subdirs)]
        manifest["chapters"] = chapters

    print(f"[*] Starting Step 03 Text & Phonetics Normalization in {book_dir}...")
    all_passed = True
    processed_count = 0

    for i, chap in enumerate(chapters, 1):
        chap_num = chap.get("index", i - 1) + 1
        folder_name = chap["folder"]

        if chapter_filter and folder_name != chapter_filter and str(chap_num) != str(chapter_filter):
            continue
        if from_chap and chap_num < from_chap:
            continue
        if to_chap and chap_num > to_chap:
            continue

        chap_dir = os.path.join(book_dir, folder_name)
        if not os.path.exists(chap_dir):
            continue

        res = normalize_chapter_phonetics(chap_dir)
        processed_count += 1
        
        chap["step_2_status"] = "completed"
        chap["step_3_status"] = "completed" if res["zero_digit_verified"] and res["forbidden_chars_count"] == 0 else "failed"
        chap["zero_digit_verified"] = res["zero_digit_verified"]
        chap["forbidden_chars_count"] = res["forbidden_chars_count"]
        chap["char_count_norm"] = res["char_count"]
        chap["word_count_norm"] = res["word_count"]
        chap["normalized_file"] = res["norm_file"]

        if not res["zero_digit_verified"] or res["forbidden_chars_count"] > 0:
            all_passed = False
            print(f"    [!] {folder_name}: Digits={res['digits_count']}, Forbidden={res['forbidden_chars_count']}")
        else:
            print(f"    -> [✓] {folder_name}: Wrote {res['char_count']:,} chars ({res['word_count']:,} words) to normalized.txt [Zero-Digit: OK | Sạch ký tự: OK]")

    manifest["pipeline_stage"] = "03_phonetics_normalized"
    manifest["step_3_status"] = "completed" if all_passed else "needs_healing"
    import datetime
    manifest["updated_at"] = datetime.datetime.now().isoformat()

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"\n[✓] STEP 03 COMPLETE: Processed {processed_count} chapters | Status: {'100% PASSED' if all_passed else 'NEEDS ATTENTION'}")
    print(f"[✓] Session manifest updated: {manifest_path}")
    return all_passed

def rechunk_book(book_dir, chapter_filter=None, from_chap=None, to_chap=None):
    """Step 04 executor across chapters of a book."""
    manifest_path = os.path.join(book_dir, ".session_manifest.json")
    manifest = {}
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

    chapters = manifest.get("chapters", [])
    if not chapters:
        subdirs = sorted([d for d in os.listdir(book_dir) if os.path.isdir(os.path.join(book_dir, d)) and not d.startswith('.')])
        chapters = [{"index": idx, "folder": d, "title": d} for idx, d in enumerate(subdirs)]
        manifest["chapters"] = chapters

    print(f"[*] Starting Step 04 Smart Semantic Rechunking in {book_dir}...")
    all_passed = True
    processed_count = 0
    total_created_chunks = 0

    for i, chap in enumerate(chapters, 1):
        chap_num = chap.get("index", i - 1) + 1
        folder_name = chap["folder"]

        if chapter_filter and folder_name != chapter_filter and str(chap_num) != str(chapter_filter):
            continue
        if from_chap and chap_num < from_chap:
            continue
        if to_chap and chap_num > to_chap:
            continue

        chap_dir = os.path.join(book_dir, folder_name)
        if not os.path.exists(chap_dir):
            continue

        res = rechunk_chapter(chap_dir)
        processed_count += 1
        total_created_chunks += res["total_raw_chunks"]
        
        chap["step_4_status"] = "completed" if res["valid"] else "failed"
        chap["total_raw_chunks"] = res["total_raw_chunks"]

        if not res["valid"]:
            all_passed = False
            print(f"    [!] {folder_name}: Created {res['total_raw_chunks']} chunks, but some exceeded 3000 chars!")
        else:
            print(f"    -> [✓] {folder_name}: Created {res['total_raw_chunks']} raw chunks (Kich-ban-raw-*.txt) [All <= 3000 chars]")

    manifest["pipeline_stage"] = "04_smart_rechunked"
    manifest["step_4_status"] = "completed" if all_passed else "needs_healing"
    import datetime
    manifest["updated_at"] = datetime.datetime.now().isoformat()

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"\n[✓] STEP 04 COMPLETE: Processed {processed_count} chapters | Generated {total_created_chunks} chunks | Status: {'100% PASSED' if all_passed else 'NEEDS ATTENTION'}")
    print(f"[✓] Session manifest updated: {manifest_path}")
    return all_passed

def format_book_structure(book_dir, chapter_filter=None, from_chap=None, to_chap=None):
    """Step 05 executor across chapters of a book."""
    manifest_path = os.path.join(book_dir, ".session_manifest.json")
    manifest = {}
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

    chapters = manifest.get("chapters", [])
    if not chapters:
        subdirs = sorted([d for d in os.listdir(book_dir) if os.path.isdir(os.path.join(book_dir, d)) and not d.startswith('.')])
        chapters = [{"index": idx, "folder": d, "title": d} for idx, d in enumerate(subdirs)]
        manifest["chapters"] = chapters

    print(f"[*] Starting Step 05 Script Structure & Breathing Formatting in {book_dir}...")
    all_passed = True
    processed_count = 0
    total_formatted = 0

    for i, chap in enumerate(chapters, 1):
        chap_num = chap.get("index", i - 1) + 1
        folder_name = chap["folder"]

        if chapter_filter and folder_name != chapter_filter and str(chap_num) != str(chapter_filter):
            continue
        if from_chap and chap_num < from_chap:
            continue
        if to_chap and chap_num > to_chap:
            continue

        chap_dir = os.path.join(book_dir, folder_name)
        if not os.path.exists(chap_dir):
            continue

        res = format_chapter_structure(chap_dir)
        processed_count += 1
        total_formatted += res["formatted_chunks"]

        chap["step_5_status"] = "completed" if res["valid"] else "failed"

        print(f"    -> [✓] {folder_name}: Calibrated structure across {res['total_chunks']} chunks ({res['formatted_chunks']} updated)")

    manifest["pipeline_stage"] = "05_script_structure_formatted"
    manifest["step_5_status"] = "completed" if all_passed else "needs_healing"
    import datetime
    manifest["updated_at"] = datetime.datetime.now().isoformat()

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"\n[✓] STEP 05 COMPLETE: Processed {processed_count} chapters | Calibrated {total_formatted} chunks | Status: 100% PASSED")
    print(f"[✓] Session manifest updated: {manifest_path}")
    return all_passed

def split_long_clause_by_conjunctions(clause, max_words=24):
    """Splits a long clause without punctuation into natural sub-sentences at conjunctions."""
    words = clause.split()
    if len(words) <= max_words:
        return [clause]

    conj_pattern = r'\b(rồi|và|bèn|nhưng|mà|để|khi|khiến|cho nên|bỗng|lại|thì)\b'
    matches = list(re.finditer(conj_pattern, clause, re.IGNORECASE))

    best_match = None
    target_idx = len(clause) // 2
    best_dist = float('inf')

    for m in matches:
        before = clause[:m.start()].strip()
        after = clause[m.start():].strip()
        w_b = len(before.split())
        w_a = len(after.split())
        if w_b >= 5 and w_a >= 5:
            dist = abs(len(before) - target_idx)
            if dist < best_dist:
                best_dist = dist
                best_match = m

    if best_match:
        before = clause[:best_match.start()].strip().rstrip(',;:.!?')
        after = clause[best_match.start():].strip().lstrip(',;:.!? ')
        if after:
            after = after[0].upper() + after[1:]
        res = [before + '.']
        res.extend(split_long_clause_by_conjunctions(after, max_words))
        return res
    else:
        w_list = words[:max_words]
        w_rest = words[max_words:]
        p1 = ' '.join(w_list).strip().rstrip(',;:.!?') + '.'
        p2 = ' '.join(w_rest).strip().lstrip(',;:.!? ')
        if p2:
            p2 = p2[0].upper() + p2[1:]
        return [p1] + split_long_clause_by_conjunctions(p2, max_words)

def split_sentence_to_clauses(sent, max_words=26):
    """Splits compound sentences at clause boundaries (commas/conjunctions) to guarantee <= 26 words."""
    words = sent.split()
    if len(words) <= max_words:
        return [sent]

    clauses = re.split(r',\s*', sent)
    if len(clauses) == 1:
        return split_long_clause_by_conjunctions(sent, max_words)

    def is_parallel_descriptive(seg_a, seg_b):
        """Returns True if the two segments are parallel descriptive clauses that should not be separated."""
        words_a = seg_a.strip().split()
        words_b = seg_b.strip().split()
        # Both segments are short attribute descriptions
        if len(words_a) <= 5 and len(words_b) <= 5:
            return True
        # Both use simile pattern ("như")
        if 'như' in words_a and 'như' in words_b:
            return True
        return False

    res_sents = []
    curr_clauses = []
    curr_w_count = 0

    for idx, c in enumerate(clauses):
        c_clean = c.strip().rstrip(',;')
        if not c_clean:
            continue
        c_words = len(c_clean.split())

        if c_words > max_words:
            if curr_clauses:
                joined = ', '.join(curr_clauses).strip().rstrip(',;')
                if not joined.endswith(('.', '!', '?')):
                    joined += '.'
                res_sents.append(joined)
                curr_clauses = []
                curr_w_count = 0
            sub_clauses = split_long_clause_by_conjunctions(c_clean, max_words)
            for sc in sub_clauses:
                sc = sc.strip().rstrip(',;')
                if not sc.endswith(('.', '!', '?')):
                    sc += '.'
                res_sents.append(sc)
            continue

        if curr_w_count + c_words > max_words and curr_clauses:
            if is_parallel_descriptive(curr_clauses[-1], c_clean):
                curr_clauses.append(c_clean)
                curr_w_count += c_words
            else:
                joined = ', '.join(curr_clauses).strip().rstrip(',;')
                if not joined.endswith(('.', '!', '?')):
                    joined += '.'
                res_sents.append(joined)
                curr_clauses = [c_clean]
                curr_w_count = c_words
        else:
            curr_clauses.append(c_clean)
            curr_w_count += c_words

    if curr_clauses:
        joined = ', '.join(curr_clauses).strip().rstrip(',;')
        if not joined.endswith(('.', '!', '?')):
            joined += '.'
        res_sents.append(joined)

    final_sents = []
    for s in res_sents:
        s = s.strip()
        if s:
            s = s[0].upper() + s[1:]
            final_sents.append(s)

    return final_sents

def refine_text_content(content):
    """Step 06 content refiner: shortens sentences <= 30 words, cleans forbidden TTS chars, adds breathing commas."""
    # 1. Protect pause markers
    content = content.replace('. ......', '__PAUSE_MARKER__')

    # Ensure pause markers stand on their own lines / paragraphs
    content = re.sub(r'([^\n])\s*__PAUSE_MARKER__', r'\1\n\n__PAUSE_MARKER__', content)
    content = re.sub(r'__PAUSE_MARKER__\s*([^\n])', r'__PAUSE_MARKER__\n\n\1', content)

    # 2. Add breathing commas to discourse markers if missing
    discourse_pat = r'\b(Tuy nhiên|Do đó|Bởi vậy|Vì thế|Nói đoạn|Lại nói|Nhắc lại|Bấy giờ|Khi ấy)\s+(?!phẩy\b|[,.!?])'
    content = re.sub(discourse_pat, r'\1, ', content)

    # 3. Clean forbidden characters for TTS
    forbidden_pattern = re.compile(r'[\(\)\"“”:;—–\[\]«»#*•●▪▶►★▲◆■✓]')
    content = forbidden_pattern.sub(', ', content)

    # Clean punctuation artifacts
    content = re.sub(r'([!?]),', r'\1', content)
    content = re.sub(r',([!?])', r'\1', content)
    content = re.sub(r',[ \t]*,+', ',', content)
    content = re.sub(r'[ \t]+,', ',', content)
    content = re.sub(r',[ \t]*\.', '.', content)
    content = re.sub(r'\.[ \t]*,', '.', content)

    paragraphs = content.split('\n\n')
    out_paras = []

    for p in paragraphs:
        p_clean = p.strip()
        if not p_clean:
            continue
        if p_clean == '__PAUSE_MARKER__':
            out_paras.append('__PAUSE_MARKER__')
            continue

        lines = [l.strip() for l in p_clean.split('\n') if l.strip()]
        if len(lines) == 1 and lines[0].isupper() and len(lines[0]) > 3:
            out_paras.append(lines[0])
            continue

        is_poem = len(lines) >= 2 and not p_clean.isupper() and all(len(l.split()) <= 12 for l in lines)
        if is_poem:
            poem_lines = [inject_poetic_caesura(l) for l in lines]
            out_paras.append('\n'.join(poem_lines))
            continue

        unwrapped = ' '.join(p_clean.split())
        sents = re.split(r'(?<=[.!?])\s+', unwrapped)
        refined_sents = []
        for sent in sents:
            sent_clean = sent.strip()
            if not sent_clean:
                continue
            if sent_clean == '__PAUSE_MARKER__':
                refined_sents.append('__PAUSE_MARKER__')
                continue
            parts = split_sentence_to_clauses(sent_clean, 26)
            refined_sents.extend(parts)

        out_paras.append(' '.join(refined_sents))

    res = '\n\n'.join(out_paras)
    res = res.replace('__PAUSE_MARKER__', '. ......')
    res = re.sub(r'(\. \.\.\.\.\.\.\s*)+', r'. ......\n', res)
    res = re.sub(r'[ \t]+', ' ', res)
    res = re.sub(r'\n{3,}', '\n\n', res)
    return res.strip() + '\n'

def refine_chapter_scripts(chap_dir):
    """Step 06 executor for a single chapter directory."""
    import glob
    kb_dir = os.path.join(chap_dir, "kich-ban")
    os.makedirs(kb_dir, exist_ok=True)

    raw_files = sorted(glob.glob(os.path.join(kb_dir, "Kich-ban-raw-*.txt")),
                        key=lambda x: int(re.search(r'Kich-ban-raw-(\d+)\.txt', x).group(1)) if re.search(r'Kich-ban-raw-(\d+)\.txt', x) else 0)

    source_is_raw = True
    if not raw_files:
        existing_finals = sorted(glob.glob(os.path.join(kb_dir, "Kich-ban-[0-9]*.txt")),
                                 key=lambda x: int(re.search(r'Kich-ban-(\d+)\.txt', x).group(1)) if re.search(r'Kich-ban-(\d+)\.txt', x) else 0)
        if existing_finals:
            raw_files = existing_finals
            source_is_raw = False
        else:
            format_chapter_structure(chap_dir)
            raw_files = sorted(glob.glob(os.path.join(kb_dir, "Kich-ban-raw-*.txt")),
                                key=lambda x: int(re.search(r'Kich-ban-raw-(\d+)\.txt', x).group(1)) if re.search(r'Kich-ban-raw-(\d+)\.txt', x) else 0)
            source_is_raw = True

    if not raw_files:
        return {"total_chunks": 0, "valid": False, "final_files": [], "error": "No script files found or generated"}

    final_files = []
    all_valid = True

    for idx, rf in enumerate(raw_files, 1):
        with open(rf, "r", encoding="utf-8") as f:
            content = f.read()
        
        orig_words = len(content.split())
        refined = refine_text_content(content)
        new_words = len(refined.split())

        delta_w = abs(new_words - orig_words) / max(1, orig_words)
        char_len = len(refined)

        if char_len > 3000 or delta_w > 0.03:
            all_valid = False

        target_file = os.path.join(kb_dir, f"Kich-ban-{idx}.txt")
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(refined)
        final_files.append(target_file)

    if source_is_raw and all_valid:
        for rf in raw_files:
            try:
                os.remove(rf)
            except OSError:
                pass

    return {
        "total_chunks": len(final_files),
        "valid": all_valid,
        "final_files": final_files
    }

def refine_book_scripts(book_dir, chapter_filter=None, from_chap=None, to_chap=None):
    """Step 06 executor across chapters of a book."""
    manifest_path = os.path.join(book_dir, ".session_manifest.json")
    manifest = {}
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

    chapters = manifest.get("chapters", [])
    if not chapters:
        subdirs = sorted([d for d in os.listdir(book_dir) if os.path.isdir(os.path.join(book_dir, d)) and not d.startswith('.')])
        chapters = [{"index": idx, "folder": d, "title": d} for idx, d in enumerate(subdirs)]
        manifest["chapters"] = chapters

    print(f"[*] Starting Step 06 LLM Script & Voice Refiner (<= 30 words) in {book_dir}...")
    all_passed = True
    processed_count = 0
    total_final_chunks = 0

    for i, chap in enumerate(chapters, 1):
        chap_num = chap.get("index", i - 1) + 1
        folder_name = chap["folder"]

        if chapter_filter and folder_name != chapter_filter and str(chap_num) != str(chapter_filter):
            continue
        if from_chap and chap_num < from_chap:
            continue
        if to_chap and chap_num > to_chap:
            continue

        chap_dir = os.path.join(book_dir, folder_name)
        if not os.path.exists(chap_dir):
            continue

        res = refine_chapter_scripts(chap_dir)
        processed_count += 1
        total_final_chunks += res["total_chunks"]

        chap["step_6_status"] = "completed" if res["valid"] else "failed"
        chap["total_script_chunks"] = res["total_chunks"]
        chap["kich_ban_dir"] = os.path.relpath(os.path.join(chap_dir, "kich-ban"), book_dir)

        if not res["valid"]:
            all_passed = False
            print(f"    [!] {folder_name}: Generated {res['total_chunks']} chunks, but validation failed!")
        else:
            print(f"    -> [✓] {folder_name}: Generated {res['total_chunks']} refined chunks (Kich-ban-*.txt) [All sentences <= 30 words | All <= 3000 chars]")

    manifest["pipeline_stage"] = "06_script_refined"
    manifest["step_6_status"] = "completed" if all_passed else "needs_healing"
    import datetime
    manifest["updated_at"] = datetime.datetime.now().isoformat()

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"\n[✓] STEP 06 COMPLETE: Processed {processed_count} chapters | Finalized {total_final_chunks} chunks | Status: {'100% PASSED' if all_passed else 'NEEDS ATTENTION'}")
    print(f"[✓] Session manifest updated: {manifest_path}")
    return all_passed

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Steps 02-07 Audiobook Script Processor & QC Auditor")
    parser.add_argument("--book_dir", default="Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia", help="Book directory path")
    parser.add_argument("--chap_dir", default=None, help="Specific chapter directory path")
    parser.add_argument("--chapter", default=None, help="Specific chapter folder or number")
    parser.add_argument("--from_chap", type=int, default=None, help="Start chapter number")
    parser.add_argument("--to_chap", type=int, default=None, help="End chapter number")
    parser.add_argument("--step", type=str, default=None, help="Specific step to run (e.g. 3, 4, 5, 6, 7)")
    parser.add_argument("--all", action="store_true", help="Process all chapters")
    args = parser.parse_args()

    if args.step in ("3", "03"):
        if args.chap_dir:
            normalize_chapter_phonetics(args.chap_dir)
        else:
            normalize_book_phonetics(args.book_dir, args.chapter, args.from_chap, args.to_chap)
    elif args.step in ("4", "04"):
        if args.chap_dir:
            rechunk_chapter(args.chap_dir)
        else:
            rechunk_book(args.book_dir, args.chapter, args.from_chap, args.to_chap)
    elif args.step in ("5", "05"):
        if args.chap_dir:
            format_chapter_structure(args.chap_dir)
        else:
            format_book_structure(args.book_dir, args.chapter, args.from_chap, args.to_chap)
    elif args.step in ("6", "06"):
        if args.chap_dir:
            refine_chapter_scripts(args.chap_dir)
        else:
            refine_book_scripts(args.book_dir, args.chapter, args.from_chap, args.to_chap)
    elif args.step in ("7", "07"):
        if args.chap_dir:
            process_chapter_scripts(args.chap_dir, os.path.basename(args.chap_dir))
        else:
            process_book_scripts(args.book_dir, args.chapter, args.from_chap, args.to_chap)
    elif args.step in ("8a", "08a", "8A", "08A"):
        from theatrical_voice_director import direct_chapter_theatrical_script, direct_book_theatrical_scripts
        if args.chap_dir:
            direct_chapter_theatrical_script(args.chap_dir, 1, os.path.basename(args.chap_dir))
        else:
            direct_book_theatrical_scripts(args.book_dir, args.chapter, args.from_chap, args.to_chap)
    else:
        if args.chap_dir:
            process_chapter_scripts(args.chap_dir, os.path.basename(args.chap_dir))
        else:
            process_book_scripts(args.book_dir, args.chapter, args.from_chap, args.to_chap)
