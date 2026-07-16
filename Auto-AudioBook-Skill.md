---
name: auto-audiobook
description: Tự động hóa quy trình đọc sách PDF và xuất ra các kịch bản Audio Book chuẩn Text-to-Speech (TTS) cho Clipchamp với ngắt nghỉ tự nhiên, nhập vai tác giả.
---

# Kỹ năng: Tự động tạo Audio Book Script từ PDF (Auto AudioBook)

Kỹ năng này hướng dẫn AI tự động hóa toàn bộ quy trình đọc một cuốn sách PDF và tạo ra các file kịch bản chuẩn TTS.

## Quy trình thực hiện (AI cần thực hiện đúng theo các bước sau):

### Bước 1: Thu thập thông tin từ người dùng
Ngay khi kỹ năng này được gọi, AI hãy gửi tin nhắn chào mừng và hỏi người dùng 2 thông tin sau:
1. Đường dẫn tuyệt đối đến file PDF của cuốn sách, HOẶC đường dẫn đến THƯ MỤC chứa nhiều file PDF.
2. Đường dẫn thư mục lưu trữ kết quả đầu ra.

*Lưu ý: Không thực hiện các bước tiếp theo cho đến khi người dùng cung cấp đủ thông tin.*

### Bước 2: Phân tích yêu cầu và Khởi tạo Subagents (Nếu cần)
- **Nếu người dùng cung cấp 1 file PDF duy nhất**: AI thực hiện quy trình tuần tự bình thường như bên dưới.
- **Nếu người dùng cung cấp 1 thư mục chứa nhiều file PDF**: AI hãy đóng vai trò Nhạc trưởng (Orchestrator). Sử dụng công cụ `invoke_subagent` để tạo ra nhiều Trợ lý AI phụ (Subagents). Mỗi Subagent sẽ được phân công xử lý độc lập một file PDF theo chuẩn quy trình bên dưới. AI chính chỉ cần theo dõi tiến độ và báo cáo lại cho người dùng khi tất cả Subagents hoàn thành.

### Bước 3: Chuẩn bị môi trường & Đọc văn bản từ PDF
- Tự động chạy lệnh terminal để cài đặt thư viện đọc PDF (nếu môi trường chưa có): `pip install PyMuPDF pdfplumber`
- AI (hoặc Subagent) sử dụng script Python để đọc toàn bộ văn bản từ file PDF đã phân công.
- Phân tích văn bản thô để nhận diện các chương (chapters) của cuốn sách và lưu tạm thời để chuẩn bị chuyển đổi.

### Bước 4: Nhận diện ngôn ngữ & Dịch thuật
- AI kiểm tra ngôn ngữ của văn bản gốc.
- **Nếu là Tiếng Việt**: Bỏ qua bước này và tiến thẳng tới Bước 5.
- **Nếu là Tiếng Anh (hoặc ngôn ngữ khác)**: AI phải tự động thực hiện dịch thuật toàn bộ nội dung sang Tiếng Việt. Yêu cầu bản dịch phải có ngôn ngữ tự nhiên, mượt mà, bám sát nội dung và ý nghĩa của bản gốc (tuyệt đối không dịch máy móc, khô khan).

### Bước 5: Chuyển đổi thành Kịch bản TTS (Áp dụng Tiêu chí Vàng)
AI phải xử lý các văn bản (đã dịch hoặc bản gốc Tiếng Việt) của từng chương theo **ĐÚNG TIÊU CHÍ** sau (Đây là prompt cố định, không cần người dùng cung cấp lại):
- **Nhập vai tác giả**: Giọng văn phải mang sắc thái của chính tác giả đang kể chuyện, truyền cảm, tâm huyết.
- **Không dùng dấu ngoặc kép (`""`), ngoặc đơn `()`, gạch ngang `-`, dấu hai chấm `:`**. Chuyển đổi chúng thành dấu câu đọc được hoặc loại bỏ hoàn toàn.
- **Không dùng dấu chấm lửng (`...`) giữa các từ/giữa câu**. Chỉ dùng `......` (6 dấu chấm) ở cuối đoạn văn để báo hiệu một khoảng lặng dài hoặc khi chuyển sang phần mới.
- **Ngắt nghỉ bằng dấu phẩy (`,`) và dấu chấm (`.`)**: Thêm các dấu câu này vào những chỗ nghỉ hơi tự nhiên (giống như nhịp thở của người thật nói) để AI đọc không bị hụt hơi.
- **Chuyển số thành chữ**: Viết toàn bộ số thành chữ. VD: "80%" -> "tám mươi phần trăm", "Chương 5" -> "Chương năm".
- **Việt hóa tên riêng tiếng Anh**: Phiên âm tên nước ngoài để AI tiếng Việt đọc chính xác. VD: "Pareto" -> "Pa rê tô", "Victor" -> "Vích to".
- **Chia nhỏ kịch bản**: Nếu chương sách quá dài, chia thành nhiều phần. Mỗi phần (kịch bản) dài vừa phải (khoảng 15-20 câu). 

### Bước 6: Lưu trữ cấu trúc thư mục
Tạo cấu trúc thư mục tại đường dẫn đầu ra mà người dùng đã cung cấp, ví dụ:
`[Thư mục đầu ra]/[Tên sách]/Chuong-1/Kich-ban-1.txt`
`[Thư mục đầu ra]/[Tên sách]/Chuong-1/Kich-ban-2.txt`
`[Thư mục đầu ra]/[Tên sách]/Chuong-2/Kich-ban-1.txt`

Ghi nội dung của từng kịch bản vào các file txt tương ứng.

### Bước 7: Dọn dẹp thư mục làm việc
AI hãy chủ động xóa bỏ tất cả các file nháp, file text thô (raw chapters), hoặc các file tạm thời sinh ra trong quá trình làm việc, đảm bảo thư mục dự án gọn gàng và chỉ giữ lại những file kịch bản kết quả quan trọng cuối cùng.

### Bước 8: Báo cáo hoàn tất
Sau khi ghi xong tất cả các chương và dọn dẹp, AI hãy thông báo cho người dùng biết dự án đã hoàn tất, in ra màn hình cấu trúc thư mục kết quả, và chúc người dùng làm video/audio thành công!
