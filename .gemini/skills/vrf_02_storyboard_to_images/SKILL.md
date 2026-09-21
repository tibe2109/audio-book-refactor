---
name: vrf_02_storyboard_to_images
description: "Bước 02 trong Dây chuyền Tái cấu trúc Video (Video Refactor Framework - VRF): Đọc kịch bản phân cảnh từ storyboard_video (ví dụ Kich-ban-N.md), tự động bóc tách danh sách các shots, Master AI Prompts, và khởi tạo thư mục lưu trữ `storyboard_video/kich-ban-N/images/`. Điều phối sinh ảnh hàng loạt theo chuẩn điện ảnh (16:9, Midjourney/FLUX/SDXL/Imagen 3), hỗ trợ Hội đồng Sub-agents xử lý song song các batch hình ảnh, kiểm soát chất lượng thẩm mỹ, khử lỗi dị tật và tự động cập nhật trạng thái nghiệm thu vào tệp storyboard."
---

# Kỹ năng VRF-02: Sản Xuất Hình Ảnh Phân Cảnh Từ Storyboard (Storyboard to Images)

## 1. Định Nghĩa & Mục Tiêu Cốt Lõi (Core Purpose & Principles)

Kỹ năng `vrf_02_storyboard_to_images` là bước thứ hai trong **Video Refactor Framework (VRF)**. Module này đảm nhận vai trò **Trưởng Phòng Sản Xuất Mỹ Thuật AI & Kỹ Sư Tạo Hình Điện Ảnh (AI Art Generation Lead & Visual Producer)**.

### Mục Tiêu Tối Thượng:
1. **Tự Động Bóc Tách Kịch Bản Phân Cảnh (Automated Storyboard Parsing):** Đọc trực tiếp tệp `[chapter_dir]/storyboard_video/Kich-ban-N.md` từ Bước VRF-01, trích xuất 100% dữ liệu: Shot ID, Tên tệp ảnh, Lời đọc audio, Master English Prompt, Negative Prompt và thông số kỹ thuật.
2. **Quy Chuẩn Hóa Thư Mục Lưu Trữ Cục Bộ (Standard Directory Structure):** Khởi tạo thư mục hình ảnh riêng biệt theo quy định:  
   👉 `[chapter_dir]/storyboard_video/kich-ban-N/images/`  
   Mỗi chunk kịch bản sở hữu một kho ảnh chuyên biệt, bảo đảm tuyệt đối tính ngăn nắp, vệ sinh thư mục và dễ dàng đóng gói thành phẩm video.
3. **Sinh Ảnh AI Đạt Chuẩn Điện Ảnh 16:9 (Cinematic Aspect Ratio & Aesthetics):** Tạo ảnh với tỉ lệ màn ảnh rộng 16:9 (`--ar 16:9`), độ phân giải cao ($1376 \times 768$ hoặc $1920 \times 1080$), phong cách hội họa/điện ảnh đồng nhất xuyên suốt tác phẩm.
4. **Điều Phối Hội Đồng Sub-Agents Song Song (Parallel Batch Dispatch):** Khi kịch bản có nhiều phân cảnh ($N \ge 6$ shots), bắt buộc kích hoạt mảng Sub-agents phân chia các batch ảnh để xử lý đồng thời, tăng tốc độ sản xuất gấp 3 – 4 lần mà không làm gián đoạn phiên làm việc chính.
5. **Vòng Kiểm Toán Chất Lượng Hình Ảnh (Visual Quality Gate - VQG):** Thẩm định file ảnh thực tế (kích thước $> 50\text{KB}$, đúng tỉ lệ 16:9, không lỗi hình học dị tật) và tự động cập nhật cột "Trạng Thái" trong file `Kich-ban-N.md` từ `Cần tạo` sang `Đã hoàn thành`.

---

## 2. Quy Chuẩn Tổ Chức Thư Mục & Tệp Tin (Directory Architecture)

Mọi tệp hình ảnh sản xuất ra bắt buộc phải nằm bên trong thư mục `images/` thuộc thư mục kịch bản tương ứng:

```text
[book_dir]/
  └── [chapter_dir]/
        ├── kich-ban/
        │     └── Kich-ban-1.txt                   <-- Kịch bản đọc gốc
        └── storyboard_video/
              ├── Kich-ban-1.md                    <-- Kịch bản phân cảnh storyboard
              └── kich-ban-1/
                    └── images/                    <-- THƯ MỤC LƯU HÌNH ẢNH CỦA KỊCH BẢN NÀY
                          ├── scene_01_truong_giang_cuon_cuon.jpg
                          ├── scene_02_ngu_tieu_doi_am.jpg
                          ├── scene_03_tieu_de_hoi_mot.jpg
                          └── ...
```

- **Quy tắc đặt tên file ảnh:** `scene_{XX}_{slug_mô_tả}.jpg` (Ví dụ: `scene_01_truong_giang_cuon_cuon.jpg`).
- **Đường dẫn tuyệt đối/tương đối:** File kịch bản `Kich-ban-N.md` cập nhật đường dẫn tương đối `storyboard_video/kich-ban-N/images/scene_XX_*.jpg` để các công cụ video editor (Clipchamp, Premiere, CapCut, FFmpeg) nhận diện trực tiếp.

