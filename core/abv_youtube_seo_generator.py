#!/usr/bin/env python3
# ==============================================================================
# ABV-03: Audiobook Video YouTube SEO Generator & Strategy Orchestrator
# Generates SEO-standard Metadata, Timestamps, Tags, and Audit Reports
# Manages Atomic Progress (.abv_seo_manifest.json) & Centralized Video Storage
# ==============================================================================
import os
import sys
import json
import re
import argparse
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# YouTube Technical Limits
LIMIT_TITLE_CHARS = 100
LIMIT_TITLE_RECOMMENDED = 70
LIMIT_DESCRIPTION_CHARS = 5000
LIMIT_TAGS_TOTAL_CHARS = 500
LIMIT_HASHTAGS_MAX = 60
LIMIT_HASHTAGS_DISPLAY = 3
LIMIT_PINNED_COMMENT_CHARS = 10000
LIMIT_CHANNEL_NAME_CHARS = 50
LIMIT_CHANNEL_ABOUT_CHARS = 1000

# Default YouTube Configuration from User Requirements
DEFAULT_YOUTUBE_CONFIG = {
    "audience": {
        "madeForKids": False,  # "Không, nội dung này không dành cho trẻ em"
        "ageRestriction": False
    },
    "paidPromotion": {
        "hasPaidPromotion": False  # "Không, video của tôi không chứa nội dung được trả tiền để quảng cáo"
    },
    "aiDeclaration": {
        "containsSyntheticMedia": True  # "Có" - Có sử dụng AI để tạo hoặc chỉnh sửa nội dung
    },
    "automaticFeatures": {
        "autoChapters": True,  # "Cho phép dùng phân cảnh tự động"
        "autoPlaces": True,    # "Cho phép chèn địa điểm tự động"
        "autoConcepts": True   # "Bật tính năng tự động thêm khái niệm"
    },
    "distributionAndInteraction": {
        "shortsRemixing": "all",  # "Cho phép phối lại video và âm thanh"
        "categoryId": "24",       # "Giải trí" (Entertainment)
        "comments": {
            "status": "enabled",
            "moderation": "none",
            "commenters": "anyone",
            "sortBy": "top"
        },
        "showLikeCount": True     # "Hiện số người xem thích video này"
    }
}

def resolve_book_directories(input_path_str: str) -> Tuple[Path, Path, Path, Path]:
    """
    Resolves (book_dir, final_dir, final_video_dir, seo_metadata_dir) from any input path.
    """
    path = Path(input_path_str).resolve()
    
    # Check if input is inside Final dir or Videos dir
    if path.name == "Videos" and "Final-" in path.parent.name:
        final_video_dir = path
        final_dir = path.parent
        book_dir = final_dir.parent
    elif path.name.startswith("Final-"):
        final_dir = path
        book_dir = path.parent
        final_video_dir = final_dir / "Videos" if (final_dir / "Videos").exists() else final_dir
    else:
        book_dir = path
        # Find Final-[book_name]
        book_name = book_dir.name
        final_dir = book_dir / f"Final-{book_name}"
        if not final_dir.exists():
            final_dir = book_dir.parent / f"Final-{book_name}"
        final_video_dir = final_dir / "Videos" if (final_dir / "Videos").exists() else final_dir

    seo_metadata_dir = final_video_dir / "youtube_metadata"
    return book_dir, final_dir, final_video_dir, seo_metadata_dir

def load_manifest(manifest_path: Path) -> Dict:
    """Loads manifest with atomic error recovery."""
    if not manifest_path.exists():
        return {}
    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[WARN] Manifest read error: {e}. Rebuilding manifest.")
        return {}

def save_manifest_atomic(manifest_path: Path, data: Dict):
    """Saves manifest atomically using a temporary file and replace."""
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    temp_dir = manifest_path.parent
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    
    with tempfile.NamedTemporaryFile("w", dir=temp_dir, delete=False, encoding="utf-8") as tf:
        json.dump(data, tf, indent=2, ensure_ascii=False)
        temp_file_name = tf.name

    os.replace(temp_file_name, manifest_path)

