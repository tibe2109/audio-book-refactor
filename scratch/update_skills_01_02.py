import os
import shutil

SKILL_01_CONTENT = """---
name: arf_01_pdf_structure_extractor
description: "Bước 01 trong Dây chuyền Sách nói Toàn năng (Universal Audiobook Pipeline): Bóc tách cấu trúc tài liệu PDF phức tạp, loại bỏ hoàn toàn nhiễu trình bày (Header, Footer, số trang in, chú thích chân trang Footnotes, các trang Mục lục TOC) và khởi tạo Session Manifest tổng thể (.session_manifest.json). Áp dụng thuật toán hàn gắn Drop-Cap nghệ thuật bị gãy dòng, giải quyết layout 1 cột và đa cột (Multi-column reading order) theo chuẩn dòng chảy ngữ nghĩa tự nhiên. Tự động tiền thẩm định cấu trúc tác phẩm theo 3 nhóm thể loại: Khoa học quản trị (loại bỏ footnotes, giữ nguyên phân cấp chương vĩ mô, chuyển đổi bảng biểu thành tuần tự), Tự lực phát triển bản thân (bảo toàn trọn vẹn callout box và bài tập hành động), và Văn học cổ điển/sử thi (bảo toàn câu đối biền ngẫu, bài thơ đề từ, hàn Drop-Cap triệt để). Tích hợp cơ chế nhận diện và đóng thẻ ngữ nghĩa chuẩn cho 6 nhóm nội dung phi văn bản trực quan phức tạp (bảng biểu số liệu, biểu đồ sơ đồ, hình ảnh minh họa tri thức, công thức toán học LaTeX, khối mã code thuật toán, ma trận dữ liệu) để bảo toàn 100% thông tin nguyên tác không bị rơi rớt hay đứt đoạn mạch đọc trước khi chuyển dịch. Xuất bản tệp văn bản gốc bất biến raw_original.txt trong từng thư mục chương độc lập làm căn cứ đối soát ground truth. Kích hoạt khi bóc tách PDF gốc hoặc bắt đầu dự án sách nói mới."
---

# Kỹ năng 01: Bóc Tách Cấu Trúc PDF (PDF Structure Extractor)

## 1. Đặc Tả Quy Trình Thao Tác Chuẩn (Specification - SOP)

Kỹ năng `arf_01_pdf_structure_extractor` là khâu tiếp nhận đầu vào nguyên bản của hệ thống ARF. Nhiệm vụ tối thượng là trích xuất dữ liệu chữ sạch từ file PDF, giữ nguyên tính chân thực 100% của tác giả, nhận diện cấu trúc phi văn bản và loại bỏ mọi tạp âm định dạng trước khi chuyển sang các bước xử lý ngôn ngữ.

### 1.1 Ma Trận Phân Loại Thể Loại Tiền Kỳ (Pre-Review Layout Matrix)
| Nhóm Thể Loại | Đặc Điểm Bố Cục Nhận Diện | Quy Chuẩn Xử Lý SOP |
| :--- | :--- | :--- |
| **Khoa học / Quản trị / PMBOK** | Mục lục số học (1.1, 1.2), bảng biểu, sơ đồ, footnote chân trang. | Khử sạch footnote và số trang; bọc thẻ cấu trúc bảng biểu và sơ đồ; giữ ranh giới chương vĩ mô. |
| **Tự lực / Phát triển bản thân** | Khung ghi chú (Callout boxes), câu hỏi đúc kết, bài tập thực hành. | Giữ trọn vẹn nội dung callout box đưa vào mạch văn chính; không nhầm lẫn callout với Header/Footer lặp lại. |
| **Văn học / Kịch nghệ / Sử thi** | Drop-Cap hoa mỹ rớt dòng, câu đối biền ngẫu, thơ đề từ đầu hồi. | Hàn gắn Drop-Cap 100%; bảo vệ tuyệt đối các khổ thơ cổ và câu đối biền ngẫu, nghiêm cấm cắt xén. |

### 1.2 Quy Chuẩn Nhận Diện & Đóng Thẻ Ngữ Nghĩa 6 Nhóm Trực Quan (Structural Tagging Matrix)
Áp dụng quy chuẩn từ `Docs/HUONG_DAN_THUYET_MINH_NOI_DUNG_TRUC_QUAN_AUDIOBOOK.md` để không làm mất thông tin tác giả và không làm vỡ mạch câu khi bóc tách:

| Nhóm Phần Tử | Dấu Hiệu Nhận Diện Trong PDF | Cú Pháp Đóng Thẻ Ngữ Nghĩa Chuẩn | Mục Đích Cho Bước Sau |
| :--- | :--- | :--- | :--- |
| **1. Bảng biểu (Tables)** | Khung lưới ô, bảng Markdown, bảng text cách tab/khoảng trắng. | `[TABLE: <tiêu đề bảng nếu có>]` ... `[END_TABLE]` | Bảo toàn tiêu đề hàng/cột và số liệu; ngăn đứt câu văn xuôi xung quanh. |
| **2. Biểu đồ (Charts/Diagrams)** | Khối sơ đồ dòng chảy, cây phân cấp, đồ thị trục X-Y kèm caption. | `[CHART_DIAGRAM: <loại sơ đồ, tiêu đề>]` ... `[END_CHART]` | Giữ nguyên các thông số trục, xu hướng và chú giải để B02 thuyết minh. |
| **3. Minh họa (Illustrations)** | Hình vẽ, tranh minh họa, ảnh chụp tư liệu có kèm caption/chú thích. | `[ILLUSTRATION: <caption ảnh>]` | Lọc bỏ ảnh trang trí trống nghĩa; giữ lại caption ảnh ngụ ngôn/tri thức. |
| **4. Công thức (Math)** | Biểu thức toán học ký hiệu đặc biệt, phân số, tích phân, LaTeX. | `[MATH_FORMULA: <công thức raw/LaTeX>]` | Giữ nguyên công thức gốc để B02 chuyển thể Spoken Math. |
| **5. Mã nguồn (Code/Algorithms)** | Khối thụt lề code, font chữ đơn cách (Monospace), hàm và biến. | `[CODE_BLOCK: <ngôn ngữ>]` ... `[END_CODE]` | Bảo toàn luồng lệnh và định danh tiếng Anh, ngăn xáo trộn ký tự. |
| **6. Ma trận (Matrices)** | Bảng số ma trận nhiều chiều, mảng ngoặc vuông chứa hệ số. | `[MATRIX: <kích thước, tiêu đề>]` ... `[END_MATRIX]` | Giữ nguyên giá trị các chiều để B02 thuyết minh đặc tính toán học. |

### 1.3 Quy Chuẩn Kỹ Thuật Bất Biến
- **Hàn gắn chữ cái Drop-Cap (Drop-Cap Healer):** Bắt buộc nối liền các chữ cái đơn lẻ rớt dòng: `T\\nrong` $\\to$ `Trong`, `B\\nạn` $\\to$ `Bạn`, `C\\non` $\\to$ `Con`, `Đ\\niều` $\\to$ `Điều`, `M\\nột` $\\to$ `Một`.
- **Thứ tự đọc đa cột (Multi-column Reading Order):** Với layout 2 cột, đọc hết cột bên trái từ trên xuống dưới trước khi chuyển sang cột bên phải.
- **Tính Bất Biến Của Văn Bản Gốc (Ground Truth Invariance):** Tệp `raw_original.txt` là dữ liệu nguồn cố định, dùng làm căn cứ tính tỷ lệ giãn nở từ vựng $R = W_{vi} / W_{en}$ ở Bước 02 ($R \\ge 0.85$) và Bước 07 ($R \\ge 0.75$).

---

## 2. Điều Kiện Kích Hoạt & Cụm Từ Khóa (When to Use & Triggers)

### 2.1 Bối Cảnh Sử Dụng
- Khi người dùng cung cấp một file PDF sách nguồn và muốn bắt đầu dự án sản xuất sách nói.
- Khi sách chứa nhiều bảng biểu, đồ thị, công thức hoặc đoạn code cần bóc tách bảo toàn thông tin.
- Khi cần bóc tách lại một chương cụ thể từ tệp PDF gốc để làm lại dữ liệu thô.

### 2.2 Câu Lệnh Người Dùng Điển Hình (User Prompt Triggers)
- *"Bóc tách cuốn sách PDF này: `path/to/book.pdf`"*
- *"Trích xuất cấu trúc các chương từ file PDF vào dự án"*
- *"Khởi tạo dự án sách nói từ file PDF `tailieu.pdf`"*
- *"Bóc tách sách kỹ thuật có nhiều bảng biểu, code và sơ đồ"*
- *"Chạy bước 1 cho cuốn sách PDF mới"*

---

## 3. Trình Tự Thực Thi Từng Bước (Step-by-Step Execution)

```mermaid
flowchart TD
    P1["Pha 1: Tiền Kiểm Tra\\n- Kiểm tra đường dẫn PDF hợp lệ\\n- Đọc Mục lục & 10 trang đầu thẩm định layout\\n- Quét sự xuất hiện của bảng biểu, sơ đồ, code"] --> P2["Pha 2: Thực Thi Cốt Lõi (Python)\\n- Khử Header/Footer/Footnotes\\n- Hàn nối Drop-Cap gãy dòng\\n- Đóng thẻ ngữ nghĩa 6 nhóm trực quan\\n- Trích xuất theo dải trang chương vĩ mô"]
    P2 --> P3["Pha 3: Khởi Tạo Manifest & Hậu Kiểm\\n- Sinh raw_original.txt từng chương\\n- Tạo .session_manifest.json\\n- Kiểm tra kích thước file (>100 bytes)"]
```

### Pha 1: Tiền kiểm tra & Khảo sát cấu trúc (Pre-checks)
1. Xác thực sự tồn tại của file PDF đầu vào và quyền đọc.
2. Quét mục lục (Table of Contents) và dải trang (Page Ranges) để lập danh sách chương vĩ mô (00-Preface, 01-Intro, 02-Chuong-01...).
3. Khảo sát sơ bộ xem tài liệu có chứa bảng biểu, sơ đồ, công thức toán hoặc mã nguồn để kích hoạt chế độ đóng thẻ cấu trúc.

### Pha 2: Thao tác bóc tách kỹ thuật (Core Processing)
1. AI Chính trực tiếp chạy script Python bóc tách (không qua sub-agent trung gian để đảm bảo tốc độ < 2 giây):
   ```bash
   python core/antigravity_audiobook_pipeline.py --pdf "<PATH_TO_PDF>" --book_slug "<BOOK_SLUG>"
   ```
   hoặc chạy module trực tiếp:
   ```bash
   python core/extract_pdf_structure.py "<PATH_TO_PDF>" "Kich-ban-clipchamp/<BOOK_SLUG>"
   ```
2. Bộ lọc regex tự động quét và loại bỏ số trang, tiêu đề lặp lại ở đầu và cuối trang.
3. Nối các đoạn văn bị ngắt dòng do giới hạn trang in (`\\n` giữa câu chưa kết thúc dấu chấm).
4. Áp dụng các thẻ ngữ nghĩa `[TABLE: ...]`, `[CHART_DIAGRAM: ...]`, `[ILLUSTRATION: ...]`, `[MATH_FORMULA: ...]`, `[CODE_BLOCK: ...]`, `[MATRIX: ...]` cho các khối phần tử trực quan tương ứng.

### Pha 3: Khởi tạo Manifest & Hậu kiểm (Post-Processing & Verification)
1. Lưu nội dung thô nguyên bản vào `raw_original.txt` trong từng thư mục chương.
2. Khởi tạo hoặc cập nhật `.session_manifest.json` ghi nhận số từ, dải trang, và gán `step_1_status: "completed"`.
3. Kiểm tra kiểm toán: Xác nhận mọi file `raw_original.txt` có kích thước $> 100$ bytes và các thẻ cấu trúc đóng mở đầy đủ.

---

## 4. Ràng Buộc Đầu Ra (Output Contract)

Mọi lần chạy thành công của kỹ năng `arf_01` phải đảm bảo cấu trúc thư mục chuẩn xác:

```text
Kich-ban-clipchamp/[book_slug]/
├── .session_manifest.json          # Ghi nhận session_id, pipeline_stage: "01_pdf_extracted"
├── 00-Preface/
│   └── raw_original.txt           # Văn bản thô phần Mở đầu (Bất biến, chứa thẻ cấu trúc nếu có)
├── 01-Intro/
│   └── raw_original.txt           # Văn bản thô phần Dẫn nhập (Bất biến)
├── 02-Chuong-01/
│   └── raw_original.txt           # Văn bản thô Chương 1 (Bất biến)
└── ...
```

### Cấu Trúc Tệp `.session_manifest.json` Tối Thiểu:
```json
{
  "book_slug": "Ten-Sach",
  "pipeline_stage": "01_pdf_extracted",
  "chapters": [
    {
      "index": 1,
      "folder": "01-chuong-1",
      "title": "Chương 1: Khởi Đầu",
      "step_1_status": "completed",
      "word_count_raw": 3450
    }
  ]
}
```

---

## 5. Cơ Chế Phủ Định & Điều Cấm Kỵ (Negative Triggers & Constraints)

- **TUYỆT ĐỐI KHÔNG TỰ Ý DỊCH THUẬT:** Kỹ năng này chỉ bóc tách ngôn ngữ gốc nguyên bản của tác giả. Cấm gọi API dịch thuật tại Bước 01.
- **TUYỆT ĐỐI KHÔNG TÓM TẮT HOẶC BIÊN TẬP:** Không được lược bỏ ví dụ, bảng biểu, sơ đồ, công thức hay code thuật toán của tác giả. Bắt buộc giữ nguyên vẹn trong các thẻ cấu trúc tương ứng.
- **TUYỆT ĐỐI KHÔNG BĂM NHỎ CHƯƠNG VĨ MÔ:** Cấm tạo thư mục con theo tiểu mục nhỏ (H2, H3). Chỉ chia theo Chương/Hồi lớn.
- **KHÔNG SỬ DỤNG KHI ĐẦU VÀO ĐÃ LÀ FILE TEXT SẴN CÓ:** Nếu người dùng đã cung cấp file text sạch (`raw_original.txt`), bỏ qua Bước 01 và chuyển thẳng sang Bước 02.
- **CẤM TẠO FILE TẠM Ở THƯ MỤC GỐC (ROOT):** Mọi tệp xử lý trung gian phải nằm trong thư mục sách hoặc `scratch/`.
"""

