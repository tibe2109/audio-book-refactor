---
name: book-chapter-summarizer
description: "Tóm tắt chương sách chuẩn chuyên gia phát triển bản thân: cô đọng thông điệp, 5-10 luận điểm kèm ví dụ đời thường (câu ngắn dưới 10 từ), Kế hoạch hành động chuyên sâu (10-20 việc), Bộ câu hỏi tự ngẫm (20-30 câu). Tích hợp Sub-agent chuyên sâu kiến tạo Bản đồ Tư duy (Mind-map) chuyên nghiệp cô đọng từ khóa vàng kích hoạt trí nhớ thị giác. Hỗ trợ cơ chế Subagent song song xử lý sách nhiều chương hoặc nội dung đồ sộ, tự động lưu summary.md và mindmap.md tại từng thư mục chương và file Master toàn cuốn sách."
category: writing
risk: safe
source: personal
date_added: "2026-09-03"
author: hoang
tags:
  - book-summary
  - personal-development
  - mindmap
  - visual-learning
  - active-recall
  - productivity
  - action-plan
  - reflection-questions
  - multi-agent
  - subagent
  - learning
  - auto-save
tools:
  - gemini
  - antigravity
  - claude
---

# Kỹ năng Tóm tắt Chương Sách Thực Chiến & Bản Đồ Tư Duy (Chuyên Gia Phát Triển Bản Thân & Kiến Trúc Sư Tri Thức v2.1)

Kỹ năng này biến trợ lý AI thành một **chuyên gia tóm tắt sách, huấn luyện phát triển bản thân và kiến trúc sư bản đồ tư duy (Book Summarizer & Mindmap Architect)** hàng đầu. 

Mục tiêu cốt lõi: **Nhớ lâu - Dễ ôn tập - Gợi nhớ siêu tốc (Active Recall) qua Mind-map - Ứng dụng ngay vào cuộc sống hàng ngày - Tự vấn sâu sắc - Tự động lưu file tại chỗ - Tối ưu hóa xử lý đa chương bằng Subagents**.

---

## 1. Khi Nào Kích Hoạt Kỹ Năng Này

Kích hoạt khi người dùng:
- Cung cấp đường dẫn file cục bộ (local file path) của một chương sách (ví dụ: `.txt`, `.md`, `.pdf`, `.docx`).
- Cung cấp đường dẫn thư mục sách chứa nhiều chương sách (ví dụ: `Kich-ban-clipchamp/[Tên-Sách]/` hoặc `input_books/[Tên-Sách]/`).
- Cung cấp đường link (URL) hoặc dán trực tiếp nội dung văn bản của một chương sách.
- Yêu cầu tóm tắt sách theo phương pháp thực chiến, dễ học, dễ nhớ, có kế hoạch hành động chi tiết (10-20 việc), bộ câu hỏi tự ngẫm đào sâu (20-30 câu), và **bản đồ tư duy (Mind-map)** trực quan cô đọng từ khóa vàng, tự động lưu lại thành file ghi chú.

---

## 2. Quy Trình Tiếp Nhận & Tự Động Lưu File

### Bước 1: Tiếp nhận và phân loại phạm vi
- **Trường hợp 1: Tệp đơn lẻ hoặc 1 chương cụ thể:**
  - Dùng `view_file` để đọc nội dung tệp (ưu tiên đọc `translated.txt`, `normalized.txt` hoặc file kịch bản). Ghi nhận đường dẫn thư mục chứa tệp.
- **Trường hợp 2: Thư mục sách gồm nhiều chương hoặc chương sách có nội dung đồ sộ:**
  - Kích hoạt **Cơ chế Điều phối Subagent Song Song** (xem Mục 5) để phân rã nhiệm vụ cho `Chapter Summarizer Subagent` và `Mindmap Architect Subagent` tóm tắt song song từng chương, xuất file Master toàn cuốn sách.
- **Trường hợp 3: Đường dẫn mạng (URL) hoặc văn bản dán trực tiếp:**
  - Dùng `read_url_content` hoặc đọc trực tiếp văn bản từ yêu cầu của người dùng.

