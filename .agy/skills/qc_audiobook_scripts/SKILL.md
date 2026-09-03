---
name: qc_audiobook_scripts
description: Tự động kiểm tra (QC) chất lượng kịch bản sách nói, đảm bảo đúng cấu trúc thư mục, độ dài ký tự và tiêu chuẩn văn bản.
---

# QC Audiobook Scripts Skill

Skill này đóng vai trò như một nhân viên Kiểm tra Chất lượng (QC). Nó sẽ quét qua toàn bộ các thư mục chương sách và file kịch bản để kiểm tra các tiêu chí khắt khe nhất nhằm đảm bảo quá trình tạo âm thanh (TTS) sau này không bị lỗi hoặc đọc sai định dạng.

## Hướng dẫn thực hiện

Khi người dùng yêu cầu kiểm tra hoặc QC kịch bản, bạn (AI) hãy thực hiện các bước sau:

### Bước 1: Lấy đường dẫn thư mục kịch bản
Hãy hỏi người dùng đường dẫn đến thư mục chứa các kịch bản cần kiểm tra (Ví dụ: `/mnt/d/Solution/Audio-Book-Refactor/Kich-ban-clipchamp/Nghe-thuat-quyen-ru`).

### Bước 2: Chạy công cụ kiểm tra tự động
Sử dụng công cụ `run_command` để chạy file script kiểm tra đã được đóng gói sẵn trong thư mục của skill này:
- **Lệnh thực thi:**
  ```bash
  python /mnt/d/Solution/Audio-Book-Refactor/.agy/skills/qc_audiobook_scripts/scripts/qc_pipeline.py --input_dir "<INPUT_DIR>"
  ```
Lệnh này sẽ quét toàn bộ và xuất ra một file `QC_Report.md` tại thư mục của người dùng.

### Bước 3: Đọc kết quả và Xử lý
Hãy dùng công cụ `view_file` để đọc file `QC_Report.md` vừa được tạo ra.
1. **Trong file Báo cáo sẽ luôn hiển thị mục: TẤT CẢ ĐỀU HOÀN HẢO / VERIFIED 100%**:
   - Đây là danh sách các chương đã vượt qua bài test. Hãy thông báo cho người dùng biết để họ có thể yên tâm chuyển ngay các chương này qua tiến trình tạo Audio nếu muốn.
2. **Nếu báo cáo liệt kê CÁC SAI SÓT (Báo cáo sẽ dừng lại ở NGAY CHƯƠNG ĐẦU TIÊN CÓ LỖI)**:
   - Thông báo rõ ràng cho người dùng biết lỗi đó là gì và thuộc về CHƯƠNG NÀO. 
   - **TRƯỜNG HỢP LỖI ĐỊNH DẠNG (Format):** NGAY LẬP TỨC báo người dùng kích hoạt skill `generate_audiobook_scripts` (tại `D:\Solution\Audio-Book-Refactor\.agy\skills\generate_audiobook_scripts\SKILL.md`) để FIX XONG CHƯƠNG ĐÓ.
   - **TRƯỜNG HỢP RED FLAG (Cảnh báo hao hụt nội dung):** Nếu báo cáo có chứa cờ đỏ "RED FLAG", điều này có nghĩa là số chữ bị chênh lệch quá 15%. Bạn (AI) phải ĐÓNG VAI LÀ THẨM ĐỊNH VIÊN, tự động sử dụng công cụ đọc file `raw_original.txt` và các file kịch bản của chương đó để so sánh ngữ nghĩa (Semantic QC). 
     - Nếu phát hiện bớt xén thật sự -> Cảnh báo cho người dùng và yêu cầu gọi skill `generate_audiobook_scripts` để làm lại.
     - Nếu chỉ là do dịch thuật/số hóa (không mất ý) -> Bỏ qua lỗi này và xác nhận thủ công là PASS.
   - Nhấn mạnh rằng phải FIX XONG VÀ PASS QC CHO CHƯƠNG NÀY thì hệ thống QC mới chịu quét tiếp các chương tiếp theo. Tuyệt đối không nhảy cóc!
