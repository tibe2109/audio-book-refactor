#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ABV-02: Audiobook Video Compiler & Batch Renderer
Tự động quét thư viện Final Audio (hoặc nhận diện từ thư mục tác phẩm),
quản lý tiến trình công việc bằng Manifest (.abv_manifest.json) hỗ trợ Atomic Resume,
và kết xuất Video MP4 chuẩn 1080p cho từng chương kết hợp bộ ảnh nền điện ảnh (Step 1).
"""

import os
import sys
import re
import json
import time
import shutil
import argparse
import datetime
import subprocess
from typing import List, Dict, Tuple, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed


def find_ffmpeg() -> str:
    """Xác định đường dẫn nhị phân FFmpeg khả dụng nhất."""
    local_tool = os.path.abspath("./tools/ffmpeg/ffmpeg")
    if os.path.exists(local_tool) and os.access(local_tool, os.X_OK):
        return local_tool

    # Kiểm tra trong venv imageio_ffmpeg
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        pass

    # Kiểm tra trong PATH hệ thống
    sys_bin = shutil.which("ffmpeg")
    if sys_bin:
        return sys_bin

    return "ffmpeg"


def get_media_duration(file_path: str, ffmpeg_bin: str) -> float:
    """Lấy thời lượng chính xác của tệp media (audio/video) qua FFmpeg/FFprobe (giây)."""
    if not os.path.exists(file_path):
        return 0.0

    # Ưu tiên ffprobe nếu có
    ffprobe_bin = ffmpeg_bin.replace("ffmpeg", "ffprobe")
    if os.path.exists(ffprobe_bin) or shutil.which("ffprobe"):
        bin_to_use = ffprobe_bin if os.path.exists(ffprobe_bin) else "ffprobe"
        try:
            cmd = [bin_to_use, "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", file_path]
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
            val = float(res.stdout.strip())
            if val > 0:
                return val
        except Exception:
            pass

    # Fallback FFmpeg đọc metadata header (chỉ lấy thông tin từ stderr không cần decode)
    cmd = [ffmpeg_bin, "-i", file_path]
    try:
        res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL, text=True)
        m = re.search(r'Duration:\s*(\d+):(\d+):([\d\.]+)', res.stderr)
        if m:
            hours = int(m.group(1))
            mins = int(m.group(2))
            secs = float(m.group(3))
            return hours * 3600 + mins * 60 + secs
    except Exception:
        pass
    return 0.0


def resolve_paths(input_path: str) -> Tuple[str, str, str]:
    """
    Tự động phân giải đường dẫn đầu vào:
    Hỗ trợ cả trường hợp người dùng truyền đường dẫn folder Final, hoặc đường dẫn source của tác phẩm.
    Trả về: (book_dir, final_dir, book_name)
    """
    abs_path = os.path.abspath(input_path)
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"Đường dẫn không tồn tại: {input_path}")

    base_name = os.path.basename(abs_path)

    # 1. Người dùng truyền trực tiếp thư mục Final-[Tên-Sách]
    if base_name.startswith("Final-") and os.path.isdir(abs_path):
        final_dir = abs_path
        book_dir = os.path.dirname(abs_path)
        book_name = base_name.replace("Final-", "")
        return book_dir, final_dir, book_name

    # 2. Người dùng truyền thư mục gốc của tác phẩm (ví dụ: .../Tam-Quoc-Dien-Nghia)
    book_dir = abs_path
    book_name = base_name

    # Quét tìm thư mục Final-* bên trong
    final_candidates = [
        d for d in os.listdir(book_dir)
        if d.startswith("Final-") and os.path.isdir(os.path.join(book_dir, d))
    ]

    if final_candidates:
        final_dir = os.path.join(book_dir, final_candidates[0])
    else:
        final_dir = os.path.join(book_dir, f"Final-{book_name}")
        os.makedirs(final_dir, exist_ok=True)

    return book_dir, final_dir, book_name


def extract_chapter_sort_key(filename: str) -> Tuple[int, int, str]:
    """Trích xuất key sắp xếp tự nhiên theo số thứ tự Hồi/Chương và Part."""
    m_hoi = re.search(r'(\d+)-[hH][oO][iI]-(\d+)', filename)
    if m_hoi:
        chap_num = int(m_hoi.group(1))
    else:
        m_num = re.search(r'(\d+)', filename)
        chap_num = int(m_num.group(1)) if m_num else 9999

    m_part = re.search(r'[pP]art(\d+)', filename)
    part_num = int(m_part.group(1)) if m_part else 1

    return (chap_num, part_num, filename)


def get_available_backgrounds(final_dir: str, book_dir: str) -> List[str]:
    """Tìm nạp danh sách ảnh nền từ backgrounds/ hoặc tự động tạo nếu thiếu."""
    bg_dir = os.path.join(final_dir, "backgrounds")

    if not os.path.isdir(bg_dir) or not [f for f in os.listdir(bg_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]:
        print(f"[*] Chưa phát hiện thư viện ảnh nền tại {bg_dir}. Tự động kích hoạt ABV-01...")
        try:
            from core.abv_visual_prompter import generate_thematic_visual_assets
            generate_thematic_visual_assets(final_dir)
        except Exception as e:
            print(f"[!] Lỗi khi tự động chạy ABV-01: {e}")

    if os.path.isdir(bg_dir):
        images = sorted([
            os.path.join(bg_dir, f) for f in os.listdir(bg_dir)
            if f.lower().endswith(('.jpg', '.jpeg', '.png'))
        ])
        if images:
            return images

    return []


def load_manifest(manifest_path: str) -> Dict:
    """Tải file quản lý tiến trình .abv_manifest.json."""
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def save_manifest_atomic(manifest_path: str, data: Dict):
    """Lưu file manifest nguyên tử (Atomic Write) tránh hỏng dữ liệu khi ngắt giữa chừng."""
    tmp_path = manifest_path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp_path, manifest_path)


def is_video_valid(video_path: str, expected_duration: float, ffmpeg_bin: str) -> bool:
    """Kiểm tra video đã dựng có toàn vẹn không (tồn tại, size > 1MB, duration khớp audio)."""
    if not os.path.exists(video_path):
        return False
    if os.path.getsize(video_path) < 1024 * 1024:  # < 1MB là video hỏng/rỗng
        return False
    if expected_duration > 0:
        actual_dur = get_media_duration(video_path, ffmpeg_bin)
        # Chênh lệch không quá 5.0 giây so với audio gốc
        if abs(actual_dur - expected_duration) > 5.0:
            return False
    return True


def render_single_audiobook_video(
    audio_path: str,
    final_dir: str,
    backgrounds: List[str],
    ffmpeg_bin: str,
    manifest: Dict,
    manifest_path: str,
    force: bool = False,
    output_dir: Optional[str] = None
) -> Dict:
    """
    Dựng video MP4 chuẩn Full HD 1080p cho 1 tệp Final Audio cụ thể.
    """
    audio_filename = os.path.basename(audio_path)
    video_filename = audio_filename.replace("Final_Audio_", "Final_Video_").replace(".mp3", ".mp4")
    if not video_filename.endswith(".mp4"):
        video_filename = os.path.splitext(audio_filename)[0] + ".mp4"

    save_dir = output_dir if output_dir else final_dir
    os.makedirs(save_dir, exist_ok=True)
    video_path = os.path.join(save_dir, video_filename)
    audio_dur = get_media_duration(audio_path, ffmpeg_bin)

    # Khởi tạo hoặc cập nhật mục manifest cho file này
    entry = manifest.get("videos", {}).get(audio_filename, {
        "audio_file": audio_filename,
        "video_file": video_filename,
        "status": "pending",
        "audio_duration": audio_dur,
        "rendered_at": None,
        "file_size": 0
    })

    # Kiểm tra Atomic Resume: Nếu đã hoàn thành và hợp lệ -> SKIP
    if not force and entry.get("status") == "completed" and is_video_valid(video_path, audio_dur, ffmpeg_bin):
        print(f"    [SKIP] Đã hoàn thành trước đó: {video_filename} ({audio_dur:.1f}s, {os.path.getsize(video_path):,} bytes)")
        return {"status": "skipped", "file": video_filename, "duration": audio_dur}

    print(f"\n▶ [RENDER] Đang dựng video: {video_filename} (Thời lượng: {audio_dur:.1f}s)...")
    start_time = time.time()

    num_bgs = len(backgrounds)
    if num_bgs == 0:
        raise RuntimeError("Không tìm thấy ảnh nền nào trong backgrounds/ để dựng video!")

    concat_txt_path = None
    if num_bgs == 1:
        # Tối ưu hóa cực đại cho 1 ảnh nền tĩnh: -loop 1 và -tune stillimage
        cmd = [
            ffmpeg_bin, "-y",
            "-loop", "1",
            "-i", os.path.abspath(backgrounds[0]),
            "-i", audio_path,
            "-t", f"{audio_dur:.3f}",
            "-c:v", "libx264",
            "-tune", "stillimage",
            "-preset", "veryfast",
            "-crf", "20",
            "-pix_fmt", "yuv420p",
            "-r", "25",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            "-movflags", "+faststart",
            video_path
        ]
    else:
        dur_per_bg = audio_dur / float(num_bgs)
        concat_txt_path = os.path.join(save_dir, f".concat_{os.path.splitext(audio_filename)[0]}.txt")
        with open(concat_txt_path, "w", encoding="utf-8") as cf:
            cf.write("ffconcat version 1.0\n")
            for bg in backgrounds:
                cf.write(f"file '{os.path.abspath(bg)}'\n")
                cf.write(f"duration {dur_per_bg:.3f}\n")
            cf.write(f"file '{os.path.abspath(backgrounds[-1])}'\n")

        cmd = [
            ffmpeg_bin, "-y",
            "-f", "concat", "-safe", "0", "-i", concat_txt_path,
            "-i", audio_path,
            "-t", f"{audio_dur:.3f}",
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "20",
            "-pix_fmt", "yuv420p",
            "-r", "25",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            "-movflags", "+faststart",
            video_path
        ]

    try:
        proc = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
        if proc.returncode != 0:
            print(f"❌ Lỗi FFmpeg khi dựng {video_filename}:\n{proc.stderr[-500:]}")
            entry["status"] = "failed"
            entry["error"] = proc.stderr[-200:]
            manifest.setdefault("videos", {})[audio_filename] = entry
            save_manifest_atomic(manifest_path, manifest)
            return {"status": "failed", "file": video_filename, "error": proc.stderr[-200:]}

        # Dọn dẹp tệp concat tạm
        if concat_txt_path and os.path.exists(concat_txt_path):
            os.remove(concat_txt_path)

        elapsed = time.time() - start_time
        fsize = os.path.getsize(video_path) if os.path.exists(video_path) else 0

        # Cập nhật kết quả vào Manifest
        entry["status"] = "completed"
        entry["rendered_at"] = datetime.datetime.now().isoformat()
        entry["video_duration"] = get_media_duration(video_path, ffmpeg_bin)
        entry["file_size"] = fsize
        entry["render_time_sec"] = round(elapsed, 1)

        manifest.setdefault("videos", {})[audio_filename] = entry
        manifest["completed_videos"] = sum(1 for v in manifest["videos"].values() if v.get("status") == "completed")
        manifest["failed_videos"] = sum(1 for v in manifest["videos"].values() if v.get("status") == "failed")
        manifest["updated_at"] = datetime.datetime.now().isoformat()
        save_manifest_atomic(manifest_path, manifest)

        print(f"    [✓] Hoàn thành: {video_filename} ({fsize:,} bytes | Dựng trong {elapsed:.1f}s)")
        return {"status": "completed", "file": video_filename, "duration": audio_dur, "size": fsize}

    except Exception as e:
        print(f"❌ Ngoại lệ khi dựng {video_filename}: {e}")
        entry["status"] = "failed"
        entry["error"] = str(e)
        manifest.setdefault("videos", {})[audio_filename] = entry
        save_manifest_atomic(manifest_path, manifest)
        return {"status": "failed", "file": video_filename, "error": str(e)}


def compile_audiobook_videos(
    input_path: str,
    specific_file: Optional[str] = None,
    batch_start: Optional[int] = None,
    batch_end: Optional[int] = None,
    parallel: int = 1,
    force: bool = False,
    output_dir: Optional[str] = None,
    background_path: Optional[str] = None
) -> Dict:
    """
    Hàm điều phối dựng Video Sách Nói:
    - Quét toàn bộ hoặc lọc theo batch.
    - Quản lý Atomic Resume qua .abv_manifest.json.
    - Xuất video trực tiếp vào thư mục Final hoặc thư mục chỉ định (output_dir).
    """
    book_dir, final_dir, book_name = resolve_paths(input_path)
    ffmpeg_bin = find_ffmpeg()

    dest_dir = os.path.abspath(output_dir) if output_dir else os.path.join(final_dir, "Videos")
    os.makedirs(dest_dir, exist_ok=True)

    print("=" * 80)
    print(f"🎬 [ABV-02] AUDIOBOOK VIDEO COMPILER & BATCH RENDERER")
    print(f"📖 Tác phẩm: {book_name}")
    print(f"📂 Thư mục Final: {final_dir}")
    print(f"💾 Thư mục lưu Video: {dest_dir}")
    print(f"⚙️ FFmpeg Binary: {ffmpeg_bin}")
    print("=" * 80)

    # 1. Tìm nạp toàn bộ file Final_Audio_*.mp3
    all_audio_files = [
        f for f in os.listdir(final_dir)
        if f.startswith("Final_Audio_") and f.endswith(".mp3")
    ]
    all_audio_files.sort(key=extract_chapter_sort_key)

    if not all_audio_files:
        # Thử tìm các file .mp3 thông thường trong final_dir
        all_audio_files = [f for f in os.listdir(final_dir) if f.endswith(".mp3")]
        all_audio_files.sort(key=extract_chapter_sort_key)

    if not all_audio_files:
        print(f"❌ Không tìm thấy tệp audio nào trong thư mục Final: {final_dir}")
        return {"status": "error", "message": "No audio files found"}

    print(f"[*] Tìm thấy tổng cộng {len(all_audio_files)} tệp audio sách nói.")

    # 2. Tìm nạp danh sách ảnh nền
    if background_path and os.path.exists(background_path):
        backgrounds = [os.path.abspath(background_path)]
        print(f"[*] Sử dụng ảnh nền đơn định danh: {backgrounds[0]}")
    else:
        backgrounds = get_available_backgrounds(final_dir, book_dir)
        print(f"[*] Thư viện ảnh nền sử dụng: {len(backgrounds)} ảnh tại backgrounds/")

    # 3. Quản lý Manifest
    manifest_path = os.path.join(dest_dir, ".abv_manifest.json")
    if not os.path.exists(manifest_path) and os.path.exists(os.path.join(final_dir, ".abv_manifest.json")):
        manifest_path = os.path.join(final_dir, ".abv_manifest.json")

    manifest = load_manifest(manifest_path)
    if not manifest:
        manifest = {
            "book_name": book_name,
            "book_dir": book_dir,
            "final_dir": final_dir,
            "output_dir": dest_dir,
            "created_at": datetime.datetime.now().isoformat(),
            "updated_at": datetime.datetime.now().isoformat(),
            "total_audio_files": len(all_audio_files),
            "completed_videos": 0,
            "failed_videos": 0,
            "videos": {}
        }
        save_manifest_atomic(manifest_path, manifest)

    # 4. Lọc danh sách file cần xử lý theo tham số CLI
    target_files = list(all_audio_files)

    if specific_file:
        target_files = [f for f in target_files if f == specific_file or os.path.basename(specific_file) == f]
        print(f"[*] Chế độ xử lý đơn lẻ: {target_files}")
    else:
        if batch_start is not None or batch_end is not None:
            start_idx = (batch_start - 1) if (batch_start and batch_start > 0) else 0
            end_idx = batch_end if batch_end else len(target_files)
            target_files = target_files[start_idx:end_idx]
            print(f"[*] Chế độ xử lý theo Batch: từ file {start_idx + 1} đến {end_idx} (Tổng {len(target_files)} files)")

    # 5. Thực thi dựng video (Tuần tự hoặc Đa luồng song song)
    completed_count = 0
    skipped_count = 0
    failed_count = 0

    if parallel > 1 and len(target_files) > 1:
        print(f"[*] Khởi chạy song song với {parallel} workers...")
        with ThreadPoolExecutor(max_workers=parallel) as executor:
            futures = {
                executor.submit(
                    render_single_audiobook_video,
                    os.path.join(final_dir, f),
                    final_dir,
                    backgrounds,
                    ffmpeg_bin,
                    manifest,
                    manifest_path,
                    force,
                    dest_dir
                ): f for f in target_files
            }
            for fut in as_completed(futures):
                res = fut.result()
                if res.get("status") == "completed":
                    completed_count += 1
                elif res.get("status") == "skipped":
                    skipped_count += 1
                else:
                    failed_count += 1
    else:
        for idx, f in enumerate(target_files, 1):
            print(f"\n--- Tiến độ: [{idx}/{len(target_files)}] ---")
            audio_path = os.path.join(final_dir, f)
            res = render_single_audiobook_video(
                audio_path,
                final_dir,
                backgrounds,
                ffmpeg_bin,
                manifest,
                manifest_path,
                force,
                dest_dir
            )
            if res.get("status") == "completed":
                completed_count += 1
            elif res.get("status") == "skipped":
                skipped_count += 1
            else:
                failed_count += 1

    # 6. Xuất bản báo cáo Master Video Report Markdown
    master_report_path = os.path.join(dest_dir, "Master_Video_Report.md")
    report_lines = [
        f"# BÁO CÁO KẾT XUẤT VIDEO SÁCH NÓI (MASTER VIDEO REPORT)",
        f"## Tác phẩm: {book_name.replace('-', ' ')}",
        f"**Tổng số file Audio:** {len(all_audio_files)}",
        f"**Đã hoàn thành Video:** {manifest.get('completed_videos', completed_count + skipped_count)} / {len(all_audio_files)}",
        f"**Thư mục lưu trữ Video:** `{dest_dir}`",
        f"**Thời điểm cập nhật:** `{datetime.datetime.now().isoformat()}`\n",
        "| STT | Tệp Audio Nguồn | Tệp Video Thành Phẩm | Thời Lượng | Dung Lượng | Trạng Thái |",
        "| :---: | :--- | :--- | :---: | :---: | :---: |"
    ]

    for idx, f in enumerate(all_audio_files, 1):
        v_info = manifest.get("videos", {}).get(f, {})
        v_name = v_info.get("video_file", f.replace("Final_Audio_", "Final_Video_").replace(".mp3", ".mp4"))
        v_status = v_info.get("status", "pending")
        v_dur = f"{v_info.get('audio_duration', 0.0):.1f}s"
        v_size = f"{v_info.get('file_size', 0) / (1024 * 1024):.1f} MB" if v_info.get('file_size') else "0 MB"

        status_tag = "✅ HOÀN THÀNH" if v_status == "completed" else ("❌ LỖI" if v_status == "failed" else "⏳ CHƯA DỰNG")
        report_lines.append(f"| {idx:03d} | `{f}` | [`{v_name}`](file://{os.path.join(dest_dir, v_name)}) | {v_dur} | {v_size} | {status_tag} |")

    report_lines.append("\n---\n*Kết xuất tự động bởi ABV-02: Audiobook Video Compiler*")
    with open(master_report_path, "w", encoding="utf-8") as mrf:
        mrf.write("\n".join(report_lines))

    print("\n" + "=" * 80)
    print(f"[✓] TỔNG KẾT BƯỚC ABV-02:")
    print(f"    - Mới hoàn thành: {completed_count} video")
    print(f"    - Bỏ qua (đã có): {skipped_count} video")
    print(f"    - Thất bại: {failed_count} video")
    print(f"    - Manifest: {manifest_path}")
    print(f"    - Master Report: {master_report_path}")
    print("=" * 80)

    return {
        "status": "success",
        "total": len(target_files),
        "completed": completed_count,
        "skipped": skipped_count,
        "failed": failed_count,
        "manifest_path": manifest_path,
        "report_path": master_report_path
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ABV-02: Audiobook Video Compiler")
    parser.add_argument("input_path", help="Đường dẫn thư mục tác phẩm hoặc thư mục Final audio")
    parser.add_argument("--output_dir", "-o", default=None, help="Thư mục lưu video đầu ra (mặc định: [final_dir]/Videos)")
    parser.add_argument("--background", "-bg", default=None, help="Đường dẫn đến tệp ảnh nền cụ thể")
    parser.add_argument("--file", default=None, help="Tên file audio cụ thể cần dựng")
    parser.add_argument("--batch_start", type=int, default=None, help="Chỉ số bắt đầu (1-indexed)")
    parser.add_argument("--batch_end", type=int, default=None, help="Chỉ số kết thúc (1-indexed)")
    parser.add_argument("--parallel", type=int, default=1, help="Số luồng dựng song song")
    parser.add_argument("--force", action="store_true", help="Ghi đè dựng lại video kể cả khi đã xong")
    args = parser.parse_args()

    compile_audiobook_videos(
        input_path=args.input_path,
        specific_file=args.file,
        batch_start=args.batch_start,
        batch_end=args.batch_end,
        parallel=args.parallel,
        force=args.force,
        output_dir=args.output_dir,
        background_path=args.background
    )

