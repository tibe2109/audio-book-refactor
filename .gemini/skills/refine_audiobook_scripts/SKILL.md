---
name: refine_audiobook_scripts
description: Tinh chỉnh kịch bản Audio Book cấp 1 (Kich-ban-1.txt) bằng LLM - thực hiện rechunk thông minh về 2800-3000 ký tự, áp dụng prompt TTS chuẩn để LLM refactor từng đoạn, xuất ra các file kịch bản final sẵn sàng đưa vào Clipchamp TTS.
---

# Kỹ năng: Tinh chỉnh & Rechunk Kịch bản Audio Book (Bước 6–8)

Kỹ năng này là **giai đoạn 2** trong quy trình sản xuất AudioBook. Nó nhận đầu vào là các file `Kich-ban-1.txt` (kịch bản thô cấp 1 do Bước 5 tạo ra) và xuất ra các file kịch bản final chuẩn TTS, sẵn sàng đưa vào Clipchamp hoặc Azure TTS.

> **⚠️ YÊU CẦU TIÊN QUYẾT:** Skill `generate_audiobook_scripts` đã chạy xong Bước 5 và mỗi thư mục chương đã có file `Kich-ban-1.txt`.

---

## Thông tin cần thu thập

Khi skill này được kích hoạt, AI hỏi người dùng:
1. **Thư mục gốc** chứa các thư mục chương (ví dụ: `D:\Solution\Audio-Book-Refactor\Kich-ban-clipchamp\Eat-that-frog`)
2. **File prompt chuẩn TTS** (ví dụ: `D:\Solution\Audio-Book-Refactor\Promt-chuan-danh-cho-AI-tao-kich-ban-tts-clipchamp`)
3. **Tên/vai trò tác giả** để AI nhập vai khi đọc (ví dụ: "Brian Tracy", "Robert Greene")
4. **(Tuỳ chọn)** Giới hạn ký tự mỗi file: mặc định là **2800 ký tự**

*Không thực hiện các bước tiếp theo cho đến khi người dùng cung cấp đủ thông tin.*

---

## Quy trình thực hiện

### Bước 6: Rechunk thông minh bằng Python

Viết và chạy script Python **`rechunk_scripts.py`** để chia nhỏ kịch bản:

**Nguyên tắc rechunk:**
- Đọc toàn bộ nội dung `Kich-ban-1.txt` của mỗi chương
- Gom thành 1 luồng văn bản liên tục
- Cắt thành các chunk với giới hạn **2800–3000 ký tự**, theo thứ tự ưu tiên:
  1. Cắt tại ranh giới đoạn (`\n\n`) — ưu tiên cao nhất
  2. Nếu đoạn quá dài, cắt tại dấu `. ......` (marker ngắt nghỉ)
  3. Nếu vẫn quá dài, cắt tại dấu chấm câu (`.`, `!`, `?`)
  4. **Tuyệt đối không cắt ngang giữa câu**
- Lưu các chunk thành: `Kich-ban-raw-1.txt`, `Kich-ban-raw-2.txt`, ... trong mỗi thư mục chương
- Xóa `Kich-ban-1.txt` sau khi rechunk xong (đã được gom vào các file raw mới)

**Kiểm tra bắt buộc sau rechunk:**
- Không file nào vượt quá **3000 ký tự**
- Không file nào ngắn hơn **500 ký tự** (nếu có, gộp vào file trước)
- Tổng ký tự các file raw = tổng ký tự `Kich-ban-1.txt` (kiểm tra hao hụt nội dung)

```
[chapter_dir]/
├── raw_original.txt
├── translated.txt
├── Kich-ban-raw-1.txt    ← Chunk thô 1 (chưa qua LLM)
├── Kich-ban-raw-2.txt    ← Chunk thô 2
└── ...
```

---

### Bước 7: Tinh chỉnh LLM theo chuẩn Prompt TTS

Đây là bước AI thực hiện **tinh chỉnh ngôn ngữ và nhịp thở** cho từng chunk.

#### 7.1 — Đọc file Prompt chuẩn
Đọc toàn bộ nội dung file prompt mà người dùng đã cung cấp. Đây là "bản hướng dẫn nhập vai" chứa:
- Vai trò tác giả (ví dụ: Brian Tracy đọc sách của chính mình)
- Quy tắc ngắt nghỉ (dấu phẩy, `. ......`, xuống dòng)
- Quy tắc xử lý ký tự đặc biệt, phiên âm, số → chữ
- Định dạng đầu ra yêu cầu (trong code block)

