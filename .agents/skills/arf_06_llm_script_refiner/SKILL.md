---
name: arf_06_llm_script_refiner
description: Bước 6 - Tinh chỉnh diễn đọc và nhịp thở bằng LLM theo Prompt chuẩn TTS, dọn dẹp file tạm.
---

# Kỹ năng 06: Tinh chỉnh Kịch bản Diễn Đọc bằng LLM (`06_llm_script_refiner`)

Kỹ năng này chịu trách nhiệm nhận các khối kịch bản thô (`Kich-ban-raw-N.txt`) từ thư mục con `kich-ban/` của bước Rechunk, áp dụng **Prompt TTS chuẩn** và gọi LLM để biên tập lại câu từ cho phù hợp với giọng đọc tự nhiên (thêm dấu phẩy ngắt hơi, sửa lỗi ngữ pháp, tách tiêu đề dính, chuẩn hóa phiên âm, giữ nguyên marker ngắt nghỉ `. ......`), sau đó xuất ra các file kịch bản hoàn chỉnh `Kich-ban-N.txt` ngay trong thư mục `kich-ban/` và dọn dẹp các file thô tạm.

---

## 1. Mục tiêu & Nguyên tắc Tinh chỉnh

### 1.1 Mục tiêu cốt lõi: AI Voice & Prosody Director
- Đóng vai trò là **Tổng đạo diễn Diễn đọc Âm thanh**, hiểu sâu sắc ngữ cảnh văn học (Literary Context) và nhịp thở của người đọc thật.
- Biến đổi văn bản dịch thô/OCR thành kịch bản có ngữ điệu diễn đọc truyền cảm, nhịp nhàng, êm ái, tối ưu cho các bộ Text-To-Speech (TTS như Microsoft Edge TTS, Clipchamp, Azure Neural Voice).

### 1.2 Nguyên tắc tinh chỉnh AI bắt buộc
1. **Phân tích Ngữ điệu & Cảm xúc (Emotional Tone Analysis):** Nhận diện phân đoạn đang xử lý là triết lý trầm ngâm, câu chuyện lịch sử kịch tính, lời khuyên hành động hay phân tích tâm lý để điều phối nhịp văn phù hợp.
2. **Bổ sung nhịp thở tự nhiên (Breathing Commas):** Thêm dấu phẩy `,` tại các mệnh đề phụ, sau các liên từ mở đầu (`tuy nhiên,`, `bởi vì,`, `do đó,`), và ở các câu phức dài trên 12 từ để bộ đọc TTS lấy hơi tự nhiên, không bị đọc dồn dập hoặc hụt hơi.
3. **Phân biệt Lời dẫn chuyện & Lời thoại nhân vật:** Đảm bảo lời trích dẫn danh ngôn hoặc lời thoại được đặt sau dấu phẩy và ngắt nhịp rõ ràng để tạo điểm nhấn âm thanh.
4. **Giữ nguyên Marker ngắt nghỉ `. ......`:** Tuyệt đối giữ nguyên ký hiệu `. ......` ở cuối mỗi đoạn văn hoặc câu chuyển ý quan trọng. Ký hiệu này giúp TTS ngắt nghỉ 1.5 - 2 giây để người nghe chiêm nghiệm.
5. **Không tóm tắt / Không lược ý (100% Content Fidelity):** Giữ trọn vẹn 100% nội dung, không rút gọn luận điểm, ví dụ hay số liệu của tác giả.
6. **Không thêm lời dẫn thoại của AI:** Tuyệt đối không thêm các câu mở đầu/kết bài máy móc như *"Dưới đây là kịch bản"*, *"Chào bạn"*... Chỉ xuất nội dung kịch bản sạch.
7. **Biên tập Chống Lặp Thuật Ngữ Ngoại Lai & Giảm Mỏi Thính Giác (Anti-Auditory Fatigue Principle):**
   - Tuân thủ **Chiến Lược Biên Tập Thuật Ngữ 3 Tầng**: Chỉ giữ nguyên ký tự quốc tế của từ tiếng Anh/Latinh ở câu giới thiệu ban đầu hoặc đầu đề mục mới (Tier 1 & 2) để định vị khái niệm cho người nghe.
   - Trong toàn bộ phần thân bài diễn giải tiếp theo (Tier 3), AI biên tập viên chủ động chuyển đổi linh hoạt sang tiếng Việt tự nhiên (ví dụ: *Stakeholder* $\to$ *các bên liên quan*, *Project Charter* $\to$ *bản điều lệ dự án*), viết tắt tách âm phát thanh (*P-M-I*, *W-B-S*, *K-P-I*), hoặc dùng đại từ thay thế ngắn gọn (*nhóm này, đối tác này, tài liệu này*). Tuyệt đối tránh việc lặp đi lặp lại từ ngoại ngữ máy móc làm bộ đọc TTS phải đảo giọng liên tục gây gián đoạn cảm xúc của thính giả.

