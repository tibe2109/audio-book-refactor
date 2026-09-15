#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Structure Formatter (Step 05)
Ensures section titles are standalone UPPERCASE (IN HOA), formats pacing pause markers (. ......),
eliminates colons (replacing with commas), and standardizes breathing intervals across all Kich-ban-raw-*.txt chunks.
"""

import os
import sys
import re
import json
import argparse
import datetime

def format_chunk_content(text):
    """
    Format a single raw script chunk:
    - Standalone ALL-CAPS section headers.
    - Replace colon ':' with ',' in headers.
    - Proper placement of pause marker '. ......' (1.5 - 2.0s).
    - Clean paragraph spacing.
    """
    lines = text.splitlines()
    new_lines = []
    i = 0
    header_formatted_count = 0
    
    while i < len(lines):
        line = lines[i].strip()
        # Check if line is a header followed by pause marker
        if i + 1 < len(lines) and lines[i + 1].strip() == '. ......':
            header_text = line
            # Convert header to uppercase and replace colons with commas
            formatted_header = header_text.upper().replace(':', ',')
            formatted_header = re.sub(r',\s*,', ',', formatted_header).strip()
            if formatted_header != header_text:
                header_formatted_count += 1
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
    formatted_text = re.sub(r'\n{3,}', '\n\n', formatted_text).strip() + '\n'
    
    return formatted_text, header_formatted_count

def process_chapter(chap_path, chap_name=""):
    kich_ban_dir = os.path.join(chap_path, "kich-ban")
    target_dir = kich_ban_dir if (os.path.isdir(kich_ban_dir) and any(f.startswith("Kich-ban-raw-") for f in os.listdir(kich_ban_dir))) else chap_path

    raw_files = sorted(
        [f for f in os.listdir(target_dir) if f.startswith("Kich-ban-raw-") and f.endswith(".txt")],
        key=lambda x: int(re.search(r'raw-(\d+)', x).group(1)) if re.search(r'raw-(\d+)', x) else 0
    )
    
    if not raw_files:
        print(f"[-] No Kich-ban-raw-*.txt files found in {target_dir}. Skipping.")
        return None
        
    total_headers_changed = 0
    words_total_before = 0
    words_total_after = 0
    chars_total_after = 0
    
    for fname in raw_files:
        fpath = os.path.join(target_dir, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
            
        words_before = len(content.split())
        words_total_before += words_before
        
        formatted_content, h_changed = format_chunk_content(content)
        total_headers_changed += h_changed
        
        words_after = len(formatted_content.split())
        words_total_after += words_after
        chars_total_after += len(formatted_content)
        
        assert words_before == words_after, f"Word count mismatch in {fpath}: {words_before} vs {words_after}"
        
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(formatted_content)
            
    print(f"[✓] {chap_name or os.path.basename(chap_path)}: Formatted {len(raw_files)} raw chunks | "
          f"Headers adjusted: {total_headers_changed} | Total words: {words_total_after} (Delta=0)")
          
    return {
        "folder": os.path.basename(chap_path),
        "total_raw_chunks": len(raw_files),
        "headers_adjusted": total_headers_changed,
        "words": words_total_after,
        "chars": chars_total_after
    }

def main():
    parser = argparse.ArgumentParser(description="Script Structure Formatter (Step 05)")
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
            kb_sub = os.path.join(full_p, "kich-ban")
            has_raw = False
            if os.path.isdir(full_p):
                if os.path.isdir(kb_sub) and any(f.startswith("Kich-ban-raw-") for f in os.listdir(kb_sub)):
                    has_raw = True
                elif any(f.startswith("Kich-ban-raw-") for f in os.listdir(full_p)):
                    has_raw = True
            if has_raw:
                chapters_to_process.append(full_p)
                
    print(f"[*] Formatting script structure for {len(chapters_to_process)} chapters in: {book_dir}\n" + "="*70)
    
    results = {}
    for chap_p in chapters_to_process:
        chap_name = os.path.basename(chap_p)
        res = process_chapter(chap_p, chap_name)
        if res:
            results[chap_name] = res
            
    # Update manifest
    if manifest:
        manifest["pipeline_stage"] = "05_structure_formatted"
        manifest["step_5_status"] = "completed"
        manifest["step_5_completed_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        manifest["updated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        
        for c in manifest.get("chapters", []):
            f_name = c.get("folder")
            if f_name in results:
                c["status"] = "structure_formatted"
                c["step_5_formatted"] = True
                
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        print(f"\n[✓] Successfully updated session manifest: {manifest_path}")
        
    print("="*70 + "\n[✓] Step 05 Structure Formatting completed successfully!")

if __name__ == "__main__":
    main()