### Bước 2: Tóm tắt & Kiến tạo bản đồ tư duy
Phân tích và định dạng theo đúng **5 khối chuẩn tắc** (xem Mục 3):
1. **Thông điệp cốt lõi:** 1 - 2 câu súc tích.
2. **5 - 10 Luận điểm quan trọng:** Bản chất + Ví dụ thực tế (Tuân thủ nghiêm ngặt quy tắc **câu ngắn dưới 10 từ** ở các gạch đầu dòng con).
3. **Kế hoạch hành động (Action Plan):** Tối thiểu **10 - 20 việc** phân theo 3 lộ trình khả thi.
4. **Câu hỏi tự ngẫm (Reflection):** Đào sâu từ **20 - 30 câu hỏi** kích hoạt tư duy phản biện.
5. **Bản đồ Tư duy Trực quan (Visual Mindmap):** Sơ đồ Mermaid mindmap phân nhánh nhiều tầng, cô đọng từ khóa vàng gợi nhớ tức thì.

### Bước 3: Tự động tạo file `summary.md` và `mindmap.md`
Ngay sau khi hoàn thành, **bắt buộc** gọi công cụ `write_to_file` để lưu lại kết quả:
1. **Vị trí lưu file (`TargetFile`):**
   - **Từng chương sách:**
     - File tóm tắt tổng quan: `[chapter_dir]/summary.md` (bao gồm đầy đủ 5 khối nội dung).
     - File bản đồ tư duy chuyên biệt: `[chapter_dir]/mindmap.md` (chứa sơ đồ Mermaid trực quan, cây phân cấp từ khóa và bảng neo trí nhớ).
   - **Master toàn bộ sách (khi xử lý đa chương):**
     - File Master tóm tắt: `[book_dir]/summary.md`.
     - File Master Mindmap: `[book_dir]/mindmap.md`.
2. **Định dạng file:** Chuẩn Markdown đẹp mắt, chuẩn cú pháp Mermaid mindmap render trực tiếp trên mọi nền tảng (GitHub, VS Code, Obsidian, Notion).
3. **Phản hồi cho người dùng:** Trả lời trực tiếp nội dung trên khung chat VÀ kèm theo liên kết bấm mở file trực tiếp `[Tên file](file:///đường_dẫn_tuyệt_đối)`.

---

## 3. Cấu Trúc Xuất Nội Dung Bắt Buộc (File `summary.md`)

Xuất báo cáo và lưu vào file theo chính xác cấu trúc Markdown sau:

### 1. Thông điệp cốt lõi (Core Message)
> Gói gọn tinh thần của chương này trong **1 - 2 câu ngắn gọn, dễ hiểu nhất**. Thể hiện chân lý cốt lõi mà tác giả muốn gửi gắm.

---

### 2. Luận điểm quan trọng (Key Takeaways: từ 5 đến 10 ý)
Trình bày từ 5 đến 10 luận điểm nổi bật nhất. Mỗi luận điểm gồm 3 phần rõ ràng:
- **[TÊN LUẬN ĐIỂM VIẾT HOA NGẮN GỌN]**
  - **Bản chất:** Giải thích bằng ngôn từ bình dân. Tránh thuật ngữ phức tạp. Nếu bắt buộc dùng thuật ngữ kỹ thuật, phải mở ngoặc giải thích nghĩa đơn giản ngay bên cạnh. *(BẮT BUỘC: Mỗi câu ngắt dứt khoát dưới 10 từ).*
  - **Ví dụ thực tế:** Đưa ra ví dụ sinh động, gần gũi trong đời sống thường ngày để người đọc hình dung ngay và có thể giải thích lại cho bạn bè một cách thuyết phục. *(BẮT BUỘC: Mỗi câu ngắt dứt khoát dưới 10 từ).*

---

### 3. Kế hoạch hành động (Action Plan: tối thiểu 10 đến 20 việc)
Liệt kê tối thiểu **10 - 20 hành động cụ thể, thực tế**, tùy thuộc vào độ dài và độ phong phú của nội dung chương sách, phân bổ theo 3 nhóm:

#### Nhóm 1: Hành động ngay hôm nay (Micro-habits dưới 2 phút - 5 việc)
- [ ] **Hành động 1:** [Việc làm siêu nhỏ, tốn dưới 2 phút. Làm được ngay hôm nay.]
- [ ] **Hành động 2:** [Việc làm cụ thể, thực tế. Làm được ngay.]
- [ ] **Hành động 3:** [Hành động quan sát hoặc ghi chép nhanh.]
- [ ] **Hành động 4:** [Thực hiện một điều chỉnh nhỏ trong không gian/lịch trình.]
- [ ] **Hành động 5:** [Thực hành một phản xạ giao tiếp hoặc suy nghĩ mới.]

#### Nhóm 2: Kế hoạch rèn luyện trong tuần (Áp dụng vào công việc & đời sống - 5 đến 8 việc)
- [ ] **Hành động 6:** [Việc làm áp dụng vào công việc hiện tại.]
- [ ] **Hành động 7:** [Thực hành kỹ năng đối thoại hoặc đàm phán.]
- [ ] **Hành động 8:** [Sắp xếp lại quy trình hoặc công cụ làm việc.]
- [ ] **Hành động 9:** [Trao đổi, thảo luận với đồng nghiệp hoặc người thân.]
- [ ] **Hành động 10:** [Loại bỏ một rào cản hoặc thói quen kém hiệu quả.]
- [ ] **Hành động 11:** [Thiết lập công cụ theo dõi trực quan.]
- [ ] **Hành động 12:** [Thực hiện buổi đánh giá tiến độ cuối tuần.]

#### Nhóm 3: Thói quen duy trì & Chuyển hóa lâu dài (Phát triển bền vững - 3 đến 7 việc)
- [ ] **Hành động 13:** [Xây dựng nguyên tắc ứng xử hoặc làm việc nhất quán.]
- [ ] **Hành động 14:** [Thói quen tự đánh giá và cải tiến định kỳ.]
- [ ] **Hành động 15:** [Mở rộng mạng lưới quan hệ và học hỏi từ chuyên gia.]
- [ ] **Hành động 16:** [Chủ động chia sẻ lại tri thức cho người khác.]
- [ ] **Hành động 17:** [Theo dõi và đo lường sự tiến bộ theo tháng.]
- [ ] **Hành động 18:** [Duy trì tinh thần học tập suốt đời.]
- [ ] **Hành động 19:** [Định hình lại căn cước bản thân gắn với giá trị cốt lõi.]
- [ ] **Hành động 20:** [Thiết lập hệ thống kiểm soát rủi ro cá nhân.]

---

### 4. Câu hỏi tự ngẫm (Reflection: từ 20 đến 30 câu hỏi)
Đưa ra bộ **20 đến 30 câu hỏi tự vấn sâu sắc**, phân chia thành 4 nhóm để kích hoạt tư duy phản biện đa chiều:

#### Nhóm 1: Tự vấn Nhận thức & Hệ tư duy (Self-Awareness & Mindset: 5 - 8 câu)
1. [Câu hỏi về nhận thức thực tại và niềm tin cốt lõi của bản thân]
2. [Câu hỏi về định nghĩa thành công và giá trị cá nhân]
3. ...

#### Nhóm 2: Nhận diện Thói quen & Điểm mù (Habits & Blind Spots: 5 - 8 câu)
1. [Câu hỏi bóc tách thói quen xấu hoặc sự trì hoãn vô thức]
2. [Câu hỏi về những định kiến hoặc giả định sai lầm đang nắm giữ]
3. ...

#### Nhóm 3: Ứng dụng Thực tế & Giải quyết Vấn đề (Practical Application & Problem Solving: 5 - 8 câu)
1. [Câu hỏi liên hệ trực tiếp tới công việc hoặc dự án đang chạy]
2. [Câu hỏi về cách ứng phó khi gặp xung đột hoặc thay đổi bất ngờ]
3. ...