---

## 2. Quản lý Session & Checkpoint (Resume Logic)

Kỹ năng lưu vết quá trình thực thi thông qua tệp `.session_manifest.json` nằm tại thư mục gốc của dự án hoặc thư mục đầu vào.

### 2.1 Cấu trúc Manifest
```json
{
  "session_id": "session_20260816_100000",
  "step_6_status": "in_progress",
  "updated_at": "2026-08-16T10:15:00+07:00",
  "chapters": {
    "01-Chuong-01": {
      "status": "completed",
      "total_raw_chunks": 3,
      "completed_chunks": [1, 2, 3]
    },
    "02-Chuong-02": {
      "status": "in_progress",
      "total_raw_chunks": 4,
      "completed_chunks": [1, 2]
    }
  }
}
```

### 2.2 Cơ chế Khôi phục (Resume)
- Trước khi xử lý file `Kich-ban-raw-N.txt`, script sẽ kiểm tra xem file đích `Kich-ban-N.txt` đã tồn tại và có dung lượng hợp lệ (> 50 byte) hay chưa.
- Nếu đã tồn tại: **Bỏ qua (Skip)** chunk này và ghi nhận vào checkpoint, giúp tiết kiệm token và thời gian khi chạy lại sau sự cố mất kết nối hoặc dừng đột ngột.
- Khi toàn bộ các chunk trong một chương hoàn thành, cập nhật trạng thái chương thành `"completed"`.
- Khi toàn bộ các chương hoàn thành, cập nhật `step_6_status` thành `"completed"`.

---

## 3. Tự Động Dọn Dẹp File Trung Gian (Auto-Cleanup)

Sau khi một chương (hoặc toàn bộ dự án) hoàn thành tinh chỉnh 100%:
- 🗑️ **Xóa các file thô trung gian:** `Kich-ban-raw-*.txt`
- 🗑️ **Xóa các file tạm:** `translated.txt` (nếu có)
- 🔒 **GIỮ LẠI BẮT BUỘC:**
  - `raw_original.txt`: Bằng chứng văn bản gốc để phục vụ Quality Control (QC).
  - `Kich-ban-1.txt`, `Kich-ban-2.txt`, ...: Các kịch bản hoàn chỉnh (Final Output).

---

## 4. Hướng Dẫn Kích Hoạt Sub-Agent Biên Kịch Giọng Đọc Từng Chương (Senior Voice Refiner Subagent)

Khi muốn tinh chỉnh sâu sắc ngữ điệu từng chương hoặc tài liệu dài bằng LLM:

```python
invoke_subagent(
    Subagents=[
        {
            "TypeName": "self",
            "Role": "Senior Voice Script Refiner [01-quy-luat-01]",
            "Prompt": (
                "Bạn là Tổng biên kịch Diễn đọc Giọng nói cho chương '01-quy-luat-01-lam-chu-cai-toi-cam-xuc'.\n"
                "Tác giả: Robert Greene | Thể loại: Tâm lý học hành vi / Triết học quyền lực.\n"
                "Nhiệm vụ: Đọc toàn bộ các chunk 'Kich-ban-raw-N.txt' của chương này và tinh chỉnh thành 'Kich-ban-N.txt'.\n"
                "Yêu cầu biên tập thính giác:\n"
                "1. Thêm dấu phẩy lấy hơi tự nhiên ở những câu dài để bộ đọc TTS ngắt giọng êm ái.\n"
                "2. Áp dụng Chiến Lược Thuật Ngữ 3 Tầng: Giữ nguyên thuật ngữ tiếng Anh/Latinh ở phần giới thiệu đầu chương hoặc đầu đề mục mới; trong thân bài diễn giải, linh hoạt chuyển ngữ sang tiếng Việt tự nhiên, từ viết tắt tách âm (W-B-S, P-M-I) hoặc đại từ thay thế ngắn gọn để chống lặp từ ngoại ngữ gây mỏi tai người nghe.\n"
                "3. Bảo toàn 100% nội dung logic và marker ngắt nghỉ '. ......'.\n"
                "4. Khử sạch toàn bộ ký tự cấm TTS (ngoặc, nháy) và chuyển chữ số thành chữ viết."
            )
        }
    ]
)
```

---

## 5. Hướng dẫn Sử dụng Script `refine_llm.py`

### 5.1 Vị trí tệp
- File thực thi: [refine_llm.py](file:///d:/Solution/Audio-Book-Refactor/.agy/skills/arf_06_llm_script_refiner/scripts/refine_llm.py)

### 5.2 Ví dụ câu lệnh
```bash
python .agy/skills/arf_06_llm_script_refiner/scripts/refine_llm.py --input_dir "D:/Solution/Audio-Book-Refactor/Kich-ban-clipchamp/Nhung-quy-luat-ve-ban-chat-con-nguoi" --force
```