#### 7.2 — Xử lý từng Chunk bằng LLM

Với **mỗi file `Kich-ban-raw-N.txt`**, AI thực hiện:

1. Đọc nội dung chunk
2. Kiểm tra nếu file `Kich-ban-N.txt` (file đã tinh chỉnh) **đã tồn tại** → bỏ qua (để cho phép resume)
3. Tạo prompt = `[Nội dung prompt chuẩn]` + `\n\nVăn bản cần xử lý:\n` + `[Nội dung chunk]`
4. Gọi AI (dùng lệnh `agy --print "[prompt]"`) để lấy kết quả tinh chỉnh
5. Trích xuất nội dung từ trong code block ` ```...``` ` của response
6. Lưu kết quả vào `Kich-ban-N.txt` (cùng thư mục)

**Quy tắc sống còn khi tinh chỉnh LLM:**
- ✅ PHẢI giữ nguyên toàn bộ nội dung, không được bớt xén
- ✅ PHẢI giữ nguyên dấu `. ......` ở cuối đoạn
- ✅ PHẢI tách tiêu đề dính vào đoạn văn (ví dụ: `Học từ thất bại Mỗi thất bại...` → tách thành 2 đoạn riêng)
- ✅ ĐƯỢC PHÉP thêm dấu phẩy tạo nhịp thở tự nhiên
- ✅ ĐƯỢC PHÉP cải thiện phiên âm tên nước ngoài
- ❌ KHÔNG thêm từ đệm, lời bình luận, tóm tắt
- ❌ KHÔNG thay đổi ý nghĩa hoặc lược bỏ câu

#### 7.3 — Xử lý theo chương, tuần tự

Xử lý từng chương một, từ chunk 1 đến chunk cuối. Nếu gặp lỗi:
- Thử lại tối đa 3 lần
- Nếu vẫn lỗi: giữ nguyên nội dung chunk thô, ghi log cảnh báo và tiếp tục

```
[chapter_dir]/
├── raw_original.txt
├── translated.txt
├── Kich-ban-raw-1.txt    ← Chunk thô
├── Kich-ban-1.txt        ← Chunk đã tinh chỉnh LLM ✅
├── Kich-ban-raw-2.txt
├── Kich-ban-2.txt        ← Chunk đã tinh chỉnh LLM ✅
└── ...
```

---

### Bước 8: Dọn dẹp thư mục làm việc

Sau khi tất cả chunk đã được tinh chỉnh:
1. Xóa tất cả các file `Kich-ban-raw-*.txt` (file thô trung gian)
2. Xóa file `translated.txt` (cache dịch thuật, không cần nữa)
3. **GIỮ LẠI** file `raw_original.txt` — đây là bằng chứng gốc QC
4. **GIỮ LẠI** tất cả `Kich-ban-N.txt` — đây là kịch bản final

**Cấu trúc thư mục sau khi dọn dẹp:**
```
[output_dir]/
└── 02-Chuong-01/
    ├── raw_original.txt    ← Giữ lại (QC)
    ├── Kich-ban-1.txt      ← Kịch bản final (≤ 3000 ký tự)
    ├── Kich-ban-2.txt      ← Kịch bản final
    └── Kich-ban-3.txt      ← Kịch bản final
```

---

### Bước 9: Kiểm tra QC tự động & Báo cáo

Trước khi báo cáo hoàn tất, chạy kiểm tra tự động:

| Tiêu chí | Điều kiện Pass |
|---|---|
| Kích thước file | Mọi `Kich-ban-N.txt` ≤ 3000 ký tự |
| Không bỏ sót chunk | Số file final = số file raw đã tạo |
| Không file trống | Mọi `Kich-ban-N.txt` > 0 ký tự |
| Không còn file thô | Không có `Kich-ban-raw-*.txt` nào |

**Báo cáo hoàn tất** bao gồm:
- Số chương đã xử lý
- Tổng số file kịch bản final
- Danh sách các file cần kiểm tra thủ công (nếu có lỗi)
- Đường dẫn thư mục output

---

## 📋 Tóm tắt luồng dữ liệu

```
Kich-ban-1.txt (cấp 1, thô)
       ↓ rechunk_scripts.py (Bước 6)
Kich-ban-raw-1.txt, Kich-ban-raw-2.txt, ...
       ↓ LLM + Prompt chuẩn (Bước 7)
Kich-ban-1.txt, Kich-ban-2.txt, ... (final ✅)
       ↓ Dọn dẹp (Bước 8)
Thư mục gọn gàng, sẵn sàng cho Clipchamp TTS
```
