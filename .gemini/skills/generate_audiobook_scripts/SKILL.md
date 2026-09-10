---
name: generate_audiobook_scripts
description: Tự động hóa quy trình đọc sách PDF và xuất ra các kịch bản Audio Book chuẩn Text-to-Speech (TTS) cho Clipchamp - xử lý đến Bước 5 (kịch bản thô cấp 1). AI trực tiếp dịch thuật và phân tích cấu trúc tiêu đề/nội dung. Bước 6 trở đi dùng skill refine_audiobook_scripts.
---

# Kỹ năng: Tự động tạo Audio Book Script từ PDF (Bước 1–5)

Kỹ năng này hướng dẫn AI tự động hóa quy trình **trích xuất, dịch thuật và định dạng cơ học** nội dung sách PDF thành kịch bản TTS chuẩn cấp 1. **AI đóng vai trò trực tiếp là người dịch thuật và phân tích cấu trúc** — không phụ thuộc hoàn toàn vào Google Translate.

> **⚠️ PHẠM VI:** Kỹ năng này chỉ thực hiện **Bước 1 → Bước 5**.
> Để tinh chỉnh LLM, rechunk và hoàn thiện kịch bản, hãy kích hoạt tiếp: **`refine_audiobook_scripts`**

---

## Quy trình thực hiện

### Bước 1: Thu thập thông tin từ người dùng
Ngay khi kỹ năng này được gọi, AI hãy chào mừng và hỏi người dùng **3 thông tin**:
1. Đường dẫn tuyệt đối đến **file PDF** của cuốn sách, HOẶC đường dẫn đến **thư mục** chứa nhiều file PDF.
2. Đường dẫn **thư mục lưu kết quả** đầu ra.
3. **Tên tác giả** và **tên cuốn sách** (để AI nhập vai dịch thuật đúng văn phong).

*Lưu ý: Không thực hiện các bước tiếp theo cho đến khi người dùng cung cấp đủ thông tin.*

---

### Bước 2: Phân tích yêu cầu và Khởi tạo Subagents (nếu cần)
- **1 file PDF duy nhất**: Thực hiện quy trình tuần tự bình thường.
- **Thư mục nhiều file PDF**: Dùng `invoke_subagent` để tạo các Trợ lý phụ xử lý song song từng file.

---

### Bước 3: Chuẩn bị môi trường & Trích xuất văn bản từ PDF

Cài đặt thư viện cần thiết: `pip install pdfplumber num2words`

Viết và chạy script Python **`extract_raw.py`** để:
1. Đọc toàn bộ PDF bằng `pdfplumber`
2. Xác định trang Mục Lục (TOC) và **bỏ qua** các trang đó khi tìm chương
3. Phát hiện ranh giới các **Chương chính** dựa vào dòng đầu trang khớp với pattern tiêu đề
4. Lưu nội dung thô từng chương vào thư mục riêng

**YÊU CẦU BẮT BUỘC:** Mỗi thư mục chương phải có file `raw_original.txt` — đây là **bằng chứng gốc** để QC sau này, tuyệt đối không được sửa đổi file này.

```
[output_dir]/
├── 00-Preface/    └── raw_original.txt
├── 01-Intro/      └── raw_original.txt
├── 02-Chuong-01/  └── raw_original.txt
└── ...
```

---

### Bước 4: Dịch thuật & Phân tích Cấu trúc bằng AI — TRỰC TIẾP

> 🧠 **AI là tác nhân chính trong bước này**, không phụ thuộc Google Translate API.

AI đọc từng file `raw_original.txt` và thực hiện **đồng thời 2 nhiệm vụ** trong một lần xử lý:

#### 4.1 — Dịch thuật chất lượng cao (AI-Powered)

AI trực tiếp dịch toàn bộ nội dung từ tiếng Anh sang **tiếng Việt chuẩn xác, tự nhiên**, theo phong cách phù hợp với thể loại sách:

- **Dịch sát nghĩa, giữ văn phong tác giả**: Không diễn giải lại, không tóm tắt
- **Giữ nguyên tên riêng, thuật ngữ** rồi phiên âm ra tiếng Việt ở bước 5
- **Ưu tiên câu văn tự nhiên** khi đọc thành tiếng (không dịch theo nghĩa từng từ kiểu máy móc)
- Nếu đoạn quá dài để dịch một lần, AI tự chia thành các đoạn nhỏ (theo ranh giới đoạn văn) và dịch tuần tự

#### 4.2 — Phân tích cấu trúc và tách Tiêu đề/Nội dung

Đây là nhiệm vụ **quan trọng nhất** của bước này. PDF thường không có định dạng rõ ràng nên tiêu đề và nội dung bị dính liền nhau. AI phải tự phân tích và tách chúng.

**Nhận diện dòng là TIÊU ĐỀ khi:**
- Là tên chương (ví dụ: `1 Set the Table`, `Chapter 3 Apply the 80/20 Rule`)
- Là tiêu đề phụ (sub-heading) đứng trước đoạn giải thích (ví dụ: `Focus on Activities, Not Accomplishments`)
- Ngắn, cô đọng, không kết thúc bằng dấu chấm câu trong bản gốc
- Thường viết hoa chữ cái đầu mỗi từ (Title Case) trong tiếng Anh

