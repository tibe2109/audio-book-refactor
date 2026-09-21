---
name: abv_01_thematic_visual_prompter
description: "Kỹ năng phân tích chuyên sâu nội dung, văn học, lịch sử và nghệ thuật hội họa đa vùng miền của tác phẩm sách nói (Audiobook Thematic Visual & Artistic Prompter). Đóng vai trò chuyên gia phân tích văn học và họa sĩ bậc thầy am hiểu hội họa Á - Âu từ cổ trang đến hiện đại (Sơn thủy, Hoa điểu, Bạch họa Trung Hoa, Ukiyo-e Nhật Bản, Tranh lụa và Sơn mài Việt Nam, Tranh Phục hưng, Baroque Chiaroscuro Tây Âu, Hiện thực bi tráng Nga và Tiểu họa Ba Tư). Kỹ năng tự động quét nạp kho tri thức tác phẩm đồ sộ (quét summary.md toàn sách, summary.md từng chương hoặc normalized.txt), phân tích thể loại, lịch sử bối cảnh, chọn lọc mô tả chi tiết về thiên nhiên đất trời hùng vỹ, hình tượng nhân vật và biến cố đặc sắc. Kỹ năng xác định chuẩn xác chất liệu vẽ (Mực nho Tùng yên, Màu khoáng tự nhiên, Sơn dầu nhiều lớp, Màu keo tempera, Vữa ướt Fresco, Vàng quỳ, Bạc quỳ) và bề mặt vẽ (Giấy Tuyên Thành, Giấy dâu tằm Washi, Giấy điệp, Lụa thô, Vải toan lanh, Gỗ tấm, Tường thạch cao). Xuất bản bộ 10 Master Prompts 7 tầng đỉnh cao đạt chuẩn Midjourney v6, FLUX.1 Pro, SDXL (16:9) kèm bảng danh mục backgrounds/prompts.json và BACKGROUNDS_CATALOG.md lưu trực tiếp trong thư mục Final của tác phẩm. Kỹ năng chỉ tạo tài liệu và kịch bản prompt chi tiết cho người dùng tự tạo ảnh, không tự động sinh ảnh AI, bảo tồn nguyên vẹn ảnh do người dùng cung cấp. Bắt buộc kích hoạt Hội đồng Multi-Agent Swarm (Literary Analyst, Art Historian, Master Prompt Artist, Continuity QC) xử lý song song toàn bộ tác phẩm."
---

# 🎨 ABV-01: THEMATIC VISUAL & ARTISTIC MASTER PROMPTER
## QUY TRÌNH THAO TÁC CHUẨN (SOP) PHÂN TÍCH VĂN HỌC & THIẾT LẬP MASTER PROMPTS HỘI HỌA ĐA VÙNG MIỀN

---

## 1. SOP / ĐẶC TẢ KỸ THUẬT (SPECIFICATION)
`abv_01_thematic_visual_prompter` là kỹ năng bước 1 trong nhánh sản xuất Video Sách Nói (ABV Pipeline), đảm nhiệm vai trò kép: **Chuyên Gia Phân Tích Văn Học - Lịch Sử** và **Họa Sĩ Nghệ Thuật Bậc Thầy (Master Fine Art Prompt Artist)**:
- **Tự động phân giải đường dẫn (Smart Path Resolution):** Tiếp nhận linh hoạt đường dẫn thư mục gốc tác phẩm (ví dụ `.../Tam-Quoc-Dien-Nghia`) hoặc đường dẫn thư mục Final Audio (`.../Final-Tam-Quoc-Dien-Nghia`) do người dùng cung cấp, tự động định vị chính xác vị trí lưu trữ và quét nạp nguyên liệu.
- **Phân tích bối cảnh lịch sử, văn học & trường phái hội họa đa vùng miền:**
  1. *Trung Quốc Cổ phong / Sử thi / Huyền huyễn:* Tranh Sơn thủy (山水 - Thanh lục sơn thủy, Thủy mặc loang mờ), Tranh Hoa điểu (花鳥), Tranh Nhân vật (人物), Bạch họa (白描).
  2. *Nhật Bản Cổ điển:* Ukiyo-e (Phù thế hội mộc bản), Yamato-e, Suibokuga (Thủy mặc thiền tông).
  3. *Việt Nam & Đông Nam Á:* Tranh khắc gỗ dân gian Đông Hồ, Hàng Trống, Tranh lụa cung đình / phố thị cận đại, Tranh sơn mài truyền thống (Sơn ta, vỏ trứng, vàng bạc quỳ).
  4. *Tây Âu Kinh điển & Kịch nghệ:* Tranh Phục hưng (Renaissance Art), Tranh Baroque (Chiaroscuro tương phản kịch tính Caravaggio/Rembrandt), Tranh Tôn giáo giáo đường.
  5. *Đông Âu & Nga:* Hiện thực bi tráng thế kỷ 19 (Peredvizhniki - Ilya Repin, Shishkin), Thánh tượng cổ (Icon).
  6. *Trung Á & Ba Tư:* Tranh tiểu họa Ba Tư (Persian Miniature), arabesque kỷ hà, bột ngọc lưu ly Lapis Lazuli.
  7. *Hiện đại / Triết học / Quản trị:* Tối giản điện ảnh (Cinematic Minimalism), kiến trúc ánh sáng tự nhiên.
