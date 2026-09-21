---
name: vrf_03_video_renderer
description: "Bước 03 trong Dây chuyền Tái cấu trúc Video (Video Refactor Framework - VRF): Tổng hợp và kết xuất video MP4 phân cảnh từ nguồn tài nguyên storyboard_video và audio_chunks. Video được dựng riêng cho từng kịch bản (Kich-ban-N) tương ứng với số lượng kịch bản của hồi/chương đó. Cơ chế hiển thị hình ảnh đứng yên (still frame), đoạn chuyển cảnh áp dụng hiệu ứng hòa tan transition-preset-dissolve (cross-dissolve). Sử dụng trực tiếp file âm thanh gốc trong audio_chunks/chunk_N.mp3 mà không cần clone. Video thành phẩm lưu tại thư mục [chapter_dir]/video/ cùng cấp với storyboard_video. Hỗ trợ chạy linh hoạt cho từng kịch bản đơn lẻ, toàn bộ chương hoặc toàn bộ tác phẩm. Bắt buộc kích hoạt Sub-agents song song theo từng kịch bản/chương để tối ưu hóa hiệu suất và chất lượng."
---

# Kỹ năng VRF-03: Dựng & Kết Xuất Video Phân Cảnh (Storyboard Video Renderer)

## 1. Định Nghĩa & Mục Tiêu Cốt Lõi (Core Purpose & Principles)

Kỹ năng `vrf_03_video_renderer` là bước thứ ba trong **Video Refactor Framework (VRF)**. Module này đảm nhận vai trò **Kỹ Sư Dựng Phim & Tổng Hợp Video Thành Phẩm (Chief Video Assembly & Rendering Engineer)**.

### Mục Tiêu Tối Thượng:
1. **Dựng Video Theo Từng Kịch Bản Độc Lập:** Tạo file video MP4 riêng biệt cho từng file kịch bản (`Kich-ban-1`, `Kich-ban-2`...) tương ứng với cấu trúc phân đoạn của chương/hồi.
2. **Hình Ảnh Đứng Yên Sắc Nét (Still Frame Display):** Hình ảnh phân cảnh được giữ nguyên vị trí tĩnh (không lia zoom, không pan motion phức tạp), tối ưu hóa độ sắc nét của hình ảnh 2K/4K và mang lại trải nghiệm xem đĩnh đạc, trầm ổn.
3. **Hiệu Ứng Chuyển Cảnh Hòa Tan Mượt Mà (Transition Preset Dissolve):** Điểm nối tiếp giữa các phân cảnh áp dụng hiệu ứng **Cross-Dissolve (Hòa tan / Chồng mờ)** với độ dài chuyển tiếp chuẩn **0.8s – 1.0s**, loại bỏ hoàn toàn hiện tượng cắt cảnh đột ngột (jump-cut) hoặc nhấp nháy đen.
4. **Tái Sử Dụng Trực Tiếp Audio Gốc (Zero-Audio-Duplication):** Sử dụng trực tiếp tệp âm thanh giọng đọc có sẵn trong `[chapter_dir]/audio_chunks/chunk_N.mp3`. Tuyệt đối không sao chép hay nhân bản thêm file audio thừa thãi, tối ưu dung lượng lưu trữ.
5. **Quy Chuẩn Thư Mục Lưu Trữ Cùng Cấp:** Video thành phẩm xuất xưởng bắt buộc được lưu vào thư mục `video/` nằm cùng cấp với `storyboard_video/`:  
   👉 `[chapter_dir]/video/video_Kich-ban-N.mp4`
6. **Khả Năng Thực Thi Linh Hoạt & Đa Cấp Độ:** Cho phép vận hành linh hoạt trên 3 cấp độ:
   - Cấp độ Kịch bản: Dựng video cho 1 kịch bản cụ thể (`Kich-ban-N`).
   - Cấp độ Chương/Hồi: Dựng toàn bộ video cho tất cả kịch bản của 1 chương.
   - Cấp độ Tác phẩm: Dựng video cho toàn bộ các chương của một cuốn sách.
7. **Điều Phối Sub-Agents Song Song (Parallel Swarm Enforcement):** Khi xử lý từ 2 kịch bản trở lên hoặc xử lý đa chương, bắt buộc kích hoạt mảng Sub-agents phân chia độc lập từng kịch bản để tăng tốc độ render tối đa.

---

## 2. Quy Chuẩn Tổ Chức Thư Mục & Tài Nguyên (Directory Architecture)

Mọi tài nguyên đầu vào và đầu ra tuân theo sơ đồ quan hệ chặt chẽ:

