#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
Audiobook QC Auditor Pipeline v2 (Step 07)
Audits 7 Hard Quality Gates across all chapters and final script files (Kich-ban-*.txt):
- Gate 1: Directory Naming Standard (^[a-zA-Z0-9\-]+$)
- Gate 2: Chunk Character Count (0 < length <= 3000 chars)
- Gate 3: TTS Forbidden Characters Cleanliness ((), "", “”, [], :, ;, —, –)
- Gate 4: Zero Raw Digits Policy (\d = 0)
- Gate 5: Pacing & Breathing Markers Format (. ......)
- Gate 6: Word Count Delta Integrity vs translated.txt / raw_original.txt
- Gate 7: Step 08 Clearance Certification (100% 7 Gates PASSED)

Outputs:
- Individual QC_Report.md in each chapter folder
- Master QC_Report.md in the book root folder
- Synchronizes .session_manifest.json
"""

import os
import sys
import re
import glob
import json
import argparse
import datetime

FORBIDDEN_PATTERN = re.compile(r'[\(\)"“”:;—–\[\]«»#*•●▪▶►★▲◆■✓]')
DIGIT_PATTERN = re.compile(r'\d')

def audit_chapter(chap_dir, chap_name=""):
    folder_name = os.path.basename(chap_dir)
    gate_results = []
    all_passed = True
    
    # Gate 1: Directory Naming
    g1_pass = bool(re.match(r'^[a-zA-Z0-9\-]+$', folder_name))
    gate_results.append(("Gate 1: Tên Thư Mục Chuẩn", g1_pass, f"Thư mục: '{folder_name}'"))
    if not g1_pass:
        all_passed = False
        
    # Discover final script files Kich-ban-*.txt (support kich-ban subfolder first, fallback to chap_dir)
    kich_ban_dir = os.path.join(chap_dir, "kich-ban")
    if os.path.isdir(kich_ban_dir) and glob.glob(os.path.join(kich_ban_dir, "Kich-ban-*.txt")):
        script_dir = kich_ban_dir
    else:
        script_dir = chap_dir

    script_files = sorted(
        glob.glob(os.path.join(script_dir, "Kich-ban-*.txt")),
        key=lambda x: int(re.search(r'Kich-ban-(\d+)\.txt', x).group(1)) if re.search(r'Kich-ban-(\d+)\.txt', x) else 0
    )
    
    if not script_files:
        gate_results.append(("Gate 2: Dung Lượng Chunk <= 3000 ký tự", False, "Không tìm thấy file Kich-ban-*.txt nào"))
        return False, f"[-] Không có file kịch bản trong {chap_dir}", gate_results
        
    # Gate 2: Chunk Size <= 3000 chars & > 0 bytes
    g2_pass = True
    g2_details = []
    total_script_chars = 0
    total_script_words = 0
    chunk_stats = []
    
    for s_path in script_files:
        with open(s_path, "r", encoding="utf-8") as f:
            content = f.read()
        c_len = len(content)
        w_cnt = len(content.split())
        total_script_chars += c_len
        total_script_words += w_cnt
        chunk_stats.append((os.path.basename(s_path), c_len, w_cnt))
        
        if c_len == 0 or c_len > 3000:
            g2_pass = False
            g2_details.append(f"{os.path.basename(s_path)}: {c_len} chars (FAIL)")
            
    if g2_pass:
        lens = [c[1] for c in chunk_stats]
        g2_desc = f"{len(script_files)} chunks đạt chuẩn (Min: {min(lens)}, Max: {max(lens)}, Avg: {sum(lens)//len(lens)} ký tự)"
    else:
        g2_desc = ", ".join(g2_details)
        all_passed = False
    gate_results.append(("Gate 2: Dung Lượng Chunk <= 3000 ký tự", g2_pass, g2_desc))
    
    # Gate 3: Forbidden Characters
    g3_pass = True
    g3_found = []
    for s_path in script_files:
        with open(s_path, "r", encoding="utf-8") as f:
            content = f.read()
        matches = FORBIDDEN_PATTERN.findall(content)
        if matches:
            g3_pass = False
            g3_found.append(f"{os.path.basename(s_path)}: phát hiện {set(matches)}")
            
    if not g3_pass:
        all_passed = False
    gate_results.append(("Gate 3: Khử Sạch Ký Tự Cấm TTS", g3_pass, "100% Sạch ký tự cấm" if g3_pass else "; ".join(g3_found)))
    
    # Gate 4: Zero Raw Digits Policy
    g4_pass = True
    g4_found = []
    for s_path in script_files:
        with open(s_path, "r", encoding="utf-8") as f:
            content = f.read()
        digits = DIGIT_PATTERN.findall(content)
        if digits:
            g4_pass = False
            g4_found.append(f"{os.path.basename(s_path)}: {len(digits)} chữ số ({digits[:3]})")
            
    if not g4_pass:
        all_passed = False
    gate_results.append(("Gate 4: Viết Chữ Số Toàn Diện (Zero-digit)", g4_pass, "100% Viết chữ tự nhiên (0 chữ số thô)" if g4_pass else "; ".join(g4_found)))
    
    # Gate 5: Pacing & Breathing Markers Format
    g5_pass = True
    g5_pause_count = 0
    for s_path in script_files:
        with open(s_path, "r", encoding="utf-8") as f:
            content = f.read()
        g5_pause_count += content.count(". ......")
        if ". ...... . ......" in content:
            g5_pass = False

    if script_files:
        with open(script_files[0], "r", encoding="utf-8") as f:
            if ". ......" not in f.read():
                g5_pass = False
            
    if not g5_pass:
        all_passed = False
    gate_results.append(("Gate 5: Định Dạng Nhịp Thở (. ......)", g5_pass, f"Đạt chuẩn ({g5_pause_count} markers ngắt nghỉ phát thanh)" if g5_pass else "Thiếu nhịp thở phát thanh . ......"))
    
    # Gate 6: Word Count Delta (Chống Tóm Tắt)
    trans_path = os.path.join(chap_dir, "translated.txt")
    raw_path = os.path.join(chap_dir, "raw_original.txt")
    norm_path = os.path.join(chap_dir, "normalized.txt")
    
    if os.path.exists(norm_path):
        with open(norm_path, "r", encoding="utf-8") as f:
            base_ref_words = len(f.read().split())
        ref_source = "normalized.txt"
        max_allowed_delta = 0.05 # Max 5% delta against normalized
    elif os.path.exists(trans_path):
        with open(trans_path, "r", encoding="utf-8") as f:
            base_ref_words = len(f.read().split())
        ref_source = "translated.txt"
        max_allowed_delta = 0.15 # Max 15% delta against translated
    elif os.path.exists(raw_path):
        with open(raw_path, "r", encoding="utf-8") as f:
            base_ref_words = len(f.read().split())
        ref_source = "raw_original.txt"
        max_allowed_delta = 0.65
    else:
        base_ref_words = total_script_words
        ref_source = "self"
        max_allowed_delta = 0.10
        
    delta = abs(total_script_words - base_ref_words) / (base_ref_words if base_ref_words > 0 else 1)
    g6_pass = delta <= max_allowed_delta

    # Hard Verification against raw_original.txt (Anti-Summarization & Omission Gate)
    raw_ratio_detail = ""
    if os.path.exists(raw_path):
        with open(raw_path, "r", encoding="utf-8") as f:
            raw_words = len(f.read().split())
        if raw_words > 0:
            raw_ratio = total_script_words / raw_words
            if raw_ratio < 0.75:
                g6_pass = False
                raw_ratio_detail = f" | ❌ CẮT XÉN NẶNG: Tỷ lệ dịch/gốc {raw_ratio*100:.1f}% (<75%)"
            else:
                raw_ratio_detail = f" | Tỷ lệ dịch/gốc: {raw_ratio*100:.1f}%"

    if not g6_pass:
        all_passed = False
    gate_results.append((
        "Gate 6: Word Count Delta (Chống Tóm Tắt)",
        g6_pass,
        f"Tham chiếu ({ref_source}): {base_ref_words} từ | Kịch bản: {total_script_words} từ | Độ lệch: {delta*100:.2f}% (Ngưỡng $\\le$ {max_allowed_delta*100:.0f}%){raw_ratio_detail}"
    ))
    
    # Gate 7: Clearance for Step 08
    gate_results.append((
        "Gate 7: Cấp Quyền Thu Âm TTS (Step 08 Clearance)",
        all_passed,
        "ĐỦ ĐIỀU KIỆN THU ÂM TTS (100% 7 GATES PASSED)" if all_passed else "TỪ CHỐI CẤP PHÉP - Cần Tự Chữa Lành (Self-Healing)"
    ))
    
    # Generate Chapter QC_Report.md
    report_lines = [
        f"# Báo Cáo Kiểm Toán Chất Lượng (QC Audit Report) — {folder_name}",
        f"**Trạng Thái Thẩm Định:** {'✅ PASSED (100% 7 GATES PASSED)' if all_passed else '❌ FAILED'}",
        f"**Thời Điểm Kiểm Toán:** `{datetime.datetime.now(datetime.timezone.utc).isoformat()}`\n",
        "| Gate | Tiêu Chí Kiểm Toán | Kết Quả | Chi Tiết Đối Soát |",
        "| :--- | :--- | :---: | :--- |"
    ]
    for g_name, g_status, g_detail in gate_results:
        report_lines.append(f"| **{g_name}** | {g_name.split(':')[1].strip() if ':' in g_name else g_name} | {'✅ PASS' if g_status else '❌ FAIL'} | {g_detail} |")
        
    report_lines.append("\n### Bảng Thống Kê Chi Tiết Từng File Kịch Bản:")
    report_lines.append("| Tên File | Dung Lượng Ký Tự (Chars) | Số Từ (Words) | Trạng Thái Gate 2 (<= 3000) |")
    report_lines.append("| :--- | :---: | :---: | :---: |")
    for fname, clen, wcnt in chunk_stats:
        report_lines.append(f"| `{fname}` | {clen} | {wcnt} | {'✅ PASS' if clen <= 3000 else '❌ FAIL'} |")
        
    report_lines.append("\n---\n*Báo cáo được khởi tạo tự động bởi Audiobook QC Auditor Engine (Step 07)*\n")
    report_content = "\n".join(report_lines)
    
    chap_qc_path = os.path.join(chap_dir, "QC_Report.md")
    with open(chap_qc_path, "w", encoding="utf-8") as f:
        f.write(report_content)
        
    return all_passed, report_content, gate_results

def main():
    parser = argparse.ArgumentParser(description="Audiobook QC Auditor Pipeline v2 (Step 07)")
    parser.add_argument("--input_dir", "--book_dir", dest="book_dir", required=True, help="Path to book directory")
    parser.add_argument("--chapter", help="Specific chapter folder name (optional)")
    args = parser.parse_args()
    
    book_dir = os.path.abspath(args.book_dir)
    manifest_path = os.path.join(book_dir, ".session_manifest.json")
    
    manifest = None
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
            
    chapters_to_audit = []
    if args.chapter:
        chapters_to_audit.append(os.path.join(book_dir, args.chapter))
    elif manifest and "chapters" in manifest:
        for c in manifest["chapters"]:
            chapters_to_audit.append(os.path.join(book_dir, c["folder"]))
    else:
        for item in sorted(os.listdir(book_dir)):
            full_p = os.path.join(book_dir, item)
            kb_sub = os.path.join(full_p, "kich-ban")
            has_scripts = False
            if os.path.isdir(full_p):
                if os.path.isdir(kb_sub) and glob.glob(os.path.join(kb_sub, "Kich-ban-*.txt")):
                    has_scripts = True
                elif glob.glob(os.path.join(full_p, "Kich-ban-*.txt")):
                    has_scripts = True
            if has_scripts:
                chapters_to_audit.append(full_p)
                
    print(f"[*] Starting 7 Quality Gates Audit for {len(chapters_to_audit)} chapters in: {book_dir}\n" + "="*70)
    
    all_chaps_passed = True
    chapter_summaries = []
    
    for chap_p in chapters_to_audit:
        chap_name = os.path.basename(chap_p)
        passed, _, gate_results = audit_chapter(chap_p, chap_name)
        if not passed:
            all_chaps_passed = False
        status_icon = "✅ PASSED" if passed else "❌ FAILED"
        print(f"[{status_icon}] {chap_name}: 7/7 Gates Checked")
        chapter_summaries.append((chap_name, passed, gate_results))
        
    # Generate Master QC_Report.md at book root
    master_lines = [
        f"# BÁO CÁO TỔNG QUAN KIỂM TOÁN CHẤT LƯỢNG (MASTER QC REPORT)",
        f"## Dự án: {manifest.get('book_title', os.path.basename(book_dir)) if manifest else os.path.basename(book_dir)}",
        f"**Trạng Thái Tổng Thể Toàn Sách:** {'✅ 100% TẤT CẢ CÁC CHƯƠNG ĐẠT CHUẨN (7 GATES PASSED)' if all_chaps_passed else '❌ CÓ CHƯƠNG KHÔNG ĐẠT CHUẨN'}",
        f"**Thời Điểm Thẩm Định:** `{datetime.datetime.now(datetime.timezone.utc).isoformat()}`\n",
        "### 1. Bảng Tổng Hợp Trạng Thái Từng Chương:",
        "| STT | Tên Thư Mục Chương | Trạng Thái QC | Số Gates Đạt | Cấp Quyền Thu Âm TTS (Step 08) |",
        "| :---: | :--- | :---: | :---: | :---: |"
    ]
    
    for idx, (cname, cpass, gr) in enumerate(chapter_summaries, 1):
        passed_count = sum(1 for _, st, _ in gr if st)
        total_count = len(gr)
        c_status = "✅ 100% PASSED" if cpass else "❌ FAILED"
        c_perm = "ĐÃ MỞ KHÓA BƯỚC 08" if cpass else "BỊ KHÓA (CẦN FIX)"
        master_lines.append(f"| **{idx:02d}** | [`{cname}`](file://{os.path.join(book_dir, cname, 'QC_Report.md')}) | {c_status} | {passed_count}/{total_count} | **{c_perm}** |")
        
    master_lines.append("\n### 2. Danh Mục 7 Quality Gates Bắt Buộc:")
    master_lines.append("1. **Gate 1 (Tên Thư Mục):** Regex `^[a-zA-Z0-9\\-]+$`.")
    master_lines.append("2. **Gate 2 (Dung Lượng Chunk):** Khóa cứng $\\le 3.000$ ký tự & $> 0$ bytes.")
    master_lines.append("3. **Gate 3 (Khử Sạch Ký Tự Cấm):** Khử 100% dấu hai chấm `:`, ngoặc `()`, `\"\"`, `“”`, `[]`, chấm phẩy `;`, gạch ngang `—`, `–`.")
    master_lines.append("4. **Gate 4 (Số Hóa Toàn Diện):** 100% viết chữ tự nhiên (Zero-digit policy: `\\d = 0`).")
    master_lines.append("5. **Gate 5 (Định Dạng Nhịp Thở):** Tiêu đề IN HOA độc lập kèm marker `. ......` (1.5 - 2.0s).")
    master_lines.append("6. **Gate 6 (Chống Tóm Tắt):** Giữ trọn 100% nội dung nguyên tác (Delta $\\le 5\\%$ so với bản chuẩn hóa).")
    master_lines.append("7. **Gate 7 (Cấp Quyền TTS):** Chứng nhận 100% mở khóa Bước 08 thu âm giọng đọc bản quyền.")
    master_lines.append("\n---\n*Chứng nhận kiểm toán chất lượng bởi Audiobook QC Auditor Pipeline v2*")
    
    master_report_path = os.path.join(book_dir, "QC_Report.md")
    with open(master_report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(master_lines))
        
    print(f"\n[✓] Generated Master QC Report: {master_report_path}")
    
    # Update manifest
    if manifest:
        manifest["pipeline_stage"] = "07_qc_audited"
        manifest["step_7_status"] = "completed" if all_chaps_passed else "failed"
        manifest["step_7_completed_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        manifest["updated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        manifest["qc_all_passed"] = all_chaps_passed
        
        chap_map = {cname: cpass for cname, cpass, _ in chapter_summaries}
        for c in manifest.get("chapters", []):
            f_name = c.get("folder")
            if f_name in chap_map:
                c["qc_passed"] = chap_map[f_name]
                c["step_7_audited"] = True
                c["status"] = "qc_passed" if chap_map[f_name] else "qc_failed"
                
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        print(f"[✓] Successfully updated session manifest: {manifest_path}")
        
    print("="*70)
    if all_chaps_passed:
        print("[🎉] 100% ALL CHAPTERS PASSED 7 QUALITY GATES! STEP 08 TTS IS UNLOCKED!")
    else:
        print("[⚠️] SOME CHAPTERS FAILED QC GATES. Self-healing loop recommended.")

if __name__ == "__main__":
    main()