**Ví dụ nhận diện và xử lý:**

❌ **Sai** — tiêu đề bị dính vào nội dung:
```
Số lượng nhiệm vụ so với tầm quan trọng Đây là một khám phá thú vị. Mỗi nhiệm vụ...
```

✅ **Đúng** — tách tiêu đề ra, thêm ngắt nghỉ:
```
Số lượng nhiệm vụ so với tầm quan trọng. ......

Đây là một khám phá thú vị. Mỗi nhiệm vụ...
```

**Quy tắc tách bắt buộc:**
1. Tiêu đề chương/phần đứng **trên một dòng riêng**
2. Sau tiêu đề: thêm **`. ......`** rồi xuống **1 dòng trắng**
3. Nội dung đoạn văn bắt đầu trên dòng mới
4. Kết thúc mỗi đoạn văn cũng thêm **`. ......`** rồi xuống **1 dòng trắng**

#### 4.3 — Định dạng output sau khi dịch

AI lưu kết quả vào file `translated.txt` với định dạng chuẩn như sau:

```
[Tiêu đề chương dịch sang tiếng Việt]. ......

[Đoạn nội dung 1 đã dịch, các câu trong đoạn cách nhau bằng dấu phẩy hoặc chấm tự nhiên]. ......

[Tiêu đề phụ nếu có]. ......

[Đoạn nội dung 2 đã dịch]. ......
```

**Ví dụ output chuẩn** (từ chương 3 Eat That Frog):
```
Chương ba. Áp dụng Quy tắc Tám Mươi, Hai Mươi cho Mọi Thứ. ......

Chúng ta luôn có đủ thời gian, nếu chúng ta biết sử dụng nó đúng cách. ......

Quy tắc Tám Mươi, Hai Mươi là một trong những khái niệm hữu ích nhất về quản lý thời gian và cuộc sống. Nó còn được gọi là Nguyên lý Pa-rê-tô, theo tên nhà kinh tế học người Ý Vin-frê-đô Pa-rê-tô, người đầu tiên viết về nó vào năm một nghìn tám trăm chín mươi lăm. ......

Tập trung vào Hoạt động, không phải Thành tích. ......

Bạn thường thấy những người có vẻ bận rộn cả ngày, nhưng lại hoàn thành rất ít việc thực chất. Điều này hầu như luôn luôn xảy ra vì họ đang bận làm những công việc có giá trị thấp, trong khi trì hoãn một hoặc hai nhiệm vụ quan trọng thực sự tạo ra sự khác biệt. ......
```

#### 4.4 — Xử lý theo chương, dùng Subagents song song (nếu nhiều chương)

- Nếu sách có nhiều chương (> 5), AI dùng `invoke_subagent` để dịch song song nhiều chương cùng lúc
- Mỗi subagent nhận: `raw_original.txt` của 1 chương + tên tác giả + tên sách
- Kết quả lưu vào `translated.txt` tương ứng

---

### Bước 5: Xử lý định dạng TTS chuẩn bằng Python — BẮT BUỘC

Sau khi AI đã dịch và phân tách cấu trúc (Bước 4), Python script **`format_auto.py`** áp dụng các xử lý cơ học bổ sung lên `translated.txt`:

1. **Xóa ký tự đặc biệt không TTS-friendly:**
   - Ngoặc kép `""`, nháy đơn `'`, ngoặc đơn `()`
   - Gạch ngang `—`, gạch nối `-`, dấu hai chấm `:`, dấu chấm phẩy `;`
   - Thay thế bằng dấu phẩy `,` nếu cần giữ nhịp

2. **Chuyển số còn sót thành chữ tiếng Việt** bằng `num2words(n, lang='vi')`:
   - Ví dụ: `80%` → `tám mươi phần trăm`, `21` → `hai mươi mốt`

3. **Phiên âm tên nước ngoài còn sót** bằng Regex (dự phòng cho những tên AI chưa phiên âm):
   - Ví dụ: `Brian Tracy` → `Brai-ân Tờ-rây-xi`, `Peter Drucker` → `Pi-tờ Đrắc-kờ`

4. **Kiểm tra và đảm bảo** mọi đoạn văn đều kết thúc bằng `. ......` và có 1 dòng trắng phân tách

5. **Lưu kết quả** vào `Kich-ban-1.txt` trong mỗi thư mục chương

**Cấu trúc output sau Bước 5:**
```
[output_dir]/
└── 02-Chuong-01/
    ├── raw_original.txt    ← Văn bản thô từ PDF (KHÔNG sửa)
    ├── translated.txt      ← Bản dịch AI (đã phân tách cấu trúc)
    └── Kich-ban-1.txt      ← Kịch bản thô cấp 1 ✅
```

---

## ✅ Hoàn thành Bước 5

Sau khi tất cả các chương có `Kich-ban-1.txt`, thông báo cho người dùng và **hướng dẫn kích hoạt skill tiếp theo**:

> 🎯 **Bước tiếp theo:** Kích hoạt skill **`refine_audiobook_scripts`** để:
> - Rechunk kịch bản về 2800–3000 ký tự/file
> - Tinh chỉnh nhịp thở bằng LLM theo chuẩn prompt TTS
> - Dọn dẹp thư mục và báo cáo hoàn tất
