#!/usr/bin/env python3
import os
import sys
import re
import json
import threading
import subprocess
import concurrent.futures
import time

sys.path.insert(0, os.path.abspath('.'))
import imageio_ffmpeg
from core.audio_smart_aggregator_bgm import get_audio_duration, _update_manifest_step10

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()
manifest_lock = threading.Lock()

def get_num(s):
    m = re.search(r'Hoi-(\d+)', s)
    return int(m.group(1)) if m else 999

def update_manifest_locked(chap_dir, chap_name, final_master_files):
    with manifest_lock:
        _update_manifest_step10(chap_dir, chap_name, final_master_files)

def master_single_chapter(item):
    chap_name = item['chap_name']
    full_mp3 = item['full_file']
    final_mp3 = item['final_file']
    bgm_path = item['bgm_path']
    bgm_start = item['bgm_start']
    bgm_end = item['bgm_end']
    track_name = item['track_name']
    chap_dir = item['chap_dir']
    
    t0 = time.time()
    part_duration = item['duration']
    
    bgm_filters = [
        f"atrim=start={bgm_start:.2f}:end={bgm_end:.2f}",
        "asetpts=PTS-STARTPTS",
        "volume=0.070",
        "afade=t=in:ss=0:d=3.0",
        f"afade=t=out:st={max(0.0, part_duration - 5.0):.2f}:d=5.0"
    ]
    bgm_chain = ",".join(bgm_filters)
    filter_complex = (
        f"[0:a]aformat=channel_layouts=stereo[voice];"
        f"[1:a]{bgm_chain}[bgm];"
        f"[voice][bgm]amix=inputs=2:duration=first:weights=1 1:normalize=0,"
        f"loudnorm=I=-16:TP=-1.5:LRA=6[out]"
    )
    
    cmd_mix = [
        FFMPEG_EXE, "-y",
        "-i", full_mp3,
        "-stream_loop", "-1",
        "-i", bgm_path,
        "-filter_complex", filter_complex,
        "-map", "[out]",
        "-b:a", "192k",
        "-ar", "48000",
        final_mp3
    ]
    
    try:
        subprocess.run(cmd_mix, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        if not os.path.exists(final_mp3):
            raise RuntimeError(f"Master file failed to generate: {final_mp3}")
            
        sz_mb = os.path.getsize(final_mp3) / (1024 * 1024)
        out_dur = get_audio_duration(final_mp3)
        elapsed = time.time() - t0
        
        final_master_files = [{
            "part_index": 1,
            "file_name": os.path.basename(final_mp3),
            "file_path": final_mp3,
            "duration_seconds": round(out_dur, 2),
            "duration_minutes": round(out_dur / 60, 2),
            "file_size_mb": round(sz_mb, 2),
            "bgm_track": track_name
        }]
        
        update_manifest_locked(chap_dir, chap_name, final_master_files)
        return (chap_name, True, os.path.basename(final_mp3), out_dur, sz_mb, elapsed, track_name, None)
    except Exception as e:
        elapsed = time.time() - t0
        return (chap_name, False, None, 0, 0, elapsed, track_name, str(e))

def main():
    book_dir = '/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia'
    full_dir = os.path.join(book_dir, 'Full-Tam-Quoc-Dien-Nghia')
    final_dir = os.path.join(book_dir, 'Final-Tam-Quoc-Dien-Nghia')
    os.makedirs(final_dir, exist_ok=True)
    
    bgm_06 = os.path.abspath('bgm_audio_library/06_epic_three_kingdoms_shu_theme.mp3')
    bgm_05 = os.path.abspath('bgm_audio_library/05_dan_tranh_co_cam_truyen_thong.mp3')
    
    full_files = sorted([f for f in os.listdir(full_dir) if f.startswith('Full_') and f.endswith('.mp3')], key=get_num)
    existing_final = set(os.listdir(final_dir))
    
    # Calculate baseline offsets from chapters 1-40
    offset_06 = 0.0
    offset_05 = 0.0
    for f in full_files:
        num = get_num(f)
        if num <= 40:
            dur = get_audio_duration(os.path.join(full_dir, f))
            if num % 2 == 1:
                offset_06 += dur
            else:
                offset_05 += dur
                
    # Build schedule for chapters 41 to 120
    schedule = []
    for f in full_files:
        chap_num = get_num(f)
        if chap_num < 41:
            continue
        final_name = f.replace('Full_', 'Final_Audio_')
        if final_name in existing_final:
            continue
            
        parts = f.replace('Full_', '').replace('.mp3', '').split('_')
        chap_name = parts[0]
        c_dir = os.path.join(book_dir, chap_name)
        full_mp3 = os.path.join(full_dir, f)
        final_mp3 = os.path.join(final_dir, final_name)
        dur = get_audio_duration(full_mp3)
        
        if chap_num % 2 == 1:
            bgm_path = bgm_06
            bgm_start = offset_06
            offset_06 += dur
            track_name = "06_epic_three_kingdoms_shu_theme.mp3"
        else:
            bgm_path = bgm_05
            bgm_start = offset_05
            offset_05 += dur
            track_name = "05_dan_tranh_co_cam_truyen_thong.mp3"
            
        schedule.append({
            'chap_name': chap_name,
            'chap_num': chap_num,
            'chap_dir': c_dir,
            'full_file': full_mp3,
            'final_file': final_mp3,
            'duration': dur,
            'bgm_path': bgm_path,
            'bgm_start': bgm_start,
            'bgm_end': bgm_start + dur,
            'track_name': track_name
        })
        
    print(f"=== BATCH STEP 10 MASTERING: {len(schedule)} CHAPTERS (Hồi 41 to 120) ===")
    print("Strategy: Odd chapters -> Epic Shu Theme | Even chapters -> Đàn Tranh Cổ Cầm")
    print("Continuous timeline offset shifting enabled (Zero repetition)")
    print("Parallelism: 4 workers\n")
    
    total = len(schedule)
    completed = 0
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(master_single_chapter, item): item['chap_name'] for item in schedule}
        for future in concurrent.futures.as_completed(futures):
            c_name = futures[future]
            chap_name, success, out_file, dur, sz, elapsed, track, err = future.result()
            completed += 1
            if success:
                print(f"[{completed}/{total}] [✓] {chap_name} -> {out_file} ({dur/60:.2f}m, {sz:.2f}MB, BGM: {track[:15]}..) in {elapsed:.1f}s")
            else:
                print(f"[{completed}/{total}] [✗] {chap_name} FAILED: {err} ({elapsed:.1f}s)")
                
    print("\n=== STEP 10 MASTERING COMPLETE FOR ALL CHAPTERS ===")

if __name__ == '__main__':
    main()