---

## 3. Công Thức & Quy Trình Bóc Tách Kịch Bản (Storyboard Parsing)

AI trích xuất từng Shot từ tệp `storyboard_video/Kich-ban-N.md` thông qua mẫu cấu trúc chuẩn:

### 3.1 Các Trường Dữ Liệu Bắt Buộc:
- **`shot_id`:** Ví dụ `Shot 01`, `Shot 02`...
- **`scene_title`:** Tên mô tả ngắn của phân cảnh.
- **`audio_sync`:** Đoạn lời đọc tương ứng trong audio.
- **`target_filename`:** Tên file ảnh đích (Ví dụ: `scene_01_truong_giang_cuon_cuon.jpg`).
- **`master_prompt`:** Đoạn prompt tiếng Anh chi tiết 7 tầng nằm trong khối code `Master AI Image Prompt`.
- **`negative_prompt`:** Danh sách từ khóa phủ định.
- **`aspect_ratio`:** Mặc định `16:9`.

---

## 4. Giao Thức Kích Hoạt Sub-Agents Xử Lý Batch Song Song (Parallel Batch Dispatch Protocol)

> **CHỈ THỊ HIỆU SUẤT TỐI CAO:**  
> Một kịch bản hoàn chỉnh thường chứa từ 8 đến 12 phân cảnh (hoặc 25 - 35 phân cảnh cho toàn chương). Nếu AI Chính tự tuần tự gọi lệnh sinh từng bức ảnh một, thời gian xử lý sẽ kéo dài gây quá tải phiên làm việc.  
> 👉 **BẮT BUỘC KÍCH HOẠT HỘI ĐỒNG SUB-AGENTS XỬ LÝ THEO BATCH**.

### 4.1 Quy Tắc Phân Chia Batch:
- Mỗi Sub-agent phụ trách một **Batch từ 2 đến 4 shots liền kề**.
- Ví dụ với kịch bản 10 shots (Shot 01 đến Shot 10):
  * **Subagent 1 (`Role: "AI Visual Producer [Batch 1: Shots 01-03]"`):** Sinh ảnh cho Shot 01, Shot 02, Shot 03.
  * **Subagent 2 (`Role: "AI Visual Producer [Batch 2: Shots 04-06]"`):** Sinh ảnh cho Shot 04, Shot 05, Shot 06.
  * **Subagent 3 (`Role: "AI Visual Producer [Batch 3: Shots 07-08]"`):** Sinh ảnh cho Shot 07, Shot 08.
  * **Subagent 4 (`Role: "AI Visual Producer [Batch 4: Shots 09-10]"`):** Sinh ảnh cho Shot 09, Shot 10.

### 4.2 Mẫu Lệnh Kích Hoạt Đồng Thời (Dispatch Template):
```python
invoke_subagent(
  Subagents=[
    {
      "TypeName": "self",
      "Role": "AI Visual Producer [Batch 1: Shots 01-03]",
      "Prompt": "Tạo thư mục [chapter_dir]/storyboard_video/kich-ban-N/images/. Đọc prompt của Shot 01, 02, 03 trong [chapter_dir]/storyboard_video/Kich-ban-N.md. Tiến hành tạo 3 ảnh tương ứng với AspectRatio 16:9, lưu vào đúng thư mục đích với tên scene_01_*.jpg, scene_02_*.jpg, scene_03_*.jpg. Báo cáo lại đường dẫn file đã tạo."
    },
    {
      "TypeName": "self",
      "Role": "AI Visual Producer [Batch 2: Shots 04-06]",
      "Prompt": "Đọc prompt của Shot 04, 05, 06 trong [chapter_dir]/storyboard_video/Kich-ban-N.md. Tiến hành tạo 3 ảnh tương ứng với AspectRatio 16:9, lưu vào [chapter_dir]/storyboard_video/kich-ban-N/images/ với tên scene_04_*.jpg, scene_05_*.jpg, scene_06_*.jpg. Báo cáo lại đường dẫn file đã tạo."
    },
    {
      "TypeName": "self",
      "Role": "AI Visual Producer [Batch 3: Shots 07-08]",
      "Prompt": "Đọc prompt của Shot 07, 08 trong [chapter_dir]/storyboard_video/Kich-ban-N.md. Tiến hành tạo 2 ảnh tương ứng với AspectRatio 16:9, lưu vào [chapter_dir]/storyboard_video/kich-ban-N/images/ với tên scene_07_*.jpg, scene_08_*.jpg. Báo cáo lại đường dẫn file đã tạo."
    },
    {
      "TypeName": "self",
      "Role": "AI Visual Producer [Batch 4: Shots 09-10]",
      "Prompt": "Đọc prompt của Shot 09, 10 trong [chapter_dir]/storyboard_video/Kich-ban-N.md. Tiến hành tạo 2 ảnh tương ứng với AspectRatio 16:9, lưu vào [chapter_dir]/storyboard_video/kich-ban-N/images/ với tên scene_09_*.jpg, scene_10_*.jpg. Báo cáo lại đường dẫn file đã tạo."
    }
  ]
)
```