def parse_chunks_duration(chapter_dir: Path) -> List[Tuple[str, float, float]]:
    """
    Parse .chunks_duration.json to calculate exact timestamps for YouTube Chapters.
    Returns a list of tuples: (chunk_name, start_time_seconds, duration_seconds)
    """
    dur_file = chapter_dir / ".chunks_duration.json"
    if not dur_file.exists():
        return []

    try:
        with open(dur_file, "r", encoding="utf-8") as f:
            durations = json.load(f)

        sorted_chunks = sorted(durations.items(), key=lambda x: [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', x[0])])
        result = []
        current_time = 0.0
        for chunk_name, dur in sorted_chunks:
            result.append((chunk_name, current_time, float(dur)))
            current_time += float(dur)
        return result
    except Exception as e:
        print(f"[WARN] Error parsing .chunks_duration.json: {e}")
        return []

def format_timestamp(seconds: float) -> str:
    """Formats seconds into MM:SS or HH:MM:SS format."""
    total_sec = int(seconds)
    hours = total_sec // 3600
    minutes = (total_sec % 3600) // 60
    sec = total_sec % 60
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{sec:02d}"
    return f"{minutes:02d}:{sec:02d}"

def extract_chapter_narrative_beats(chapter_dir: Path) -> List[str]:
    """Extracts narrative beats from summary.md or kich-ban files."""
    summary_file = chapter_dir / "summary.md"
    beats = []
    if summary_file.exists():
        try:
            with open(summary_file, "r", encoding="utf-8") as f:
                content = f.read()
            matches = re.findall(r'(?:###\s*🎬|\d+\.\s*\*\*)(.*?)(?:\n|$)', content)
            if matches:
                beats = [m.strip().replace("**", "").replace("*", "") for m in matches if m.strip()]
        except Exception:
            pass

    return beats

def audit_youtube_metadata(metadata: Dict) -> Dict[str, any]:
    """Audits a YouTube metadata dictionary against platform limits."""
    title = metadata.get("title", "")
    description = metadata.get("description", "")
    tags = metadata.get("tags", [])
    hashtags = metadata.get("hashtags", [])
    pinned_comment = metadata.get("pinned_comment", "")

    tags_total_chars = sum(len(t) for t in tags) + max(0, len(tags) - 1)
    title_len = len(title)
    desc_len = len(description)
    pinned_len = len(pinned_comment)

    audit_results = {
        "title": {
            "length": title_len,
            "max": LIMIT_TITLE_CHARS,
            "recommended": LIMIT_TITLE_RECOMMENDED,
            "passed": title_len <= LIMIT_TITLE_CHARS,
            "warning": title_len > LIMIT_TITLE_RECOMMENDED
        },
        "description": {
            "length": desc_len,
            "max": LIMIT_DESCRIPTION_CHARS,
            "passed": desc_len <= LIMIT_DESCRIPTION_CHARS,
            "has_timestamps": "00:00" in description
        },
        "tags": {
            "count": len(tags),
            "total_chars": tags_total_chars,
            "max_chars": LIMIT_TAGS_TOTAL_CHARS,
            "passed": tags_total_chars <= LIMIT_TAGS_TOTAL_CHARS
        },
        "hashtags": {
            "count": len(hashtags),
            "max": LIMIT_HASHTAGS_MAX,
            "display_top": min(len(hashtags), LIMIT_HASHTAGS_DISPLAY),
            "passed": len(hashtags) <= LIMIT_HASHTAGS_MAX
        },
        "pinned_comment": {
            "length": pinned_len,
            "max": LIMIT_PINNED_COMMENT_CHARS,
            "passed": pinned_len <= LIMIT_PINNED_COMMENT_CHARS
        },
        "all_passed": (
            title_len <= LIMIT_TITLE_CHARS and
            desc_len <= LIMIT_DESCRIPTION_CHARS and
            tags_total_chars <= LIMIT_TAGS_TOTAL_CHARS and
            len(hashtags) <= LIMIT_HASHTAGS_MAX and
            pinned_len <= LIMIT_PINNED_COMMENT_CHARS
        )
    }
    return audit_results

def generate_chapter_seo_template(
    book_title: str,
    chapter_num: int,
    chapter_title: str,
    timestamps: List[Tuple[str, float, str]],
    thumbnail_path: Optional[str] = None,
    channel_name: str = "Tibe audio book",
    series_playlist: str = "Tam Quốc Diễn Nghĩa - Trọn Bộ Sách Nói Kịch Nghệ"
) -> Dict:
    """Generates structured SEO metadata template adhering to limits and golden layout."""
    title_opt1 = f"SÁCH NÓI {book_title.upper()} — Hồi {chapter_num}: {chapter_title}"
    if len(title_opt1) > LIMIT_TITLE_CHARS:
        title_opt1 = f"Sách Nói {book_title} — Hồi {chapter_num}: {chapter_title}"[:LIMIT_TITLE_CHARS]

    # Timestamps Formatting
    ts_lines = []
    if timestamps:
        for chunk_name, sec, desc in timestamps:
            ts_str = format_timestamp(sec)
            ts_lines.append(f"{ts_str} {desc}")
    else:
        ts_lines = [
            "00:00 Mở đầu: Khúc từ bi tráng & Bối cảnh thời đại",
            "03:00 Diễn biến biến cố trung tâm",
            "10:00 Cao trào đối đầu & Mưu lược",
            "18:00 Cục diện ngã ngũ & Bài học nhân sinh"
        ]
    ts_block = "\n".join(ts_lines)

    desc = (
        f"🔥 Sách Nói Kịch Nghệ Đa Thanh: {book_title.upper()}\n"
        f"⚔️ HỒI {chapter_num}: {chapter_title.upper()}\n\n"
        f"Khám phá diễn biến kịch tính trong Hồi {chapter_num} của tác phẩm bất hủ {book_title}. "
        f"Tác phẩm đưa người nghe bước vào thời kỳ binh đao biến loạn, nơi mưu lược trí tuệ va chạm cùng dũng khí sa trường, "
        f"phơi bày những bài học sâu sắc về nhân tâm, chữ Tín và quy luật thịnh suy của thời cuộc.\n\n"
        f"⏱️ MỤC LỤC CHI TIẾT & TIMESTAMPS (Bấm vào mốc thời gian để nghe đoạn bạn thích):\n"
        f"{ts_block}\n\n"
        f"---\n"
        f"✨ ĐẶC TRƯNG BẢN SÁCH NÓI:\n"
        f"• Diễn đọc: Phân vai kịch nghệ đa thanh sống động, giữ trọn khẩu khí cổ phong của từng nhân vật.\n"
        f"• Âm thanh: Hòa âm nhạc nền mộc cổ phong (Cổ cầm, Đàn tranh, Tiêu sáo) chuẩn phát thanh EBU R128 (-16 LUFS).\n"
        f"• Hình ảnh: Minh họa nghệ thuật 1080p Full HD điện ảnh.\n\n"
        f"📌 ĐĂNG KÝ KÊNH {channel_name.upper()} để đón nghe trọn bộ các Hồi tiếp theo:\n"
        f"👉 Nhấn Đăng Ký (Subscribe) và Bật Chuông thông báo 🔔\n"
        f"👉 Danh sách phát trọn bộ: {series_playlist}\n"
        f"👉 Đừng quên bấm Like và để lại Bình Luận cảm nghĩ của bạn về nhân vật trong hồi này nhé!\n\n"
        f"#{book_title.replace(' ', '')} #SachNoi #{channel_name.replace(' ', '')} #LichSu #SachNoiHay"
    )

    slug_book = book_title.lower()
    tags = [
        slug_book,
        f"sach noi {slug_book}",
        f"sách nói {slug_book}",
        f"{slug_book} hoi {chapter_num}",
        f"hoi {chapter_num} {chapter_title.lower()}",
        "sach noi kich nghe",
        "truyen doc lich su",
        "audio book",
        "sach noi hay nhat",
        channel_name.lower()
    ]
    cur_len = sum(len(t) for t in tags) + len(tags) - 1
    if cur_len > LIMIT_TAGS_TOTAL_CHARS:
        while tags and (sum(len(t) for t in tags) + len(tags) - 1) > LIMIT_TAGS_TOTAL_CHARS:
            tags.pop()

    pinned_comment = (
        f"🔥 Chào mừng quý thính giả đến với Hồi {chapter_num} tác phẩm {book_title} trên kênh {channel_name}!\n\n"
        f"💬 Bạn tâm đắc nhất với tình tiết hay câu nói nào của nhân vật trong hồi này? Hãy để lại cảm nghĩ dưới phần bình luận nhé!\n"
        f"👉 Đừng quên bấm Đăng Ký kênh và Bật Chuông 🔔 để đón nghe Hồi {chapter_num + 1} sớm nhất!"
    )

    return {
        "title": title_opt1,
        "title_options": [
            title_opt1,
            f"{book_title} Hồi {chapter_num}: {chapter_title} | Sách Nói Kịch Nghệ Đa Thanh",
            f"[Sách Nói] {book_title} — Hồi {chapter_num}: {chapter_title}"
        ],
        "description": desc,
        "tags": tags,
        "hashtags": [
            f"#{book_title.replace(' ', '')}",
            "#SachNoi",
            f"#{channel_name.replace(' ', '')}",
            "#LichSu",
            "#SachNoiHay"
        ],
        "pinned_comment": pinned_comment,
        "privacy": "unlisted",
        "category": DEFAULT_YOUTUBE_CONFIG["distributionAndInteraction"]["categoryId"],
        "thumbnail": thumbnail_path or "",
        "default_config": DEFAULT_YOUTUBE_CONFIG
    }

def print_manifest_status(manifest: Dict):
    """Prints a structured summary of the progress manifest."""
    total = manifest.get("total_videos", 0)
    completed = manifest.get("completed_metadata", 0)
    pending = manifest.get("pending_metadata", 0)
    failed = manifest.get("failed_metadata", 0)
    pct = (completed / total * 100) if total > 0 else 0.0

    print(f"\n=======================================================")
    print(f"📊 ABV-03 PROGRESS STATUS: {pct:.1f}% ({completed}/{total})")
    print(f"=======================================================")
    print(f"  ✅ Completed Metadata : {completed}")
    print(f"  ⏳ Pending Metadata   : {pending}")
    print(f"  ❌ Failed Metadata    : {failed}")
    print(f"  🕒 Last Updated       : {manifest.get('updated_at', 'N/A')}")
    print(f"=======================================================\n")

def main():
    parser = argparse.ArgumentParser(description="ABV-03 YouTube SEO Metadata Orchestrator & Progress Manager")
    parser.add_argument("--book_dir", required=True, help="Path to book project or Final folder")
    parser.add_argument("--chapter", help="Specific chapter slug to process (e.g. 01-Hoi-01)")
    parser.add_argument("--batch_start", type=int, help="Start index of chapter batch (1-based)")
    parser.add_argument("--batch_end", type=int, help="End index of chapter batch (1-based)")
    parser.add_argument("--status", action="store_true", help="Display current progress and exit")
    parser.add_argument("--force", action="store_true", help="Force re-generate metadata even if completed")

    args = parser.parse_args()
    book_dir, final_dir, final_video_dir, seo_metadata_dir = resolve_book_directories(args.book_dir)
    seo_metadata_dir.mkdir(parents=True, exist_ok=True)

    manifest_path = final_video_dir / ".abv_seo_manifest.json"
    manifest = load_manifest(manifest_path)

    # Initialize manifest structure if empty
    if not manifest or "videos" not in manifest:
        manifest = {
            "book_name": book_dir.name,
            "book_dir": str(book_dir),
            "final_video_dir": str(final_video_dir),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "total_videos": 0,
            "completed_metadata": 0,
            "pending_metadata": 0,
            "failed_metadata": 0,
            "videos": {}
        }

    # Discover videos in final_video_dir
    video_files = sorted(final_video_dir.glob("Final_Video_*.mp4"))
    if not video_files:
        # Fallback to scanning final_dir or book_dir chapters
        video_files = sorted(final_dir.glob("Final_Video_*.mp4"))

    # Update manifest with newly discovered videos
    for vf in video_files:
        v_name = vf.name
        if v_name not in manifest["videos"]:
            # Extract chapter slug from video filename
            match = re.search(r'Final_Video_(\d+-[^._]+)', v_name)
            chap_slug = match.group(1) if match else v_name.replace("Final_Video_", "").replace(".mp4", "")
            manifest["videos"][v_name] = {
                "video_file": v_name,
                "chapter_dir": chap_slug,
                "metadata_file": f"youtube_metadata_{chap_slug}.json",
                "status": "pending",
                "audit_passed": False,
                "uploaded": False,
                "youtube_url": None,
                "updated_at": None
            }

    # Sync counters
    manifest["total_videos"] = len(manifest["videos"])
    manifest["completed_metadata"] = sum(1 for v in manifest["videos"].values() if v.get("status") == "completed")
    manifest["failed_metadata"] = sum(1 for v in manifest["videos"].values() if v.get("status") == "failed")
    manifest["pending_metadata"] = manifest["total_videos"] - manifest["completed_metadata"] - manifest["failed_metadata"]
    save_manifest_atomic(manifest_path, manifest)

    if args.status:
        print_manifest_status(manifest)
        sys.exit(0)

    print(f"\n=======================================================")
    print(f"🎯 ABV-03: YOUTUBE SEO METADATA & PROGRESS ORCHESTRATOR")
    print(f"=======================================================")
    print(f"📚 Book Directory       : {book_dir}")
    print(f"📁 Final Video Directory: {final_video_dir}")
    print(f"📑 SEO Metadata Storage : {seo_metadata_dir}")
    print(f"🧭 Progress Manifest    : {manifest_path}")
    print_manifest_status(manifest)

    # Filter target videos based on arguments
    target_videos = []
    sorted_items = sorted(manifest["videos"].items(), key=lambda x: [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', x[0])])

    for idx, (v_name, v_info) in enumerate(sorted_items, start=1):
        # Filter by chapter
        if args.chapter and args.chapter not in v_info["chapter_dir"]:
            continue
        # Filter by batch
        if args.batch_start and idx < args.batch_start:
            continue
        if args.batch_end and idx > args.batch_end:
            continue
        target_videos.append((v_name, v_info))

    print(f"🎯 Targeted videos for this run: {len(target_videos)}")

    for v_name, v_info in target_videos:
        chap_slug = v_info["chapter_dir"]
        meta_file_path = seo_metadata_dir / f"youtube_metadata_{chap_slug}.json"
        
        # Check Atomic Resume: Skip if already completed and audit passed
        if not args.force and v_info.get("status") == "completed" and meta_file_path.exists() and v_info.get("audit_passed"):
            print(f"  ⏭️ [SKIP COMPLETED] {v_name} (Metadata verified)")
            continue

        print(f"\n--- 🎬 Processing SEO for: {v_name} ({chap_slug}) ---")
        chap_dir = book_dir / chap_slug
        if not chap_dir.exists():
            # Try finding chapter by pattern
            matches = list(book_dir.glob(f"*{chap_slug}*"))
            chap_dir = matches[0] if matches else chap_dir

        timestamps = parse_chunks_duration(chap_dir)
        print(f"  ⏱️ Parsed {len(timestamps)} chunk timestamps from {chap_dir.name}")

        # Extract chapter number and title
        match = re.search(r'(\d+)[-_]Hoi[-_](\d+)', chap_slug, re.IGNORECASE)
        if match:
            c_num = int(match.group(2))
        else:
            num_match = re.search(r'\d+', chap_slug)
            c_num = int(num_match.group(0)) if num_match else 1
            
        c_title = chap_slug.replace(f"{c_num:02d}-", "").replace(f"Hoi-{c_num:02d}", "").replace("-", " ").strip()
        if not c_title:
            c_title = f"Hồi {c_num}"

        # Thumbnail discovery
        thumb_file = None
        # Check backgrounds folder in Final
        bg_folder = final_dir / "backgrounds"
        if bg_folder.exists():
            candidates = list(bg_folder.glob(f"*Background-{c_num}.*")) or list(bg_folder.glob("Background-1.*"))
            if candidates:
                thumb_file = str(candidates[0])

        meta_data = generate_chapter_seo_template(
            book_title=book_dir.name.replace("-", " "),
            chapter_num=c_num,
            chapter_title=c_title,
            timestamps=[(c, s, f"Phân đoạn {i+1}") for i, (c, s, d) in enumerate(timestamps)],
            thumbnail_path=thumb_file
        )

        # Audit
        audit = audit_youtube_metadata(meta_data)
        meta_data["audit_results"] = audit

        # Save metadata to centralized folder
        with open(meta_file_path, "w", encoding="utf-8") as f:
            json.dump(meta_data, f, indent=2, ensure_ascii=False)

        # Also mirror in chapter dir for backward compatibility
        if chap_dir.exists():
            chap_meta = chap_dir / "youtube_metadata.json"
            with open(chap_meta, "w", encoding="utf-8") as f:
                json.dump(meta_data, f, indent=2, ensure_ascii=False)

        # Update manifest atomically
        v_info["status"] = "completed" if audit["all_passed"] else "failed"
        v_info["audit_passed"] = audit["all_passed"]
        v_info["title"] = meta_data["title"]
        v_info["metadata_file"] = f"youtube_metadata/youtube_metadata_{chap_slug}.json"
        v_info["updated_at"] = datetime.now(timezone.utc).isoformat()

        # Update counters
        manifest["completed_metadata"] = sum(1 for v in manifest["videos"].values() if v.get("status") == "completed")
        manifest["failed_metadata"] = sum(1 for v in manifest["videos"].values() if v.get("status") == "failed")
        manifest["pending_metadata"] = manifest["total_videos"] - manifest["completed_metadata"] - manifest["failed_metadata"]
        save_manifest_atomic(manifest_path, manifest)

        status_icon = "✅" if audit["all_passed"] else "❌"
        print(f"  {status_icon} Saved metadata to: {meta_file_path.name}")
        print(f"     Title ({audit['title']['length']}/100): {meta_data['title']}")
        print(f"     Tags Total: {audit['tags']['total_chars']}/500 chars ({audit['tags']['count']} tags)")

    print(f"\n=======================================================")
    print(f"🎉 BATCH PROCESSING COMPLETE")
    print(f"=======================================================")
    print_manifest_status(manifest)

if __name__ == "__main__":
    main()