- **Xác định chính xác Chất liệu màu (Medium) và Bề mặt vẽ (Support):**
  - *Chất liệu màu:* Mực nho Tùng yên (Pine soot ink), Màu khoáng tự nhiên (Chu sa cinnabar, Thạch thanh azurite, Thạch lục malachite), Sơn dầu nhiều lớp (Layered Oil Glazes), Màu keo tempera (Egg Tempera), Vữa ướt (Fresco), Sơn mài đắp nổi, Điệp vỏ sò, Lá chàm.
  - *Bề mặt vẽ:* Giấy Tuyên Thành rắc vụn vàng (Xuan paper), Giấy dâu tằm Washi, Giấy điệp, Giấy dó thô, Lụa tơ tằm cổ (Raw Silk), Vải toan lanh Bỉ (Linen Canvas), Gỗ dương/gỗ sồi tấm (Wood Panels), Tường thạch cao (Plaster Wall), Vóc gỗ mài bóng.
- **Thiết lập 10 Master Prompts 7 tầng (7-Tier Visual & Medium Engineering):**
  - Phân bổ cân đối: 4 bức Thiên nhiên Đất trời Hùng vỹ + 3 bức Hình tượng / Chân dung Nhân vật Biểu tượng + 3 bức Không gian Kiến trúc & Cao trào Lịch sử.
  - Tầng 1: Chủ đề trung tâm & Tinh thần nhân vật/cảnh quan.
  - Tầng 2: Môi trường & Bối cảnh không gian địa lý chính xác thời đại.
  - Tầng 3: Chi tiết kiến trúc, cổ vật, binh khí, hoa văn, trang phục lịch sử.
  - Tầng 4: Ánh sáng mỹ thuật & Hiệu ứng không khí (Chiaroscuro, God rays, Volumetric mist, Amber glow).
  - Tầng 5: Góc máy, cự ly ống kính & Quy luật phối cảnh hội họa (35mm, Anamorphic, Linear perspective).
  - Tầng 6: Trường phái hội họa, Bảng màu sắc thái, Chất liệu màu và Bề mặt vẽ nguyên bản.
  - Tầng 7: Tham số render Midjourney v6 / FLUX.1 Pro / SDXL (`--ar 16:9 --style raw --v 6.0`).
- **Phân định trách nhiệm rõ ràng (Prompt Artifacts Only):** Kỹ năng **chỉ tạo tài liệu kịch bản prompt**, không tự động gọi API sinh ảnh AI tốn kém, cho phép người dùng dùng prompt tự tạo ảnh theo ý muốn và lưu vào `Final-[Tên-Sách]/backgrounds/`.

---

## 2. TRIGGER / KHI NÀO SỬ DỤNG (ACTIVATION CONDITIONS)
Kỹ năng được kích hoạt trong các trường hợp sau:
1. **Tiền kỳ sản xuất Video Sách Nói:** Người dùng cung cấp đường dẫn tác phẩm hoặc thư mục Final Audio để phân tích tác phẩm và tạo bộ prompt ảnh nền 16:9.
2. **Thiết lập Concept Mỹ thuật Đỉnh cao:** Cần xây dựng bộ 10 Master Prompts mang đậm chất hội họa chuyên sâu cho các tác phẩm sử thi, kinh điển phương Đông hoặc phương Tây.
3. **Thực thi trực tiếp từ CLI:**
   ```bash
   ./venv/bin/python core/abv_visual_prompter.py "Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia"
   ```

---

## 3. TRÌNH TỰ TỪNG BƯỚC THỰC THI (STEP-BY-STEP WORKFLOW)

### Bước 3.1: Tiếp nhận và Phân giải Đường dẫn Đầu vào
- Tiếp nhận `input_path` từ người dùng. Tự động nhận diện folder `Final-[Tên-Sách]` hoặc folder gốc tác phẩm.

