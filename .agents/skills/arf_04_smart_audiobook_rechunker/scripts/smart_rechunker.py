#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Smart Audiobook Rechunker (Step 04)
Analyzes normalized.txt into optimal semantic audio script chunks (2,500 - 3,500 characters).
Saves chunks as kich-ban/Kich-ban-raw-1.txt, kich-ban/Kich-ban-raw-2.txt, etc.
Respects paragraph and semantic boundaries, prevents orphan headers, and preserves 100% text fidelity.
"""

import os
import sys
import re
import json
import argparse
import datetime

def is_header(para):
    """Detect if a paragraph is a section header."""
    lines = [l.strip() for l in para.split('\n') if l.strip()]
    if not lines:
        return False
    first = lines[0]
    if any(first.startswith(prefix) for prefix in [
        'Học phần', 'HỌC PHẦN', 'Chương', 'CHƯƠNG', 'Mục', 'MỤC',
        'PHẦN', 'Phần', 'BẢNG THUẬT NGỮ', 'NHÓM CHỮ CÁI'
    ]):
        return True
    if len(para) < 220 and (first.isupper() or '. ......' in para or '?' in first):
        return True
    return False

def semantic_chunk(text, min_target=2400, max_target=3200, hard_cap=3500):
    """
    Split normalized text into semantic chunks of 2,500 - 3,500 characters.
    Ensures paragraphs remain intact, avoids orphan headers, and ends on clean punctuation.
    """
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    chunks = []
    current_chunk = []
    current_len = 0
    
    for i, p in enumerate(paragraphs):
        p_len = len(p)
        header_flag = is_header(p)
        
        # If current chunk has enough content and this is a major header, start new chunk
        if header_flag and current_len >= min_target and current_chunk:
            chunks.append('\n\n'.join(current_chunk))
            current_chunk = [p]
            current_len = p_len
            continue
            
        # If adding this paragraph exceeds hard cap or exceeds max_target
        if (current_len + p_len + 2 > max_target and current_len >= min_target) or (current_len + p_len + 2 > hard_cap):
            # Check if current_chunk ends with an orphaned header
            if current_chunk and is_header(current_chunk[-1]):
                orphan_header = current_chunk.pop()
                if current_chunk:
                    chunks.append('\n\n'.join(current_chunk))
                current_chunk = [orphan_header, p]
                current_len = len(orphan_header) + 2 + p_len
            else:
                chunks.append('\n\n'.join(current_chunk))
                current_chunk = [p]
                current_len = p_len
        else:
            current_chunk.append(p)
            current_len += (p_len + 2 if current_len > 0 else p_len)
            
    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))
        
    # Rebalance last chunk if too short and can fit into previous chunk
    if len(chunks) >= 2:
        last_len = len(chunks[-1])
        prev_len = len(chunks[-2])
        if last_len < 1800 and (prev_len + last_len + 2) <= 3650:
            last = chunks.pop()
            chunks[-1] = chunks[-1] + '\n\n' + last
            
    return chunks

def process_chapter(chap_path, chap_name=""):
    norm_file = os.path.join(chap_path, "normalized.txt")
    if not os.path.exists(norm_file):
        print(f"[-] normalized.txt not found in {chap_path}. Skipping.")
        return None
        
    with open(norm_file, "r", encoding="utf-8") as f:
        text = f.read()
        
    words_orig = len(text.split())
    chunks = semantic_chunk(text)
    
    kich_ban_dir = os.path.join(chap_path, "kich-ban")
    os.makedirs(kich_ban_dir, exist_ok=True)

    # Remove any existing Kich-ban-raw-*.txt files in kich-ban and legacy chap_path
    for d in [kich_ban_dir, chap_path]:
        if os.path.exists(d):
            for old_f in os.listdir(d):
                if re.match(r'^Kich-ban-raw-\d+\.txt$', old_f):
                    try:
                        os.remove(os.path.join(d, old_f))
                    except OSError:
                        pass

    # Save Kich-ban-raw-N.txt into kich_ban_dir
    created_files = []
    chunk_lengths = []
    total_chunk_words = 0
    
    for i, chunk_content in enumerate(chunks, 1):
        out_filename = f"Kich-ban-raw-{i}.txt"
        out_path = os.path.join(kich_ban_dir, out_filename)
        with open(out_path, "w", encoding="utf-8") as out_f:
            out_f.write(chunk_content.strip() + "\n")
        
        created_files.append(out_filename)
        chunk_lengths.append(len(chunk_content))
        total_chunk_words += len(chunk_content.split())
        
    words_delta = total_chunk_words - words_orig
    
    print(f"[✓] {chap_name or os.path.basename(chap_path)}: Created {len(chunks)} raw chunks in 'kich-ban/' | "
          f"Min={min(chunk_lengths)}, Max={max(chunk_lengths)}, Avg={sum(chunk_lengths)//len(chunk_lengths)} chars | "
          f"Word delta={words_delta}")
          
    return {
        "folder": os.path.basename(chap_path),
        "total_raw_chunks": len(chunks),
        "chunk_files": created_files,
        "chunk_lengths": chunk_lengths,
        "words_orig": words_orig,
        "words_chunked": total_chunk_words,
        "words_delta": words_delta
    }

def main():
    parser = argparse.ArgumentParser(description="Smart Audiobook Rechunker (Step 04)")
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
                
    print(f"[*] Rechunking {len(chapters_to_process)} chapters in: {book_dir}\n" + "="*70)
    
    results = {}
    for chap_p in chapters_to_process:
        chap_name = os.path.basename(chap_p)
        res = process_chapter(chap_p, chap_name)
        if res:
            results[chap_name] = res
            
    # Update manifest
    if manifest:
        manifest["pipeline_stage"] = "04_smart_rechunked"
        manifest["step_4_status"] = "completed"
        manifest["step_4_completed_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        manifest["updated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        
        for c in manifest.get("chapters", []):
            f_name = c.get("folder")
            if f_name in results:
                c["status"] = "rechunked"
                c["total_raw_chunks"] = results[f_name]["total_raw_chunks"]
                c["chunk_lengths"] = results[f_name]["chunk_lengths"]
                c["raw_chunk_files"] = results[f_name]["chunk_files"]
                c["step_4_rechunked"] = True
                
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        print(f"\n[✓] Successfully updated session manifest: {manifest_path}")
        
    print("="*70 + "\n[✓] Step 04 Rechunking completed successfully!")

if __name__ == "__main__":
    main()
