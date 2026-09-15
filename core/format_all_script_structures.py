#!/usr/bin/env python3
# ==============================================================================
# Step 05: Script Structure & Poetic Prosody Formatter
# Skill: arf_05_script_structure_formatter
# ==============================================================================
import os
import re
import glob
import json
import argparse
import datetime

POEM_INTRO_PATTERN = (
    r'((?:(?:Có|Lại có|Người sau có|Đời sau có|Sử thần có|Cổ nhân có|Sau này có)\s+(?:bài\s+)?'
    r'(?:từ|thơ|thơ khen|thơ than|thơ vịnh|thơ viếng|thơ tiễn|thơ tứ tuyệt|thơ lục bát|bài từ khúc|bài phú|phú|ca)?'
    r'(?:\s+luận\s+về\s+[^,:]+)?\s*rằng)|'
    r'(?:Thơ\s+(?:khen|than|vịnh|viếng|tiễn)?\s*rằng)|'
    r'(?:Bèn\s+ngâm\s*rằng)|'
    r'(?:Ngâm\s*rằng)|'
    r'(?:Đó\s+chính\s+là))(?:\s*[:,]\s*)?'
)

POEM_INTRO_RE = re.compile(
    r'(?P<intro>' + POEM_INTRO_PATTERN + r')$',
    re.IGNORECASE | re.UNICODE
)

INNER_POEM_INTRO_RE = re.compile(
    r'(\b(?:Lại có|Người sau có|Đời sau có|Sau này có)\s+(?:thơ|bài thơ|thơ luận về\s+[^,:]+)\s*rằng)[,:]?\s*(.*)',
    re.IGNORECASE | re.UNICODE
)

def inject_poetic_caesura(line_str):
    clean = line_str.strip()
    if not clean or clean == '. ......':
        return clean

    clean = re.sub(r'([!?,;])\.', r'\1', clean)
    clean = re.sub(r'\.+', '.', clean)

    trailing_punct = ''
    m_punct = re.search(r'([,;!?.…]+)$', clean)
    if m_punct:
        trailing_punct = m_punct.group(1)
        raw_text = clean[:-len(trailing_punct)].strip()
    else:
        raw_text = clean

    if ',' in raw_text or ';' in raw_text:
        res = raw_text
    else:
        words = raw_text.split()
        n = len(words)
        if n == 7:
            if words[0][0].isupper() and len(words) > 1 and words[1][0].isupper() and (len(words) <= 2 or not words[2][0].isupper()):
                res = f"{' '.join(words[:2])}, {' '.join(words[2:4])}, {' '.join(words[4:])}"
            else:
                res = f"{' '.join(words[:4])}, {' '.join(words[4:])}"
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
        res = res + ','

    if not res.endswith(('.', ',', ';', '!', '?', '…')):
        res = res + ','
    return res

