---
name: vrf_01_script_to_video_storyboard
description: "Bước 01 trong Dây chuyền Tái cấu trúc Video (Video Refactor Framework - VRF): Phân tích kịch bản sách nói (script .txt hoặc theatrical_script.json) và thiết lập kịch bản video phân cảnh chi tiết (Shot-by-Shot Storyboard & Scene Continuity). Tự động tính toán nhịp thị giác (Visual Pacing: 15–28s/ảnh), khớp audio narration timing, xác định bố cục góc máy (Cinematography & Ken Burns motion), viết Master Prompt AI hình ảnh chi tiết (Midjourney/FLUX/SDXL/Imagen), và chuẩn hóa đường dẫn lưu ảnh đầu ra."
---

# Kỹ năng VRF-01: Phân Tích Kịch Bản & Xây Dựng Storyboard Video Chi Tiết (Script to Video Storyboard)

## 1. Định Nghĩa & Mục Tiêu Cốt Lõi (Core Purpose & Principles)

Kỹ năng `vrf_01_script_to_video_storyboard` là module khởi đầu chuyên biệt thuộc **Video Refactor Framework (VRF)**. Module này tách biệt hoàn toàn với chuỗi kỹ năng âm thanh `arf_*` (Audiobook Pipeline), giữ vai trò **Tổng Đạo Diễn Hình Ảnh & Phân Cảnh Thị Giác (Visual Director & Storyboard Architect)**.

### Mục Tiêu Tối Thượng:
1. **Chuyển dịch Kịch bản Nghe sang Kịch bản Nhìn (Auditory to Visual Translation):** Tiếp nhận kịch bản đọc (`Kich-ban-N.txt` hoặc `theatrical_script.json`), bóc tách cấu trúc kịch tính thành chuỗi phân cảnh liên tục, nhịp nhàng và giàu sức gợi.
2. **Khóa cứng Nhịp Thị Giác Chống Mỏi Mắt (Visual Pacing Standard):** Khắc phục triệt để lỗi "ảnh chết" (ảnh đứng yên quá lâu gây buồn ngủ) hoặc "ảnh giật" (đổi ảnh quá nhanh gây mất tập trung). Khóa cứng dải hiển thị lý tưởng: **15 – 28 giây / ảnh** (trung bình 20 – 22 giây/ảnh).
3. **Bảo Toàn Mạch Kể Liền Mạch (100% Narrative Coverage):** 100% câu thoại và lời dẫn trong kịch bản gốc phải được neo trực tiếp vào từng shot tương ứng. Không bỏ sót bất kỳ phân đoạn nào.
4. **Chuẩn Hóa Prompt AI Hình Ảnh Chuẩn Điện Ảnh (Cinematic Master Prompting):** Thiết kế prompt tiếng Anh chi tiết theo cấu trúc 7 tầng, tương thích cao nhất với các mô hình tạo ảnh hiện đại (Midjourney v6, FLUX.1 Schnell/Dev, SDXL, Imagen 3).
5. **Đạo Diễn Bố Cục & Chuyển Động (Cinematography & Ken Burns Motion):** Từng shot phải có chỉ dẫn góc máy, cự ly, ánh sáng, và hướng chuyển động camera (Pan / Tilt / Zoom) để tạo cảm giác video sống động từ ảnh tĩnh.

---

## 2. Công Thức Toán Học Tính Nhịp Thị Giác (Visual Pacing & Timing Math)

### 2.1 Ước Tính Thời Lượng Lời Đọc (Audio Narration Estimation)
Tốc độ đọc giọng phát thanh tiêu chuẩn tiếng Việt (Nam Minh / Hoài My) trung bình đạt **2.4 – 2.7 từ/giây** (tương đương khoảng 14 – 16 ký tự/giây bao gồm dấu cách).

$$T_{\text{audio}} \text{ (giây)} \approx \frac{\text{Tổng số từ Tiếng Việt}}{2.55} \approx \frac{\text{Tổng số ký tự}}{15.2}$$

*Lưu ý:* Nếu có sẵn file `theatrical_script.json` hoặc file audio render thực tế, ưu tiên dùng timestamp thực tế.

### 2.2 Xác Định Số Lượng Shot Mục Tiêu (Optimal Shot Allocation)
Số lượng khung hình (shots) cho một kịch bản được tính bằng:

$$N_{\text{shots}} = \max\left(1, \text{round}\left(\frac{T_{\text{audio}}}{21.0}\right)\right)$$

Trong đó:
- $t_{\text{shot\_min}} = 15.0\text{s}$ (Trừ trường hợp cao trào hành động dồn dập có thể xuống 10 - 12s).
- $t_{\text{shot\_max}} = 28.0\text{s}$ (Nếu một phân cảnh dài hơn 28s, bắt buộc phải chia thành 2 góc máy khác nhau: ví dụ Wide shot sang Close-up shot).

### 2.3 Điểm Ngắt Shot Nghệ Thuật (Dramatic Cut Points)
Không ngắt shot cơ học theo số từ đơn thuần. Điểm chuyển cảnh (Cut) bắt buộc rơi vào một trong các sự kiện sau:
- **Thay đổi không gian / bối cảnh:** Từ ngự điện triều đình sang ngoại ô bến sông; từ cổng thành sang quán rượu.
- **Thay đổi nhân vật trung tâm:** Từ lời dẫn của người kể chuyện sang cận cảnh nhân vật chính xuất hiện hoặc cất tiếng thoại.
- **Biến cố kịch tính / Điềm báo:** Khi có hành động bất ngờ (sấm sét, rắn rớt xuống bàn, đập bàn đứng dậy, tiếng chiêng lệnh).
- **Ngắt nhịp thi ca:** Bài từ/bài thơ kết thúc bước sang văn xuôi chính văn.

---

## 3. Quy Chuẩn Master Prompt AI Tạo Ảnh (AI Prompt Engineering Standard)

Mỗi shot trong Storyboard bắt buộc phải có **Master English Prompt** tuân thủ nghiêm ngặt cấu trúc 7 tầng:

```text
[Subject & Core Action] + [Setting & Architectural Context] + [Composition & Camera Angle] + [Lighting & Weather/Atmosphere] + [Art Style & Historical Accuracy] + [Color Palette & Mood] + [Technical Quality & Aspect Ratio: --ar 16:9]
```

### 3.1 Ma Trận Phong Cách Nghệ Thuật (Art Style Taxonomy)
| Thể Loại Sách | Định Danh Nghệ Thuật (Style Keyword) | Bối Cảnh, Phục Trang & Chi Tiết | Ánh Sáng & Màu Sắc (Color & Mood) |
| :--- | :--- | :--- | :--- |
| **Sử thi / Cổ phong Đông Á** (*Tam Quốc, Hán Sở, Thủy Hử*) | `Cinematic Historical Realism, Chinese Dynasty Epic` | Trang phục Hán phục cổ, giáp sắt tinh xảo, cờ hiệu thêu chỉ vàng, kiến trúc cung đình gỗ sơn son | Ánh nến lung linh, khói trầm bàng bạc, ánh trăng mờ ảo hoặc nắng chiều tà vàng óng (`golden hour`, `dramatic chiaroscuro`) |
| **Văn học Hiện thực Xã hội** (*Nam Cao, Vũ Trọng Phụng*) | `Cinematic Period Realism, Gritty Documentary Aesthetic` | Nhà tranh vách đất, áo tơi nón lá, đường làng Bắc Bộ xưa, chi tiết phong hóa sương gió | Màu đất ấm, tông màu sepia hoặc film grain 35mm, ánh sáng tự nhiên mộc mạc |
| **Tâm lý Hiện sinh / Trinh thám** (*Dostoevsky, Higashino*) | `Neo-noir Cinematic, Atmospheric Psychological Realism` | Căn phòng hẹp, bóng người kéo dài, đường phố đêm ướt mưa, ngõ tối hun hút | Ánh sáng tương phản cao (High-contrast chiaroscuro), bóng đổ dài, ánh đèn vàng leo lét |
| **Tự lực / Phát triển Bản thân** (*Kinh doanh, Kỹ năng*) | `Modern Minimalist Editorial, Inspiring Cinematic Concept` | Bàn làm việc gọn gàng, cửa sổ kính nhìn ra chân trời thành phố, con người trầm tư sáng tạo | Ánh sáng ban mai trong trẻo, tông màu tươi sáng, tối giản (clean high-key lighting) |