```text
[book_dir]/
  └── [chapter_dir]/
        ├── kich-ban/
        │     ├── Kich-ban-1.txt
        │     └── ...
        ├── audio_chunks/
        │     ├── chunk_1.mp3                      <-- NGUỒN AUDIO TRỰC TIẾP (Không clone)
        │     └── ...
        ├── storyboard_video/
        │     ├── Kich-ban-1.md                    <-- Kịch bản phân cảnh & timing
        │     └── kich-ban-1/
        │           └── images/                    <-- NGUỒN ẢNH ĐẦU VÀO
        │                 ├── scene_01_*.jpg/png
        │                 └── ...
        └── video/                                 <-- THƯ MỤC LƯU VIDEO XUẤT XƯỞNG (CÙNG CẤP)
              ├── video_Kich-ban-1.mp4             <-- Video thành phẩm Kịch bản 1
              ├── video_Kich-ban-2.mp4             <-- Video thành phẩm Kịch bản 2
              └── ...
```

- **Quy tắc đặt tên file video:** `video_Kich-ban-N.mp4` (hoặc `video_Kich-ban-N_1080p.mp4`).

---

## 3. Quy Chuẩn Kỹ Thuật Dựng Hình & Hiệu Ứng (Technical Specifications)

### 3.1 Thông Số Video Xuất Xưởng (Video Encoding Standards)
- **Độ phân giải:** 1920x1080 Full HD (Chuẩn màn ảnh rộng 16:9).
- **Tốc độ khung hình (Frame Rate):** 25 fps (hoặc 30 fps), Progressive.
- **Video Codec:** H.264 / AVC (`libx264`), High Profile, CRF 20 – 22, Preset `fast` hoặc `veryfast`.
- **Pixel Format:** `yuv420p` (tương thích 100% mọi trình phát video, trình duyệt web và YouTube/TikTok/Clipchamp).
- **Audio Codec:** AAC Stereo, 48000 Hz, Bitrate 192 kb/s (Mux trực tiếp từ `audio_chunks/chunk_N.mp3`).

### 3.2 Cơ Chế Chuyển Cảnh Transition Preset Dissolve (Cross-Dissolve)
Khi chuyển từ Shot $i$ sang Shot $i+1$:
- Thời lượng chuyển giao (Dissolve Transition Duration): **$t_{\text{trans}} = 0.8\text{s} - 1.0\text{s}$**.
- Trong FFmpeg, áp dụng bộ lọc `xfade=transition=fade:duration=0.8:offset=OFFSET`.
- Ảnh hiển thị hoàn toàn đứng yên: `scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080`. Không thêm zoom hay pan để giữ ảnh sắc nét và tĩnh lặng.

---

## 4. Công Thức Tính Toán Thời Lượng & Điểm Chuyển Cảnh (Timing Math)

Mỗi file storyboard `Kich-ban-N.md` xác định danh sách $K$ phân cảnh (shots).
1. **Thời lượng audio thực tế:** $T_{\text{audio}}$ lấy từ file `audio_chunks/chunk_N.mp3`.
2. **Thời lượng hiển thị mỗi shot ($t_i$):** Lấy từ bảng phân cảnh trong `storyboard_video/Kich-ban-N.md`.
3. **Hiệu chỉnh khớp chính xác tổng thời lượng (Total Duration Matching):**
   $$\sum_{i=1}^{K} t_i = T_{\text{audio}}$$
   Điểm bắt đầu chuyển cảnh của shot thứ $i$:
   $$\text{Offset}_i = \left(\sum_{j=1}^{i} t_j\right) - t_{\text{trans}}$$

---

## 5. Script Kỹ Thuật Tự Động Hóa (`core/vrf_video_compiler.py`)

Hệ thống trang bị sẵn script Python tự động hóa quy trình dựng video tất định:

```bash
# 1. Dựng video cho 1 kịch bản cụ thể:
python core/vrf_video_compiler.py --chapter "Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/01-Hoi-01" --script "Kich-ban-1"

# 2. Dựng video cho toàn bộ kịch bản của 1 chương:
python core/vrf_video_compiler.py --chapter "Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/01-Hoi-01" --all-scripts

# 3. Dựng video cho toàn bộ các chương của tác phẩm:
python core/vrf_video_compiler.py --book_dir "Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia" --all
```

---

## 6. Giao Thức Bắt Buộc Kích Hoạt Sub-Agents Điều Phối Song Song (Mandatory Subagent Dispatch)

> **CHỈ THỊ HIỆU NĂNG TỐI THƯỢNG:**  
> Khi thực thi cho toàn bộ chương (thường có từ 8 – 15 kịch bản) hoặc toàn bộ tác phẩm, việc render tuần tự từng kịch bản sẽ tiêu tốn nhiều thời gian.  
> 👉 **BẮT BUỘC KÍCH HOẠT HỘI ĐỒNG SUB-AGENTS XỬ LÝ SONG SONG**.

