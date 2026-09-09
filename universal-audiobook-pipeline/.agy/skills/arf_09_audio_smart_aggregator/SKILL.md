---
name: arf_09_audio_smart_aggregator
description: "Bước 9 - A.I trực tiếp phân tích các audio kịch bản mini, lên kế hoạch gộp file full (20-30 phút) theo logic tối ưu."
---

# Kỹ năng 09: Audio Smart Aggregator (Phân Tích & Lên Kế Hoạch Gom File)

**TRIẾT LÝ CỐT LÕI:** Tuyệt đối không nhắm mắt gom file bừa bãi. A.I phải đóng vai trò là Nhà Sản Xuất (Producer), tự mình quét, tính toán, và đưa ra một "Bản Kế Hoạch" rõ ràng trước khi thực thi.

## 1. Trình tự làm việc của A.I (Bắt buộc)

### Bước 1: Quét & Phân Tích Dữ Liệu
- A.I sử dụng các lệnh Terminal hoặc tool đọc file để kiểm tra danh sách các file audio kịch bản mini (ví dụ: `chunk_1.mp3`, `chunk_2.mp3`...) đã được tạo ra từ Bước 8.
- Tính toán thời lượng (bằng công cụ `ffprobe` hoặc ước tính từ số chữ của kịch bản: ~3000 ký tự = 3.5 phút).

### Bước 2: Lập Kế Hoạch Gom Nhóm (Toán học & Logic Cân Bằng)
- **Mục tiêu:** Mỗi file Audio Full phải dài từ **25 đến 35 phút** và **KHÔNG CÓ FILE NÀO DƯỚI 25 PHÚT** (trừ phi tổng thời lượng toàn chương nhỏ hơn 25 phút).
- **Thuật toán Cân Bằng (Equitable Distribution):** Tuyệt đối KHÔNG gộp theo kiểu nhồi nhét (Greedy) dẫn đến tập cuối bị thừa một đoạn quá ngắn (vd: 5-7 phút). A.I phải:
  1. Tính Tổng thời lượng toàn bộ chương (Total Duration).
  2. Quyết định Số tập lý tưởng `N = max(1, round(Total Duration / 30 phút))`.
  3. Tính thời lượng mục tiêu cho mỗi tập: `Target = Total Duration / N` (ví dụ: Tổng 86 phút / 3 tập = ~28.6 phút/tập).
  4. Gom các chunk sao cho bám sát target 28.6 phút này nhất (sẽ dao động tự nhiên quanh mức 25 - 35 phút).
- A.I tự vạch ra kế hoạch ghép file trên màn hình cho User xem (Bảng kế hoạch). 
  - *Ví dụ:* 
    - Tập 1 (Part 1): Gồm chunk 1 đến 8 (~28.5 phút).
    - Tập 2 (Part 2): Gồm chunk 9 đến 15 (~29.1 phút).

### Bước 3: Thực thi
- Chỉ sau khi phân tích logic và (tùy chọn) được User duyệt qua, A.I mới tiến hành tạo danh sách `concat` và gọi lệnh (ví dụ FFmpeg) để nối các file mini thành `Full_ChapterX_PartY.mp3`.

### Bước 4: Giám Sát & Nghiệm Thu (Post-Execution Validation)
- Tuyệt đối không phó mặc cho Script. Sau khi Script/công cụ gom file chạy xong, A.I **BẮT BUỘC** phải kiểm tra lại:
  - File `Full_ChapterX...mp3` có được tạo ra không?
  - Dung lượng file có hợp lý không? (Tránh lỗi file rỗng hoặc lỗi nối file hỏng).
  - Báo cáo kết quả trực tiếp cho User để nghiệm thu.

---

## 2. Quy Chuẩn Lưu Trữ Tập Trung Toàn Sách (`Full-[tên-sách]`)

- **Tên thư mục đích:** Toàn bộ các file audio ghép `Full_{chap_name}_{PartX}.mp3` (bản thu giọng nói thuần khiết, không nhạc nền) của toàn bộ các chương trong sách **BẮT BUỘC** được lưu tập trung vào thư mục tổng thể của cuốn sách có tên: **`Full-[tên-sách]`** (ví dụ: `Full-ProcessGroupsPracticeGuide`, `Full-Eat-that-frog`).
- **Nghiêm cấm lưu vào thư mục chương con:** Tuyệt đối **KHÔNG lưu file Full vào thư mục riêng của từng chương**. Thư mục con của mỗi chương chỉ lưu kịch bản text, báo cáo QC và các file audio mini `audio_chunks/chunk_*.mp3`. Điều này giúp không gian làm việc luôn tinh gọn, ngăn nắp và dễ dàng kiểm âm toàn bộ các tập sách nói cùng lúc.