### 3.2 Bộ Từ Khóa Phủ Định (Negative Prompts)
Để đảm bảo tính chân thực và thẩm mỹ cao:
`ugly, deformed face, extra limbs, bad anatomy, cartoon, anime, 3d render, modern elements, watermark, text, blurry, low resolution, plastic skin`

---

## 4. Đạo Diễn Góc Máy & Chuyển Động Ken Burns (Cinematography & Motion Guide)

Trong video kịch bản từ ảnh tĩnh, chuyển động ống kính (Ken Burns Effect) là linh hồn tạo nên cảm giác điện ảnh:

### 4.1 Bảng Phối Hợp Góc Máy & Ken Burns
| Cự Ly Góc Máy (Shot Type) | Ứng Dụng Trong Kịch Bản | Hiệu Ứng Ken Burns Đề Xuất | Tác Động Tâm Lý Người Xem |
| :--- | :--- | :--- | :--- |
| **Extreme Wide Shot (EWS) / Wide Shot (WS)** | Mở đầu chương, bài từ ngâm vịnh, đại cảnh chiến trận, thiên nhiên hùng vĩ | `Slow Pan Left-to-Right` hoặc `Slow Zoom Out (1.10 -> 1.00)` | Tạo cảm giác bao la, choáng ngợp trước lịch sử và không gian |
| **Medium Shot (MS)** | Nhân vật đang tương tác, trò chuyện trong quán rượu, hội ngộ, dâng sớ | `Slow Zoom In (1.00 -> 1.08)` hoặc `Static with subtle drift` | Tập trung vào mối quan hệ và hành động của các nhân vật |
| **Close-Up (CU) / Extreme Close-Up (ECU)** | Thần thái nhân vật khi thốt lời thề, ánh mắt căm phẫn, giọt nước mắt, bàn tay cầm binh khí | `Slow Zoom In (1.02 -> 1.15)` hướng về đôi mắt hoặc chi tiết chính | Đẩy cao trào cảm xúc, kết nối nội tâm sâu sắc với người xem |
| **Low-Angle Shot (Góc ngước)** | Tôn vinh bậc anh hùng uy dũng, tướng quân ra trận, tượng đài | `Subtle Tilt Up & Slow Zoom In` | Tạo cảm giác uy nghi, hùng dũng, quyền uy áp đảo |
| **High-Angle / Bird's Eye Shot (Góc nhìn từ trên cao)** | Cảnh lầm than, bão lũ tàn phá, điềm gở đè nặng, kẻ yếu thế | `Slow Pan Down & Zoom Out` | Tạo cảm giác bất lực, nhỏ bé trước số phận và thiên nhiên |

---

## 5. Quy Chuẩn Đặt Tên & Tổ Chức Tệp Tin (File Naming & Directory Structure)

Mọi tệp kịch bản storyboard và ảnh minh họa phải nằm gọn trong cấu trúc thư mục của chương sách, tuyệt đối không tạo tệp bừa bãi tại thư mục gốc:

```text
[book_dir]/
  └── [chapter_dir]/
        ├── kich-ban/
        │     └── Kich-ban-N.txt           <-- Kịch bản đọc gốc
        ├── storyboard_video/
        │     ├── Kich-ban-N.md            <-- TỆP STORYBOARD XUẤT XƯỞNG (Đầu ra của skill này)
        │     └── kich-ban-N/              <-- Thư mục chứa hình ảnh riêng cho chunk này
        │           ├── scene_01_truong_giang.jpg
        │           ├── scene_02_ngu_tieu.jpg
        │           └── ...
        └── images/                        <-- Hoặc thư mục gom ảnh chung của toàn chương
              ├── scene_01_*.jpg
              └── ...
```

- **Quy tắc đặt tên file ảnh:** `scene_{XX}_{slug_mô_tả}.jpg` (Ví dụ: `scene_01_truong_giang_cuon_cuon.jpg`). Số thứ tự gồm 2 chữ số (`01`, `02`,...).

---

## 6. Mẫu Cấu Trúc Storyboard Hoàn Chỉnh (Output Template Standard)

File xuất xưởng `storyboard_video/Kich-ban-N.md` BẮT BUỘC có 2 bảng lớn và các thông số kỹ thuật chuẩn:

```markdown
# KỊCH BẢN VIDEO PHÂN CẢNH (VIDEO STORYBOARD)
## Tác phẩm: [Tên Tác Phẩm] — [Tên Chương / Hồi]
### Tập / Kịch bản: Kich-ban-N

---

### TỔNG QUAN THÔNG SỐ SẢN XUẤT (PRODUCTION SPECS)
- **Tệp Kịch bản Nguồn:** `kich-ban/Kich-ban-N.txt`
- **Tổng số từ:** [Số từ] từ | **Tổng ký tự:** [Số ký tự] ký tự
- **Ước tính thời lượng Audio:** [MM:SS] (~[Tổng số giây] giây)
- **Tổng số Phân cảnh (Shots):** [Số shots] phân cảnh
- **Nhịp thị giác trung bình (Pacing):** [Số giây/shot] giây / ảnh (Chuẩn 15–28s)
- **Tỉ lệ khung hình (Aspect Ratio):** 16:9 (1920x1080 Full HD / 4K UHD)
- **Phong cách Mỹ thuật (Art Style):** [Tên phong cách]
- **Thư mục lưu trữ ảnh:** `storyboard_video/kich-ban-N/images/`

---

## PHẦN 1: BẢNG PHÂN CẢNH TỔNG QUAN (SHOT-BY-SHOT STORYBOARD SUMMARY)

| Shot ID | Màn / Phân Đoạn | Thời Gian (Start - End) | Thời Lượng | Cự Ly & Góc Máy | Chuyển Động (Ken Burns) | Tên File Ảnh Dự Kiến | Trạng Thái |
| :---: | :--- | :---: | :---: | :--- | :--- | :--- | :---: |
| **Shot 01** | Màn I: Khúc Ngâm Mở Đầu | 00:00 - 00:22 | 22s | Extreme Wide Shot | Slow Zoom In (1.0 -> 1.12) | `scene_01_truong_giang.jpg` | Đã có / Cần tạo |
| **Shot 02** | Màn I: Ngư Tiều Đầu Bạc | 00:22 - 00:44 | 22s | Medium Wide Shot | Slow Pan Left to Right | `scene_02_ngu_tieu_uong_ruou.jpg`| Đã có / Cần tạo |
...

---

## PHẦN 2: BẢNG MÔ TẢ CHI TIẾT CÁC CẢNH NỐI TIẾP NHAU (SCENE CONTINUITY & PROMPTS)

### SHOT 01: [Tên Shot Ngắn Gọn]
- **Thời gian Audio:** `[MM:SS]` – `[MM:SS]` (Thời lượng: `[XX]s`)
- **Tệp hình ảnh:** `[chapter_dir]/storyboard_video/[kich-ban-N]/scene_01_[name].jpg`
- **Lời đọc Audio tương ứng (Narration Sync):**
  > "[Trích dẫn chính xác 100% câu chữ trong kịch bản đọc gốc]"
- **Diễn giải Thị giác & Mạch Kể (Visual Narrative):**
  [Mô tả chi tiết những gì người xem nhìn thấy trên màn hình: chuyển động mây trời, dòng nước, ánh mắt nhân vật, không khí phân cảnh]
- **Kỹ thuật Điện ảnh:**
  * **Cự ly & Góc máy:** Extreme Wide Shot, eye-level cinematic framing.
  * **Ánh sáng & Màu sắc:** Hoàng hôn đỏ rực (crimson golden hour), sương mù bảng lảng.
  * **Chuyển động Ken Burns:** Zoom in chậm rãi từ tỉ lệ 1.0 lên 1.12 vào trung tâm dòng sông.
  * **Điểm chuyển cảnh (Transition):** Cross-dissolve 1.2s sang Shot 02.
- **Master AI Image Prompt (Midjourney / FLUX / SDXL):**
  ```text
  [Detailed English prompt according to 7-layer standard, 8k, photorealistic, cinematic lighting --ar 16:9]
  ```
- **Negative Prompt:**
  ```text
  ugly, deformed, anime, cartoon, text, watermark, bad anatomy, modern elements
  ```

---
[Lặp lại cấu trúc chi tiết trên cho toàn bộ các Shots tiếp theo]
```

---

## 7. Quy Trình Thao Tác Chuẩn Của AI (Step-by-Step SOP)

