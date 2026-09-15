#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
batch_translate.py - Step 02: Author-Style Translator Engine & Quality Audit (v2.5)
Skill: arf_02_author_style_translator

Features:
1. Quantitative Word Count Expansion Ratio Gate (R = W_trans / W_raw >= 0.85).
2. Anti-Summarization & Omission Detection (Flags truncated chapters).
3. Pre-Translation Semantic Chunking Utility for long chapters (> 1200 words).
4. Manifest Synchronization with atomic ratio metadata.
"""

import os
import sys
import re
import json
import argparse
from datetime import datetime, timezone

DEFAULT_MIN_EXPANSION_RATIO = 0.85
WARNING_MIN_EXPANSION_RATIO = 0.70
MAX_EXPANSION_RATIO = 2.00

def count_words(text: str) -> int:
    """Accurately counts words in text."""
    if not text:
        return 0
    return len(text.strip().split())

def chunk_text_by_words(text: str, max_words: int = 1200) -> list:
    """
    Splits long raw text into logical semantic parts at paragraph boundaries,
    ensuring no single part exceeds max_words. Handles both \n\n delimited
    and single-newline wrapped text.
    """
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    if len(paragraphs) <= 1:
        # Fallback for single-newline wrapped text: split where line ends with sentence terminal
        lines = text.split('\n')
        paragraphs = []
        curr = []
        for line in lines:
            curr.append(line)
            if re.search(r'[.?!][\"\'”’]?$', line.strip()) and len(line.strip()) > 0:
                paragraphs.append(' '.join(curr))
                curr = []
        if curr:
            paragraphs.append(' '.join(curr))

    chunks = []
    curr_paras = []
    curr_words = 0

    for p in paragraphs:
        p_words = count_words(p)
        if curr_words + p_words > max_words and curr_paras:
            chunks.append("\n\n".join(curr_paras))
            curr_paras = [p]
            curr_words = p_words
        else:
            curr_paras.append(p)
            curr_words += p_words

    if curr_paras:
        chunks.append("\n\n".join(curr_paras))

    return chunks

def audit_book_translations(book_dir: str, min_ratio: float = DEFAULT_MIN_EXPANSION_RATIO, sync_manifest: bool = True):
    manifest_path = os.path.join(book_dir, ".session_manifest.json")
    if not os.path.exists(manifest_path):
        print(f"[!] Error: .session_manifest.json not found in {book_dir}")
        return False, []

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    chapters = manifest.get("chapters", [])
    results = []
    all_passed = True

    print(f"\n=========================================================================================")
    print(f" STEP 02: AUTHOR-STYLE TRANSLATION & ZERO-SUMMARIZATION AUDIT (v2.5)")
    print(f" Target Book Directory: {book_dir}")
    print(f" Required Word Count Expansion Ratio: >= {min_ratio*100:.0f}% (EN -> VI Full Translation)")
    print(f"=========================================================================================")
    print(f"{'STT':<4} | {'CHƯƠNG':<24} | {'TỪ GỐC (EN)':<12} | {'TỪ DỊCH (VI)':<12} | {'TỶ LỆ (R)':<10} | {'TRẠNG THÁI'}")
    print(f"{'-'*4}-+-{'-'*24}-+-{'-'*12}-+-{'-'*12}-+-{'-'*10}-+-{'-'*20}")

    for idx, chap in enumerate(chapters, 1):
        folder = chap.get("folder", "")
        chap_dir = os.path.join(book_dir, folder)
        raw_file = os.path.join(chap_dir, "raw_original.txt")
        trans_file = os.path.join(chap_dir, "translated.txt")

        raw_words = 0
        trans_words = 0
        raw_chars = 0
        trans_chars = 0

        if os.path.exists(raw_file):
            with open(raw_file, "r", encoding="utf-8", errors="ignore") as rf:
                raw_content = rf.read()
            raw_words = count_words(raw_content)
            raw_chars = len(raw_content)
        else:
            raw_words = 0

        has_trans = os.path.exists(trans_file) and os.path.getsize(trans_file) > 50
        if has_trans:
            with open(trans_file, "r", encoding="utf-8", errors="ignore") as tf:
                trans_content = tf.read()
            trans_words = count_words(trans_content)
            trans_chars = len(trans_content)

        ratio = (trans_words / raw_words) if raw_words > 0 else 0.0

        # Status determination
        if not os.path.exists(raw_file):
            status = "❌ THIẾU RAW FILE"
            is_pass = False
        elif not has_trans:
            status = "⏳ CHƯA DỊCH (PENDING)"
            is_pass = False
        elif ratio < WARNING_MIN_EXPANSION_RATIO:
            status = "❌ CẮT XÉN NẶNG (<70%)"
            is_pass = False
        elif ratio < min_ratio:
            status = "⚠️ THIẾU Ý (70-84%)"
            is_pass = False
        elif ratio > MAX_EXPANSION_RATIO:
            status = "⚠️ PHÓNG TÁC (>160%)"
            is_pass = True
        else:
            status = "✅ ĐẠT CHUẨN 100%"
            is_pass = True

        if not is_pass:
            all_passed = False

        ratio_str = f"{ratio*100:6.1f}%" if raw_words > 0 else "N/A"
        print(f"{idx:<4} | {folder:<24} | {raw_words:<12,} | {trans_words:<12,} | {ratio_str:<10} | {status}")

        # Update chapter metadata in memory
        chap["raw_word_count"] = raw_words
        chap["raw_char_count"] = raw_chars
        chap["translated_word_count"] = trans_words
        chap["translated_char_count"] = trans_chars
        chap["word_expansion_ratio"] = round(ratio, 4)

        if is_pass:
            chap["step_2_status"] = "completed"
            chap["status"] = "translated"
        else:
            chap["step_2_status"] = "needs_healing" if has_trans else "pending"
            chap["status"] = "translation_incomplete"

        results.append({
            "chapter": folder,
            "raw_words": raw_words,
            "trans_words": trans_words,
            "ratio": ratio,
            "is_pass": is_pass,
            "status": status
        })

    print(f"{'-'*4}-+-{'-'*24}-+-{'-'*12}-+-{'-'*12}-+-{'-'*10}-+-{'-'*20}")

    tot_raw = sum(r["raw_words"] for r in results)
    tot_trans = sum(r["trans_words"] for r in results)
    tot_ratio = (tot_trans / tot_raw) if tot_raw > 0 else 0.0
    passed_count = sum(1 for r in results if r["is_pass"])
    total_count = len(results)

    print(f" TỔNG: {total_count} chương | Đạt chuẩn: {passed_count}/{total_count} | Tổng từ gốc: {tot_raw:,} | Tổng từ dịch: {tot_trans:,} | Tỷ lệ toàn sách: {tot_ratio*100:.1f}%")

    if all_passed:
        print(f"\n[🎉] XÁC NHẬN: 100% CÁC CHƯƠNG ĐẠT CHUẨN DỊCH THUẬT TOÀN VĂN (ZERO-SUMMARIZATION PASSED)!")
    else:
        print(f"\n[!] CẢNH BÁO: Phát hiện {total_count - passed_count} chương CHƯA ĐẠT CHUẨN hoặc BỊ TÓM TẮT/CẮT XÉN!")

    if sync_manifest:
        manifest["total_raw_words"] = tot_raw
        manifest["total_translated_words"] = tot_trans
        manifest["overall_word_expansion_ratio"] = round(tot_ratio, 4)
        if all_passed:
            manifest["pipeline_stage"] = "02_translated"
            manifest["step_2_status"] = "completed"
            manifest["step_2_completed_at"] = datetime.now(timezone.utc).isoformat()
        else:
            manifest["step_2_status"] = "needs_healing"

        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        print(f"[*] Đã đồng bộ trạng thái kiểm toán vào: {manifest_path}")

    return all_passed, results

def main():
    parser = argparse.ArgumentParser(description="Author-Style Translator & Anti-Summarization Auditor v2.5")
    parser.add_argument("--input_dir", required=True, help="Path to book directory containing .session_manifest.json")
    parser.add_argument("--audit", action="store_true", help="Run quantitative audit without modifying manifest")
    parser.add_argument("--min_ratio", type=float, default=DEFAULT_MIN_EXPANSION_RATIO, help="Minimum expansion ratio (default: 0.85)")
    parser.add_argument("--chunk_raw", type=str, help="Chapter folder name to split raw_original.txt into semantic chunks")
    parser.add_argument("--chunk_size", type=int, default=1200, help="Max words per chunk (default: 1200)")

    args = parser.parse_args()
    input_dir = os.path.abspath(args.input_dir)

    if args.chunk_raw:
        c_dir = os.path.join(input_dir, args.chunk_raw)
        raw_path = os.path.join(c_dir, "raw_original.txt")
        if not os.path.exists(raw_path):
            print(f"[!] Error: raw_original.txt not found in {c_dir}")
            sys.exit(1)
        with open(raw_path, "r", encoding="utf-8") as f:
            content = f.read()
        chunks = chunk_text_by_words(content, max_words=args.chunk_size)
        print(f"[*] Phân rã '{args.chunk_raw}' thành {len(chunks)} phân đoạn logic:")
        for idx, chk in enumerate(chunks, 1):
            w = count_words(chk)
            out_name = f"raw_part_{idx}.txt"
            out_path = os.path.join(c_dir, out_name)
            with open(out_path, "w", encoding="utf-8") as f_out:
                f_out.write(chk)
            print(f"    -> Phần {idx}: {w} từ, {len(chk)} ký tự => {out_name}")
        sys.exit(0)

    audit_book_translations(input_dir, min_ratio=args.min_ratio, sync_manifest=not args.audit)

if __name__ == "__main__":
    main()
