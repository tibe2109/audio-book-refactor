---
name: arf_04_smart_audiobook_rechunker
description: Bước 4 - AI phân tách ngữ nghĩa thành các chunk ~2500-3000 ký tự (không cắt cụt ý).
---

# Kỹ năng 04: Semantic Rechunker (A.I Quyết Định)

**TRIẾT LÝ CỐT LÕI:** AI dùng tư duy ngôn ngữ để quyết định điểm cắt, đảm bảo không cắt ngang câu, không cắt ngang một ý đang mạch lạc.

## 1. Nhiệm vụ của AI
- Root Agent gọi Sub-agents đọc file `normalized.txt` (hoặc bản dịch `translated.txt` / `raw_original.txt`).
- AI phân tích và tách văn bản thành các tệp `Kich-ban-raw-N.txt` (mỗi tệp ~2500 - 3000 ký tự).
- Điểm cắt phải nằm ở cuối đoạn văn, hoặc cuối câu hoàn chỉnh, không gây hẫng nhịp cho người nghe.
- **Quy chuẩn lưu trữ kịch bản:** Toàn bộ các file `Kich-ban-raw-N.txt` PHẢI được tổ chức lưu vào thư mục con chuyên biệt `kich-ban/` bên trong thư mục chương (tự động tạo `kich-ban/` nếu chưa có).
  ```
  [chapter_dir]/
  ├── raw_original.txt
  ├── summary.md
  └── kich-ban/
      ├── Kich-ban-raw-1.txt
      ├── Kich-ban-raw-2.txt
      └── ...
  ```

## 2. Phối hợp Script
- Script chỉ được dùng để đếm số lượng ký tự (đảm bảo không vượt quá giới hạn API của TTS), còn điểm cắt (split point) phải do AI quyết định.