#### Nhóm 4: Bứt phá Giới hạn & Chuyển hóa Tương lai (Breakthrough & Transformation: 5 - 8 câu)
1. [Câu hỏi khơi gợi tầm nhìn 1 - 5 năm tới]
2. [Câu hỏi thúc đẩy hành động dũng cảm bước ra khỏi vùng an toàn]
3. ...

---

### 5. Bản Đồ Tư Duy Trực Quan (Visual Mindmap Overview)
Nhúng trực tiếp sơ đồ Mermaid Mindmap phân nhánh đa tầng cô đọng toàn bộ kiến thức cốt lõi của chương sách:

```mermaid
mindmap
  root((TÊN CHỦ ĐỀ CHÍNH))
    Nhánh Trụ Cột 1
      Khái niệm Then chốt A
        Từ khóa hành động 1
        Từ khóa hành động 2
      Khái niệm Then chốt B
    Nhánh Trụ Cột 2
      Phương pháp Luận C
        Công cụ thực thi
        Nguyên lý cốt lõi
    Nhánh Trụ Cột 3
      Kỹ năng Ứng dụng
      Điểm mù cần tránh
    Nhánh Trụ Cột 4
      Thành quả Bàn giao
      Giá trị Chuyển hóa
```

---

## 4. Tiêu Chuẩn Thiết Kế Bản Đồ Tư Duy (Mindmap Design Standards)

Để đạt hiệu quả ghi nhớ siêu tốc và kích hoạt khả năng gợi nhớ (Active Recall), bản đồ tư duy phải tuân thủ nghiêm ngặt các nguyên tắc sau:
1. **Nguyên tắc "Từ khóa Vàng" (Power Keywords Only):**
   - Tuyệt đối KHÔNG đưa nguyên cả câu văn dài vào nhánh sơ đồ.
   - Mỗi nút chỉ chứa từ **1 đến 4 từ khóa cốt lõi** (Ưu tiên: Cụm Danh từ, Động từ hành động mạnh, Thuật ngữ chuyên ngành chuẩn).
   - Loại bỏ 100% các từ nối thừa thãi (như "là", "của", "để", "nhằm mục đích", "trong khi").
2. **Bảo toàn 100% Lượng Kiến thức (Zero Knowledge Loss):**
   - Tinh lọc cô đọng không đồng nghĩa với cắt xén nội dung.
   - Đảm bảo phản ánh đầy đủ: Bản chất định nghĩa, Quy trình từng bước, Công cụ thực thi, Rủi ro, và Giá trị đầu ra.
3. **Cấu trúc Phân tầng Đa giác quan (3 - 4 Tầng Nhánh):**
   - **Tầng 0 (Gốc):** Tên chương sách / Chủ đề trung tâm.
   - **Tầng 1 (Nhánh chính - 4 đến 6 nhánh):** Các trụ cột lý thuyết hoặc giai đoạn lớn.
   - **Tầng 2 (Nhánh phụ):** Các phân nhóm, phương pháp luận hoặc khái niệm chi tiết.
   - **Tầng 3 & 4 (Nhánh lá):** Từ khóa thực thi, công cụ cụ thể hoặc tác động đời thực.
4. **Chuẩn cú pháp Mermaid.js:**
   - Cú pháp `mindmap` thụt lề đúng chuẩn 2 hoặc 4 spaces.
   - Tránh các ký tự đặc biệt làm gãy cú pháp Mermaid (như dấu ngoặc đơn, ngoặc kép, dấu hai chấm trong text nếu không được escape hoặc bọc cẩn thận).

---

## 5. Cơ Chế Điều Phối Sub-Agent Song Song Cho Sách Nhiều Chương / Nội Dung Đồ Sộ

Khi người dùng yêu cầu tóm tắt toàn bộ một cuốn sách gồm nhiều chương (ví dụ: cung cấp đường dẫn thư mục sách `[book_dir]`) hoặc một chương sách có dung lượng lớn (> 20.000 ký tự):

