---
name: arf_01_pdf_structure_extractor
description: Bước 1 - Bóc tách cấu trúc PDF phức tạp, loại bỏ Header/Footer/TOC và khởi tạo Session Manifest.
---

# Kỹ năng 01: Bóc tách Cấu trúc PDF (PDF Structure Extractor)

Kỹ năng này chịu trách nhiệm phân tích, lọc nhiễu và bóc tách toàn bộ cấu trúc nội dung từ các file sách điện tử định dạng PDF (kể cả PDF có layout phức tạp như 2 cột, header/footer biến đổi, footnote, mục lục dài). Kết quả đầu ra là hệ thống thư mục chương độc lập chứa văn bản gốc bất biến (`raw_original.txt`) kèm file theo dõi phiên làm việc (`.session_manifest.json`).

---

## 1. Mục tiêu và Phạm vi
- **Nhận diện Cấu trúc Vĩ mô (Macro Chapter Architecture):** Luôn ưu tiên phát hiện cấu trúc chương vĩ mô (Lời mở đầu, Chương 1..N, Lời kết) dựa trên dải trang (Page Range) và phân tích Mục lục. Tuyệt đối KHÔNG băm nhỏ văn bản theo các tiểu mục nội dung bên trong chương (như "Đấu trường nội tâm", "Biểu tượng", "Điểm yếu", "Ví dụ...").
- **Hàn gắn Chữ cái Nghệ thuật (Drop-Cap Healer):** Tự động phát hiện và nối liền các chữ cái Drop-Cap in hoa đơn lẻ đứng đầu dòng bị rớt dòng (`T\nrong` -> `Trong`, `B\nạn` -> `Bạn`, `C\non` -> `Con`, `Đ\niều` -> `Điều`, `M\nột` -> `Một`).
- **Lọc nhiễu văn bản (Noise Filtering):** Loại bỏ hoàn toàn Header (tiêu đề trang lặp lại), Footer, số trang (Page numbers), dòng chú thích chân trang (Footnotes/Page marks) và trang Mục lục (Table of Contents - TOC).
- **Xử lý Layout đa dạng:** Hỗ trợ sách 1 cột tiêu chuẩn và sách 2 cột (Multi-column reading order: đọc hết cột 1 từ trên xuống dưới rồi sang cột 2).
- **Tính Bất biến (Immutability):** File `raw_original.txt` được tạo ra là dữ liệu gốc nguyên bản, dùng làm bằng chứng đối soát (QC Ground Truth) cho toàn bộ quy trình dịch và tạo audio book về sau.
- **Quản trị Phiên (Session Isolation):** Mọi sách được quản lý theo thư mục định danh `[book_slug]` với file `.session_manifest.json` ghi vết trạng thái từng chương.

---

## 2. Cấu trúc Thư mục và Định dạng Output

### 2.1 Cấu trúc cây thư mục đầu ra

```
[output_dir]/[book_slug]/
├── .session_manifest.json          # File manifest theo dõi trạng thái session của sách
├── 00-Preface/
│   └── raw_original.txt           # Nội dung thô của phần Mở đầu (Bất biến)
├── 01-Intro/
│   └── raw_original.txt           # Nội dung thô phần Dẫn nhập (Bất biến)
├── 02-Chuong-01/
│   └── raw_original.txt           # Nội dung thô Chương 1 (Bất biến)
├── 03-Chuong-02/
│   └── raw_original.txt           # Nội dung thô Chương 2 (Bất biến)
└── ...
```

### 2.2 Quy cách file `.session_manifest.json`

File `.session_manifest.json` được tạo mới hoặc cập nhật sau khi hoàn thành bóc tách:

```json
{
  "session_id": "ses_20260816_a1b2c3d4",
  "book_slug": "eat-that-frog",
  "source_pdf": "D:/Solution/Audio-Book-Refactor/Docs/eat-that-frog.pdf",
  "total_pages": 144,
  "toc_range": [1, 13],
  "content_start_page": 14,
  "created_at": "2026-08-16T10:05:00+07:00",
  "updated_at": "2026-08-16T10:06:00+07:00",
  "pipeline_stage": "01_structure_extracted",
  "chapters": [
    {
      "index": 0,
      "folder": "00-Preface",
      "title": "Preface",
      "start_page": 9,
      "end_page": 11,
      "char_count": 5210,
      "status": "raw_extracted",
      "raw_file": "00-Preface/raw_original.txt"
    },
    {
      "index": 1,
      "folder": "02-Chuong-01",
      "title": "Chapter 1: Set the Table",
      "start_page": 14,
      "end_page": 19,
      "char_count": 7820,
      "status": "raw_extracted",
      "raw_file": "02-Chuong-01/raw_original.txt"
    }
  ],
  "metadata": {
    "extractor_version": "1.0.0",
    "column_layout": "single_column",
    "noise_filtered": {
      "headers_removed": true,
      "footers_removed": true,
      "page_numbers_removed": true
    }
  }
}
```

---

## 3. Hướng dẫn Dành cho AI Agent (Execution Workflow)

### Bước 1: Tiếp nhận yêu cầu & Thu thập tham số
Xác định các thông tin cần thiết:
1. `--pdf_path`: Đường dẫn tuyệt đối tới file PDF.
2. `--output_dir`: Thư mục gốc lưu trữ kết quả.
3. `--book_slug`: Slug định danh sách (ví dụ: `eat-that-frog`, `dac-nhan-tam`).
4. `--session_id`: (Tùy chọn) Mã phiên làm việc, nếu không cung cấp script sẽ tự khởi tạo.