---

## 5. Quy Chuẩn Công Cụ Tạo Ảnh (Image Generation Engine)

### 5.1 Sử Dụng Công Cụ Nội Bộ `generate_image`:
Khi AI gọi tool tạo ảnh:
- **`Prompt`:** Dùng trực tiếp Master English Prompt từ storyboard. Nếu prompt dài, chắt lọc các yếu tố cốt lõi: Subject, Setting, Composition, Lighting, Cinematic Style, 8k.
- **`ImageName`:** Tên đại diện ngắn gọn dạng snake_case (ví dụ: `scene_01_truong_giang`).
- **`AspectRatio`:** Khóa cứng giá trị `"16:9"`.
- **Hậu xử lý:** Sau khi tool `generate_image` tạo file trong thư mục artifacts của agent, tiến hành copy hoặc di chuyển file về đích:  
  `cp <artifact_path> [chapter_dir]/storyboard_video/kich-ban-N/images/scene_XX_[slug].jpg`

### 5.2 Cơ Chế Tái Sử Dụng / Liên Kết Ảnh Sẵn Có (Asset Linker & Reuser):
Nếu kho ảnh chung của chương `[chapter_dir]/images/` đã có sẵn các ảnh phù hợp với chủ đề của Shot đó, cho phép copy hoặc tạo symlink sang thư mục `storyboard_video/kich-ban-N/images/` để tiết kiệm tài nguyên và giữ tính đồng nhất nhân vật.

---

## 6. Cổng Kiểm Soát Chất Lượng Hình Ảnh (Visual Quality Gate - VQG)

Trước khi nghiệm thu bàn giao khâu VRF-02, bắt buộc phải đạt **100% 4 Tiêu Chí Kiểm Toán VQG**:

| Mã Gate | Tên Tiêu Chí | Ngưỡng Chấp Thuận (Pass Criteria) | Xử Lý Khi Vi Phạm (Fail Action) |
| :---: | :--- | :--- | :--- |
| **VQG-1** | **Tính Đầy Đủ & Dung Lượng** | 100% shots có file ảnh tồn tại trong `storyboard_video/kich-ban-N/images/`. File size $\ge 50\text{KB}$. | Sinh lại shot bị thiếu hoặc rỗng. |
| **VQG-2** | **Tỉ Lệ Màn Ảnh Ngang 16:9** | Tỉ lệ ảnh ngang chuẩn 16:9 (Chiều rộng > Chiều cao, tỉ lệ $\approx 1.77$). Cấm tạo ảnh dọc 9:16 hay vuông 1:1. | Crop / regenerate lại tỉ lệ 16:9. |
| **VQG-3** | **Zero-Glitch & Mỹ Thuật** | Không bị rách vân ảnh, không chứa chữ text rác đè lên hình, không bị biến dạng cơ thể nghiêm trọng. | Điều chỉnh Negative prompt và sinh lại. |
| **VQG-4** | **Đồng Bộ Hóa Storyboard** | Cột "Trạng Thái" trong bảng tóm tắt của file `Kich-ban-N.md` được cập nhật thành: `Đã hoàn thành: images/scene_XX_*.jpg`. | Cập nhật lại file `Kich-ban-N.md`. |

---

## 7. Quy Trình Thao Tác Chuẩn Của AI (Step-by-Step SOP)

1. **Bước 1: Khởi Tạo Thư Mục Đích:**
   ```bash
   mkdir -p [chapter_dir]/storyboard_video/kich-ban-N/images
   ```
2. **Bước 2: Phân Tích File Kịch Bản Storyboard:** Đọc `[chapter_dir]/storyboard_video/Kich-ban-N.md`, thu hoạch danh sách $N$ shots và Master Prompts.
3. **Bước 3: Điều Phối Sub-agents Sinh Ảnh Song Song:** Kích hoạt Hội đồng 3 – 4 Subagents xử lý theo từng batch (hoặc thực thi sinh ảnh cho các shot).
4. **Bước 4: Đồng Bộ Ảnh Vào Thư Mục Đích:** Đảm bảo toàn bộ ảnh được đặt tên đúng quy chuẩn `scene_XX_[slug].jpg` và nằm trong thư mục `images/`.
5. **Bước 5: Kiểm Toán VQG & Cập Nhật Kịch Bản:**
   - Kiểm tra dung lượng và kích thước các tệp ảnh.
   - Cập nhật file `storyboard_video/Kich-ban-N.md`: Đổi trạng thái từ `Cần tạo` thành `Đã hoàn thành: images/scene_XX_*.jpg`.
6. **Bước 6: Nghiệm Thu & Bàn Giao:** Xuất báo cáo tóm tắt danh sách ảnh hoàn thiện để sẵn sàng chuyển giao sang khâu dựng video (VRF-03).