Khi nhận lệnh phân tích kịch bản tạo video storyboard:
1. **Bước 1: Tiếp nhận & Kiểm tra Văn bản:** Đọc trọn vẹn tệp `Kich-ban-N.txt`. Đếm số từ, số ký tự, xác định thể loại và chia các màn kịch nghệ lớn (Acts).
2. **Bước 2: Tính Toán Nhịp Thời Gian:** Áp dụng công thức ở Mục 2 để tính tổng thời lượng audio và xác định số shot $N_{\text{shots}}$. Phân bổ thời lượng từng shot nằm trong khoảng [15s – 28s].
3. **Bước 3: Thiết Kế Bảng Phân Cảnh (Shot-by-shot Table):** Lập bảng tổng quan các shot, khớp thời gian `Start - End`, góc máy và hướng Ken Burns.
4. **Bước 4: Soạn Thảo Chi Tiết Từng Cảnh:**
   - Trích dẫn chính xác câu đọc.
   - Viết mô tả thị giác sống động.
   - Soạn Master English Prompt 7 tầng chuẩn AI.
   - Xác định rõ tên file ảnh đích.
5. **Bước 5: Kiểm Tra Đối Soát (Validation):**
   - Đảm bảo 100% câu từ trong kịch bản nguồn đã được bao phủ.
   - Không có shot nào thời lượng quá ngắn ($< 12$s) hoặc quá dài ($> 30$s).
   - Prompt chuẩn tiếng Anh, không chứa ký tự lỗi.
6. **Bước 6: Xuất Bản Tệp Storyboard:** Lưu file vào đúng thư mục `[chapter_dir]/storyboard_video/Kich-ban-N.md`.

---

## 8. Điều Khoản Bắt Buộc Kích Hoạt Hội Đồng 3 – 4 Sub-Agents Phối Hợp (Mandatory 3-4 Subagents Council Protocol)

> **CHỈ THỊ AN TOÀN & CHẤT LƯỢNG CAO NHẤT (MANDATORY SUBAGENT DISPATCH):**  
> Việc thiết lập Storyboard Video chất lượng điện ảnh đòi hỏi sự giao thoa của 4 năng lực sáng tạo đa chiều: (1) Cảm thụ kịch nghệ & tính toán nhịp thính giác, (2) Tư duy đạo diễn điện ảnh & bố cục góc máy, (3) Kỹ thuật Prompt AI tạo hình mỹ thuật đỉnh cao, và (4) Kiểm toán tính liên tục (Continuity) & đối soát câu chữ.  
> 👉 **TUYỆT ĐỐI CẤM AI CHÍNH TỰ THỰC THI ĐƠN LẺ (ZERO-SOLO ENFORCEMENT)**. Khi nhận bất kỳ nhiệm vụ nào liên quan đến phân tích kịch bản video storyboard, **LƯỢT GỌI CÔNG CỤ ĐẦU TIÊN CỦA BẠN BẮT BUỘC PHẢI LÀ `invoke_subagent`** để điều phối đồng thời Hội đồng tối thiểu 3 – 4 Subagents chuyên môn.

### 8.1 Ma Trận Phân Bổ Hội Đồng 4 Sub-agents Chuyên Môn
| Thứ Tự | Định Danh Vai Trò (Role) | Chuyên Môn & Nhiệm Vụ Cốt Lõi | Sản Phẩm Bàn Giao (Deliverables) |
| :---: | :--- | :--- | :--- |
| **1** | `Narrative & Pacing Beat Director` | Bóc tách mạch truyện theo Hồi/Màn (Acts & Beats). Tính toán thời lượng audio $T_{\text{audio}}$, chia số lượng shots $N_{\text{shots}}$, chốt dải pacing [15s – 28s/ảnh], đảm bảo 100% câu chữ lời đọc được bao phủ. | Bảng phân bổ nhịp thời gian, Start-End timing và dải câu đọc audio cho từng shot. |
| **2** | `Cinematographer & Camera Movement Director` | Đạo diễn thị giác: Thiết lập cự ly khung hình (EWS, WS, MWS, MS, CU), góc máy điện ảnh (Low-angle, Eye-level, High-angle, Dutch-angle), ánh sáng và thiết kế chuyển động Ken Burns (Zoom, Pan, Tilt, Drift) cùng điểm chuyển cảnh (Transition). | Bảng phân định góc máy, chuyển động camera và hiệu ứng chuyển cảnh cho toàn bộ shots. |
| **3** | `Visual Prompt Engineer & Art Stylist` | Chuyên gia mỹ thuật AI: Soạn Master English Prompts 7 tầng chi tiết chuẩn Midjourney v6 / FLUX.1 / SDXL / Imagen 3, kiểm soát phục trang Hán cổ, bối cảnh lịch sử và Negative Prompts chống dị tật. | Bộ Master Prompts tiếng Anh 7 tầng chuẩn điện ảnh cho từng shot. |
| **4** | `Continuity & Visual QC Lead` | Trưởng ban Kịch nghệ & Tổng hợp: Thẩm định tính liên tục thị giác (Visual Continuity) giữa các shot liền kề, kiểm tra khớp 100% câu đọc audio với mô tả hình ảnh, quy chuẩn hóa tên file ảnh và xuất bản file Markdown. | Tệp `storyboard_video/Kich-ban-N.md` hoàn thiện 100% đạt chuẩn nghiệm thu. |