### Bước 2: Xử lý Đơn sách hoặc Đa sách (Multi-Agent Dispatching)
- **Nếu là 1 file PDF:**
  AI gọi lệnh `run_command` chạy trực tiếp script `extract_structure.py`.
- **Nếu là thư mục chứa nhiều file PDF hoặc file PDF quá lớn (> 500 trang):**
  AI kích hoạt `invoke_subagent` để chia nhỏ công việc song song cho từng cuốn sách hoặc từng cụm chương lớn, mỗi subagent làm việc độc lập trong thư mục `[book_slug]` tương ứng.

### Bước 3: Chạy Script Python Bóc tách Cấu trúc

Lệnh thực thi chuẩn:
```powershell
python .agy/skills/01_pdf_structure_extractor/scripts/extract_structure.py `
  --pdf_path "D:\Solution\Audio-Book-Refactor\Docs\Eat That Frog! 21 Great Ways to Stop Procrastinating and Get More Done in Less Time ( PDFDrive ).pdf" `
  --output_dir "D:\Solution\Audio-Book-Refactor\Kich-ban-clipchamp" `
  --book_slug "Eat-that-frog"
```

### Bước 4: Kiểm tra tính hợp lệ của Output (Verification)
Sau khi script hoàn tất:
1. Đọc nội dung `.session_manifest.json` trong thư mục sách để kiểm tra danh sách chương và trang.
2. Đảm bảo toàn bộ các thư mục chương đều có file `raw_original.txt` với dung lượng `> 0 bytes`.
3. Báo cáo kết quả rõ ràng (Tổng số trang, tổng số chương phát hiện được, tổng số ký tự đã bóc tách).

---

## 4. Các Heuristic Xử lý PDF Nâng cao trong Script

1. **Bộ lọc Header & Footer theo tần suất và tọa độ:**
   - Quét qua mẫu 20-30 trang đầu và cuối để tìm các dòng văn bản lặp lại tại vị trí y-top (< 10% chiều cao trang) hoặc y-bottom (> 90% chiều cao trang).
   - Tự động cắt bỏ các chuỗi này khi ghép văn bản nội dung.

2. **Bộ lọc Số trang (Page Number Regex):**
   - Loại bỏ các dòng độc lập chỉ chứa chữ số, số La Mã (i, ii, iii, iv, v...), hoặc mẫu `Page X / Page X of Y`.

3. **Phát hiện Trang Mục lục (TOC Scanning):**
   - Quét từ khóa `Contents`, `Table of Contents`, `Mục lục`, kết hợp với mật độ xuất hiện của dấu chấm kéo dài `...` và số trang ở cuối dòng.
   - Đánh dấu vùng trang TOC để không nhận diện nhầm tiêu đề trong TOC thành chương nội dung.

4. **Xử lý Layout 2 cột (Column Flow Detection):**
   - Phân tích tọa độ x0, x1 của các block văn bản trên trang. Nếu tồn tại khoảng phân cách cột (gutter) rõ rệt ở giữa trang, script tự gom cụm block theo cột trái trước, sau đó nối tiếp cột phải.

5. **Phát hiện Ranh giới Chương (Chapter Boundary Rules):**
   - Tìm kiếm các mẫu nhận diện: `Chapter \d+`, `Chương \d+`, `Part [IVXLCDM\d]+`, `Introduction`, `Preface`, `Conclusion`, `Epilogue`, `Lời mở đầu`, `Kết luận`.
   - Kết hợp kiểm tra kiểu chữ: Font size lớn hơn font văn bản thân bài (Body text) hoặc dòng chữ in hoa độc lập trên trang mới.

---

## 5. Hướng Dẫn Kích Hoạt Sub-Agent Theo Từng Chương (Per-Chapter Subagent Spawning)

Khi đối mặt với các tài liệu PDF dài (> 200 trang) hoặc có cấu trúc phức tạp, AI Conductor có thể kích hoạt song song các Sub-agent chuyên trách thẩm tra từng chương bằng lệnh `invoke_subagent`:

```python
# Mẫu kích hoạt Subagent cho từng chương / nhóm chương
invoke_subagent(
    Subagents=[
        {
            "TypeName": "self",
            "Role": "PDF Structure Verifier [01-quy-luat-01]",
            "Prompt": (
                "Bạn là Chuyên gia Cấu trúc PDF phụ trách kiểm tra chương '01-quy-luat-01-lam-chu-cai-toi-cam-xuc'.\n"
                "Nhiệm vụ: Mở file 'raw_original.txt' của chương này, kiểm tra đối soát với PDF gốc để đảm bảo:\n"
                "1. Không còn sót Header, Footer hay số trang.\n"
                "2. Các chữ Drop-Cap đầu dòng đã được hàn gắn 100% (ví dụ: 'Trong suốt', 'Bạn thích').\n"
                "3. Không bị cắt cụt câu ở đầu hoặc cuối chương."
            )
        }
    ]
)
```

---

## 6. Chuyển tiếp Quy trình (Next Stage)

Sau khi Skill `arf_01_pdf_structure_extractor` hoàn tất, AI chuyển tiếp sang:
- **Skill 2:** `arf_02_author_style_translator` — Dịch thuật nhập vai tác giả bảo toàn 100% ngữ nghĩa.
- Dữ liệu đầu vào của Skill tiếp theo luôn lấy trực tiếp từ file `raw_original.txt` của từng chương được liệt kê trong `.session_manifest.json`.