def split_and_isolate_verses(block_text):
    # Check for chained second poem intro inside this block (e.g. 19-Hoi-19/Kich-ban-12)
    m_inner = INNER_POEM_INTRO_RE.search(block_text)
    if m_inner:
        p_before = block_text[:m_inner.start()].strip()
        intro2 = m_inner.group(1).strip().rstrip(':, ') + ','
        p_after = m_inner.group(2).strip()

        v_before, pr_before = split_and_isolate_verses(p_before)
        v_after, pr_after = split_and_isolate_verses(p_after)

        combined_blocks = []
        if v_before:
            combined_blocks.append('\n'.join(v_before))
            combined_blocks.append('__PAUSE_MARKER__')
        if pr_before:
            combined_blocks.append(pr_before)
            combined_blocks.append('__PAUSE_MARKER__')
        combined_blocks.append(intro2)
        combined_blocks.append('__PAUSE_MARKER__')
        if v_after:
            combined_blocks.append('\n'.join(v_after))
            combined_blocks.append('__PAUSE_MARKER__')
        if pr_after:
            combined_blocks.append(pr_after)
        return combined_blocks, None

    # Detect trailing prose if any
    trailing_prose = ''
    m_prose = re.search(r'(\s+[A-ZÀ-Ỹ][a-zà-ỹ]+(?:\s+[A-ZÀ-Ỹa-zà-ỹ]+)*\s+(?:hỏi|nói|tâu|đến gần|lấy xong|bảo|nghe tin|kéo về|sai quân|về đến|tiễn)[^.\n]*[.\n]?)$', block_text)
    if m_prose:
        trailing_prose = m_prose.group(1).strip()
        poem_body = block_text[:-len(m_prose.group(1))].strip()
    else:
        m_cliff = re.search(r'(\s*(?:Muốn biết|Chưa biết)[^\n]*xem (?:đến )?hồi sau sẽ rõ\.?)$', block_text, re.IGNORECASE)
        if m_cliff:
            trailing_prose = m_cliff.group(1).strip()
            poem_body = block_text[:-len(m_cliff.group(1))].strip()
        else:
            poem_body = block_text

    lines = [l.strip() for l in poem_body.splitlines() if l.strip()]
    raw_pieces = []
    for line in lines:
        subparts = re.split(r'(?<=[.!?])\s+(?=[A-ZÀ-Ỹ])', line)
        for sp in subparts:
            sp = sp.strip()
            if not sp:
                continue
            words = sp.split()
            if len(words) > 9 and ',' in sp:
                comma_parts = [p.strip() for p in sp.split(',') if p.strip()]
                if len(comma_parts) > 1 and all(4 <= len(cp.split()) <= 8 for cp in comma_parts):
                    raw_pieces.extend(comma_parts)
                    continue
                parts = re.split(r'(?<=,)\s+', sp)
                cum_words = 0
                split_idx = -1
                for idx, p in enumerate(parts[:-1]):
                    cum_words += len(p.split())
                    next_part = parts[idx + 1]
                    if 6 <= cum_words <= 8 and next_part[0].isupper():
                        split_idx = idx
                        break
                if split_idx != -1:
                    raw_pieces.append(' '.join(parts[:split_idx + 1]).strip())
                    raw_pieces.append(' '.join(parts[split_idx + 1:]).strip())
                    continue
            raw_pieces.append(sp)

    verses = []
    in_trailing = False
    more_trailing = []

    for p in raw_pieces:
        if in_trailing:
            more_trailing.append(p)
            continue

        w_cnt = len(p.split())
        is_narrative_cue = bool(re.search(r'\b(hỏi|nói|tâu|đến gần|lấy xong|bảo|nghe tin|kéo về|sai quân|về đến|tiễn|ngồi trong)\b', p))

        if len(verses) in (4, 8) and (w_cnt > 8 or (w_cnt >= 4 and is_narrative_cue and any(c.isupper() for c in p[:10]))):
            in_trailing = True
            more_trailing.append(p)
        elif 4 <= w_cnt <= 10:
            verses.append(p)
        else:
            if verses:
                in_trailing = True
                more_trailing.append(p)
            else:
                verses.append(p)

    all_prose_parts = []
    if more_trailing:
        all_prose_parts.append(' '.join(more_trailing).strip())
    if trailing_prose:
        all_prose_parts.append(trailing_prose.strip())

    formatted_verses = [inject_poetic_caesura(v) for v in verses]
    return formatted_verses, ' '.join(all_prose_parts).strip()

