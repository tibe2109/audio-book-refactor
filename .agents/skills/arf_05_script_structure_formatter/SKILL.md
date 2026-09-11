---
name: arf_05_script_structure_formatter
description: Bước 5 - AI chèn nhịp nghỉ (. ......) thông minh theo cảm nhận ngữ nghĩa, tránh máy móc.
---

# Kỹ năng 05: Formatting & Pacing (A.I 100%)

**TRIẾT LÝ CỐT LÕI:** Sự khó chịu nhất của sách nói là ngắt nghỉ máy móc. AI phải đọc, cảm nhận nội dung và đặt điểm ngắt nghỉ `. ......` như một người đọc thật đang lấy hơi và truyền cảm hứng.

## 1. Nhiệm vụ của AI
- Tách bạch rõ ràng Tiêu đề và Thân bài.
- Chèn `. ......` (nghỉ 1.5 - 2s) ở sau tiêu đề, sau những luận điểm sâu sắc cần người nghe ngẫm nghĩ, hoặc sau các đoạn văn dài.
- Tuyệt đối KHÔNG chèn bừa bãi làm gãy mạch ý nghĩa, gây hiểu lầm ngữ cảnh.
- Root Agent gọi Sub-agents tự động xử lý trực tiếp trên các file `Kich-ban-raw-N.txt` trong thư mục con `kich-ban/` của mỗi chương (hỗ trợ tự động fallback tìm ở thư mục cha nếu là dự án cũ).
