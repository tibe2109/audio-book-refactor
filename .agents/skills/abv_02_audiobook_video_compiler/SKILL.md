---
name: abv_02_audiobook_video_compiler
description: "Kỹ năng điều phối dựng và kết xuất Video Sách Nói chuẩn mực hàng loạt (Audiobook Video Compiler & Batch Renderer) dựa trên kho âm thanh hoàn thiện trong thư mục Final Audio (Final-[Tên-Sách]). Kỹ năng sở hữu trí tuệ tự động nhận diện đường dẫn đầu vào linh hoạt: tiếp nhận trực tiếp thư mục Final hoặc thư mục nguồn tác phẩm để phân giải chính xác thư viện tệp Final_Audio_*.mp3. Thiết lập hệ thống quản lý tiến trình nguyên tử (Atomic Progress Manifest) qua tệp .abv_manifest.json lưu trực tiếp tại thư mục Final, theo dõi trạng thái từng video, thời lượng, dung lượng và timestamp, tự động nhận diện video đã hoàn thành để bỏ qua (Atomic Resume & Skip Completed), loại bỏ nguy cơ gián đoạn hoặc dựng lặp. Tích hợp động cơ FFmpeg biên dịch video MP4 Full HD 1080p (1920x1080, 25 FPS, H.264 High Profile, CRF 20, âm thanh AAC 192kbps) phân bổ đều thư viện 10 ảnh nền điện ảnh (bg_01.jpg đến bg_10.jpg từ Bước 01) trải dài suốt thời lượng chương với chuyển cảnh êm ái. Bắt buộc kích hoạt mảng Sub-agents chuyên trách song song (invoke_subagent) phân chia theo từng lô chương (Batch Processing) để tăng tốc độ kết xuất toàn tác phẩm lên gấp 3 đến 5 lần so với thực thi đơn lẻ. Toàn bộ video xuất xưởng lưu trực tiếp tại thư mục Final dưới định dạng Final_Video_*.mp4 kèm báo cáo Master_Video_Report.md."
---

# 🎬 ABV-02: AUDIOBOOK VIDEO COMPILER & BATCH RENDERER
## QUY TRÌNH THAO TÁC CHUẨN (SOP) DỰNG VÀ KẾT XUẤT VIDEO SÁCH NÓI TOÀN BỘ CÁC CHƯƠNG

---

## 1. SOP / ĐẶC TẢ KỸ THUẬT (SPECIFICATION)
`abv_02_audiobook_video_compiler` là kỹ năng bước 2 trong nhánh sản xuất Video Sách Nói (ABV Pipeline), đảm nhiệm vai trò **Kỹ Sư Tổng Hợp & Kết Xuất Video Phát Hành (Audiobook Video Compiler)**. Kỹ năng chịu trách nhiệm:
- **Tự động phân giải kho âm thanh (Smart Audio Discovery):** Nhận diện trực tiếp thư mục Final Audio (`.../Final-Tam-Quoc-Dien-Nghia`) hoặc thư mục nguồn tác phẩm (`.../Tam-Quoc-Dien-Nghia`), quét toàn bộ các file âm thanh hoàn thiện (`Final_Audio_*.mp3`) đã qua xử lý master giọng đọc và nhạc nền BGM EBU R128.
- **Quản lý tiến trình nguyên tử & Tự khôi phục (Atomic Progress Manifest & Resume):**
  - Khởi tạo và quản lý tệp `.abv_manifest.json` đặt ngay tại thư mục Final.
  - Lưu trạng thái chi tiết của từng video: `status` (`pending`, `rendering`, `completed`, `failed`), `audio_file`, `video_file`, `duration`, `file_size`, `rendered_at`.
  - Cơ chế **Atomic Resume**: Khi chạy lại sau sự cố ngắt quãng hoặc chạy bổ sung, hệ thống tự động kiểm tra tính hợp lệ của video (file `.mp4` tồn tại, dung lượng $> 1\text{MB}$, độ dài khớp với audio gốc $\pm 3.0\text{s}$) và **SKIP** hoàn toàn, chỉ tiếp tục render các chương chưa hoàn thành.
