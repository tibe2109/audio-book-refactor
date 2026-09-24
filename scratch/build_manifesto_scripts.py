#!/usr/bin/env python3
import os
import re
import json
import datetime
import sys

# Add core to sys.path
sys.path.insert(0, os.path.abspath('core'))
from audiobook_script_processor import audit_7_quality_gates, num2words_vi

def create_manifesto_pipeline():
    source_path = os.path.abspath("Docs/Su-menh-ca-nhan.md")
    book_slug = "Su-menh-ca-nhan"
    book_dir = os.path.abspath(os.path.join("Kich-ban-clipchamp", book_slug))
    os.makedirs(book_dir, exist_ok=True)

    with open(source_path, "r", encoding="utf-8") as f:
        full_text = f.read()

    sections = full_text.split("---")
    part0 = sections[0].strip() # Title and preamble
    part1 = sections[1].strip() # Phần 1
    part2 = sections[2].strip() # Phần 2
    part3 = sections[3].strip() # Phần 3
    part4 = sections[4].strip() # Phần 4

    chapters_def = [
        {
            "index": 0,
            "folder": "01-Tu-duy-thinh-vuong-va-su-phat-trien-khong-ngung",
            "title": "Phần 1: Tư duy thịnh vượng và sự phát triển không ngừng",
            "raw_text": f"{part0}\n\n{part1}"
        },
        {
            "index": 1,
            "folder": "02-Nghe-thuat-quyen-ru-tu-ben-trong",
            "title": "Phần 2: Nghệ thuật quyến rũ từ bên trong",
            "raw_text": part2
        },
        {
            "index": 2,
            "folder": "03-Ban-linh-kiem-soat-va-vuot-qua-cam-bay",
            "title": "Phần 3: Bản lĩnh kiểm soát và vượt qua cạm bẫy",
            "raw_text": part3
        },
        {
            "index": 3,
            "folder": "04-Bay-tru-cot-chuyen-hoa-tam-thuc-va-tu-duong-dao-duc",
            "title": "Phần 4: Bảy trụ cột chuyển hóa tâm thức và tu dưỡng đạo đức bản lĩnh",
            "raw_text": part4
        }
    ]

    session_id = f"ses_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    session_manifest = {
        "session_id": session_id,
        "book_slug": book_slug,
        "book_title": "Bản Sứ Mệnh Giá Trị Cá Nhân (Personal Manifesto)",
        "author": "Personal Growth & Life Philosophy",
        "source_path": source_path,
        "total_chapters": len(chapters_def),
        "created_at": datetime.datetime.now().isoformat(),
        "updated_at": datetime.datetime.now().isoformat(),
        "pipeline_stage": "01_extracted",
        "step_1_status": "completed",
        "chapters": []
    }

    # Step 01: Extract Raw
    print("[*] STEP 01: Extracting raw files and initializing manifest...")
    for chap in chapters_def:
        chap_dir = os.path.join(book_dir, chap["folder"])
        os.makedirs(chap_dir, exist_ok=True)
        raw_file = os.path.join(chap_dir, "raw_original.txt")
        with open(raw_file, "w", encoding="utf-8") as f:
            f.write(chap["raw_text"])

        w_cnt = len(chap["raw_text"].split())
        c_cnt = len(chap["raw_text"])
        chap_record = {
            "index": chap["index"],
            "folder": chap["folder"],
            "title": chap["title"],
            "char_count": c_cnt,
            "word_count": w_cnt,
            "raw_file": os.path.relpath(raw_file, book_dir),
            "step_1_status": "completed",
            "status": "raw_extracted"
        }
        session_manifest["chapters"].append(chap_record)
        print(f"  [✓] {chap['folder']}: {c_cnt} chars, {w_cnt} words")

    manifest_path = os.path.join(book_dir, ".session_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(session_manifest, f, indent=2, ensure_ascii=False)

    print("\n[*] STEP 01 Complete.")
    return book_dir, chapters_def, session_manifest

if __name__ == "__main__":
    create_manifesto_pipeline()
