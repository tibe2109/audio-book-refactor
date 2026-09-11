---
name: arf_02_author_style_translator
description: Bước 2 - Dịch thuật AI nhập vai tác giả giữ trọn vẹn văn phong, hỗ trợ Subagent song song.
---

# Kỹ năng: Dịch thuật Nhập vai Tác giả (Author-Style Translator) - Bước 2

Kỹ năng này chuyên trách thực hiện **Bước 2** trong quy trình sản xuất Audio Book: Chuyển đổi toàn bộ nội dung nguyên tác từ văn bản thô đã bóc tách (`raw_original.txt`) sang bản dịch tiếng Việt hoàn chỉnh (`translated.txt`), nhập vai văn phong tác giả, bảo toàn 100% ngữ nghĩa và cấu trúc để chuẩn bị cho các bước tạo kịch bản TTS tiếp theo.

---

## 1. Mục đích Cốt lõi & Nguyên tắc Dịch thuật

### 1.1. Nhập vai trực tiếp Tác giả (Author Persona)
- AI không chỉ đơn thuần là công cụ dịch từ vựng, mà đóng vai trò là **chính tác giả đang đọc lại và tái hiện tác phẩm của mình bằng tiếng Việt**.
- Giữ trọn vẹn giọng văn, sắc thái cảm xúc, nhịp điệu diễn đạt và triết lý truyền tải của tác giả (nghiêm cẩn, hài hước, truyền cảm hứng, học thuật, phản tư,...).
- Chuẩn hóa thuật ngữ chuyên ngành nhất quán xuyên suốt toàn bộ các chương của cuốn sách.

### 1.2. Nguyên tắc "Bảo toàn Tuyệt đối 100%" (Zero Loss & Zero Deviation)
- **Không tóm tắt (No Summarization):** Mọi ý niệm, câu chuyện, dẫn chứng, số liệu đều phải được chuyển ngữ đầy đủ.
- **Không bớt xén (No Omission):** Tuyệt đối không lược bỏ các đoạn văn phụ, ví dụ minh họa hoặc lời dẫn nhập.
- **Không thêm lời bình (No Meta-commentary/Editorializing):** Tuyệt đối không tự ý chèn nhận định cá nhân của AI (như *"Theo tôi...", "Tác giả muốn nói rằng...", "Ghi chú của người dịch..."*).
- **Giữ nguyên cấu trúc văn bản:** Bảo toàn hệ thống phân cấp Tiêu đề chính, Tiêu đề phụ, Đề mục con, Đoạn văn và Danh sách liệt kê.

---

## 2. Quản lý Session & Điều phối Subagents

Quy trình hoạt động dựa trên cơ chế Session Manifest để đảm bảo tính liên tục, khả năng phục hồi khi gặp sự cố và phân tải xử lý song song mạnh mẽ.

```
[book_slug]/
├── .session_manifest.json          <-- Quản lý trạng thái và tiến trình toàn sách
├── 00-gioi-thieu/
│   ├── raw_original.txt            <-- Input
│   └── translated.txt              <-- Output của Bước 2
├── 01-chuong-01/
│   ├── raw_original.txt
│   └── translated.txt
└── ...
```

### 2.1. Cấu trúc `.session_manifest.json`
File manifest lưu trữ thông tin meta của phiên dịch thuật:
```json
{
  "session_id": "session_20260816_audiobook_01",
  "book_title": "Tên Cuốn Sách",
  "author": "Tên Tác Giả",
  "book_slug": "ten-cuon-sach",
  "step_1_status": "completed",
  "step_2_status": "in_progress",
  "step_2_started_at": "2026-08-16T10:10:00Z",
  "step_2_completed_at": null,
  "chapters": [
    {
      "id": "00-gioi-thieu",
      "title": "Lời giới thiệu",
      "folder": "00-gioi-thieu",
      "raw_file": "00-gioi-thieu/raw_original.txt",
      "translated_file": "00-gioi-thieu/translated.txt",
      "step_2_status": "completed"
    },
    {
      "id": "01-chuong-01",
      "title": "Chương 1",
      "folder": "01-chuong-01",
      "raw_file": "01-chuong-01/raw_original.txt",
      "translated_file": "01-chuong-01/translated.txt",
      "step_2_status": "in_progress"
    }
  ]
}
```

### 2.2. Chiến lược Điều phối Subagent Song Song
1. **Xác định các chương cần xử lý:** Đọc `.session_manifest.json`, lọc danh sách các chương có `step_2_status` là `"pending"` hoặc `"error"`.
2. **Kích hoạt Subagents:**
   - Khi xử lý cuốn sách có nhiều chương, phân bổ mỗi chương (hoặc nhóm 2-3 chương ngắn) cho một Subagent độc lập thực hiện thông qua `invoke_subagent`.
   - Khi xử lý hàng loạt sách (Batch Books), mỗi Subagent phụ trách riêng một thư mục `[book_slug]`.
