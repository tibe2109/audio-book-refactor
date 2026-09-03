---
name: arf_08_tts_neural_bgm_mixer
description: Bước 8 - Sinh âm thanh Edge-TTS Neural, ghép chương, gom nhóm 25-35 phút và hòa âm BGM tịnh tiến offset 300s.
---

# 🎙️ Kỹ Năng 08: TTS Neural & BGM Audio Mixer

## 1. Mục Đích & Tổng Quan (Overview)
Kỹ năng này chịu trách nhiệm chuyển đổi toàn bộ kịch bản sách nói tiếng Việt đã vượt qua khâu kiểm duyệt chất lượng (Quality Control - QC) thành sản phẩm Audiobook hoàn chỉnh với chất lượng âm thanh cao:
1. **Kiểm duyệt QC nghiêm ngặt:** Chỉ xử lý các chương đã được đánh dấu nghiệm thu `- [x]` trong file `QC_Report.md`.
2. **Tổng hợp giọng đọc AI (Neural TTS):** Sử dụng công nghệ Microsoft Edge-TTS với giọng đọc tự nhiên `vi-VN-NamMinhNeural` (hoặc cấu hình tùy chỉnh), tốc độ đọc tối ưu `-10%` (chuẩn nghe audiobook tự nhiên, rõ ràng, truyền cảm).
3. **Gom nhóm thời lượng thông minh (Smart Grouping):** Ghép các chương liên tiếp thành từng tập hoàn chỉnh có độ dài tối ưu **25 – 35 phút** (`Group-X-Y-Z-Full.mp3`), phù hợp với định dạng phát hành trên YouTube, Spotify, Podcast.
4. **Hòa âm nhạc nền tịnh tiến (Sliding BGM Mixing):** Sử dụng `ffmpeg` lồng nhạc nền không lời êm dịu, áp dụng kỹ thuật offset tịnh tiến 300 giây (5 phút) cho mỗi group để âm điệu không bị lặp lại đơn điệu, cân bằng âm lượng (Voice 100%, BGM ~12-15%) và làm mượt bằng hiệu ứng Fade In / Fade Out.
5. **Thư mục cách ly & Quản lý trạng thái:** Toàn bộ file âm thanh đầu ra được lưu trữ độc lập trong `[book_slug]/audio_output/` và tự động đồng bộ tiến trình vào `.session_manifest.json` (`step_8_status`).

---

## 2. Cấu Trúc Thư Mục & Tài Nguyên
```
.agy/skills/08_tts_neural_bgm_mixer/
├── SKILL.md                          # Tài liệu hướng dẫn kỹ năng
└── scripts/
    └── audio_mixer_pipeline.py       # Script thực thi pipeline tạo audio & hòa âm
```

---

## 3. Điều Kiện Tiên Quyết (Prerequisites)
Trước khi chạy pipeline, hệ thống cần đảm bảo:
- **Python 3.10+** với gói thư viện `edge-tts`.
- **FFmpeg & FFprobe:** Đã được cài đặt trong hệ thống PATH hoặc thư mục nhị phân cục bộ.
- **Kịch bản sách đã qua QC:** File `QC_Report.md` nằm trong thư mục sách có chứa ít nhất một chương được tích chọn `- [x]`.

---

## 4. Tham Số Dòng Lệnh (CLI Interface)

Script `audio_mixer_pipeline.py` hỗ trợ các tham số sau:

| Tham số | Bắt buộc | Mặc định | Ý nghĩa |
| :--- | :---: | :---: | :--- |
| `--input_dir` | **Có** | - | Đường dẫn thư mục sách chứa các chương kịch bản |
| `--output_dir` | Không | `[input_dir]/audio_output` | Thư mục cách ly lưu trữ file âm thanh đầu ra |
| `--bgm` | Không | `""` | Đường dẫn file nhạc nền MP3 |
| `--voice` | Không | `vi-VN-NamMinhNeural` | Mã giọng đọc AI Edge-TTS |
| `--rate` | Không | `-10%` | Tốc độ đọc (Rate) |
| `--session_id` | Không | `auto-generated` | Mã phiên làm việc để ghi log manifest |
| `--manifest_path` | Không | `.session_manifest.json` | Đường dẫn file quản lý trạng thái session |
| `--test` | Không | `False` | Chế độ test nhanh (chỉ xử lý nhóm đầu tiên) |