- **Điều phối Sub-agents song song (Mandatory Parallel Subagent Swarm):** Khi xử lý toàn bộ tác phẩm gồm nhiều chương, AI Chính bắt buộc chia nhỏ thành các batch (ví dụ 3–5 chương/agent) và kích hoạt song song qua `invoke_subagent` để tăng tốc độ gấp 3 đến 5 lần.
- **Tiêu chuẩn kết xuất Video MP4 phát hành:**
  - Định dạng: MP4 (H.264 High Profile, CRF 20, 25 FPS, Pixel Format yuv420p).
  - Độ phân giải: 1920x1080 (16:9 Full HD).
  - Âm thanh: AAC 192kbps stereo, bảo toàn dải động và độ to EBU R128 (-16 LUFS) của bản thu gốc.
  - Trình chiếu ảnh nền: Phân bổ đều thư viện 10 ảnh nền (`bg_01.jpg` đến `bg_10.jpg` từ Bước 01) trải dài suốt thời lượng chương qua cơ chế `ffconcat` mượt mà, tối ưu hiệu năng render.
  - Vị trí lưu trữ: Lưu trực tiếp tại `Final-[Tên-Sách]/Final_Video_{Tên_Chương}.mp4`.

---

## 2. TRIGGER / KHI NÀO SỬ DỤNG (ACTIVATION CONDITIONS)
Kỹ năng được kích hoạt trong các tình huống:
1. **Dựng Video Sách Nói sau khi hoàn thành Audio Final:** Sau khi Bước 10 (`arf_10_bgm_dynamic_mixer`) đã xuất xưởng toàn bộ file `Final_Audio_*.mp3`.
2. **Người dùng yêu cầu tạo video cho tác phẩm:** Người dùng truyền đường dẫn thư mục Final hoặc thư mục nguồn và yêu cầu biến các file audio thành video.
3. **Tiếp tục tiến trình dang dở:** Khởi chạy lại để hoàn tất các chương bị ngắt quãng nhờ cơ chế Atomic Resume.
4. **Lệnh thực thi CLI chuẩn:**
   ```bash
   # Dựng video cho 1 file audio cụ thể (dành cho Sub-agent)
   ./venv/bin/python core/abv_video_compiler.py "Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/Final-Tam-Quoc-Dien-Nghia" --file "Final_Audio_01-Hoi-01_Part1.mp3"

   # Dựng video theo dải chương (Batch processing)
   ./venv/bin/python core/abv_video_compiler.py "Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia" --batch_start 1 --batch_end 10

   # Dựng video toàn bộ tác phẩm với đa luồng
   ./venv/bin/python core/abv_video_compiler.py "Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia" --parallel 2
   ```

---

## 3. TRÌNH TỰ TỪNG BƯỚC THỰC THI (STEP-BY-STEP WORKFLOW)

### Bước 3.1: Tiếp nhận và Quét Danh mục Audio Final
- Phân giải đường dẫn đầu vào qua hàm `resolve_paths`.
- Quét nạp toàn bộ danh sách `Final_Audio_*.mp3`, sắp xếp theo thứ tự số chương tự nhiên.
- Kiểm tra thư viện ảnh nền tại `Final-[Tên-Sách]/backgrounds/`. Nếu chưa có, tự động gọi Bước 01 (`abv_01_thematic_visual_prompter`) để khởi tạo 10 ảnh nền.

### Bước 3.2: Khởi tạo và Đồng bộ Manifest Tiến Trình
- Nạp hoặc khởi tạo tệp `.abv_manifest.json` trong thư mục Final.
- Lọc danh sách các tệp cần dựng (loại trừ các file đã có status `completed` và tệp video hợp lệ).