3. **Cập nhật tiến độ nguyên tử (Atomic Manifest Update):**
   - Trước khi dịch chương: Cập nhật `step_2_status: "in_progress"` cho chương tương ứng trong manifest.
   - Sau khi tạo xong file `translated.txt`: Cập nhật trạng thái chương thành `"completed"`.
   - Khi tất cả các chương hoàn tất: Cập nhật trường tổng thể `step_2_status: "completed"` và ghi nhận `step_2_completed_at`.

---

## 3. Quy trình Triển khai Chuẩn

### Bước 1: Tiếp nhận và Xác thực Dữ liệu Đầu vào
- Kiểm tra sự tồn tại của thư mục sách và file `.session_manifest.json`.
- Kiểm tra các file `raw_original.txt` trong từng thư mục chương. Đảm bảo file gốc không rỗng.

### Bước 2: Thiết lập Prompt Nhập vai Tác giả
Khi thực hiện dịch thuật (qua AI Subagent hoặc tool tự động), sử dụng hệ thống chỉ dẫn sau:
```text
Bạn là [Tác giả], đang trực tiếp đọc lại và chuyển tải trọn vẹn tác phẩm "[Tên sách]" sang tiếng Việt.
Yêu cầu:
1. Giữ trọn vẹn phong cách, ngôn từ, thần thái và nhịp điệu của nguyên tác.
2. Dịch chính xác 100%, không bỏ sót bất kỳ chi tiết, luận điểm, số liệu hay ví dụ nào.
3. Tuyệt đối KHÔNG tóm tắt, KHÔNG lược dịch, KHÔNG thêm lời bình luận, mở đầu hay kết bài của AI.
4. Giữ nguyên cấu trúc phân đoạn, tiêu đề chương mục.
5. Ngôn ngữ tự nhiên, mạch lạc, dễ nghe khi chuyển thành giọng đọc Audio Book.
```

### Bước 3: Dịch thuật & Ghi file Đầu ra
- Đọc nội dung từ `[chapter_dir]/raw_original.txt`.
- Chuyển ngữ toàn văn theo chuẩn nhập vai tác giả.
- Ghi trực tiếp kết quả vào `[chapter_dir]/translated.txt` (sử dụng UTF-8).

### Bước 4: Đồng bộ Manifest & Báo cáo
- Ghi nhận trạng thái hoàn thành vào `.session_manifest.json`.
- Báo cáo kết quả chi tiết cho Agent điều phối hoặc người dùng.

---

## 4. Hướng Dẫn Kích Hoạt Sub-Agent Dịch Thuật Theo Từng Chương (Per-Chapter Translator Subagent)

Để đảm bảo chất lượng dịch thuật cao nhất, AI Conductor phân bổ mỗi chương (hoặc nhóm 2-3 chương) cho một Sub-agent nhập vai độc lập:

```python
# Mẫu kích hoạt Subagent dịch thuật chuyên sâu từng chương
invoke_subagent(
    Subagents=[
        {
            "TypeName": "self",
            "Role": "Author Persona Translator [01-quy-luat-01]",
            "Prompt": (
                "Bạn là Chuyên gia Dịch thuật Văn học cao cấp nhập vai tác giả Robert Greene.\n"
                "Tác phẩm: 'Những Quy Luật Về Bản Chất Con Người' | Thể loại: Tâm lý học hành vi / Triết học quyền lực.\n"
                "Nhiệm vụ: Dịch toàn văn file '01-quy-luat-01-lam-chu-cai-toi-cam-xuc/raw_original.txt' sang 'translated.txt'.\n"
                "Yêu cầu:\n"
                "1. Dịch trung thành 100%, không tóm tắt, không bớt xén dù một câu chuyện lịch sử hay ẩn dụ.\n"
                "2. Giữ nguyên văn phong sắc sảo, hùng biện và giọng điệu chiêm nghiệm của tác giả.\n"
                "3. Viết trực tiếp vào file 'translated.txt' của chương tương ứng."
            )
        }
    ]
)
```

---

## 5. Công cụ Hỗ trợ Dịch Hàng Loạt: `batch_translate.py`

Trong thư mục `scripts/`, công cụ `batch_translate.py` được cung cấp sẵn để thực thi CLI tự động:

```bash
# Cú pháp chạy cơ bản:
python .agy/skills/arf_02_author_style_translator/scripts/batch_translate.py --input_dir "path/to/book_folder" --author "Tên Tác Giả" --book_title "Tên Sách"
```
