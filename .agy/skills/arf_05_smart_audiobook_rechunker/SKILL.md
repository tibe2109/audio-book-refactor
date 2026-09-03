---
name: arf_05_smart_audiobook_rechunker
description: Bước 5 - Rechunk thông minh văn bản thành các chunk chuẩn đệm TTS 2.800–3.000 ký tự (không cắt ngang câu).
---

# Kỹ năng: Phân Đoạn Thông Minh Kịch Bản Audio Book (Bước 5 - Smart Rechunker)

Kỹ năng này chuyên trách thực hiện **Bước 5** trong quy trình sản xuất Audio Book: Tái phân đoạn (Rechunk) kịch bản thô cấp 1 (`Kich-ban-1.txt`) thành các file đệm TTS tối ưu (`Kich-ban-raw-1.txt`, `Kich-ban-raw-2.txt`,...) với dung lượng lý tưởng từ **2.800 – 3.000 ký tự**, đáp ứng hoàn hảo giới hạn nạp của các công cụ Text-to-Speech (như Clipchamp, Azure TTS, v.v.).

---

## 1. Mục Đích & Tiêu Chuẩn Phân Đoạn

1. **Dung lượng tiêu chuẩn**:
   - **Tối đa (Max chunk)**: 2.800 – 3.000 ký tự (mặc định 3.000 ký tự).
   - **Tối thiểu (Min chunk)**: 500 ký tự. Không tạo ra các file con quá ngắn. Nếu file cuối cùng < 500 ký tự, tự động gộp vào file trước đó.
2. **Thứ tự ưu tiên cắt gọt (Split Priority)**:
   - **Ưu tiên 1 (Cao nhất)**: Cắt tại ranh giới đoạn văn (`\n\n`).
   - **Ưu tiên 2**: Nếu đoạn văn quá dài (> max_chunk), cắt tại marker ngắt nghỉ (`. ......`).
   - **Ưu tiên 3**: Nếu một khối vẫn quá dài, cắt tại dấu kết thúc câu (`.`, `!`, `?`).
   - **Ràng buộc tuyệt đối**: **Tuyệt đối không cắt ngang giữa câu hoặc giữa từ**.
3. **Bảo toàn dữ liệu (Zero Data Loss)**:
   - Tổng số ký tự trước và sau khi rechunk phải được đối soát (độ lệch cho phép do chuẩn hóa khoảng trắng $\le 0.05\%$).
   - Giữ nguyên vẹn toàn bộ marker `. ......` và nội dung phiên âm.
4. **Quy ước tệp tin**:
   - **Đầu vào (Input)**: `Kich-ban-1.txt` (hoặc các file kịch bản thô trong thư mục chương).
   - **Đầu ra (Output)**: `Kich-ban-raw-1.txt`, `Kich-ban-raw-2.txt`, `Kich-ban-raw-3.txt`,...
   - Xóa bỏ hoặc thay thế an toàn file `Kich-ban-1.txt` sau khi rechunk thành công.

---

## 2. Quản Lý Phiên Làm Việc (Session State Tracking)

Khi nhận tham số `--session_id`, hệ thống tự động ghi nhận và cập nhật trạng thái:
- Khóa trạng thái: `step_5_status` = `"IN_PROGRESS"` -> `"COMPLETED"` (hoặc `"FAILED"`).
- Báo cáo đối soát dung lượng:
  - `total_chars_before`: Tổng ký tự ban đầu của kịch bản.
  - `total_chars_after`: Tổng ký tự của toàn bộ các file `Kich-ban-raw-*.txt` đã tạo.
  - `integrity_rate`: Tỷ lệ bảo toàn dữ liệu (%).
  - `chapters_processed`: Danh sách các chương và số lượng file sinh ra.

File session được lưu tại `.agy/sessions/<session_id>.json` hoặc `session.json` trong thư mục làm việc.

---

## 3. Cấu Trúc Thư Mục Sau Rechunk

```
[output_dir]/
└── 02-Chuong-01/
    ├── raw_original.txt        # Bản gốc từ PDF (bảo lưu)
    ├── translated.txt          # Bản dịch tiếng Việt (bảo lưu)
    ├── Kich-ban-raw-1.txt      # Chunk thô 1 (2.800 - 3.000 ký tự)
    ├── Kich-ban-raw-2.txt      # Chunk thô 2 (2.800 - 3.000 ký tự)
    └── Kich-ban-raw-3.txt      # Chunk thô 3 (>= 500 ký tự)
```

---

## 4. Hướng Dẫn Vận Hành Cho AI & CLI

AI điều phối quy trình có thể chạy script bằng công cụ `run_command`:

### Chạy cho toàn bộ các chương trong thư mục sách:
```powershell
python .agy/skills/05_smart_audiobook_rechunker/scripts/rechunk_smart.py --input_dir "D:/Solution/Audio-Book-Refactor/Kich-ban-clipchamp/Eat-that-frog" --max_chunk 3000 --min_chunk 500 --session_id "session_001"
```

### Chạy cho một chương đơn lẻ:
```powershell
python .agy/skills/05_smart_audiobook_rechunker/scripts/rechunk_smart.py --input_dir "D:/Solution/Audio-Book-Refactor/Kich-ban-clipchamp/Eat-that-frog/02-Chuong-01" --max_chunk 3000 --min_chunk 500
```

---

## 5. Hướng Dẫn Kích Hoạt Sub-Agent Phân Đoạn Từng Chương (Semantic Chunking Subagent)

Khi cần tối ưu phân đoạn cho từng chương riêng biệt:

```python
invoke_subagent(
    Subagents=[
        {
            "TypeName": "self",
            "Role": "Semantic Chunking Specialist [01-quy-luat-01]",
            "Prompt": (
                "Bạn là Chuyên gia Phân đoạn Kịch bản (Smart Rechunker) cho chương '01-quy-luat-01'.\n"
                "Nhiệm vụ: Phân đoạn 'Kich-ban-1.txt' thành các file 'Kich-ban-raw-N.txt' từ 2.800–3.000 ký tự theo ranh giới đoạn văn và marker '. ......'.\n"
                "Yêu cầu: Bảo toàn 100% nội dung (Zero Data Loss), không cắt ngang câu."
            )
        }
    ]
)
```

---

## 6. Tiêu Chí Nghiệm Thu (Acceptance Criteria)

1. Mọi file `Kich-ban-raw-*.txt` có dung lượng $\le 3.000$ ký tự.
2. Không có file nào có dung lượng $< 500$ ký tự (trừ khi toàn bộ chương sách ngắn hơn 500 ký tự).
3. Không có câu văn nào bị cắt đứt giữa chừng.
4. Session cập nhật `step_5_status = "completed"`.