def format_script_content(text):
    clean = text.replace('. ......', '__PAUSE_MARKER__')
    clean = re.sub(r'(?<!\w)\.{2,}(?!\w)', ', ', clean)
    clean = re.sub(r'__PAUSE_MARKER__', r'\n\n__PAUSE_MARKER__\n\n', clean)

    raw_paras = [p.strip() for p in clean.split('\n\n') if p.strip()]
    out_blocks = []
    expecting_poem = False

    for p in raw_paras:
        if p == '__PAUSE_MARKER__':
            if not out_blocks or out_blocks[-1] != '__PAUSE_MARKER__':
                out_blocks.append('__PAUSE_MARKER__')
            continue

        # Check for chapter title e.g. "HỒI MỘT", "HỒI HAI"
        m_hoi = re.match(r'^(HỒI\s+[A-ZÀ-Ỹ\s]+)$', p)
        if m_hoi:
            out_blocks.append(m_hoi.group(1).strip())
            out_blocks.append('__PAUSE_MARKER__')
            continue

        # Check for couplet heading (two all-uppercase lines)
        lines = [l.strip() for l in p.splitlines() if l.strip()]
        if len(lines) == 2 and all(l.isupper() for l in lines) and len(lines[0].split()) >= 3:
            c1 = lines[0].rstrip(';,.') + ','
            c2 = lines[1].rstrip(';,.') + '.'
            out_blocks.append(f"{c1}\n{c2}")
            out_blocks.append('__PAUSE_MARKER__')
            continue

        # Check for poem intro
        m_intro = POEM_INTRO_RE.search(p)
        if m_intro:
            before_intro = p[:m_intro.start()].strip()
            intro_text = m_intro.group('intro').strip().rstrip(':, ') + ','
            if before_intro:
                out_blocks.append(before_intro)
            out_blocks.append(intro_text)
            out_blocks.append('__PAUSE_MARKER__')
            expecting_poem = True
            continue

        if expecting_poem:
            res_verses, res_prose = split_and_isolate_verses(p)
            if res_prose is None:
                out_blocks.extend(res_verses)
            else:
                poem_text = '\n'.join(res_verses)
                out_blocks.append(poem_text)
                out_blocks.append('__PAUSE_MARKER__')
                if res_prose:
                    out_blocks.append(res_prose)
            expecting_poem = False
            continue

        # Normal prose: check for cliffhanger
        m_cliff = re.search(r'^(.*?)((?:Muốn biết|Chưa biết)[^\n]*xem (?:đến )?hồi sau sẽ rõ\.?)$', p, re.IGNORECASE | re.DOTALL)
        if m_cliff:
            pre_cliff = m_cliff.group(1).strip()
            cliff_text = m_cliff.group(2).strip()
            if pre_cliff:
                out_blocks.append(pre_cliff)
            if not out_blocks or out_blocks[-1] != '__PAUSE_MARKER__':
                out_blocks.append('__PAUSE_MARKER__')
            out_blocks.append(cliff_text)
            continue

        out_blocks.append(p)

    final_text = '\n\n'.join(out_blocks)
    final_text = final_text.replace('__PAUSE_MARKER__', '. ......')
    final_text = re.sub(r'(\. \.\.\.\.\.\.\s*\n*){2,}', r'. ......\n\n', final_text)
    return final_text.strip() + '\n'

def format_all_chapters(book_dir):
    kb_files = sorted(
        glob.glob(os.path.join(book_dir, "*", "kich-ban", "Kich-ban-*.txt")),
        key=lambda x: (
            int(re.search(r'/(\d+)-', x).group(1)) if re.search(r'/(\d+)-', x) else 0,
            int(re.search(r'Kich-ban-(\d+)\.txt', x).group(1)) if re.search(r'Kich-ban-(\d+)\.txt', x) else 0
        )
    )

    print(f"[*] Starting Step 05 Script Structure & Poetic Prosody Formatter in {book_dir}...")
    print(f"[*] Total script chunks discovered: {len(kb_files)}")

    updated_files = 0
    modified_chapters = set()

    for fpath in kb_files:
        with open(fpath, "r", encoding="utf-8") as fh:
            orig = fh.read()

        formatted = format_script_content(orig)

        if len(formatted) > 3000:
            print(f"    [!] Warning: {fpath} exceeded 3000 chars ({len(formatted)} chars). Checking...")

        if formatted != orig:
            with open(fpath, "w", encoding="utf-8") as fh:
                fh.write(formatted)
            updated_files += 1
            chap_folder = os.path.basename(os.path.dirname(os.path.dirname(fpath)))
            modified_chapters.add(chap_folder)

    print(f"\n[✓] Step 05 Formatter completed successfully!")
    print(f"    -> Total files updated: {updated_files}/{len(kb_files)}")
    print(f"    -> Chapters with structural enhancements: {len(modified_chapters)}")

    return updated_files

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Step 05 Script Structure & Poetic Prosody Formatter")
    parser.add_argument("--book_dir", default="Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia", help="Book directory path")
    args = parser.parse_args()

    format_all_chapters(args.book_dir)