### 8.2 Mẫu Lệnh Gọi Đồng Thời Hội Đồng Sub-agents (Dispatch Template)
Khi nhận lệnh, AI Chính phát lệnh kích hoạt duy nhất một lượt gọi công cụ chứa toàn bộ các Subagents:

```python
invoke_subagent(
  Subagents=[
    {
      "TypeName": "self",
      "Role": "Narrative & Pacing Beat Director",
      "Prompt": "Đọc kịch bản [đường_dẫn_kich_ban]. Bóc tách cấu trúc kịch tính thành các Acts/Beats. Tính toán thời lượng audio dự kiến, xác định số lượng shots mục tiêu (mỗi shot 15-28s). Ánh xạ 100% từng câu chữ lời đọc vào từng shot, chốt bảng thời gian Start-End chính xác."
    },
    {
      "TypeName": "self",
      "Role": "Cinematographer & Camera Movement Director",
      "Prompt": "Dựa trên mạch kịch tính của kịch bản [đường_dẫn_kich_ban], thiết kế toàn diện ngôn ngữ điện ảnh cho từng shot: cự ly khung hình (EWS/WS/MS/CU), góc máy (Low-angle/Eye-level/High-angle/Dutch-angle), ánh sáng điện ảnh (Chiaroscuro/Golden hour), chuyển động Ken Burns cụ thể (Slow Zoom In/Out, Pan, Tilt) và nhịp chuyển cảnh."
    },
    {
      "TypeName": "self",
      "Role": "Visual Prompt Engineer & Art Stylist",
      "Prompt": "Soạn thảo bộ Master English Prompts 7 tầng chuẩn điện ảnh cho từng phân cảnh của kịch bản [đường_dẫn_kich_ban], tối ưu hóa cho Midjourney v6 / FLUX.1 / SDXL / Imagen 3. Đảm bảo độ chính xác phục trang lịch sử cổ phong, kiến trúc thời đại, ánh sáng và thiết lập Negative Prompts hoàn chỉnh."
    },
    {
      "TypeName": "self",
      "Role": "Continuity & Visual QC Lead",
      "Prompt": "Tổng hợp kết quả từ các Sub-agents, rà soát tính liên tục thị giác (Continuity) giữa các khung hình kề nhau, đối soát 100% câu đọc audio với mô tả hình ảnh. Chuẩn hóa đường dẫn lưu ảnh và xuất bản tệp kịch bản hoàn chỉnh tại storyboard_video/Kich-ban-N.md."
    }
  ]
)
```

### 8.3 Chế Tài Khóa Cứng (Zero-Solo Invariant & Quality Gate)
- **Tự ý làm một mình bị coi là lỗi nghiêm trọng:** Bất kỳ tệp storyboard nào được tạo ra mà trong phiên không có lịch sử gọi `invoke_subagent` điều phối Hội đồng tối thiểu 3 – 4 Subagents đều bị coi là **Vi phạm quy chuẩn hệ thống**, không được nghiệm thu sang khâu sinh hình ảnh hay dựng video.
- **Tốc độ và chất lượng:** Khi phân phối cho 4 Subagents chuyên trách chạy song song, toàn bộ quá trình phân tích kịch bản sâu sắc, tính toán nhịp thời gian, viết prompt 8k và thiết kế góc máy hoàn tất chỉ trong vòng **1 – 2 phút**, mang lại chất lượng điện ảnh vượt trội so với một mô hình đơn lẻ tự làm.