### Bước 3.2: Quét Nạp Kho Tri Thức Tác Phẩm (Multi-Tier Corpus Harvesting)
- Tự động quét tìm và đọc:
  1. `summary.md` tại thư mục gốc tác phẩm (bức tranh toàn cảnh).
  2. Toàn bộ các file `summary.md` trong từng thư mục chương (`[chapter]/summary.md`).
  3. Nếu thiếu summary: Quét nạp các file `normalized.txt` hoặc `kich-ban/*.txt` để rút trích các đoạn miêu tả thiên nhiên, binh pháp, nhân vật.

### Bước 3.3: Điều phối Hội Đồng Multi-Agent Swarm (Mandatory Subagent Dispatch)
Đối với các bộ tác phẩm đồ sộ (Tam Quốc, Tây Du Ký, Những người khốn khổ...), AI Chính kích hoạt Hội đồng 4 Sub-agents qua `invoke_subagent`:
- **Sub-agent 1 (`Literary & Historical Archivist`):** Đọc toàn bộ các file summary, phân tích 4 trục sự kiện chiến lược, chọn lọc 10 khoảnh khắc mang tính biểu tượng nhất.
- **Sub-agent 2 (`Art Historian & Medium Stylist`):** Xác định trường phái mỹ thuật, đối soát trang phục, kiến trúc, chỉ định chất liệu màu vẽ và bề mặt nền tương thích.
- **Sub-agent 3 (`Master Visual Prompt Artist`):** Chắp bút 10 Master English Prompts 7 tầng chuẩn mực Midjourney v6/FLUX.1 kèm Negative Prompts triệt tiêu chi tiết hiện đại.
- **Sub-agent 4 (`Art Quality & Continuity QC`):** Kiểm định tính nhất quán mỹ thuật, tỷ lệ 16:9, xuất bản `prompts.json` và `BACKGROUNDS_CATALOG.md`.

### Bước 3.4: Xuất bản Hồ Sơ Mỹ Thuật & Khởi tạo Canvas Dự Phòng
- Ghi tệp cấu hình `prompts.json` và tài liệu Markdown `BACKGROUNDS_CATALOG.md` tại `Final-[Tên-Sách]/backgrounds/`.
- Khởi tạo sẵn 10 tệp canvas nền dự phòng độ phân giải 1920x1080 (16:9) `bg_01.jpg` đến `bg_10.jpg` (giữ nguyên không ghi đè nếu người dùng đã tự đưa ảnh AI vào).

---

## 4. OUTPUT CONTRACT (CHUẨN ĐẦU RA & RÀNG BUỘC TỆP TIN)
Toàn bộ thành phẩm bắt buộc lưu trực tiếp tại thư mục `backgrounds/` bên trong thư mục Final:
- `Final-[Tên-Sách]/backgrounds/prompts.json`: Chứa 10 Master Prompts 7 tầng, phân tích bối cảnh, chất liệu vẽ, bề mặt nền và tham số kỹ thuật.
- `Final-[Tên-Sách]/backgrounds/BACKGROUNDS_CATALOG.md`: Hồ sơ danh mục mỹ thuật hoàn chỉnh định dạng Markdown để người dùng dễ dàng sao chép prompt.
- `Final-[Tên-Sách]/backgrounds/bg_01.jpg` đến `bg_10.jpg`: Đúng 10 tệp hình ảnh tỉ lệ 16:9 Full HD ($1920 \times 1080$).

---

## 5. PHỦ ĐỊNH & CẤM KỴ (NEGATIVE TRIGGERS & SYSTEM INVARIANTS)
1. **NO AUTO-AI RENDERING:** Tuyệt đối không tự động gọi API sinh ảnh tốn kém hoặc sinh ảnh nháp bừa bãi. Kỹ năng chỉ xuất bản tài liệu kịch bản prompt để người dùng tự tạo ảnh.
2. **ZERO-ROOT-FILE INVARIANT:** Cấm tạo file tạm, prompt nháp hay ảnh thử nghiệm ở thư mục root. Mọi thành phẩm phải nằm trong `Final-[Tên-Sách]/backgrounds/`.
3. **NON-DESTRUCTIVE OVERWRITE:** Nếu người dùng đã đặt các tệp ảnh AI chất lượng cao vào `bg_*.jpg`, hệ thống tuyệt đối không được ghi đè làm mất ảnh gốc.
4. **NO ANACHRONISM BLEED:** Cấm đưa bất kỳ yếu tố hiện đại (xe cộ, cột điện, dây điện, chữ ký số, phong cách hoạt hình anime) vào Master Prompts của các tác phẩm cổ điển/sử thi.
5. **ASPECT-RATIO LOCK:** Tuyệt đối khóa cứng tỷ lệ 16:9 (`--ar 16:9`), cấm tỉ lệ vuông 1:1 hoặc dọc 9:16.
