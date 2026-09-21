#!/usr/bin/env python3
import os
import sys
import threading
import concurrent.futures
import time

sys.path.insert(0, os.path.abspath('.'))

import core.audio_smart_aggregator_bgm as aggregator_mod
from core.audio_smart_aggregator_bgm import (
    dynamic_bgm_mixer,
    get_audio_duration,
    _update_manifest_step10
)

manifest_lock = threading.Lock()
orig_update_manifest = _update_manifest_step10

def locked_update_manifest(chap_dir, chap_name, final_master_files):
    with manifest_lock:
        orig_update_manifest(chap_dir, chap_name, final_master_files)

# Monkey-patch thread-safe manifest update
aggregator_mod._update_manifest_step10 = locked_update_manifest

def process_chapter(chap_info):
    c, c_dir, bgm_file = chap_info
    t0 = time.time()
    try:
        results = dynamic_bgm_mixer(c_dir, c, bgm_file=bgm_file)
        elapsed = time.time() - t0
        return (c, True, results, elapsed, None)
    except Exception as e:
        elapsed = time.time() - t0
        return (c, False, [], elapsed, str(e))

def main():
    book_dir = '/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia'
    full_dir = os.path.join(book_dir, 'Full-Tam-Quoc-Dien-Nghia')
    final_dir = os.path.join(book_dir, 'Final-Tam-Quoc-Dien-Nghia')
    os.makedirs(final_dir, exist_ok=True)

    bgm_file = '04_tam_quoc_epic_theme.mp3'

    full_files = sorted([f for f in os.listdir(full_dir) if f.startswith('Full_') and f.endswith('.mp3')])
    existing_final = set(os.listdir(final_dir))

    chapters_to_master = []
    for f in full_files:
        final_name = f.replace('Full_', 'Final_Audio_')
        if final_name not in existing_final:
            parts = f.replace('Full_', '').replace('.mp3', '').split('_')
            chap_name = parts[0]
            c_dir = os.path.join(book_dir, chap_name)
            if os.path.isdir(c_dir) and (chap_name, c_dir, bgm_file) not in chapters_to_master:
                chapters_to_master.append((chap_name, c_dir, bgm_file))

    print(f"=== BATCH STEP 10 MASTERING: {len(chapters_to_master)} CHAPTERS ===")
    print(f"BGM: {bgm_file}")
    print(f"Concurrency: 4 workers\n")

    completed = 0
    total = len(chapters_to_master)

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(process_chapter, item): item[0] for item in chapters_to_master}
        for future in concurrent.futures.as_completed(futures):
            c = futures[future]
            chap_name, success, results, elapsed, err = future.result()
            completed += 1
            if success:
                res_files = ", ".join(r['file_name'] for r in results)
                print(f"[{completed}/{total}] [✓] {chap_name} -> {res_files} ({elapsed:.1f}s)")
            else:
                print(f"[{completed}/{total}] [✗] {chap_name} FAILED: {err} ({elapsed:.1f}s)")

    print("\n=== ALL CHAPTERS PROCESSED ===")

if __name__ == '__main__':
    main()