### 6.1 Phân Bổ Sub-agents:
- **Cấp độ Chương:** Chia mảng Sub-agents (`Role: "Video Rendering Producer [Kich-ban-X]"`), mỗi Sub-agent đảm nhận 1 đến 2 kịch bản độc lập.
- **Cấp độ Toàn Sách:** Kích hoạt `Cross-Chapter Swarm`, mỗi Sub-agent phụ trách toàn bộ video của 1 chương.

### 6.2 Mẫu Lệnh Kích Hoạt Sub-agents (Dispatch Template):
```python
invoke_subagent(
  Subagents=[
    {
      "TypeName": "self",
      "Role": "Video Rendering Producer [Kich-ban-1]",
      "Prompt": "Thực thi kỹ năng vrf_03_video_renderer cho Kịch bản 1 của chương [chapter_dir]. Kiểm tra tài nguyên ảnh tại storyboard_video/kich-ban-1/images/, audio tại audio_chunks/chunk_1.mp3. Dựng video MP4 1080p hình đứng yên, chuyển cảnh transition-preset-dissolve, lưu thành phẩm vào [chapter_dir]/video/video_Kich-ban-1.mp4."
    },
    {
      "TypeName": "self",
      "Role": "Video Rendering Producer [Kich-ban-2]",
      "Prompt": "Thực thi kỹ năng vrf_03_video_renderer cho Kịch bản 2 của chương [chapter_dir]. Dựng video MP4 1080p hình đứng yên, chuyển cảnh transition-preset-dissolve, lưu thành phẩm vào [chapter_dir]/video/video_Kich-ban-2.mp4."
    }
  ]
)
```

---

## 7. Cổng Kiểm Soát Chất Lượng Video (Video Quality Gate - VQG-3)

Video xuất xưởng phải vượt qua 100% các tiêu chí:

| Mã Gate | Tiêu Chí Kiểm Toán | Ngưỡng Nghiệm Thu (Pass Threshold) | Biện Pháp Khắc Phục |
| :---: | :--- | :--- | :--- |
| **VQG3-1** | **Tệp Video & Dung Lượng** | File `[chapter_dir]/video/video_Kich-ban-N.mp4` tồn tại, dung lượng $\ge 5\text{MB}$. | Render lại nếu file lỗi hoặc rỗng. |
| **VQG3-2** | **Đồng Bộ Thời Lượng (Duration Sync)** | Chênh lệch thời lượng video so với `chunk_N.mp3` đạt $\Delta t \le 0.5\text{s}$. | Cân chỉnh lại tổng thời lượng frames. |
| **VQG3-3** | **Độ Phân Giải & Định Dạng** | Đúng chuẩn 1920x1080, aspect ratio 16:9, codec H.264 / AAC. | Re-mux nếu sai định dạng. |
| **VQG3-4** | **Chuyển Cảnh Mượt Mà** | Hiệu ứng dissolve êm ái, không giật khung hình, không có màn hình đen bất thường. | Kiểm tra tham số xfade. |

---

## 8. Quy Trình Thao Tác Chuẩn Của AI (Step-by-Step SOP)

1. **Bước 1: Khởi Tạo Thư Mục Video:** Tạo thư mục `[chapter_dir]/video/` nếu chưa có.
2. **Bước 2: Đối Soát Tài Nguyên Đầu Vào:**
   - Kiểm tra file kịch bản phân cảnh: `storyboard_video/Kich-ban-N.md`.
   - Kiểm tra thư mục ảnh: `storyboard_video/kich-ban-N/images/`.
   - Kiểm tra audio gốc: `audio_chunks/chunk_N.mp3`.
3. **Bước 3: Bóc Tách Danh Sách Shots & Timing:** Trích xuất tên file ảnh và thời lượng từng shot.
4. **Bước 4: Điều Phối Render Video:**
   - Sử dụng script `core/vrf_video_compiler.py` hoặc lệnh FFmpeg trực tiếp.
   - Áp dụng cấu hình: Hình đứng yên (Still frame) + Chuyển cảnh `transition-preset-dissolve` (0.8s) + Ghép audio gốc `chunk_N.mp3`.
5. **Bước 5: Kiểm Toán VQG-3:** Đối soát thời lượng và kích thước tệp video kết xuất tại `[chapter_dir]/video/video_Kich-ban-N.mp4`.
6. **Bước 6: Báo Cáo Kết Quả:** Cung cấp thông số kỹ thuật, đường dẫn file video và hướng dẫn sử dụng cho người dùng.
