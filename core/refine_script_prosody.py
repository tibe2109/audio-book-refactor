#!/usr/bin/env python3
# ==============================================================================
# Step 06: LLM Script & Prosody Refiner (ARF v2.5)
# Skill: arf_06_llm_script_refiner
# ==============================================================================
import os
import re
import sys
import glob
import json
import argparse

TRANSITIONS = [
    "tuy nhiên", "do đó", "vì vậy", "mặt khác", "hơn nữa", "bởi vậy",
    "cho nên", "thế nhưng", "ngoài ra", "đồng thời", "tóm lại", "nhìn chung",
    "nói cách khác", "chính vì thế", "nói đoạn", "lại nói", "nhắc lại"
]

def refine_text_prosody(content):
    """Refines a single script chunk: adds breathing commas, verifies sentence length, cleans formatting."""
    # Protect pause markers
    clean = content.replace(". ......", "__PAUSE_MARKER__")

    # Insert breathing commas after key transitions if missing
    for t in TRANSITIONS:
        # Match transition word preceded by word boundary and not followed by punctuation
        pattern = re.compile(r'\b(' + re.escape(t) + r')\s+(?![\,\.\:\;\!\?])', re.IGNORECASE)
        clean = pattern.sub(r'\1, ', clean)

    # Clean double commas or spaces
    clean = re.sub(r',[ \t]*,+', ',', clean)
    clean = re.sub(r'[ \t]+,', ',', clean)
    clean = re.sub(r',[ \t]*\.', '.', clean)
    clean = re.sub(r'\.[ \t]*,', '.', clean)

    # Restore pause markers
    clean = clean.replace("__PAUSE_MARKER__", ". ......")
    clean = re.sub(r'(\. \.\.\.\.\.\.\s*\n*){2,}', r'. ......\n\n', clean)
    return clean.strip() + '\n'

def process_chapter_refinement(chap_dir):
    """Processes and refines all scripts in a chapter directory."""
    kb_dir = os.path.join(chap_dir, "kich-ban")
    if not os.path.isdir(kb_dir):
        return None

    kb_files = sorted(
        glob.glob(os.path.join(kb_dir, "Kich-ban-*.txt")),
        key=lambda x: int(re.search(r'Kich-ban-(\d+)\.txt', x).group(1)) if re.search(r'Kich-ban-(\d+)\.txt', x) else 0
    )

    if not kb_files:
        return None

    # Delete any lingering raw files
    raw_files = glob.glob(os.path.join(kb_dir, "Kich-ban-raw-*.txt"))
    for rf in raw_files:
        try:
            os.remove(rf)
        except OSError:
            pass

    results = {
        "chapter": os.path.basename(chap_dir),
        "total_chunks": len(kb_files),
        "modified_chunks": 0,
        "max_sentence_words": 0,
        "max_delta_ratio": 0.0,
        "qc_passed": False
    }

    for fpath in kb_files:
        with open(fpath, "r", encoding="utf-8") as fh:
            orig = fh.read()

        w_orig = len(orig.split())
        refined = refine_text_prosody(orig)
        w_ref = len(refined.split())

        delta_ratio = abs(w_ref - w_orig) / max(w_orig, 1)
        if delta_ratio > results["max_delta_ratio"]:
            results["max_delta_ratio"] = delta_ratio

        # Check max sentence words (in prose)
        clean_p = refined.replace(". ......", " ")
        for line in clean_p.splitlines():
            line = line.strip()
            if not line:
                continue
            for sent in re.split(r'[.!?]+', line):
                sent_words = len(sent.strip().split())
                if sent_words > results["max_sentence_words"]:
                    results["max_sentence_words"] = sent_words

        if refined != orig:
            with open(fpath, "w", encoding="utf-8") as fh:
                fh.write(refined)
            results["modified_chunks"] += 1

    # Run QC check
    qc_script_path = os.path.abspath(".agent/skills/arf_07_audiobook_qc_auditor/scripts")
    if qc_script_path not in sys.path:
        sys.path.insert(0, qc_script_path)
    try:
        from qc_pipeline_v2 import audit_chapter
        passed, _, _ = audit_chapter(chap_dir, os.path.basename(chap_dir))
        results["qc_passed"] = passed
    except Exception as e:
        results["qc_error"] = str(e)

    return results

def refine_book_range(book_dir, from_chap=None, to_chap=None):
    """Processes a range of chapters in the book."""
    manifest_path = os.path.join(book_dir, ".session_manifest.json")
    chapters = []
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
            chapters = manifest.get("chapters", [])

    if not chapters:
        subdirs = sorted([d for d in os.listdir(book_dir) if os.path.isdir(os.path.join(book_dir, d)) and not d.startswith('.')])
        chapters = [{"index": idx, "folder": d} for idx, d in enumerate(subdirs)]

    processed = 0
    modified = 0
    qc_failures = []

    for i, chap in enumerate(chapters, 1):
        chap_num = chap.get("index", i - 1) + 1
        folder = chap["folder"]

        if from_chap and chap_num < from_chap:
            continue
        if to_chap and chap_num > to_chap:
            continue

        c_dir = os.path.join(book_dir, folder)
        res = process_chapter_refinement(c_dir)
        if not res:
            continue

        processed += 1
        if res["modified_chunks"] > 0:
            modified += 1

        if not res["qc_passed"]:
            qc_failures.append(folder)

        print(f"[{chap_num:03d}] {folder}: {res['modified_chunks']}/{res['total_chunks']} chunks refined | Max words/sent: {res['max_sentence_words']} | Delta: {res['max_delta_ratio']*100:.2f}% | QC: {'PASSED' if res['qc_passed'] else 'FAILED'}")

    return {
        "processed": processed,
        "modified": modified,
        "qc_failures": qc_failures
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Step 06 LLM Script & Prosody Refiner")
    parser.add_argument("--book_dir", default="Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia", help="Book directory path")
    parser.add_argument("--from_chap", type=int, default=None, help="Start chapter index")
    parser.add_argument("--to_chap", type=int, default=None, help="End chapter index")
    args = parser.parse_args()

    refine_book_range(args.book_dir, args.from_chap, args.to_chap)
