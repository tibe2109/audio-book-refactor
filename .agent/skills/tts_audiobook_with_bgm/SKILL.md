---
name: tts_audiobook_with_bgm
description: Tự động hóa tạo Audiobook bằng TTS, ghép chương, và lồng nhạc nền.
---

# TTS Audiobook with BGM Skill

Skill này tự động hóa quy trình tạo sách nói (Audiobook). Nó sẽ đọc các thư mục chứa các chương kịch bản (được đánh số), sau đó chuyển đổi các file text thành giọng nói bằng AI của Microsoft (thông qua `edge-tts`), gộp các file lại thành từng chương, gộp 3 chương thành một nhóm lớn, và cuối cùng lồng nhạc nền (Background Music) vào file tổng với một đoạn ngắt tịnh tiến mỗi 5 phút để nhạc nền không bị nhàm chán.

## Hướng dẫn thực hiện

Khi người dùng yêu cầu kích hoạt skill này (hoặc yêu cầu tạo sách nói/lồng nhạc), bạn với tư cách là trợ lý AI (Antigravity) hãy thực hiện theo đúng các bước sau đây:

### Bước 1: Thu thập thông tin từ người dùng
Bạn bắt buộc phải hỏi người dùng 2 câu hỏi sau để lấy đường dẫn chính xác:
1. **Đường dẫn đến thư mục chứa các thư mục kịch bản?** (Ví dụ: `/mnt/d/Solution/Audio-Book-Refactor/Kich-ban-clipchamp/Eat-that-frog`)
2. **Bạn có muốn lồng nhạc nền không? Nếu có, xin vui lòng cho biết đường dẫn đến file nhạc nền?** (Ví dụ: `/mnt/d/Solution/Audio-Book-Refactor/nhac-nen.mp3`)

Đợi người dùng phản hồi. Nếu người dùng không cung cấp đủ thông tin, hãy tiếp tục hỏi cho rõ ràng.

### Bước 2: Tự động kiểm tra và cài đặt môi trường
Bạn (AI) **PHẢI** thực hiện kiểm tra và tự động cài đặt các công cụ cần thiết trước khi xử lý âm thanh. Cần đảm bảo tất cả cài đặt thành công thì mới được phép đi tiếp sang Bước 3:
1. Dùng `run_command` chạy lệnh `ffmpeg -version`. Nếu máy chưa có, hãy thử tự động cài đặt bằng lệnh `sudo apt update && sudo apt install -y ffmpeg`. Nếu tiến trình bị kẹt do hệ thống đòi mật khẩu (sudo password), hãy tạm dừng và nhắc người dùng mở terminal tự chạy lệnh đó.
2. Dùng `run_command` chạy lệnh kiểm tra/cài đặt `edge-tts` bằng lệnh `python3 -m pip install edge-tts`. Nếu bị lỗi môi trường Python (externally-managed-environment), hãy linh hoạt tự tạo virtual environment (`python3 -m venv venv && ./venv/bin/pip install edge-tts`).
Chỉ khi nào bạn xác nhận được `ffmpeg` và `edge-tts` đã cài thành công và sẵn sàng hoạt động thì mới được đi tiếp.

### Bước 2.5: Kiểm tra Báo Cáo QC (QC_Report.md) - BẮT BUỘC
Hệ thống **TUYỆT ĐỐI KHÔNG ĐƯỢC PHÉP** chạy tạo âm thanh bừa bãi nếu kịch bản chưa được QC (Quality Control). 
- Bạn (AI) phải tìm và đọc file `QC_Report.md` nằm bên trong thư mục kịch bản (Ví dụ: `Kich-ban-clipchamp/Nghe-thuat-quyen-ru/QC_Report.md`).
- Nếu file này không tồn tại, hoặc người dùng chưa đánh dấu `[x]` (hoàn thành) cho các chương, bạn phải dừng lại và yêu cầu người dùng nghiệm thu kịch bản trước.
- Script sinh Audio (`audio_pipeline.py`) đã được tối ưu để tự động đọc file này và **chỉ sinh âm thanh cho các chương đã được verify `[x]`**.

### Bước 3: Khởi chạy tiến trình
Sử dụng công cụ `run_command` để chạy file script pipeline đã được đóng gói sẵn trong thư mục của skill này.
- **Script Path:** `scripts/audio_pipeline.py` (nằm chung thư mục với file `SKILL.md` này)
- **Lệnh thực thi:**
  ```bash
  python /mnt/d/Solution/Audio-Book-Refactor/.agy/skills/tts_audiobook_with_bgm/scripts/audio_pipeline.py --input_dir "<INPUT_DIR>" --bgm "<BGM_FILE>"
  ```
  *(Nếu người dùng chọn không chèn nhạc, bạn hãy bỏ qua tham số `--bgm "<BGM_FILE>"`).*

### Bước 4: Theo dõi và thông báo
Tiến trình có thể tốn khá nhiều thời gian (thường từ 5 đến 30 phút tùy lượng kịch bản). Hãy khởi chạy lệnh này trong chế độ ngầm (Background Task) bằng cách đặt `WaitMsBeforeAsync` nhỏ.
Thông báo cho người dùng biết rằng công việc đang được tiến hành tự động và hãy để họ thoải mái đi làm việc khác, bạn sẽ báo cáo khi hoàn tất!
