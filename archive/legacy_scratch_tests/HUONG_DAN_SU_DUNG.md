# 📖 CẨM NANG SẢN XUẤT SÁCH NÓI CHUYÊN NGHIỆP
## HƯỚNG DẪN DÀNH CHO NGƯỜI DÙNG KHÔNG CẦN BIẾT LẬP TRÌNH (v2.0)

Chào mừng bạn đến với **Hệ Thống Sản Xuất Sách Nói Tự Động Vạn Năng**! Tài liệu này được thiết kế để bất kỳ ai, dù không rành về kỹ thuật hay lập trình, cũng có thể tự tay tạo ra những bộ Sách Nói (Audiobook) chất lượng cao chuẩn phát thanh.

---

## ⚡ PHẦN 1: CÀI ĐẶT 1-CLICK (CHỈ LÀM 1 LẦN DUY NHẤT)

Khi tải hoặc copy thư mục dự án về bất kỳ máy tính nào:

1. Mở thư mục dự án:
2. Nhấp đúp chuột trái (Double-Click) vào file:
   👉 **`setup_environment.bat`**
3. Màn hình màu đen sẽ hiện ra và máy tính sẽ tự động:
   - Kiểm tra Python.
   - Tạo môi trường ảo riêng biệt (`venv`).
   - Cài đặt đầy đủ các thư viện âm thanh và giọng đọc AI.
   - Tự động tải công cụ xử lý âm thanh FFmpeg (nếu máy tính chưa có).
4. Khi thấy thông báo màu xanh: **"🎉 CÀI ĐẶT HOÀN TẤT 100%! BẤM PHÍM BẤT KỲ ĐỂ HOÀN TẤT"**, bạn chỉ cần bấm phím cách (Space) là xong!

---

## 📚 PHẦN 2: CHUẨN BỊ SÁCH ĐẦU VÀO

Bạn có thể làm sách theo một trong hai cách cực kỳ linh hoạt:

### Cách 1: Bạn đã có sẵn file sách PDF
1. Sao chép file PDF của bạn vào thư mục:
   📁 **`Docs\`** (Ví dụ: `Docs\Dac-Nhan-Tam.pdf`).
2. Mở trợ lý AI (Antigravity IDE hoặc bất kỳ AI nào bạn dùng), nhắn tin:
   > *"Tôi đã để cuốn sách Dac-Nhan-Tam.pdf trong thư mục Docs. Hãy bắt đầu tạo sách nói cho tôi!"*

### Cách 2: Bạn đã có đoạn kịch bản hoặc văn bản chữ
1. Mở thư mục: **`Kich-ban-clipchamp\`**.
2. Tạo thư mục sách của bạn, ví dụ: `Kich-ban-clipchamp\Dac-Nhan-Tam\01-chuong-1\`.
3. Lưu văn bản của bạn vào file có tên **`raw_original.txt`** trong thư mục đó.

---

## 🎮 PHẦN 3: RA LỆNH CHO TRỢ LÝ AI BẰNG TIẾNG VIỆT TỰ NHIÊN

Bạn không cần gõ lệnh phức tạp, chỉ cần sao chép (copy) các câu nói dưới đây dán vào khung chat với AI:

### 1. Khi muốn AI tự động làm trọn gói từ A đến Z:
> *"Hãy áp dụng Quy trình Universal Audiobook Workflow 10 bước để sản xuất sách nói hoàn chỉnh cho Chương 1 cuốn Đắc Nhân Tâm. Tự động kiểm tra chất lượng và hòa âm nhạc nền giúp tôi."*

### 2. Khi muốn AI chuyển thể văn bản thô thành kịch bản diễn đọc chuẩn phát thanh:
> *"Tôi gửi bạn văn bản gốc dưới đây. Hãy chuyển đổi đoạn văn bản này thành kịch bản sách nói chuẩn phát thanh: bỏ số trang, viết 100% số thành chữ cái tiếng Việt, câu dưới 30 từ, thêm dấu phẩy ngắt nghỉ lấy hơi và khoảng lặng '. ......' ở các đoạn chuyển ý. Giữ nguyên thuật ngữ tiếng Anh gốc."*

### 3. Khi kịch bản bị báo lỗi ký tự cấm:
> *"Hãy tự động sửa chữa toàn bộ các lỗi ký tự cấm và số trần trong kịch bản theo đúng 7 Cổng Kiểm Toán Chất Lượng rồi chạy tiếp cho tôi."*

---

## 🚀 PHẦN 4: CHẠY BẰNG MENU 1-CLICK VỚI `run_audiobook.bat`

Nếu bạn muốn máy tính tự động thu âm và lồng nhạc mà không cần mở giao diện chat với AI:

1. Nhấp đúp chuột vào file:
   👉 **`run_audiobook.bat`**
2. Bảng Menu điều khiển tiếng Việt sẽ hiện ra:
   ```text
   ================================================================================
        HỆ THỐNG SẢN XUẤT SÁCH NÓI TỰ ĐỘNG VẠN NĂNG (UNIVERSAL AUDIOBOOK v2.0)
   ================================================================================

     [1] Xử lý tự động 1 chương cụ thể (Kiểm toán QC -> Thu âm Song thanh -> Hòa âm BGM)
     [2] Xử lý tự động TOÀN BỘ các chương chưa hoàn thành
     [3] Kiểm toán chất lượng kịch bản (Thẩm định 7 Cổng Hard Quality Gates)
     [4] Kiểm tra hoặc Cài đặt lại môi trường hệ thống (Setup/Repair)
     [0] Thoát

   ================================================================================
   Nhập lựa chọn của bạn (1/2/3/4/0): 
   ```
3. Bạn chỉ cần gõ số **1** hoặc **2** rồi bấm **Enter**. Máy tính sẽ tự động chạy toàn bộ quy trình cho bạn.

---

## 🎧 PHẦN 5: LẤY FILE ÂM THANH KẾT QUẢ Ở ĐÂU?

Sau khi hệ thống thông báo thành công, toàn bộ các file sách nói chất lượng cao nhất sẽ được đặt tại:

👉 Thư mục phát hành trung tâm: **`audio_output\`**  
*(Ví dụ: `audio_output\Final_Audio_01_chuong_1_Part1.mp3`)*

### Điểm đặc biệt của file sách nói thành phẩm:
- **Độ dài lý tưởng:** Mỗi tập dài đúng **25 đến 35 phút** — vừa vặn cho một chuyến đi xe, buổi tập thể dục hoặc nghe trước khi ngủ.
- **Giọng đọc tự nhiên như người thật:** Nhờ công nghệ AI song thanh, tiếng Việt đọc truyền cảm, các từ tiếng Anh (như Leader, Marketing, Agile) được phát âm chuẩn bản ngữ quốc tế.
- **Nhạc nền chuyên nghiệp (Dynamic BGM):** Nhạc nền du dương, nhẹ nhàng, tự động nhỏ tiếng khi có giọng đọc và chuyển đổi cảm xúc mượt mà qua các phần của chương sách.

---

## ❓ GIẢI ĐÁP CÁC CÂU HỎI THƯỜNG GẶP (FAQ)

**1. Máy tính không có kết nối mạng có chạy được không?**  
- Khâu chuyển văn bản thành giọng nói (TTS) cần kết nối Internet để kết nối với máy chủ AI giọng đọc Microsoft Neural. Các khâu xử lý kịch bản, ghép file và hòa âm BGM hoàn toàn chạy trên máy tính không tốn dữ liệu mạng.

**2. Nếu tôi muốn đổi nhạc nền khác thì làm thế nào?**  
- Bạn chỉ cần copy file nhạc MP3 yêu thích vào thư mục `bgm_audio_library\` hoặc đặt tên là `nhac-nen.mp3` ở thư mục gốc của dự án. Hệ thống sẽ tự động nhận diện và sử dụng.

**3. Tại sao file audio không bao giờ dài quá 35 phút?**  
- Đây là quy chuẩn vàng của hệ thống để đảm bảo người nghe không bị mỏi tai và file dễ dàng đăng tải lên YouTube, Spotify, Podcast mà không bị quá tải dung lượng. Nếu chương dài 60 phút, hệ thống sẽ tự động chia thành Part 1 (30 phút) và Part 2 (30 phút) rất cân bằng và khoa học.
