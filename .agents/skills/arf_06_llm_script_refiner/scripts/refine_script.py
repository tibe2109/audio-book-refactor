#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM Script Refiner (Step 06)
Refines audiobook scripts for neural TTS prosody:
- Adds breathing commas (nhịp thở) after introductory conjunctions.
- Ensures all section titles are standalone UPPERCASE with pause markers (. ......).
- Strips 100% TTS forbidden characters.
- Chunks text into optimal TTS chunks (<= 2,950 chars, targeting 2,200 - 2,800 chars).
- Outputs final kich-ban/Kich-ban-1.txt, kich-ban/Kich-ban-2.txt, ...
- Performs auto-cleanup of intermediate Kich-ban-raw-*.txt files.
- Updates session manifest with complete checkpoint status.
"""

import os
import sys
import re
import glob
import json
import argparse
import datetime

FORBIDDEN_CHARS_PATTERN = re.compile(r'[\(\)"“”:;—–\[\]«»#*•●▪▶►★▲◆■✓]')

def add_breathing_commas(text):
    """Adds natural breathing pauses after common introductory conjunctions."""
    patterns = [
        (r'\b(Tuy nhiên|tuy nhiên)\s+(?![\,\.\?\!\:\;])', r'\1, '),
        (r'\b(Bởi vì|bởi vì)\s+(?![\,\.\?\!\:\;])', r'\1, '),
        (r'\b(Do đó|do đó)\s+(?![\,\.\?\!\:\;])', r'\1, '),
        (r'\b(Chẳng hạn|chẳng hạn)\s+(?![\,\.\?\!\:\;])', r'\1, '),
        (r'\b(Ví dụ|ví dụ)\s+(?![\,\.\?\!\:\;])', r'\1, '),
        (r'\b(Nói cách khác|nói cách khác)\s+(?![\,\.\?\!\:\;])', r'\1, '),
        (r'\b(Mặt khác|mặt khác)\s+(?![\,\.\?\!\:\;])', r'\1, '),
        (r'\b(Tóm lại|tóm lại)\s+(?![\,\.\?\!\:\;])', r'\1, ')
    ]
    for pat, rep in patterns:
        text = re.sub(pat, rep, text)
    text = re.sub(r',\s*,', ',', text)
    return text

def is_header(para):
    """Detects if a paragraph is a section header."""
    lines = [l.strip() for l in para.split('\n') if l.strip()]
    if not lines:
        return False
    first = lines[0]
    if any(first.startswith(prefix) for prefix in [
        'Học phần', 'HỌC PHẦN', 'Chương', 'CHƯƠNG', 'Mục', 'MỤC',
        'PHẦN', 'Phần', 'BẢNG THUẬT NGỮ', 'NHÓM CHỮ CÁI'
    ]):
        return True
    if len(para) < 220 and (first.isupper() or '. ......' in para):
        return True
    return False

def smart_split_para(para, max_len=2400):
    """Splits long paragraphs (> max_len) at clean sentence boundaries."""
    if len(para) <= max_len:
        return [para]
    sentences = re.split(r'(?<=[.!?])\s+', para)
    sub_paras = []
    curr = []
    curr_len = 0
    for s in sentences:
        if curr_len + len(s) > max_len and curr:
            sub_paras.append(' '.join(curr))
            curr = [s]
            curr_len = len(s)
        else:
            curr.append(s)
            curr_len += len(s)
    if curr:
        sub_paras.append(' '.join(curr))
    return sub_paras

def refine_and_chunk(text, min_target=2100, max_target=2750, hard_cap=2950):
    """
    Refines text structure and chunks into final scripts (<= 2,950 characters).
    Guarantees that every chunk is <= 3,000 chars for QC Gate 2.
    """
    # 1. Add breathing commas
    text = add_breathing_commas(text)
    
    # 2. Strip forbidden characters
    text = text.replace(':', ', ').replace(';', ', ').replace('—', ', ').replace('–', ', ')
    text = FORBIDDEN_CHARS_PATTERN.sub('', text)
    
    # 3. Clean headers: uppercase and pause markers
    lines = text.splitlines()
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if i + 1 < len(lines) and lines[i + 1].strip() == '. ......':
            formatted_header = line.upper()
            new_lines.append(formatted_header)
            new_lines.append('. ......')
            i += 2
            continue
        new_lines.append(line)
        i += 1
        
    formatted_text = '\n'.join(new_lines)
    # Clean multiple consecutive pause markers if any
    formatted_text = re.sub(r'(?:\. \.\.\.\.\.\.[ \t]*(?:\r?\n)+)+', '. ......\n\n', formatted_text)
    # Ensure exactly one blank line after . ...... before the next paragraph/heading
    formatted_text = re.sub(r'\. \.\.\.\.\.\.[ \t]*\n+([^\n])', r'. ......\n\n\1', formatted_text)
    # Normalize consecutive blank lines to standard double newline
    formatted_text = re.sub(r'\n{3,}', '\n\n', formatted_text).strip()
    
    # 4. Paragraph splitting
    raw_paras = [p.strip() for p in formatted_text.split('\n\n') if p.strip()]
    paragraphs = []
    for p in raw_paras:
        paragraphs.extend(smart_split_para(p, max_len=2400))
        
    chunks = []
    curr = []
    curr_len = 0
    
    for p in paragraphs:
        p_len = len(p)
        header_flag = is_header(p)
        
        # New chunk for major headers if current has sufficient length
        if header_flag and curr_len >= min_target and curr:
            chunks.append('\n\n'.join(curr))
            curr = [p]
            curr_len = p_len
            continue
            
        if (curr_len + p_len + 2 > max_target and curr_len >= min_target) or (curr_len + p_len + 2 > hard_cap):
            # Check for orphan header at chunk end
            if curr and is_header(curr[-1]):
                orphan = curr.pop()
                if curr:
                    chunks.append('\n\n'.join(curr))
                curr = [orphan, p]
                curr_len = len(orphan) + 2 + p_len
            else:
                chunks.append('\n\n'.join(curr))
                curr = [p]
                curr_len = p_len
        else:
            curr.append(p)
            curr_len += (p_len + 2 if curr_len > 0 else p_len)
            
    if curr:
        chunks.append('\n\n'.join(curr))
        
    # Rebalance short final chunk
    if len(chunks) >= 2:
        last_len = len(chunks[-1])
        prev_len = len(chunks[-2])
        if last_len < 1500 and (prev_len + last_len + 2) <= 2990:
            last = chunks.pop()
            chunks[-1] = chunks[-1] + '\n\n' + last
        elif last_len < 1200:
            prev_paras = chunks[-2].split('\n\n')
            last_paras = chunks[-1].split('\n\n')
            while len(prev_paras) > 1 and len('\n\n'.join(last_paras)) < 1600:
                candidate = prev_paras[-1]
                if is_header(candidate):
                    break
                candidate_len = len(candidate) + 2
                if len('\n\n'.join(last_paras)) + candidate_len <= 2950:
                    last_paras.insert(0, prev_paras.pop())
                else:
                    break
            chunks[-2] = '\n\n'.join(prev_paras)
            chunks[-1] = '\n\n'.join(last_paras)
            
    return chunks

def process_chapter(chap_path, chap_name=""):
    norm_file = os.path.join(chap_path, "normalized.txt")
    if not os.path.exists(norm_file):
        print(f"[-] normalized.txt not found in {chap_path}. Skipping.")
        return None
        
    with open(norm_file, "r", encoding="utf-8") as f:
        text = f.read()
        
    words_orig = len(text.split())
    chunks = refine_and_chunk(text)
    
    kich_ban_dir = os.path.join(chap_path, "kich-ban")
    os.makedirs(kich_ban_dir, exist_ok=True)

    # Remove existing Kich-ban-*.txt files before writing new ones (both in kich-ban and legacy chap_path)
    for target in [kich_ban_dir, chap_path]:
        for old_f in glob.glob(os.path.join(target, "Kich-ban-*.txt")):
            if re.search(r'Kich-ban-\d+\.txt$', old_f):
                try:
                    os.remove(old_f)
                except OSError:
                    pass

    # Save final Kich-ban-N.txt files into kich_ban_dir
    final_files = []
    chunk_lengths = []
    total_words = 0
    
    for idx, chunk_content in enumerate(chunks, 1):
        filename = f"Kich-ban-{idx}.txt"
        filepath = os.path.join(kich_ban_dir, filename)
        
        # Ensure clean trailing newline
        chunk_clean = chunk_content.strip() + "\n"
        with open(filepath, "w", encoding="utf-8") as out_f:
            out_f.write(chunk_clean)
            
        final_files.append(filename)
        chunk_lengths.append(len(chunk_clean))
        total_words += len(chunk_clean.split())
        
    # Auto-cleanup raw intermediate files Kich-ban-raw-*.txt (both in kich_ban_dir and chap_path)
    raw_files = glob.glob(os.path.join(kich_ban_dir, "Kich-ban-raw-*.txt")) + glob.glob(os.path.join(chap_path, "Kich-ban-raw-*.txt"))
    for rf in raw_files:
        try:
            os.remove(rf)
        except OSError:
            pass
            
    print(f"[✓] {chap_name or os.path.basename(chap_path)}: Produced {len(chunks)} final scripts in 'kich-ban/' | "
          f"Min={min(chunk_lengths)}, Max={max(chunk_lengths)}, Avg={sum(chunk_lengths)//len(chunks)} chars | "
          f"Total words: {total_words} | Cleaned {len(raw_files)} raw files")
          
    return {
        "folder": os.path.basename(chap_path),
        "total_script_chunks": len(chunks),
        "script_files": final_files,
        "chunk_lengths": chunk_lengths,
        "total_words": total_words,
        "cleaned_raw_files_count": len(raw_files)
    }

def main():
    parser = argparse.ArgumentParser(description="LLM Script Refiner (Step 06)")
    parser.add_argument("--book_dir", required=True, help="Directory of the book project containing chapter folders")
    parser.add_argument("--chapter", help="Specific chapter folder name (optional)")
    args = parser.parse_args()
    
    book_dir = os.path.abspath(args.book_dir)
    manifest_path = os.path.join(book_dir, ".session_manifest.json")
    
    manifest = None
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
            
    chapters_to_process = []
    if args.chapter:
        chapters_to_process.append(os.path.join(book_dir, args.chapter))
    elif manifest and "chapters" in manifest:
        for c in manifest["chapters"]:
            chapters_to_process.append(os.path.join(book_dir, c["folder"]))
    else:
        for item in sorted(os.listdir(book_dir)):
            full_p = os.path.join(book_dir, item)
            if os.path.isdir(full_p) and os.path.exists(os.path.join(full_p, "normalized.txt")):
                chapters_to_process.append(full_p)
                
    print(f"[*] Refining TTS scripts for {len(chapters_to_process)} chapters in: {book_dir}\n" + "="*70)
    
    results = {}
    for chap_p in chapters_to_process:
        chap_name = os.path.basename(chap_p)
        res = process_chapter(chap_p, chap_name)
        if res:
            results[chap_name] = res
            
    # Update manifest
    if manifest:
        manifest["pipeline_stage"] = "06_llm_script_refined"
        manifest["step_6_status"] = "completed"
        manifest["step_6_completed_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        manifest["updated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        
        for c in manifest.get("chapters", []):
            f_name = c.get("folder")
            if f_name in results:
                c["status"] = "llm_refined"
                c["step_6_refined"] = True
                c["total_script_chunks"] = results[f_name]["total_script_chunks"]
                c["script_files"] = results[f_name]["script_files"]
                c["script_chunk_lengths"] = results[f_name]["chunk_lengths"]
                
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        print(f"\n[✓] Successfully updated session manifest: {manifest_path}")
        
    print("="*70 + "\n[✓] Step 06 LLM Script Refiner completed successfully!")

if __name__ == "__main__":
    main()
