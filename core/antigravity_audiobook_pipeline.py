#!/usr/bin/env python3
# ==============================================================================
# Universal Audiobook Production Pipeline CLI Orchestrator v2.0
# Core Controller for Antigravity, Claude Code, Cursor, Codex
# ==============================================================================
import os
import sys
import re
import json
import argparse
import asyncio

from extract_pdf_structure import extract_pdf_chapters
from audiobook_script_processor import process_chapter_scripts
from seamless_dual_voice_splicer import synthesize_chapter_tts
from audio_smart_aggregator_bgm import aggregate_and_mix_bgm

def main():
    parser = argparse.ArgumentParser(description="Universal Audiobook Pipeline Orchestrator v2.0")
    parser.add_argument("--pdf", type=str, help="Path to input source PDF file")
    parser.add_argument("--book_slug", type=str, default="ProcessGroupsPracticeGuide", help="Book identifier slug")
    parser.add_argument("--book_dir", type=str, default="Kich-ban-clipchamp/ProcessGroupsPracticeGuide", help="Book working directory")
    parser.add_argument("--chapter", type=str, help="Specific chapter directory to process (e.g. 04-Initiating-Process-Group)")
    parser.add_argument("--all", action="store_true", help="Process all pending chapters")
    parser.add_argument("--bgm", type=str, default="nhac-nen.mp3", help="BGM file path or filename in bgm_audio_library")

    parser.add_argument("--from_chap", type=int, help="Start chapter index (1-based)")
    parser.add_argument("--to_chap", type=int, help="End chapter index (1-based)")
    parser.add_argument("--force", action="store_true", help="Force re-run all steps even if completed")

    args = parser.parse_args()

    # Step 01: PDF Extraction if --pdf provided
    if args.pdf:
        print(f"=========================================================")
        print(f" STEP 01: Extracting PDF Structure: {args.pdf}")
        print(f"=========================================================")
        extract_pdf_chapters(args.pdf, "Kich-ban-clipchamp", args.book_slug)

    book_dir = args.book_dir
    manifest_file = os.path.join(book_dir, ".session_manifest.json")

    if not os.path.exists(manifest_file):
        print(f"[!] Session manifest not found in {book_dir}")
        sys.exit(1)

    with open(manifest_file, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    target_chapters = []
    if args.chapter:
        target_chapters = [c for c in manifest["chapters"] if c["folder"] == args.chapter]
    elif args.from_chap is not None or args.to_chap is not None:
        start_idx = (args.from_chap - 1) if args.from_chap is not None else 0
        end_idx = args.to_chap if args.to_chap is not None else len(manifest["chapters"])
        target_chapters = manifest["chapters"][start_idx:end_idx]
    elif args.all:
        target_chapters = manifest["chapters"]
    else:
        target_chapters = manifest["chapters"]

    book_name = os.path.basename(os.path.abspath(book_dir))
    final_output_dir = os.path.join(book_dir, f"Final-{book_name}")

    for chap in target_chapters:
        chap_folder = chap["folder"]
        c_dir = os.path.join(book_dir, chap_folder)

        # Check if already completed
        if not args.chapter and not args.force and chap.get("step_10_status") == "completed":
            if os.path.isdir(final_output_dir) and any(f.startswith(f"Final_Audio_{chap_folder}") for f in os.listdir(final_output_dir)):
                print(f"[*] Skipping {chap_folder}: Already completed and mastered in Final-{book_name}.")
                continue

        print(f"\n=========================================================")
        print(f" PIPELINE RUNNER: {chap_folder} ({chap['title']})")
        print(f"=========================================================")

        # Step 07: Hard QC Gate Audit Verification
        kich_ban_dir = os.path.join(c_dir, "kich-ban")
        has_scripts = (os.path.isdir(kich_ban_dir) and any(re.match(r'^Kich-ban-\d+\.txt$', f) for f in os.listdir(kich_ban_dir))) or any(re.match(r'^Kich-ban-\d+\.txt$', f) for f in os.listdir(c_dir))

        qc_passed = False
        if has_scripts:
            try:
                qc_script_path = os.path.abspath(".agent/skills/arf_07_audiobook_qc_auditor/scripts")
                if qc_script_path not in sys.path:
                    sys.path.insert(0, qc_script_path)
                from qc_pipeline_v2 import audit_chapter
                all_passed, report_md, _ = audit_chapter(c_dir, chap_folder)
                if all_passed:
                    qc_passed = True
                    print(f"[*] [✓] Step 07 Audit: Chapter {chap_folder} has 100% 7/7 Quality Gates PASSED. Step 08 TTS is Unlocked!")
                else:
                    print(f"[!] Step 07 Audit: Chapter {chap_folder} failed QC. Attempting script processor...")
                    qc_passed = process_chapter_scripts(c_dir, chap_folder)
            except Exception as e:
                print(f"[!] QC check error: {e}. Falling back to process_chapter_scripts...")
                qc_passed = process_chapter_scripts(c_dir, chap_folder)
        else:
            print("\n[+] No script chunks found. Executing Steps 02 - 07 (Translate, Normalize, Rechunk, Format, Refine, QC Audit)...")
            qc_passed = process_chapter_scripts(c_dir, chap_folder)

        if not qc_passed:
            print(f"[!] QC Gate FAILED for {chap_folder}. Stopping Step 08 TTS.")
            continue

        # Step 08: Seamless Dual-Voice Speech Synthesis
        print("\n[+] Executing Step 08 (Seamless Dual-Voice Neural Speech Synthesis)...")
        chunks = asyncio.run(synthesize_chapter_tts(c_dir, chap_folder))

        # Step 09 & 10: Audio Aggregation & BGM Dynamic Mastering
        print("\n[+] Executing Steps 09 & 10 (Smart Aggregation & BGM Dynamic Mastering)...")
        final_files = aggregate_and_mix_bgm(c_dir, chap_folder, bgm_file=args.bgm)

        print(f"\n[✓] CHAPTER COMPLETE: {chap_folder}")
        for ff in final_files:
            f_path = ff.get("file_path", ff) if isinstance(ff, dict) else ff
            print(f"    -> Output Master File: {f_path}")

if __name__ == "__main__":
    main()