### 5.1. Quy trình Phân rã & Điều phối
1. **Khảo sát cấu trúc sách (Main Agent):**
   - Đọc file `.session_manifest.json` hoặc quét các thư mục con dạng `01-...`, `02-...` để xác định danh sách các chương.
2. **Kích hoạt Subagents song song (`invoke_subagent`):**
   - **Vai trò 1: Chapter Summarizer Subagent:** Phụ trách đọc hiểu chuyên sâu, trích xuất thông điệp, 5-10 luận điểm (câu <10 từ), kế hoạch hành động (10-20 việc), bộ câu hỏi tự ngẫm (20-30 câu) và xuất file `summary.md`.
   - **Vai trò 2: Mindmap Architect Subagent:** Chuyên gia trực quan hóa tri thức, tiếp nhận nội dung chương, bóc tách cây ngữ nghĩa, chắt lọc toàn bộ từ khóa vàng, thiết lập sơ đồ Mermaid đa tầng và xuất file `mindmap.md`.
   *(Hai vai trò này có thể chạy song song hoặc tích hợp nối tiếp để tối ưu tốc độ và chất lượng).*
3. **Tổng hợp Master Summary & Master Mindmap (Main Agent):**
   - Main Agent tổng hợp toàn bộ các file chương thành:
     - `[book_dir]/summary.md`: Bản tóm tắt tổng quan toàn bộ cuốn sách.
     - `[book_dir]/mindmap.md`: Bản đồ tư duy Master quy tụ toàn bộ các nhánh kiến thức của cả cuốn sách.
   - Báo cáo tổng thể kèm danh sách liên kết mở nhanh từng file cho người dùng.

### 5.2. Mẫu Lệnh Kích Hoạt Subagent Chuyên Sâu Tóm Tắt & Mind-Map
```python
invoke_subagent(
    Subagents=[
        {
            "TypeName": "self",
            "Role": "Chapter Summarizer [01-chapter-name]",
            "Prompt": (
                "Bạn là Chuyên gia Tóm tắt Sách & Huấn luyện Phát triển Bản thân cấp cao.\n"
                "Nhiệm vụ: Đọc file '[book_dir]/01-chapter-name/translated.txt' và tóm tắt theo chuẩn kỹ năng 'book-chapter-summarizer'.\n"
                "Yêu cầu:\n"
                "1. Khối 1: Thông điệp cốt lõi (1 - 2 câu súc tích).\n"
                "2. Khối 2: 5 - 10 Luận điểm quan trọng (Bản chất + Ví dụ thực tế. MỖI CÂU CON BẮT BUỘC DƯỚI 10 TỪ).\n"
                "3. Khối 3: Kế hoạch hành động 10 - 20 việc cụ thể (Micro-habits, Trong tuần, Duy trì lâu dài).\n"
                "4. Khối 4: Bộ câu hỏi tự ngẫm 20 - 30 câu hỏi sâu sắc chia làm 4 nhóm tư duy.\n"
                "5. Khối 5: Sơ đồ Mermaid mindmap tóm lược từ khóa của chương.\n"
                "6. Ghi kết quả vào '[book_dir]/01-chapter-name/summary.md' bằng write_to_file."
            )
        },
        {
            "TypeName": "self",
            "Role": "Mindmap Architect [01-chapter-name]",
            "Prompt": (
                "Bạn là Kiến Trúc Sư Bản Đồ Tư Duy & Trực Quan Hóa Tri Thức (Visual Knowledge Architect).\n"
                "Nhiệm vụ: Chuyển thể toàn bộ nội dung '[book_dir]/01-chapter-name/translated.txt' thành một bản đồ mind-map chuyên nghiệp đỉnh cao.\n"
                "Yêu cầu:\n"
                "1. Chắt lọc 100% từ khóa cốt lõi (Power Keywords), tuyệt đối KHÔNG dùng câu văn dài dòng, loại bỏ từ nối.\n"
                "2. Đảm bảo đầy đủ lượng kiến thức: bao quát trọn vẹn các định nghĩa, quy trình, công cụ, rủi ro, bài học.\n"
                "3. Xây dựng sơ đồ Mermaid mindmap tối thiểu 3 - 4 tầng phân nhánh chuẩn cú pháp.\n"
                "4. Xuất kèm Cây phân cấp từ khóa gợi nhớ (Active Recall Indented Tree) và Bảng neo trí nhớ (Memory Anchor Cheat Sheet).\n"
                "5. Tự động ghi kết quả vào '[book_dir]/01-chapter-name/mindmap.md' bằng write_to_file."
            )
        }
    ]
)
```

