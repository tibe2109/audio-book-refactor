---
name: arf_10_bgm_dynamic_mixer
description: "Bước 10: Bậc thầy Đạo diễn Âm thanh (A.I Music Director). Phân tích sâu kịch bản, lên timeline âm nhạc theo từng phân cảnh, ghép nhạc nghệ thuật và render file final liền mạch."
---

# BƯỚC 10: ĐẠO DIỄN ÂM THANH A.I (DYNAMIC SCENE-SCORING)

## TRIẾT LÝ CỐT LÕI (CORE PHILOSOPHY)
- **A.I là Tổng Đạo Diễn:** A.I tuyệt đối KHÔNG được giao phó toàn bộ công việc cho một đoạn script Python tự động (như kiểu FFmpeg loop mù quáng). A.I phải là người **đọc hiểu kịch bản, chia khung cảm xúc, và quyết định bài nhạc nào phát ở phút thứ mấy**. Code Python/FFmpeg chỉ đóng vai trò là "công cụ thực thi" bản phác thảo của A.I.
- **Sách nói là Nghệ thuật:** Âm nhạc phải bám sát nhịp điệu của nội dung. Vui dùng nhạc vui, triết lý dùng nhạc Focus. Không lặp lại nhàm chán.
- **Quy tắc Liền mạch (True Seamless):** Các Part cắt lẻ phải nối với nhau hoàn hảo. KHÔNG được dùng Fade-in/Fade-out ở giữa các điểm nối của các Part.

---

## QUY TRÌNH 4 BƯỚC CỦA ĐẠO DIỄN A.I

### Bước 1: Emotional Mapping (Phân tích Cảm xúc theo Phân cảnh)
- A.I tự động đọc lại các file kịch bản của Chương đang xử lý.
- A.I phải chia chương đó thành các **Phân cảnh (Scenes)**. 
  - *Ví dụ:* 
    - Scene 1 (Mở bài): Khơi gợi vấn đề.
    - Scene 2 (Kể chuyện): Các ví dụ lịch sử, tâm lý.
    - Scene 3 (Đúc kết): Bài học, tư duy sâu.
- A.I tự đưa ra **Tone/Mood Guidelines** cho từng Scene. Bám sát các thể loại tích cực: Focus, Uplifting, Relaxing, Baroque, Ghibli, Traditional. Cấm tuyệt đối nhạc ma mị, rùng rợn, u ám.

### Bước 2: Casting & Nhặt Nhạc (Lấy từ Kho hoặc Tải Mới)
- A.I quét kho `bgm_audio_library`. Với mỗi Scene, A.I chọn đích danh 1 bài nhạc cụ thể.
- Nếu bài nhạc quá ngắn, A.I ghi chú sẽ loop nó trong phạm vi của Scene. Nếu nhạc quá dài, A.I ghi chú điểm ngắt.
- Nếu kho nhạc thiếu, A.I tự gọi `yt-dlp` tải bài mới (sử dụng từ khóa chính xác), convert sang MP3, và nạp vào kho trước khi dùng.

### Bước 3: Lên Sơ đồ Thời gian (Timeline Architect)
- A.I đo đạc chính xác thời lượng của các file giọng đọc (`Full_ChapterX_PartY.mp3`).
- A.I vẽ ra một Timeline tổng thể cho cả Chương. 
  - *Ví dụ:* Tổng chương dài 45 phút. 
  - Từ phút 0 -> 10: Nhạc A (Scene 1).
  - Từ phút 10 -> 25: Nhạc B (Scene 2). Giao thoa giữa A và B dùng Crossfade 3 giây.
  - Từ phút 25 -> 45: Nhạc C (Scene 3).

### Bước 4: Viết Lệnh Thực Thi (Master Execution)
- Từ Sơ đồ ở Bước 3, A.I tự tay code ra một đoạn script Python sinh lệnh FFmpeg cực kỳ chi tiết (`-filter_complex`).
- **Quy tắc Bắt buộc khi Render:**
  - **Volume Ducking:** Nhạc nền phải giảm âm lượng (`volume=0.10` hoặc `0.12`) để tôn giọng đọc.
  - **Crossfade:** Chuyển bài hát giữa các Scene phải dùng hiệu ứng nối tiếp (`acrossfade`).
  - **Seamless Part Cut:** Khi xuất ra thành các file `Final_Audio_PartX.mp3`:
    - Chỉ được Fade-in đúng 3 giây ở điểm bắt đầu của **Part 1**.
    - Chỉ được Fade-out đúng 5 giây ở điểm kết thúc của **Part Cuối Cùng**.
    - Các điểm giao cắt giữa Part 1 sang Part 2, Part 2 sang Part 3... **phải cắt thô (Raw cut)**, khớp chính xác thời gian (Offset), tuyệt đối không áp dụng Fade-in/out để đảm bảo tính liên tục khi người nghe phát tự động.
  - **Quy chuẩn Lưu trữ Tập trung Toàn Sách (`Final-[tên-sách]`):**
    - Toàn bộ các file audio master thành phẩm `Final_Audio_{chap_name}_{PartX}.mp3` (đã hòa âm BGM hoàn chỉnh) **BẮT BUỘC** được lưu tập trung vào thư mục tổng thể của cuốn sách: **`Final-[tên-sách]`** (ví dụ: `Final-ProcessGroupsPracticeGuide`, `Final-Eat-that-frog`).
    - Tuyệt đối **KHÔNG lưu file Final vào thư mục riêng của từng chương**. Thư mục con của mỗi chương chỉ lưu kịch bản text, báo cáo QC và các file audio mini `audio_chunks/chunk_*.mp3`, giữ không gian làm việc luôn gọn gàng, chuyên nghiệp và sẵn sàng xuất bản.

---
**TÓM LẠI:** Ở bước này, A.I phải trình bày Sơ đồ Cảm xúc và Sơ đồ Thời gian cho User xem trước, sau đó mới tự động viết script thực thi theo đúng Sơ đồ đó. Xuất file trực tiếp vào thư mục `Final-[tên-sách]`.