SKILL_02_CONTENT = """---
name: arf_02_author_style_translator
description: "Bước 02 trong Dây chuyền Sách nói Toàn năng (Universal Audiobook Pipeline): Động cơ dịch thuật chuyên sâu nhập vai tác giả (Author Style Dual-Engine Translator), chuyển thể văn bản gốc tiếng Anh (raw_original.txt) sang tiếng Việt (translated.txt) với cam kết bảo toàn nguyên tác 100% (Zero-Summarization Invariant). Tích hợp cơ chế Dual-Engine chuyên biệt: Profile 2A dành cho sách Phi hư cấu / Quản trị / Khoa học kỹ thuật (ngôi xưng Tôi - Bạn truyền cảm hứng, súc tích, đĩnh đạc, nạp từ điển chuyên ngành custom_phonetics.json, bảo tồn thuật ngữ Latinh gốc); Profile 2B dành cho Văn học kinh điển / Kịch nghệ / Sử thi (5 Trụ cột kịch nghệ, bảo tồn 100% âm Hán-Việt, đại từ xưng hô cổ phong và thi ca biền ngẫu). Tích hợp toàn diện quy chuẩn Thuyết minh nội dung trực quan (Narrative Audio Adaptation) từ Docs/HUONG_DAN_THUYET_MINH_NOI_DUNG_TRUC_QUAN_AUDIOBOOK.md cho 6 nhóm phi văn bản: Bảng biểu (thuyết minh tổng hợp, cấm đọc tọa độ ô lưới), Biểu đồ sơ đồ (nêu trục đo, xu hướng, thông điệp), Ảnh minh họa tri thức, Công thức toán học (Spoken Math ngữ âm Việt hoàn chỉnh, khử sạch mã LaTeX), Code máy tính và thuật toán (tường thuật luồng logic, cấm đọc cú pháp gõ phím), và Ma trận dữ liệu. Khóa cứng tỷ lệ dãn nở từ vựng R = W_vi / W_en bắt buộc đạt R >= 0.85 (Hard Fail nếu R < 0.80). Kích hoạt khi yêu cầu dịch thuật chương sách hoặc chuyển ngữ tài liệu sang tiếng Việt chuẩn phát thanh."
---

# Kỹ năng 02: Dịch Thuật Nhập Vai Tác Giả (Author Style Translator)

## 1. Đặc Tả Quy Trình Thao Tác Chuẩn (Specification - SOP)

Kỹ năng `arf_02_author_style_translator` thực hiện chuyển thể ngôn ngữ có chiều sâu, giữ trọn vẹn 100% nội dung, số liệu, ví dụ và văn phong của tác giả. Tích hợp năng lực chuyển hóa các khối trực quan và phi văn bản thành lời nói tự nhiên chuẩn phát thanh (Narrative Audio Adaptation).

### 1.1 Phân Định Dual-Engine Chuyên Biệt
| Tiêu Chí | Profile 2A: Phi Hư Cấu / Quản Trị / Kỹ Thuật | Profile 2B: Văn Học Kinh Điển / Sử Thi / Kịch Nghệ |
| :--- | :--- | :--- |
| **Ngôi xưng tác giả** | Khóa cứng ngôi `Tôi - Bạn` truyền cảm hứng, gần gũi, chuyên nghiệp. | Đa thanh theo góc nhìn tác phẩm (ngôi thứ ba toàn tri hoặc độc thoại nhân vật). |
| **Thuật ngữ chuyên môn** | Giữ nguyên chữ quốc tế ở lần đầu giới thiệu (*Stakeholder*, *Project Charter*); thân bài dùng tiếng Việt tự nhiên hoặc viết tắt (*P-M-I*). | Giữ nguyên 100% âm Hán-Việt (chức danh, nhân vật, thành quách); số hóa cổ kính (*canh ba, ba vạn quân, hai mươi trượng*). |
| **Nhịp điệu câu cú** | Câu gãy gọn, liên từ rõ ràng (*tuy nhiên,*, *do đó,*), chuẩn bị lấy hơi cho TTS. | Giữ trọn khẩu khí nhân vật (*Chúa công, Quân sư*), bảo toàn thể thơ và câu đối biền ngẫu. |
| **Từ điển áp dụng** | Nạp `custom_phonetics.json` trong thư mục sách. | Nạp hệ thống xưng hô cổ phong và danh xưng nhân vật lịch sử. |

### 1.2 Quy Chuẩn Thuyết Minh Nội Dung Trực Quan & Phi Văn Bản (Visual Audio Adaptation)
Chuyển thể toàn diện 6 nhóm thẻ cấu trúc từ Bước 01 theo `Docs/HUONG_DAN_THUYET_MINH_NOI_DUNG_TRUC_QUAN_AUDIOBOOK.md`:

| Nhóm Phần Tử | Quy Chuẩn Chuyển Thể Phát Thanh (SOP) | Điều Tuyệt Đối Cấm (Negative Rules) |
| :--- | :--- | :--- |
| **1. Bảng biểu (`[TABLE]`)** | **Thuyết minh tổng hợp (Narrative Synthesis):** Nêu mục đích so sánh, xu hướng chính và các số liệu trọng yếu nhất. | Cấm đọc tọa độ ô lưới (`|---|---|` hoặc "Hàng một cột một là..."). |
| **2. Biểu đồ (`[CHART_DIAGRAM]`)** | Thuyết minh loại biểu đồ, 2 trục đo lường, xu hướng vận động chính (tăng, giảm, điểm uốn) và thông điệp tác giả chứng minh. | Cấm mô tả chi tiết pixel, màu sắc đường nét đồ họa. |
| **3. Minh họa (`[ILLUSTRATION]`)** | Lược bỏ ảnh trang trí; diễn giải ảnh mang tri thức/ẩn dụ ngụ ngôn thành 1 - 2 câu văn xuôi súc tích, giàu hình tượng. | Cấm đọc các câu tham chiếu giấy in (*"xem hình trang bên"*). |
| **4. Công thức (`[MATH_FORMULA]`)** | **Spoken Math:** Diễn ngôn bằng câu chữ ngữ âm tiếng Việt hoàn chỉnh, giữ tên biến Latinh chuẩn quốc tế. | Cấm để sót mã LaTeX thô (`$`, `$$`, `\\frac`, `\\sum`, `\\sqrt`). |
| **5. Code & Thuật toán (`[CODE_BLOCK]`)** | Tường thuật **luồng logic và ý nghĩa thuật toán** (Input $\\to$ Logic kiểm tra $\\to$ Output), giữ nguyên định danh tiếng Anh. | Cấm đọc từng ký tự cú pháp gõ phím (ngoặc nhọn `{}`, thụt lề, `;`). |
| **6. Ma trận (`[MATRIX]`)** | Thuyết minh kích thước, ý nghĩa các hàng và cột, đặc tính toán học quan trọng (đường chéo chính, ma trận chuyển vị). | Cấm đọc danh sách dài các con số rời rạc không có ngữ cảnh. |
| **Khử tham chiếu in ấn** | Chuyển đổi linh hoạt: *"như hình dưới đây"* $\\to$ *"qua sơ đồ phân tích"*, *"bảng trang bên"* $\\to$ *"bảng so sánh sau đây"*. | Cấm giữ nguyên từ ngữ chỉ vị trí trang in vật lý. |

### 1.3 Khóa Cứng Tỷ Lệ Giãn Nở Từ Vựng (Zero-Summarization Formula)
$$R = \\frac{\\text{Số từ Tiếng Việt } (W_{vi})}{\\text{Số từ Tiếng Anh Gốc } (W_{en})}$$
- **Quy chuẩn đánh giá:**
  - $0.85 \\le R \\le 1.50$: **ĐẠT CHUẨN (PASSED)**. Thuyết minh trực quan giúp mở rộng tự nhiên lượng từ vựng, bảo toàn trọn vẹn thông điệp gốc.
  - $R < 0.80$: **HARD FAIL (BỊ TÓM TẮT)** $\\to$ Từ chối nghiệm thu, khóa quyền chuyển sang Bước 03, kích hoạt tự động dịch lại.

---

## 2. Điều Kiện Kích Hoạt & Cụm Từ Khóa (When to Use & Triggers)

### 2.1 Bối Cảnh Sử Dụng
- Khi thư mục chương đã có file `raw_original.txt` từ Bước 01 hoặc do người dùng cung cấp.
- Khi tài liệu kỹ thuật, quản trị chứa nhiều bảng biểu, công thức hoặc mã code cần chuyển thể thành lời nói tự nhiên.
- Khi người dùng muốn dịch một chương sách hoặc toàn bộ sách sang tiếng Việt chuẩn bị cho thu âm sách nói.

### 2.2 Câu Lệnh Người Dùng Điển Hình (User Prompt Triggers)
- *"Dịch chương này sang tiếng Việt: `01-chuong-1`"*
- *"Dịch nội dung cuốn sách từ tiếng Anh sang tiếng Việt chuẩn phát thanh"*
- *"Chuyển thể tài liệu kỹ thuật có nhiều công thức toán và code sang kịch bản sách nói"*
- *"Thuyết minh các bảng biểu và sơ đồ trong chương theo chuẩn audio"*
- *"Bản dịch này bị ngắn quá, hãy dịch lại đầy đủ không tóm tắt"*

---

## 3. Trình Tự Thực Thi Từng Bước (Step-by-Step Execution)

```mermaid
flowchart TD
    P1["Pha 1: Tiền Phân Đoạn & Anchor Ngữ Cảnh\\n- Kiểm tra raw_original.txt\\n- Quét các thẻ trực quan [TABLE], [CHART]...\\n- Phân đoạn 800-1200 từ nếu W > 1200\\n- Nạp từ điển custom_phonetics.json"] --> P2["Pha 2: Dịch Thuật Đa Tác Tử Song Song\\n- Giao việc đồng thời qua invoke_subagent\\n- Áp dụng Narrative Audio Adaptation cho thẻ trực quan\\n- Rolling Context: 3 câu tiếng Việt cuối đoạn k-1\\n- Áp dụng Profile 2A hoặc 2B tương ứng"]
    P2 --> P3["Pha 3: Ghép Nối, Seam Smoothing & Hậu Kiểm\\n- Nối các đoạn thành translated.txt\\n- Khử sạch rác LaTeX và cú pháp bảng thô\\n- Làm mượt câu ranh giới tiếp giáp\\n- Kiểm toán tỷ lệ R >= 0.85"]
```

### Pha 1: Tiền phân đoạn & Khóa ngữ cảnh (Pre-checks)
1. Đọc `raw_original.txt`, đếm số từ tiếng Anh $W_{en}$.
2. Nhận diện các thẻ trực quan `[TABLE]`, `[CHART_DIAGRAM]`, `[ILLUSTRATION]`, `[MATH_FORMULA]`, `[CODE_BLOCK]`, `[MATRIX]` trong văn bản nguồn.
3. Nạp từ điển tùy biến `custom_phonetics.json` (nếu có trong thư mục sách).
4. **Phân đoạn tiền dịch thuật:** Nếu $W_{en} > 1.200$ từ, AI chia nhỏ thành các khối 800 – 1.200 từ theo tiêu đề hoặc ranh giới đoạn `\\n\\n` (không cắt giữa các khối thẻ trực quan).

### Pha 2: Dịch thuật đa tác tử song song (Core Translation & Sub-agents)
1. Với văn bản dài, AI Chính kích hoạt đồng thời mảng Sub-agents chuyên môn qua `invoke_subagent`:
   - Nạp hướng dẫn chuyển thể Narrative Synthesis cho các thẻ trực quan.
   - Áp dụng Profile 2A hoặc 2B tương ứng.
2. **Rolling Context:** Mỗi Sub-agent phụ trách đoạn $k \\ge 2$ bắt buộc nạp kèm 3 câu tiếng Việt cuối của đoạn $k-1$ để giữ liền mạch đại từ và liên từ.

### Pha 3: Ghép nối, Seam Smoothing & Hậu kiểm (Post-Processing & QC)
1. Nối các bản dịch con thành `translated.txt`.
2. **Khử rác định dạng:** Đảm bảo 100% không còn ký tự LaTeX thô (`$`), không còn ký tự bảng Markdown (`|---|`), không còn ký tự code gõ phím (`{}`).
3. **Seam Smoothing:** Rà soát và chỉnh sửa các câu ranh giới tiếp giáp giữa các đoạn con, đảm bảo liên từ tiếp nối tự nhiên không lộ vết cắt.
4. **Kiểm toán từ vựng:** Đếm $W_{vi}$, tính $R = W_{vi} / W_{en}$. Nếu $R < 0.80$, kích hoạt Self-Healing Loop dịch lại đoạn thiếu ý.
5. Cập nhật `.session_manifest.json` ghi nhận `step_2_status: "completed"`, `word_count_translated: W_vi`, `expansion_ratio: R`.

---

## 4. Ràng Buộc Đầu Ra (Output Contract)

File đầu ra bắt buộc nằm tại thư mục gốc của chương:
- Đường dẫn: `[book_dir]/[chapter_folder]/translated.txt`
- Tiêu chí nghiệm thu:
  - File tồn tại, định dạng UTF-8, không rỗng.
  - Tỷ lệ giãn nở đạt $R \\ge 0.85$.
  - Tiêu đề chương hồi giữ nguyên phân cấp.
  - Bảng biểu, sơ đồ, công thức, code được chuyển thể thành văn xuôi tường thuật tự nhiên hoàn chỉnh.
  - Không chứa dấu vết dịch máy thô thiển hoặc câu bị cắt cụt.

### Mẫu Cập Nhật Manifest:
```json
{
  "folder": "01-chuong-1",
  "step_2_status": "completed",
  "word_count_raw": 2400,
  "word_count_translated": 2520,
  "expansion_ratio": 1.05
}
```

---

## 5. Cơ Chế Phủ Định & Điều Cấm Kỵ (Negative Triggers & Constraints)

- **TUYỆT ĐỐI CẤM TÓM TẮT (ZERO-SUMMARIZATION):** Không được lược bỏ bất kỳ ví dụ, số liệu, luận điểm, bảng biểu hay công thức nào của tác giả. Nếu phát hiện $R < 0.80$, coi là vi phạm nghiêm trọng.
- **CẤM ĐỌC CÚ PHÁP GÕ PHÍM HOẶC TỌA ĐỘ BẢNG:** Tuyệt đối cấm đọc "Hàng một cột một", "Dấu ngoặc nhọn", "Chấm phẩy", hoặc để nguyên bảng markdown `|---|---|`.
- **CẤM ĐỂ SÓT KÝ TỰ LATEX:** Không để sót `$`, `$$`, `\\frac`, `\\sum` trong `translated.txt`.
- **CẤM ĐỔI NGÔI XƯNG BẤT NHẤT:** Không được đoạn trước xưng `Tôi - Bạn`, đoạn sau lại đổi thành `Chúng ta` hoặc `Tác giả`.
- **KHÔNG SỬ DỤNG KHI CHƯA CÓ RAW_ORIGINAL.TXT:** Phải hoàn tất Bước 01 hoặc có file thô sạch trước khi chạy Bước 02.
- **CẤM LƯU FILE DỊCH VÀO THƯ MỤC GỐC DỰ ÁN (ROOT):** Tệp `translated.txt` phải nằm đúng trong thư mục chương.
"""

mirrors = [
    ".agent/skills",
    ".agents/skills",
    ".gemini/skills",
    ".agy/skills"
]

for mirror in mirrors:
    path_01 = os.path.join(mirror, "arf_01_pdf_structure_extractor", "SKILL.md")
    path_02 = os.path.join(mirror, "arf_02_author_style_translator", "SKILL.md")
    
    os.makedirs(os.path.dirname(path_01), exist_ok=True)
    with open(path_01, "w", encoding="utf-8") as f:
        f.write(SKILL_01_CONTENT.strip() + "\n")
    print(f"[OK] Written {path_01}")
    
    os.makedirs(os.path.dirname(path_02), exist_ok=True)
    with open(path_02, "w", encoding="utf-8") as f:
        f.write(SKILL_02_CONTENT.strip() + "\n")
    print(f"[OK] Written {path_02}")

print("Update completed successfully!")
