# 📖 CẨM NANG HƯỚNG DẪN SỬ DỤNG DÀNH CHO NGƯỜI DÙNG PHỔ THÔNG
## SẢN XUẤT SÁCH NÓI TỰ ĐỘNG CHUẨN PHÁT THANH TRÊN MỌI HỆ ĐIỀU HÀNH (v2.0)

Chào mừng bạn đến với **Universal Audiobook Pipeline**! Hướng dẫn này sẽ giúp bạn biến một cuốn sách PDF hoặc một đoạn văn bản thành một tác phẩm Sách Nói (Audiobook) có giọng đọc truyền cảm và nhạc nền du dương chỉ với vài thao tác chuột đơn giản.

---

## ⚡ BƯỚC 1: CÀI ĐẶT 1-CLICK (CHỈ LÀM 1 LẦN)

Khi bạn mang thư mục này sang một máy tính mới:

- **Nếu bạn dùng máy tính Windows:**
  Nhấp đúp chuột vào file: 👉 **`setup.bat`**
- **Nếu bạn dùng máy tính Linux hoặc Mac:**
  Mở Terminal tại thư mục này và gõ:
  ```bash
  chmod +x setup.sh run.sh
  ./setup.sh
  ```

Hệ thống sẽ tự động tạo môi trường làm việc, cài đặt thư viện cần thiết và chuẩn bị công cụ xử lý âm thanh. Khi màn hình hiện thông báo hoàn thành, bạn chỉ cần bấm một phím bất kỳ là xong.

---

## 📚 BƯỚC 2: CHUẨN BỊ SÁCH ĐẦU VÀO

Bạn có thể làm sách theo một trong hai cách:

### Cách A: Bạn có file sách PDF
1. Chuẩn bị file PDF sách gốc (ví dụ: `Dac-Nhan-Tam.pdf`).
2. Mở file **`run.bat`** (trên Windows) hoặc **`./run.sh`** (trên Linux/Mac), chọn tính năng **[4]** để hệ thống tự bóc tách thành các chương sách.
3. Hoặc bạn chỉ cần gửi file cho AI (Antigravity, Claude, ChatGPT, Cursor) và nhắn:
   > *"Tôi có file PDF sách này, hãy bắt đầu quy trình tạo sách nói giúp tôi!"*

### Cách B: Bạn có đoạn văn bản chữ
1. Mở thư mục **`input_books\`**.
2. Tạo thư mục sách của bạn, ví dụ: `input_books\Dac-Nhan-Tam\01-chuong-1\`.
3. Dán văn bản vào file có tên **`raw_original.txt`** trong thư mục đó.

---

## 🚀 BƯỚC 3: SẢN XUẤT SÁCH NÓI

Bạn có thể chọn 1 trong 2 cách sau:

### Cách 1: Sử dụng Menu có sẵn (Không cần mở AI)
1. Nhấp đúp chuột vào file: 👉 **`run.bat`** (hoặc chạy `./run.sh` trên Linux/Mac).
2. Màn hình điều khiển thân thiện sẽ hiện ra:
   ```text
   ================================================================================
         HỆ THỐNG SẢN XUẤT SÁCH NÓI TỰ ĐỘNG VẠN NĂNG (UNIVERSAL AUDIOBOOK v2.0)
   ================================================================================

     [1] Xử lý tự động 1 chương cụ thể (Kiểm toán QC -> Thu âm Song thanh -> Hòa âm BGM)
     [2] Xử lý tự động TOÀN BỘ các chương chưa hoàn thành
     [3] Kiểm toán chất lượng kịch bản (Thẩm định 7 Cổng Hard Quality Gates)
     [4] Khởi tạo dự án sách mới từ file PDF (Bước 01: Extract Structure)
     [5] Kiểm tra hoặc Cài đặt lại môi trường hệ thống (Setup/Repair)
     [0] Thoát

   ================================================================================
   Nhập lựa chọn của bạn (1/2/3/4/5/0): 
   ```
3. Gõ số **1** hoặc **2** rồi bấm **Enter**. Hệ thống sẽ tự động thực hiện toàn bộ khâu kiểm tra chất lượng, đọc giọng AI và ghép nhạc nền.

### Cách 2: Ra lệnh cho Trợ lý AI (Antigravity, Claude, ChatGPT, Cursor)
Khi bạn mở thư mục này trong các công cụ AI, AI đã tự động đọc file `AGENTS.md` và hiểu toàn bộ quy trình. Bạn chỉ cần nhắn câu lệnh bằng tiếng Việt tự nhiên:
> *"Hãy áp dụng Universal Audiobook Pipeline để sản xuất sách nói hoàn chỉnh cho cuốn sách trong thư mục input_books. Tự động kiểm tra chất lượng và hòa âm nhạc nền giúp tôi."*

---

## 🎧 BƯỚC 4: NHẬN FILE ÂM THANH MASTER

Sau khi quá trình kết thúc, toàn bộ các file sách nói chất lượng cao nhất sẽ nằm tại:

👉 Thư mục: **`audio_output\`**  
*(Ví dụ: `audio_output\Final_Audio_01_chuong_1_Part1.mp3`)*

### Ưu điểm vượt trội của file thành phẩm:
- **Độ dài chuẩn 25 – 35 phút:** Vừa vặn cho một chuyến đi xe hoặc một buổi tập thể dục, không bao giờ bị quá dài gây mệt mỏi.
- **Giọng đọc song thanh tự nhiên:** Tiếng Việt đọc truyền cảm, ấm áp; các từ tiếng Anh (như Leader, Marketing, Agile, Scope Creep...) được giọng bản ngữ quốc tế phát âm chuẩn xác 100%.
- **Nhạc nền chuyên nghiệp 3 phân cảnh:** Nhạc nền Baroque và Piano du dương, tự động nhỏ tiếng khi có giọng đọc (Ducking -20dB) và chuyển tiếp mượt mà theo cảm xúc từng phần của chương sách.
