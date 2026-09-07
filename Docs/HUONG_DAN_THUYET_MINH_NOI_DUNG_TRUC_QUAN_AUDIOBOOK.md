# HƯỚNG DẪN QUY CHUẨN THUYẾT MINH NỘI DUNG PHI VĂN BẢN (NON-TEXT & COMPLEX ELEMENTS) CHO SÁCH NÓI

Tài liệu này tổng hợp toàn bộ các quy tắc thực thi (Rules) và thực hành tốt nhất (Best Practices) được tích hợp trong bộ kỹ năng `arf_*` (từ `arf_01` đến `arf_07`), phục vụ việc chuyển đổi các nội dung trực quan và kỹ thuật phức tạp thành lời nói tự nhiên chuẩn phát thanh.

---

## 1. BẢNG BIỂU (TABLES)

### Nguyên tắc:
- **Cấm:** Không đọc từng ô lưới theo tọa độ hàng/cột (`|---|---|` hoặc "Hàng một cột một là...").
- **Chuẩn:** Thuyết minh tường thuật tổng hợp (Narrative Synthesis): Nêu mục đích so sánh, các xu hướng chính và số liệu trọng yếu nhất.

### Ví dụ Thực tế:
* **Dữ liệu gốc:**
  | Phương pháp | Chi phí ban đầu | Thời gian bàn giao | Độ linh hoạt |
  | :--- | :--- | :--- | :--- |
  | Waterfall | Cao | 6 - 12 tháng | Thấp |
  | Agile | Trung bình | 2 - 4 tuần/chu kỳ | Rất cao |

* **Kịch bản Sách nói (Audio Script):**
  > *"Tác giả tổng kết sự khác biệt này qua một bảng so sánh hai phương pháp: Phương pháp Waterfall đòi hỏi chi phí ban đầu cao và thời gian bàn giao kéo dài từ sáu đến mười hai tháng với độ linh hoạt thấp. Ngược lại, phương pháp Agile tối ưu chi phí ở mức trung bình, rút ngắn thời gian bàn giao xuống chỉ còn hai đến bốn tuần cho mỗi chu kỳ, mang lại khả năng thích ứng linh hoạt rất cao."*

---

## 2. BIỂU ĐỒ & SƠ ĐỒ (CHARTS & DIAGRAMS)

### Nguyên tắc:
- **Cấm:** Không mô tả chi tiết pixel, màu sắc đường nét hay câu lệnh đồ họa.
- **Chuẩn:** Thuyết minh loại biểu đồ, hai trục đo lường, xu hướng vận động chính (tăng, giảm, điểm uốn, cực trị) và thông điệp tác giả muốn chứng minh.

### Ví dụ Thực tế:
* **Dữ liệu gốc:** Biểu đồ đường (Line chart) thể hiện đường cong quên lãng (Ebbinghaus Forgetting Curve).
* **Kịch bản Sách nói (Audio Script):**
  > *"Biểu đồ đường cong quên lãng trong tài liệu chỉ ra một thực tế đáng kinh ngạc: Não bộ chúng ta quên đi hơn năm mươi phần trăm lượng thông tin mới chỉ sau một giờ đầu tiên, và lượng kiến thức này tiếp tục tụt dốc xuống chỉ còn hai mươi phần trăm sau một tháng nếu không có sự ôn tập định kỳ."*

---

## 3. HÌNH ẢNH MINH HỌA (ILLUSTRATIONS & PHOTOS)

### Nguyên tắc:
- Ảnh trang trí vô nghĩa: Lược bỏ để giữ nhịp nghe liền mạch.
- Ảnh mang tri thức hoặc ẩn dụ: Thuyết minh bối cảnh và ý nghĩa ẩn dụ trong 1 - 2 câu súc tích.

### Ví dụ Thực tế:
* **Dữ liệu gốc:** Tranh minh họa ngụ ngôn Con ếch và Nồi nước sôi.
* **Kịch bản Sách nói (Audio Script):**
  > *"Hình ảnh minh họa phác họa câu chuyện ngụ ngôn nổi tiếng về chú ếch trong nồi nước: Khi nhiệt độ tăng lên từ từ, chú ếch thích nghi trong sự êm ấm mà không nhận ra hiểm họa, cho đến khi nước sôi thì đã quá muộn — một lời cảnh tỉnh sâu sắc về những mối nguy tiềm tàng đến từ sự thỏa hiệp chậm rãi trong cuộc sống."*