---

## 5. Quy Trình Thực Thi Chi Tiết (Pipeline Workflow)

### Bước 1: Kiểm Tra QC (QC Check Gate)
- Pipeline đọc file `QC_Report.md` bên trong `--input_dir`.
- Phân tích cú pháp Markdown tìm các chương có tiền tố `- [x] <Tên-Chương>`.
- Nếu có chương chưa verify hoặc file không tồn tại, script sẽ hiển thị cảnh báo và chỉ xử lý các chương hợp lệ.

### Bước 2: Sinh Audio Chương Bằng Edge-TTS
- Duyệt qua từng file text (`*.txt`) của mỗi chương đã được verify.
- Gọi Edge-TTS tạo file âm thanh trung gian `chunk-audio.mp3`.
- Tự động cơ chế **Retry lên đến 5 lần** nếu xảy ra gián đoạn mạng kết nối API Microsoft.
- Ghép nối các chunk thành file hoàn chỉnh cho từng chương: `[output_dir]/chapters/Chuong-X-Full.mp3`.

### Bước 3: Đo Thời Lượng & Gom Nhóm 25–35 Phút
- Dùng `ffprobe` trích xuất chính xác thời lượng của từng chương.
- Thuật toán gom nhóm (Smart Binning):
  - Nhóm các chương tuần tự sao cho tổng thời lượng đạt mốc chuẩn **25 – 35 phút (1500s – 2100s)**.
  - Tạo file gộp thô: `Group-X-Y-Z-Full.mp3`.

### Bước 4: Hòa Âm BGM Với Offset Tịnh Tiến (300s Sliding Offset)
- Nếu có tham số `--bgm`:
  - Group $0$ lấy BGM từ giây $0$.
  - Group $1$ lấy BGM từ giây $300$ ($5$ phút).
  - Group $k$ lấy BGM từ giây $(k \times 300) \pmod{\text{BGM\_Duration}}$.
  - Áp dụng bộ lọc âm lượng BGM $12\%$, fade-in $3$s, fade-out $5$s ở cuối tập.
  - Xuất ra file hoàn thiện: `Group-X-Y-Z-BGM.mp3`.

### Bước 5: Cập Nhật Manifest & Báo Cáo
- Ghi nhận trạng thái `step_8_status: "COMPLETED"` cùng toàn bộ metadata danh sách file vào `.session_manifest.json`.
- In báo cáo tổng kết chi tiết ra màn hình console.

---

## 6. Hướng Dẫn Kích Hoạt Sub-Agent Sản Xuất Âm Thanh Từng Nhóm Chương (Audio Mixer Subagent)

Khi sản xuất audiobook quy mô lớn, Master AI có thể giao việc cho Subagent giám sát từng nhóm:

```python
invoke_subagent(
    Subagents=[
        {
            "TypeName": "self",
            "Role": "Neural Audio Production Mixer [Batch_01]",
            "Prompt": (
                "Bạn là Kỹ sư Âm thanh & Hòa âm Sách nói phụ trách [Batch_01].\n"
                "Nhiệm vụ: Chạy audio_mixer_pipeline.py cho các chương đã đạt QC '- [x]' trong Batch 01.\n"
                "Tiến hành: Sinh giọng đọc Edge-TTS NamMinhNeural (rate -20%), ghép nối thành tập 25-35 phút và lồng BGM offset 300s vào 'audio_output/'."
            )
        }
    ]
)
```

---

## 7. Ví Dụ Câu Lệnh Thực Thi (Usage Examples)

```bash
python .agy/skills/arf_08_tts_neural_bgm_mixer/scripts/audio_mixer_pipeline.py \
  --input_dir "Kich-ban-clipchamp/Nhung-quy-luat-ve-ban-chat-con-nguoi" \
  --bgm "nhac-nen.mp3" \
  --voice "vi-VN-NamMinhNeural" \
  --rate "-20%"
```