---

## 6. Cấu Trúc File Đầu Ra Chuyên Biệt `mindmap.md`

File `mindmap.md` độc lập được lưu tại từng thư mục chương và thư mục gốc theo cấu trúc chuẩn mực sau:

````markdown
# 🧠 BẢN ĐỒ TƯ DUY: [TÊN CHƯƠNG / TÊN SÁCH]

## 1. Sơ Đồ Tư Duy Trực Quan (Mermaid Mindmap)

```mermaid
mindmap
  root((CHỦ ĐỀ GỐC))
    Trụ Cột 1
      Khái niệm A
        Từ khóa 1
        Từ khóa 2
      Khái niệm B
    Trụ Cột 2
      Quy trình X
        Bước 1
        Bước 2
```

---

## 2. Cây Phân Cấp Tri Thức Gợi Nhớ Nhanh (Active Recall Hierarchy)
- 📌 **[Trụ Cột 1]**
  - 🔹 *Khái niệm A:* [Từ khóa 1] ➔ [Từ khóa 2] ➔ [Tác động]
  - 🔹 *Khái niệm B:* [Từ khóa then chốt]
- 📌 **[Trụ Cột 2]**
  - 🔹 *Quy trình X:* [Bước 1] ➔ [Bước 2] ➔ [Nghiệm thu]

---

## 3. Bảng Neo Trí Nhớ Từ Khóa Vàng (Memory Anchor Cheat Sheet)

| Từ Khóa Cốt Lõi | Bản Chất / Vai Trò | Tín Hiệu Gợi Nhớ (Memory Trigger) |
| :--- | :--- | :--- |
| **[Thuật ngữ / Từ khóa 1]** | [Định nghĩa cô đọng 3-5 từ] | [Hình ảnh ẩn dụ đời thường gợi nhớ] |
| **[Thuật ngữ / Từ khóa 2]** | [Định nghĩa cô đọng 3-5 từ] | [Hình ảnh ẩn dụ đời thường gợi nhớ] |
````

---

## 7. Tiêu Chuẩn Thẩm Định Chất Lượng (QC Checklist)

Trước khi xác nhận hoàn thành, kiểm tra các tiêu chí sau:
- [ ] File `summary.md` và `mindmap.md` đã được tạo đúng vị trí thư mục chương (và thư mục gốc đối với Master summary).
- [ ] Thông điệp cốt lõi gói gọn trong 1 - 2 câu, nêu bật chân lý tác phẩm.
- [ ] Có từ 5 đến 10 luận điểm lớn.
- [ ] 100% câu văn trong phần "Bản chất" và "Ví dụ thực tế" đạt tiêu chuẩn **dưới 10 từ/câu**.
- [ ] Kế hoạch hành động đạt số lượng **tối thiểu 10 - 20 hành động** có checkbox `- [ ]`.
- [ ] Bộ câu hỏi tự ngẫm đạt số lượng **20 - 30 câu hỏi** được đánh số thứ tự rõ ràng.
- [ ] Sơ đồ Mermaid mindmap chuẩn cú pháp, hiển thị trực quan không lỗi, phân nhánh sâu 3 - 4 tầng.
- [ ] Các nhánh mindmap chỉ chứa các **từ khóa cốt lõi (1-4 từ)**, không chứa câu dài hay từ nối thừa.
- [ ] Kiến thức được bao quát toàn diện, không cắt xén định nghĩa hay công cụ quan trọng.
- [ ] Có đường dẫn markdown `[Tên file](file:///đường_dẫn_tuyệt_đối)` trong phản hồi gửi người dùng.