---

## 4. CÔNG THỨC TOÁN HỌC (MATH EQUATIONS)

### Nguyên tắc:
- **Cấm:** Không để sót mã LaTeX (`\frac`, `\sum`, `\sqrt`, `$$`).
- **Chuẩn:** Diễn ngôn bằng câu chữ ngữ âm tiếng Việt hoàn chỉnh (Spoken Math), tên biến quốc tế chuẩn Latinh.

### Ví dụ Thực tế:
* **Công thức gốc:**
  $$\sigma = \sqrt{\frac{\sum_{i=1}^N (x_i - \mu)^2}{N}}$$
* **Kịch bản Sách nói (Audio Script):**
  > *"Độ lệch chuẩn xích-ma được tính bằng căn bậc hai của một phân số: trong đó tử số là tổng xích-ma bình phương độ lệch giữa từng giá trị x-i và giá trị trung bình muy với i chạy từ một đến N, còn mẫu số là tổng số phần tử N trong tập dữ liệu."*

---

## 5. CODE MÁY TÍNH & THUẬT TOÁN (SOURCE CODE & ALGORITHMS)

### Nguyên tắc:
- **Cấm:** Tuyệt đối không đọc từng ký tự cú pháp gõ phím (dấu ngoặc nhọn `{}`, thụt lề, dấu chấm phẩy `;`).
- **Chuẩn:** Tường thuật **luồng logic và ý nghĩa thuật toán** (Input ➡️ Logic xử lý ➡️ Output). Giữ nguyên các định danh then chốt bằng tiếng Anh bản địa (Native Bilingual Code-Switching).

### Ví dụ Thực tế:
* **Mã nguồn gốc:**
  ```python
  def authenticate_user(token: str):
      if not token or is_expired(token):
          raise InvalidTokenException("Token expired")
      user = db.find_user_by_token(token)
      return user
  ```
* **Kịch bản Sách nói (Audio Script):**
  > *"Trong đoạn mã minh họa, hàm xác thực authenticate_user tiếp nhận tham số token của người dùng. Trước hết, hàm kiểm tra điều kiện: nếu token bị rỗng hoặc đã hết hạn, hệ thống sẽ kích hoạt ngoại lệ InvalidTokenException để chặn truy cập. Nếu token hợp lệ, hàm sẽ truy vấn cơ sở dữ liệu và trả về đối tượng thông tin người dùng tương ứng."*

---

## 6. MA TRẬN & ĐẠI SỐ TUYẾN TÍNH (MATRICES)

### Nguyên tắc:
- **Cấm:** Không đọc danh sách dài các con số rời rạc không ngữ cảnh.
- **Chuẩn:** Nêu kích thước, ý nghĩa các hàng và cột, đặc tính toán học quan trọng (đường chéo chính, trọng số, ma trận chuyển vị).

### Ví dụ Thực tế:
* **Dữ liệu gốc:** Ma trận tương quan $3 \times 3$ giữa Lãi suất, Lạm phát và Tăng trưởng GDP.
* **Kịch bản Sách nói (Audio Script):**
  > *"Mối quan hệ này được thể hiện qua một ma trận tương quan kích thước ba nhân ba. Trên đường chéo chính, hệ số tự tương quan luôn đạt giá trị tối đa bằng một. Ở các ô đối xứng, ta nhận thấy mối tương quan nghịch rõ rệt giữa lãi suất và lạm phát, giải thích tác động của chính sách tiền tệ đối với nền kinh tế vĩ mô."*

---

## 7. CHECKLIST QC KIỂM TRA TRƯỚC KHI THU ÂM (SKILL 07)

- [ ] Đã loại bỏ 100% rác bảng Markdown (`|`, `|---|---|`).
- [ ] Đã loại bỏ 100% rác LaTeX (`$`, `$$`, `\frac`, `\sqrt`).
- [ ] Không còn đoạn code thô dạng gõ phím chưa được chuyển thể thành logic thuật toán.
- [ ] Đã xóa sạch các câu tham chiếu giấy in (*"xem hình dưới"*, *"bảng trang bên"*).
- [ ] Đã chèn nhịp thở nghỉ `. ...... ` sau các phần diễn giải công thức hoặc biểu đồ trọng điểm.
