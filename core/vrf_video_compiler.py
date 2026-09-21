#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
VRF-03: Video Renderer & Compiler
Module dựng và kết xuất video MP4 phân cảnh từ storyboard_video và audio_chunks.
- Hiệu ứng: Hình đứng yên (still frame, 1920x1080 16:9).
- Chuyển cảnh: transition-preset-dissolve (cross-dissolve xfade, default 0.8s).
- Audio: Sử dụng trực tiếp từ audio_chunks/chunk_N.mp3 (không clone).
- Lưu trữ: [chapter_dir]/video/video_Kich-ban-N.mp4 (cùng cấp với storyboard_video).
"""

import os
import sys
import re
import glob
import shutil
import argparse
import subprocess
from typing import List, Dict, Optional, Tuple

FFMPEG_BIN = os.path.abspath("./tools/ffmpeg/ffmpeg")
if not os.path.exists(FFMPEG_BIN):
    FFMPEG_BIN = "ffmpeg"


def get_audio_duration(audio_path: str) -> float:
    """Lấy thời lượng chính xác của tệp audio (giây) qua FFmpeg."""
    cmd = [
        FFMPEG_BIN, "-i", audio_path,
        "-f", "null", "-"
    ]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
    m = re.search(r'Duration:\s*(\d+):(\d+):([\d\.]+)', res.stderr)
    if m:
        hours = int(m.group(1))
        mins = int(m.group(2))
        secs = float(m.group(3))
        return hours * 3600 + mins * 60 + secs
    return 0.0


def parse_storyboard_durations(storyboard_md: str) -> Dict[str, float]:
    """Bóc tách thời lượng từng shot từ file Kich-ban-N.md."""
    durations = {}
    if not os.path.exists(storyboard_md):
        return durations

    with open(storyboard_md, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern in table: | **Shot 01** | ... | ... | 22s | ... | `scene_01_*.jpg` | ... |
    table_pattern = re.findall(r'\|\s*\*\*Shot\s*(\d+)\*\*\s*\|[^\|]+\|[^\|]+\|\s*([\d\.]+)s\s*\|[^\|]+\|[^\|]+\|\s*`([^`]+)`', content)
    for shot_num, dur_str, filename in table_pattern:
        durations[filename.strip()] = float(dur_str)

    # Pattern in details: ### SHOT 01 ... - **Thời gian Audio:** ... (Thời lượng: `22s`) ... - **Tệp hình ảnh:** .../scene_01_*.jpg
    if not durations:
        detail_blocks = re.split(r'###\s*SHOT\s*\d+:', content)
        for block in detail_blocks[1:]:
            m_dur = re.search(r'Thời lượng:\s*`?([\d\.]+)s`?', block)
            m_file = re.search(r'scene_\d+_[^\s\)\`]+', block)
            if m_dur and m_file:
                durations[os.path.basename(m_file.group(0))] = float(m_dur.group(1))

    return durations


def compile_script_video(chapter_dir: str, script_name: str,
                         transition: str = "dissolve",
                         transition_dur: float = 0.8,
                         fps: int = 25,
                         crf: int = 20) -> Optional[str]:
    """
    Dựng video MP4 phân cảnh cho 1 kịch bản cụ thể.
    """
    chapter_dir = os.path.abspath(chapter_dir)
    print(f"\n==================================================")
    print(f"🎬 [VRF-03] BẮT ĐẦU DỰNG VIDEO: {script_name}")
    print(f"📂 Thư mục chương: {chapter_dir}")
    print(f"==================================================")

    # 1. Trích xuất chỉ số kịch bản (ví dụ Kich-ban-1 -> 1)
    m_num = re.search(r'(\d+)', script_name)
    if not m_num:
        print(f"❌ Không xác định được số thứ tự kịch bản từ '{script_name}'")
        return None
    script_idx = int(m_num.group(1))

    # 2. Định vị file audio gốc
    audio_path = os.path.join(chapter_dir, "audio_chunks", f"chunk_{script_idx}.mp3")
    if not os.path.exists(audio_path):
        print(f"❌ Không tìm thấy tệp audio gốc tại: {audio_path}")
        return None
    audio_dur = get_audio_duration(audio_path)
    print(f"🎵 Audio gốc: {audio_path} ({audio_dur:.2f} giây)")

    # 3. Định vị thư mục ảnh & kịch bản storyboard
    script_slug = script_name.lower().replace("_", "-")
    images_dir = os.path.join(chapter_dir, "storyboard_video", script_slug, "images")
    if not os.path.exists(images_dir):
        # Fallback to direct script_name
        images_dir = os.path.join(chapter_dir, "storyboard_video", script_name, "images")
    
    if not os.path.exists(images_dir):
        print(f"❌ Không tìm thấy thư mục hình ảnh tại: {images_dir}")
        return None

    # Tìm tất cả ảnh scene_*.jpg / png
    image_files = sorted([
        os.path.join(images_dir, f) for f in os.listdir(images_dir)
        if f.startswith("scene_") and f.lower().endswith((".jpg", ".jpeg", ".png"))
    ])

    if not image_files:
        print(f"❌ Không có hình ảnh nào trong thư mục: {images_dir}")
        return None

    print(f"🖼️ Tổng số phân cảnh hình ảnh tìm thấy: {len(image_files)} ảnh")

    # 4. Bóc tách thời lượng từng shot từ storyboard Markdown
    storyboard_md = os.path.join(chapter_dir, "storyboard_video", f"{script_name}.md")
    if not os.path.exists(storyboard_md):
        storyboard_md = os.path.join(chapter_dir, "storyboard_video", f"Kich-ban-{script_idx}.md")

    parsed_durations = parse_storyboard_durations(storyboard_md)
    
    # Tính thời lượng từng shot khớp với tổng audio
    shots_info = []
    total_parsed_dur = 0.0
    for img_p in image_files:
        basename = os.path.basename(img_p)
        # Search exact match or prefix match (e.g. scene_01)
        dur = parsed_durations.get(basename, 0.0)
        if dur == 0.0:
            prefix = basename.split(".")[0]
            for k, v in parsed_durations.items():
                if k.startswith(prefix[:8]):
                    dur = v
                    break
        shots_info.append({"path": img_p, "dur": dur})
        total_parsed_dur += dur

    # Nếu kịch bản chưa có timing hoặc lệch với audio, cân bằng tỉ lệ theo tổng audio_dur
    if total_parsed_dur <= 0 or abs(total_parsed_dur - audio_dur) > 2.0:
        if total_parsed_dur > 0:
            ratio = audio_dur / total_parsed_dur
            print(f"⚖️ Điều chỉnh tỉ lệ thời lượng kịch bản ({total_parsed_dur:.1f}s -> {audio_dur:.1f}s, ratio={ratio:.3f})")
            for s in shots_info:
                s["dur"] = round(s["dur"] * ratio, 2)
        else:
            even_dur = round(audio_dur / len(shots_info), 2)
            print(f"⚖️ Phân bổ đều thời lượng: {even_dur}s/ảnh")
            for s in shots_info:
                s["dur"] = even_dur

    # Đảm bảo tổng chính xác bằng audio_dur
    sum_dur = sum(s["dur"] for s in shots_info)
    shots_info[-1]["dur"] = round(shots_info[-1]["dur"] + (audio_dur - sum_dur), 2)

    for idx, s in enumerate(shots_info):
        print(f"   Shot {idx+1:02d}: {os.path.basename(s['path'])} -> {s['dur']}s")

    # 5. Khởi tạo thư mục video đích cùng cấp với storyboard_video
    video_out_dir = os.path.join(chapter_dir, "video")
    os.makedirs(video_out_dir, exist_ok=True)
    out_video_path = os.path.join(video_out_dir, f"video_{script_name}.mp4")

    # 6. Render từng still clip tĩnh
    scratch_dir = os.path.join(chapter_dir, "scratch", f"clips_{script_slug}")
    os.makedirs(scratch_dir, exist_ok=True)

    clip_paths = []
    num_shots = len(shots_info)

    print(f"\n🎨 Bắt đầu kết xuất {num_shots} phân cảnh tĩnh (Still Frame 1080p)...")
    for idx, shot in enumerate(shots_info):
        clip_name = f"clip_{idx+1:02d}.mp4"
        clip_p = os.path.join(scratch_dir, clip_name)
        clip_paths.append(clip_p)

        # Shot i kéo dài thêm transition_dur (trừ shot cuối) để hòa tan xfade
        render_dur = shot["dur"] + (transition_dur if idx < num_shots - 1 else 0.0)
        frames = int(round(render_dur * fps))

        vf_filter = "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1"

        cmd_clip = [
            FFMPEG_BIN, "-y",
            "-loop", "1",
            "-i", shot["path"],
            "-t", str(render_dur),
            "-vf", vf_filter,
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", str(crf),
            "-pix_fmt", "yuv420p",
            "-r", str(fps),
            clip_p
        ]
        res = subprocess.run(cmd_clip, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            print(f"❌ Lỗi render clip {clip_name}: {res.stderr[-300:]}")
            return None

    print("✅ Đã kết xuất xong toàn bộ phân cảnh tĩnh!")

    # 7. Ghép nối với xfade transition-preset-dissolve
    print(f"\n✨ Đang áp dụng hiệu ứng chuyển cảnh '{transition}' (độ dài {transition_dur}s)...")
    
    # Xây dựng filter_complex cho chuỗi xfade
    filter_complex = []
    input_args = []
    for idx, cp in enumerate(clip_paths):
        input_args.extend(["-i", cp])

    current_out = "v0"
    filter_complex.append(f"[0:v]copy[{current_out}]")
    
    cumulative_offset = 0.0
    for idx in range(1, num_shots):
        prev_shot_dur = shots_info[idx-1]["dur"]
        cumulative_offset += prev_shot_dur
        xfade_offset = round(cumulative_offset - transition_dur, 3)
        next_out = f"v{idx}"
        filter_complex.append(
            f"[{current_out}][{idx}:v]xfade=transition={transition}:duration={transition_dur}:offset={xfade_offset}[{next_out}]"
        )
        current_out = next_out

    final_v_label = current_out
    filter_str = ";".join(filter_complex)

    # 8. Mux trực tiếp với tệp audio gốc (không clone)
    print(f"🔊 Mux trực tiếp với âm thanh gốc: {os.path.basename(audio_path)}...")
    cmd_final = [
        FFMPEG_BIN, "-y",
        *input_args,
        "-i", audio_path,
        "-filter_complex", filter_str,
        "-map", f"[{final_v_label}]",
        "-map", f"{num_shots}:a",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", str(crf),
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        out_video_path
    ]

    res = subprocess.run(cmd_final, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print(f"❌ Lỗi ghép xfade video: {res.stderr[-400:]}")
        return None

    # Dọn dẹp thư mục nháp scratch
    shutil.rmtree(scratch_dir, ignore_errors=True)

    # 9. Kiểm toán chất lượng Video Quality Gate (VQG-3)
    if os.path.exists(out_video_path):
        v_size_mb = os.path.getsize(out_video_path) / (1024 * 1024)
        final_dur = get_audio_duration(out_video_path)
        print(f"\n==================================================")
        print(f"🎉 [VRF-03] KẾT XUẤT VIDEO THÀNH CÔNG!")
        print(f"📁 Tệp Video: {out_video_path}")
        print(f"📊 Dung lượng: {v_size_mb:.2f} MB")
        print(f"⏱️ Thời lượng: {final_dur:.2f}s (Audio gốc: {audio_dur:.2f}s, Lệch: {abs(final_dur - audio_dur):.2f}s)")
        print(f"📺 Độ phân giải: 1920x1080 Full HD (16:9 Still Frame + Dissolve)")
        print(f"==================================================")
        return out_video_path

    return None


def process_chapter(chapter_dir: str, transition: str = "dissolve") -> List[str]:
    """Xử lý toàn bộ kịch bản có trong 1 chương."""
    chapter_dir = os.path.abspath(chapter_dir)
    print(f"\n>>> QUÉT TOÀN BỘ KỊCH BẢN TRONG CHƯƠNG: {chapter_dir}")
    
    # Tìm tất cả storyboard_video/Kich-ban-*.md
    storyboard_dir = os.path.join(chapter_dir, "storyboard_video")
    if not os.path.exists(storyboard_dir):
        print(f"❌ Không tìm thấy thư mục storyboard_video tại {chapter_dir}")
        return []

    md_files = sorted(glob.glob(os.path.join(storyboard_dir, "Kich-ban-*.md")))
    if not md_files:
        # Check lowercase
        md_files = sorted(glob.glob(os.path.join(storyboard_dir, "kich-ban-*.md")))

    print(f"Tìm thấy {len(md_files)} tệp kịch bản storyboard.")
    results = []
    for md in md_files:
        base = os.path.splitext(os.path.basename(md))[0]
        # Standardize name Kich-ban-X
        script_name = base.replace("kich-ban", "Kich-ban")
        v_path = compile_script_video(chapter_dir, script_name, transition=transition)
        if v_path:
            results.append(v_path)

    return results


def main():
    parser = argparse.ArgumentParser(description="VRF-03: Storyboard Video Renderer & Compiler")
    parser.add_argument("--chapter", type=str, help="Đường dẫn đến thư mục chương (ví dụ: Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/01-Hoi-01)")
    parser.add_argument("--script", type=str, default=None, help="Tên kịch bản cần dựng (ví dụ: Kich-ban-1)")
    parser.add_argument("--all-scripts", action="store_true", help="Dựng video cho toàn bộ kịch bản trong chương")
    parser.add_argument("--book_dir", type=str, default=None, help="Đường dẫn đến thư mục sách để quét toàn bộ chương")
    parser.add_argument("--all", action="store_true", help="Dựng video cho toàn bộ tác phẩm")
    parser.add_argument("--transition", type=str, default="dissolve", help="Hiệu ứng chuyển cảnh (mặc định: dissolve)")
    parser.add_argument("--transition-dur", type=float, default=0.8, help="Thời lượng chuyển cảnh dissolve (giây, mặc định: 0.8)")
    parser.add_argument("--fps", type=int, default=25, help="Tốc độ khung hình (fps, mặc định: 25)")
    parser.add_argument("--crf", type=int, default=20, help="CRF nén video (mặc định: 20)")

    args = parser.parse_args()

    if args.all and args.book_dir:
        book_dir = os.path.abspath(args.book_dir)
        print(f"\n==================================================")
        print(f"📚 [VRF-03] KHỞI CHẠY TIẾN TRÌNH TOÀN BỘ TÁC PHẨM: {book_dir}")
        print(f"==================================================")
        chap_dirs = sorted([
            os.path.join(book_dir, d) for d in os.listdir(book_dir)
            if os.path.isdir(os.path.join(book_dir, d)) and re.match(r'^\d+', d)
        ])
        total_videos = []
        for cdir in chap_dirs:
            vids = process_chapter(cdir, transition=args.transition)
            total_videos.extend(vids)
        print(f"\n✅ ĐÃ HOÀN TẤT TOÀN TÁC PHẨM: Tổng cộng {len(total_videos)} video thành phẩm.")

    elif args.chapter:
        if args.all_scripts or args.script is None:
            process_chapter(args.chapter, transition=args.transition)
        else:
            compile_script_video(args.chapter, args.script, transition=args.transition,
                                 transition_dur=args.transition_dur, fps=args.fps, crf=args.crf)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