### Bước 3.3: Điều Phối Sub-Agents Song Song (Mandatory Parallel Swarm)
- Khi số lượng tệp cần dựng $> 2$, AI Chính **BẮT BUỘC** gọi `invoke_subagent` phân chia công việc:
  ```python
  invoke_subagent(Subagents=[
      {
          "TypeName": "self",
          "Role": "Video Render Coordinator [Batch 1: Hoi 01-10]",
          "Prompt": "Chạy dựng video từ Hồi 01 đến Hồi 10 bằng lệnh: ./venv/bin/python core/abv_video_compiler.py '...' --batch_start 1 --batch_end 10"
      },
      {
          "TypeName": "self",
          "Role": "Video Render Coordinator [Batch 2: Hoi 11-20]",
          "Prompt": "Chạy dựng video từ Hồi 11 đến Hồi 20 bằng lệnh: ./venv/bin/python core/abv_video_compiler.py '...' --batch_start 11 --batch_end 20"
      }
  ])
  ```

### Bước 3.4: Kết Xuất Video & Cập Nhật Tiến Trình
- Từng Sub-agent gọi `core/abv_video_compiler.py` xử lý tệp được giao.
- Công cụ tính toán thời gian hiển thị từng ảnh: $T_{\text{bg}} = T_{\text{audio}} / 10$.
- Biên dịch bằng FFmpeg, ghi video vào `Final-[Tên-Sách]/Final_Video_{Tên_Chương}.mp4`.
- Tự động cập nhật nguyên tử `.abv_manifest.json` sau mỗi tệp hoàn thành.

### Bước 3.5: Xuất Bản Báo Cáo Tổng Hợp (Master Video Report)
- Sau khi toàn bộ các batch hoàn tất, xuất bản tệp `Final-[Tên-Sách]/Master_Video_Report.md` thống kê tổng số video, thời lượng, dung lượng và đường dẫn trực tiếp.

---

## 4. OUTPUT CONTRACT (CHUẨN ĐẦU RA & RÀNG BUỘC TỆP TIN)
Thành phẩm của kỹ năng bắt buộc phải lưu tập trung tại thư mục Final của tác phẩm:
- `Final-[Tên-Sách]/Final_Video_{Tên_Chương}.mp4`: Tệp video MP4 1080p chuẩn mực, hình ảnh 16:9 sắc nét, âm thanh đồng bộ 100%.
- `Final-[Tên-Sách]/.abv_manifest.json`: Tệp manifest quản lý tiến trình nguyên tử ghi nhận chi tiết mọi tệp video.
- `Final-[Tên-Sách]/Master_Video_Report.md`: Báo cáo bảng Markdown tổng kết toàn bộ video sách nói của tác phẩm.

---

## 5. PHỦ ĐỊNH & CẤM KỴ (NEGATIVE TRIGGERS & SYSTEM INVARIANTS)
1. **NO-SOLO-BLOCKING INVARIANT:** Cấm AI Chính tự ý chạy render tuần tự từng file một mình khi tác phẩm có nhiều hơn 2 chương mà không kích hoạt mảng Sub-agents qua `invoke_subagent`.
2. **ROOT-ISOLATION INVARIANT:** Tuyệt đối cấm xuất file video `.mp4` hoặc file tạm vào thư mục con của từng chương hoặc thư mục gốc repository. Toàn bộ video thành phẩm bắt buộc nằm tập trung tại `Final-[Tên-Sách]/`.
3. **NO-OVERWRITE-VALID INVARIANT:** Tuyệt đối không xóa hoặc render lại các tệp video đã hoàn thành hợp lệ trừ khi có cờ `--force` từ người dùng.
4. **AUDIO-DURATION FIDELITY:** Thời lượng của file video kết xuất phải khớp tuyệt đối với thời lượng của file Final Audio gốc ($\Delta t \le 3.0\text{s}$). Cấm cắt ngắn hoặc kéo dài bất hợp lý.
