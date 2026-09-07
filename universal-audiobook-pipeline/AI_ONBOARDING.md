# 🧭 AI ONBOARDING & AUTONOMOUS BOOTSTRAPPING GUIDE
## HƯỚNG DẪN TỰ KHỞI ĐỘNG VÀ VẬN HÀNH DÀNH CHO MỌI MÔ HÌNH AI

Khi người dùng mở thư mục này trong bất kỳ IDE hoặc công cụ AI nào (**Antigravity, Claude Code, OpenAI Codex, Cursor, Windsurf, v.v.**), AI cần tuân theo quy trình 4 giai đoạn tự vận hành dưới đây.

---

### GIAI ĐOẠN 1: TỰ PHÂN TÍCH HỆ THỐNG (ENVIRONMENT RECONNAISSANCE)
Khi người dùng lần đầu giao việc hoặc hỏi về dự án, AI tự chạy ngầm các lệnh kiểm tra:

1. **Nhận diện Hệ điều hành (OS):**
   - Windows: Kiểm tra PowerShell hoặc CMD.
   - Linux / macOS: Kiểm tra bash shell.
2. **Kiểm tra Môi trường Python:**
   ```bash
   python --version || python3 --version
   ```
   Nếu chưa cài Python hoặc phiên bản < 3.10, AI thông báo ngay cho người dùng đường dẫn cài đặt chính thức (python.org).
3. **Kiểm tra Môi trường ảo (venv) & Dependencies:**
   - Nếu thư mục `venv/` chưa tồn tại:
     - Trên Windows: Chạy `setup.bat`.
     - Trên Linux/Mac: Chạy `bash setup.sh`.
   - Nếu `venv/` đã có sẵn: Kích hoạt venv trước khi chạy bất kỳ script nào.
4. **Kiểm tra Bộ giải mã Âm thanh (FFmpeg):**
   - Hệ thống đã tích hợp cơ chế 5 tầng tại `core/config.py`. Nếu máy tính chưa có FFmpeg, thư viện `imageio-ffmpeg` trong `requirements.txt` sẽ tự động đảm nhiệm vai trò này mà không gây crash.

---

### GIAI ĐOẠN 2: KHẢO SÁT DỮ LIỆU ĐẦU VÀO (INPUT INVENTORY)
AI kiểm tra xem người dùng đang có sẵn dữ liệu ở dạng nào:

- **Trường hợp A: File PDF mới nguyên** (ví dụ trong thư mục `Docs/` hoặc đường dẫn người dùng đưa):
  - Kích hoạt **Bước 01** (`arf_01_pdf_structure_extractor`) để bóc tách cấu trúc, lọc bỏ header/footer, số trang và tạo ra các thư mục chương kèm `raw_original.txt`.
- **Trường hợp B: Đã có kịch bản thô hoặc văn bản chữ**:
  - Hướng dẫn người dùng đặt vào `input_books/[Tên-Sách]/[Tên-Chương]/raw_original.txt`.
- **Trường hợp C: Đã có kịch bản `Kich-ban-*.txt`**:
  - Kiểm tra xem chương đó đã có `QC_Report.md` với `100% PASSED` chưa. Nếu chưa, chạy ngay khâu kiểm toán 7 Quality Gates.

---

### GIAI ĐOẠN 3: TỰ ĐỘNG THẨM ĐỊNH & TỰ PHỤC HỒI (SELF-HEALING)
Tại **Bước 07 (QC Auditor)**:
1. AI chạy hàm `wf.audit_quality_gates()`.
2. Nếu phát hiện vi phạm:
   - Sót ký tự cấm: `()`, `""`, `:`, `;`, `—`, `[]`.
   - Sót số trần: `2026`, `15%`, `3.5`.
   - Sót câu tham chiếu giấy in: *"xem hình 1.2"*, *"bảng trang bên"*.
3. **AI TUYỆT ĐỐI KHÔNG DỪNG LẠI CHỜ NGƯỜI DÙNG**. AI phải tự động mở file `Kich-ban-*.txt` đó ra, sửa chữa triệt để các lỗi trên, sau đó chạy lại QC cho đến khi đạt `100% PASSED`.

---

### GIAI ĐOẠN 4: SẢN XUẤT VÀ PHÁT HÀNH MASTER FINAL
Khi QC đã thông qua:
1. Gọi động cơ song thanh **Seamless Dual-Voice** (`vi-VN-NamMinhNeural` x `en-US-BrianMultilingualNeural`) để thu âm từng chunk.
2. Gom nhóm các chunk theo thuật toán cân bằng toán học **[25 – 35 phút]** (khóa cứng không vượt quá 35 phút).
3. Đạo diễn hòa âm **Dynamic BGM** theo 3 phân cảnh cảm xúc (Baroque 35% -> Deep Focus 40% -> Piano 25%), hạ volume ducking -20dB dưới giọng đọc.
4. Xuất file Master ra thư mục phát hành tập trung: `audio_output/` và thông báo hoàn thành kèm đường dẫn file cho người dùng.
