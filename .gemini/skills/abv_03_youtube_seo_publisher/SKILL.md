---
name: abv_03_youtube_seo_publisher
description: "Kỹ năng tối ưu hóa SEO video YouTube và điều phối chiến lược xuất bản Sách Nói (Audiobook YouTube SEO Publisher & Market Strategist). Tiếp nhận source dự án tác phẩm (ví dụ: Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia), kích hoạt bắt buộc Hội đồng Sub-agents chuyên môn song song để phân tích sâu sắc kịch bản từng hồi, nghiên cứu thị trường thính giả nghe sách nói (nhu cầu nghe khi lái xe, làm việc, trước khi ngủ, tìm kiếm triết lý mưu lược), từ đó kiến tạo bộ Metadata YouTube chuẩn SEO vượt trội nhằm tối ưu CTR, thời lượng xem và đề xuất thuật toán. Khóa cứng các giới hạn kỹ thuật khắt khe của YouTube: Tiêu đề tối đa 100 ký tự (khuyên dùng 60–70 ký tự), Mô tả tối đa 5.000 ký tự (3 dòng đầu là Hook thu hút trước nút 'Thêm'), Thẻ Tags tổng cộng tối đa 500 ký tự, Hashtag tối đa 60 (hiển thị 3 thẻ đầu), Bình luận ghim tối đa 10.000 ký tự, Tên kênh tối đa 50 ký tự, Mô tả kênh tối đa 1.000 ký tự. Tích hợp cấu hình mặc định (YouTube Defaults) chuẩn mực: Không dành cho trẻ em (COPPA), Tuyên bố có AI, Bật phân cảnh/địa điểm/khái niệm tự động, Cho phép phối lại Shorts, Danh mục Giải trí (Category 24), Bật bình luận công khai. Toàn bộ kết quả metadata được lưu tập trung trực tiếp tại thư mục chứa Final Video của tác phẩm (Final-[Tên-Sách]/Videos/youtube_metadata/). Tích hợp hệ thống quản lý tiến trình nguyên tử qua tệp .abv_seo_manifest.json đặt ngay tại thư mục Final Video, cho phép AI luôn biết rõ trạng thái tiến trình đang ở đâu (tỷ lệ hoàn thành %, danh sách video completed/pending/failed) và tự động tiếp tục công việc (Atomic Resume & Skip Completed) khi bị ngắt giữa chừng do bất cứ lý do gì. Đối với tác phẩm đồ sộ quy mô lớn (> 100 video), kỹ năng tự động kích hoạt mảng Sub-agents phân chia công việc theo từng lô chương (Batch Processing) để xử lý song song, xây dựng chiến lược liên kết chuỗi video (Series Inter-linking) và kế hoạch lịch đăng (Upload Cadence) tối ưu hóa toàn diện."
---

# 📺 ABV-03: AUDIOBOOK YOUTUBE SEO PUBLISHER & PROGRESS STRATEGIST
## QUY TRÌNH THAO TÁC CHUẨN (SOP) NGHIÊN CỨU THỊ TRƯỜNG, BIÊN SOẠN METADATA CHUẨN SEO, QUẢN LÝ TIẾN TRÌNH NGUYÊN TỬ & ĐIỀU PHỐI XUẤT BẢN YOUTUBE HÀNG LOẠT

---

## 1. SOP / ĐẶC TẢ KỸ THUẬT (SPECIFICATION)
`abv_03_youtube_seo_publisher` là kỹ năng bước 3 trong nhánh phát hành Video Sách Nói (ABV Pipeline), đảm nhiệm vai trò **Giám Đốc Chiến Lược Nội Dung & Tối Ưu Hóa SEO YouTube (YouTube SEO Publisher & Strategist)**. Kỹ năng chịu trách nhiệm:

### A. Quản Trị Hệ Thống Lưu Trữ Tập Trung Tại Thư Mục Final Video
Toàn bộ thành phẩm của kỹ năng **bắt buộc phải lưu tập trung trực tiếp tại thư mục chứa Final Video của tác phẩm** (`Final-[Tên-Sách]/Videos/`):
- `Final-[Tên-Sách]/Videos/youtube_metadata/youtube_metadata_{chap_slug}.json`: Tệp Metadata JSON chuẩn SEO cho từng video.
- `Final-[Tên-Sách]/Videos/.abv_seo_manifest.json`: Tệp quản lý tiến trình nguyên tử theo dõi toàn bộ video của tác phẩm.
- `Final-[Tên-Sách]/Videos/YouTube_SEO_Master_Strategy.md`: Bản báo cáo tổng thể chiến lược xuất bản, ma trận từ khóa và lịch phát hành toàn tác phẩm.
- *(Tự động tạo bản sao gối đầu tại thư mục chương để đồng bộ nếu cần).*

---

### B. Quản Lý Tiến Trình Nguyên Tử (.abv_seo_manifest.json) & Tự Động Khôi Phục (Atomic Resume)
Để đảm bảo AI luôn nắm rõ trạng thái công việc và có thể tiếp tục ngay lập tức sau sự cố (mạng đứt, server restart, hết context), kỹ năng thiết lập cơ chế **Atomic Progress Manifest**:
1. **Vị trí tệp Manifest:** Đặt tại `Final-[Tên-Sách]/Videos/.abv_seo_manifest.json`.
2. **Cấu trúc Manifest:**
   ```json
   {
     "book_name": "Tam-Quoc-Dien-Nghia",
     "final_video_dir": "/path/to/Final-Tam-Quoc-Dien-Nghia/Videos",
     "created_at": "2026-09-21T02:21:49.118782+00:00",
     "updated_at": "2026-09-21T02:22:00.724069+00:00",
     "total_videos": 120,
     "completed_metadata": 45,
     "pending_metadata": 75,
     "failed_metadata": 0,
     "videos": {
       "Final_Video_01-Hoi-01_Part1.mp4": {
         "video_file": "Final_Video_01-Hoi-01_Part1.mp4",
         "chapter_dir": "01-Hoi-01",
         "metadata_file": "youtube_metadata/youtube_metadata_01-Hoi-01.json",
         "status": "completed",
         "audit_passed": true,
         "uploaded": true,
         "youtube_url": "https://youtu.be/OUkuc46XzU0",
         "updated_at": "2026-09-21T02:21:55.014896+00:00"
       }
     }
   }
   ```
3. **Cơ chế Tự Động Khôi Phục (Atomic Resume & Skip Completed):**
   - Khi khởi chạy, AI đọc tệp manifest để kiểm tra tiến độ hiện tại.
   - Đối với các video có `status == "completed"`, tệp metadata tồn tại trên đĩa và `audit_passed == true`: **BẮT BUỘC BỎ QUA (SKIP)**, không phân tích lại, không ghi đè.
   - AI chỉ tập trung xử lý các video có trạng thái `pending` hoặc `failed`.
   - Cập nhật tiến trình sau mỗi video theo phương thức ghi file tạm rồi thay thế nguyên tử (`os.replace`) để chống hỏng file JSON khi xảy ra sự cố ngắt nguồn.

---

### C. Bảng Khóa Cứng Giới Hạn Kỹ Thuật YouTube (Technical Platform Limits)
| Thành Phần | Giới Hạn Tối Đa | Khuyến Nghị Tối Ưu | Chức Năng & Chiến Lược |
| :--- | :--- | :--- | :--- |
| **Tiêu đề (Title)** | **100 ký tự** | **60 – 70 ký tự** | Hiển thị trọn vẹn trên điện thoại di động & kết quả tìm kiếm, chứa từ khóa chính + tên hồi + yếu tố kích thích tò mò. |
| **Mô tả (Description)** | **5.000 ký tự** | **2.500 – 4.000 ký tự** | 3 dòng đầu (150–200 ký tự) là "Hook" hiển thị trước nút *Xem thêm*; kèm Timestamps, phân tích ý nghĩa, bản quyền và CTA. |
| **Thẻ Tags Video** | **500 ký tự** (tổng chuỗi) | **400 – 480 ký tự** | Phân tầng: Tag thương hiệu kênh, Tag tác phẩm/tác giả, Tag hồi/nhân vật, Tag hành vi tìm kiếm của thính giả. |
| **Hashtags (#)** | **60 thẻ** | **3 – 5 thẻ** | YouTube chỉ hiển thị tối đa **3 thẻ đầu tiên** phía trên tiêu đề video hoặc trong kết quả tìm kiếm. |
| **Bình luận ghim (Pinned Comment)**| **10.000 ký tự** | **300 – 600 ký tự** | Kích hoạt tương tác cộng đồng, đặt câu hỏi thảo luận, dẫn link danh sách phát và tập kế tiếp. |
| **Tên kênh** | **50 ký tự** | **20 – 35 ký tự** | Mặc định: `Tibe audio book`. |
| **Mô tả kênh (About)** | **1.000 ký tự** | **600 – 900 ký tự** | Định vị kênh sách nói kịch nghệ đa thanh, cam kết chất lượng âm thanh và lịch phát sóng. |

---

### D. Cấu Hình Mặc Định Chuẩn Mực (Default YouTube Configuration)
Kỹ năng khóa cứng các thiết lập mặc định theo đúng quy chuẩn hệ thống:
1. **Đối tượng người xem (Audience):**  
   🔘 **Không, nội dung này không dành cho trẻ em** (`madeForKids: false` tuân thủ COPPA).  
   *Giới hạn độ tuổi:* Không giới hạn (bất kỳ ai cũng có thể xem).
2. **Nội dung trả tiền để quảng cáo (Paid Promotion):**  
   🔘 **Không, video của tôi không chứa nội dung được trả tiền để quảng cáo** (`hasPaidPromotion: false`).
3. **Tuyên bố sử dụng AI (Altered / Synthetic Content):**  
   🔘 **Có** (`containsSyntheticMedia: true`) — Minh bạch việc sử dụng công nghệ AI trong việc diễn đọc kịch nghệ đa thanh và phục dựng hình ảnh nghệ thuật cổ điển.
4. **Tính năng tự động (Automatic Features):**  
   ☑️ **Cho phép dùng phân cảnh tự động** (`autoChapters: true`).  
   ☑️ **Cho phép chèn địa điểm tự động** (`autoPlaces: true`).  
   ☑️ **Bật tính năng tự động thêm khái niệm** (`autoConcepts: true`).
5. **Phối lại cho Shorts (Shorts Remixing):**  
   🔘 **Cho phép phối lại video và âm thanh** (`shortsRemixing: "all"` — giúp người xem tạo Shorts lan tỏa video gốc).
6. **Danh mục (Category):**  
   **Giải trí** (`categoryId: "24"`).
7. **Bình luận và mức phân loại (Comments & Ratings):**  
   Bình luận: **Bật** | Kiểm duyệt: **Không** | Người có thể bình luận: **Bất kỳ ai** | Sắp xếp theo: **Hàng đầu** (`sortBy: "top"`).  
   ☑️ **Hiện số người xem thích video này** (`showLikeCount: true`).

---

## 2. TRỌNG TÂM NGHIÊN CỨU THỊ TRƯỜNG THÍNH GIẢ SÁCH NÓI (MARKET RESEARCH)
Để video đạt tỷ lệ nhấp (CTR $> 8\%$) và thời lượng xem trung bình (AVD $> 40\%$), kỹ năng áp dụng bộ khung nghiên cứu thị trường chuyên sâu:

### A. Bốn Nhóm Thính Giả Mục Tiêu (Audience Personas)
1. **Nhóm Di Chuyển & Lái Xe (Commuters & Drivers):**
   - *Hành vi:* Nghe qua Bluetooth ô tô hoặc tai nghe khi đi đường dài / kẹt xe.
   - *Nhu cầu:* Giọng đọc truyền cảm, rõ chữ, nhịp điệu vừa phải, không giật cục; âm thanh Master EBU R128 (-16 LUFS) cân bằng không gây chói tai.
   - *Từ khóa tìm kiếm:* `sách nói nghe lái xe`, `truyện audio đi đường dài`, `sách nói trọn bộ hay nhất`.
2. **Nhóm Thư Giãn & Ngủ Đêm (Bedtime Listeners):**
   - *Hành vi:* Bật video hẹn giờ trước khi đi ngủ, màn hình úp hoặc mở độ sáng thấp.
   - *Nhu cầu:* Nhạc nền mộc êm dịu (Cổ cầm, Tiêu sáo), không có âm thanh giật mình, phân đoạn rõ ràng để tiếp tục nghe hôm sau.
   - *Từ khóa tìm kiếm:* `sách nói dễ ngủ`, `truyện đêm khuya`, `nghe sách nói tĩnh tâm`.
3. **Nhóm Làm Việc & Học Tập (Focus & Productivity):**
   - *Hành vi:* Nghe thụ động trong lúc làm việc văn phòng, vẽ tranh, lập trình, làm việc nhà.
   - *Nhu cầu:* Mạch truyện lôi cuốn, giữ nhịp tập trung, không cần nhìn màn hình liên tục.
4. **Nhóm Đam Mê Lịch Sử & Mưu Lược (History & Strategy Enthusiasts):**
   - *Hành vi:* Nghe chủ động, phân tích nhân vật, tranh luận mưu kế và bài học nhân sinh.
   - *Nhu cầu:* Bảo tồn trọn vẹn nguyên tác, khẩu khí nhân vật trung thực, phân tích sâu sắc ở phần mô tả và bình luận.
   - *Từ khóa tìm kiếm:* `tam quốc diễn nghĩa hồi 1`, `lời thề vườn đào`, `phân tích mưu kế tam quốc`.

---

## 3. GIAO THỨC BẮT BUỘC KÍCH HOẠT HỘI ĐỒNG SUB-AGENTS (MANDATORY SWARM PROTOCOL)
> ⚠️ **CHỈ THỊ KHÔNG THỰC THI ĐƠN LẺ (ZERO-SOLO ENFORCEMENT):**  
> Tuyệt đối cấm AI Chính tự ý viết mô tả, tự chế tags hoặc tự tạo metadata một mình trong phiên chính.  
> 👉 **LƯỢT GỌI CÔNG CỤ ĐẦU TIÊN CỦA BẠN BẮT BUỘC PHẢI LÀ `invoke_subagent`**.

### Ma Trận Hội Đồng Sub-Agents Chuyên Môn Bắt Buộc:
1. **Subagent 1: `Audience & Market Research Strategist`**
   - *Nhiệm vụ:* Phân tích xu hướng tìm kiếm YouTube (Search Intent), phân khúc thính giả của tác phẩm, đề xuất từ khóa hạt nhân (Seed Keywords), từ khóa mở rộng (Long-tail Keywords) và các góc tiếp cận nội dung khơi gợi cảm xúc.
2. **Subagent 2: `Chapter Literary & Narrative Analyst`**
   - *Nhiệm vụ:* Nạp và phân tích sâu các tệp kịch bản (`summary.md`, `theatrical_script.json`, `storyboard_video.md`), trích xuất các bước ngoặt kịch tính, bối cảnh, nhân vật chính; đồng thời đọc tệp `.chunks_duration.json` để tính toán chính xác mốc thời gian Timestamps chuẩn YouTube.
3. **Subagent 3: `YouTube SEO Copywriter & Prompt Architect`**
   - *Nhiệm vụ:* Soạn thảo:
     - 3 phương án Tiêu đề (Chuẩn SEO Search, Nghệ thuật khơi gợi tò mò, Chuẩn Playlist Series).
     - Đoạn Hook 3 dòng đầu cuốn hút.
     - Thân bài mô tả chi tiết kèm Timestamps, giá trị tác phẩm, thông số sản xuất và CTA.
     - Danh sách 15–25 Tags từ khóa kiểm soát tổng chiều dài $\le 500$ ký tự.
     - Nội dung Bình luận ghim (Pinned Comment) kích hoạt thảo luận.
4. **Subagent 4: `Upload Strategy & Series Batch Coordinator`**
   - *Nhiệm vụ:* Khi xử lý toàn tác phẩm gồm nhiều hồi (lên đến > 100 video):
     - Đọc `.abv_seo_manifest.json` để phân chia công việc theo từng lô (Batch 5–10 hồi/agent).
     - Xây dựng cấu trúc Danh sách phát (Playlist Architecture).
     - Lập kế hoạch lịch đăng (Upload Cadence: ví dụ 2 video/ngày vào khung giờ vàng 11:30 hoặc 19:30).
     - Thiết kế luồng liên kết video gối đầu (End Screen cards, Next Episode Links).
5. **Subagent 5: `SEO Quality Gate & Compliance Auditor`**
   - *Nhiệm vụ:* Thẩm định độc lập bộ Metadata theo 5 SEO Quality Gates (QG1 đến QG5), kiểm tra số lượng ký tự nghiêm ngặt, rà soát cấu hình YouTube Defaults trước khi cho phép ghi nhận trạng thái `completed` vào `.abv_seo_manifest.json`.

---

## 4. TRÌNH TỰ TỪNG BƯỚC THỰC THI (STEP-BY-STEP WORKFLOW)

### Bước 4.1: Kiểm Tra Trạng Thái Tiến Trình (Manifest Inspection)
Chạy lệnh kiểm tra tiến độ hiện tại:
```bash
.venv/bin/python core/abv_youtube_seo_generator.py --book_dir "Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia" --status
```
Lệnh sẽ in ra bảng tiến độ:
```text
=======================================================
📊 ABV-03 PROGRESS STATUS: 37.5% (45/120)
=======================================================
  ✅ Completed Metadata : 45
  ⏳ Pending Metadata   : 75
  ❌ Failed Metadata    : 0
  🕒 Last Updated       : 2026-09-21T02:21:49+00:00
=======================================================
```

### Bước 4.2: Kích Hoạt Hội Đồng Sub-Agents Song Song Theo Batch
Đối với các video chưa hoàn thành, AI Chính phân chia theo lô và kích hoạt Sub-agents qua `invoke_subagent`:
```python
invoke_subagent(Subagents=[
    {
        "TypeName": "self",
        "Role": "Batch SEO Coordinator [Hoi 01-10]",
        "Prompt": "Chạy tối ưu SEO cho Hồi 01-10 bằng lệnh: .venv/bin/python core/abv_youtube_seo_generator.py --book_dir '...' --batch_start 1 --batch_end 10"
    },
    {
        "TypeName": "self",
        "Role": "Batch SEO Coordinator [Hoi 11-20]",
        "Prompt": "Chạy tối ưu SEO cho Hồi 11-20 bằng lệnh: .venv/bin/python core/abv_youtube_seo_generator.py --book_dir '...' --batch_start 11 --batch_end 20"
    }
])
```

### Bước 4.3: Tự Động Hóa Kỹ Thuật & Cân Chỉnh Timestamps
- Từng worker gọi [core/abv_youtube_seo_generator.py](file:///media/hoanganh/disk1_vol1/Solution/audio-book-refactor/core/abv_youtube_seo_generator.py) để:
  - Tự động bỏ qua các video đã `completed`.
  - Tính toán tự động mốc thời gian từ `.chunks_duration.json` theo định dạng `MM:SS`.
  - Gán ảnh bìa Thumbnail tương ứng từ thư mục `Final-[Tên-Sách]/backgrounds/`.
  - Kiểm toán 5 Quality Gates.
  - Lưu metadata vào `Final-[Tên-Sách]/Videos/youtube_metadata/youtube_metadata_{chap_slug}.json`.
  - Cập nhật nguyên tử trạng thái `completed` vào `.abv_seo_manifest.json`.

### Bước 4.4: Xuất Bản Báo Cáo Tổng Thể Chiến Lược
- Sau khi toàn bộ các batch hoàn tất (100% completed), hệ thống xuất bản:
  `Final-[Tên-Sách]/Videos/YouTube_SEO_Master_Strategy.md`.

---

## 5. BỐ CỤC MÔ TẢ CHUẨN MỰC (GOLDEN DESCRIPTION TEMPLATE)
Mọi video xuất xưởng bắt buộc áp dụng cấu trúc bố cục đã kiểm chứng thành công:

```markdown
🔥 Sách Nói Kịch Nghệ Đa Thanh: [TÊN TÁC PHẨM IN HOA] — [Tác Giả]
⚔️ HỒI [X]: [TIÊU ĐỀ HỒI IN HOA]

[Đoạn Hook 2–3 dòng đầu: Khắc họa bước ngoặt kịch tính, tình thế hiểm nghèo hoặc đại sự chấn động, kích thích sự tò mò của người nghe trước khi bấm nút "Thêm"].

[Đoạn diễn giải ngắn gọn về bối cảnh lịch sử, mâu thuẫn thời cuộc và lý tưởng của các nhân vật trung tâm].

⏱️ MỤC LỤC CHI TIẾT & TIMESTAMPS (Bấm vào mốc thời gian để nghe đoạn bạn thích):
00:00 Mở đầu: [Tên phân cảnh 1]
03:06 [Tên phân cảnh 2]
... (Toàn bộ các phân đoạn trích xuất từ .chunks_duration.json)

---
✨ ĐẶC TRƯNG BẢN SÁCH NÓI:
• Giọng đọc: Phân vai kịch nghệ đa thanh (Theatrical Multi-Voice) sống động, giữ trọn thần thái và khẩu khí cổ phong của từng nhân vật.
• Âm thanh: Hòa âm nhạc nền mộc cổ phong (Cổ cầm, Đàn tranh, Tiêu sáo) chuẩn phát thanh EBU R128 (-16 LUFS) êm dịu, không gây mỏi tai.
• Hình ảnh: Minh họa nghệ thuật cổ điển 1080p Full HD.

📌 ĐĂNG KÝ KÊNH TIBE AUDIO BOOK để không bỏ lỡ các Hồi tiếp theo của bộ tiểu thuyết kinh điển [Tên Tác Phẩm]:
👉 Nhấn Đăng Ký (Subscribe) và Bật Chuông thông báo 🔔
👉 Danh sách phát trọn bộ: [Link hoặc Tên Playlist]
👉 Đừng quên bấm Like và để lại Bình Luận cảm nghĩ của bạn về nhân vật trong hồi này nhé!

#[TenTacPhamKhongDau] #SachNoi #TibeAudioBook #[NhanVatChinh] #LichSu #SachNoiHay
```

---

## 6. OUTPUT CONTRACT (CHUẨN ĐẦU RA & RÀNG BUỘC TỆP TIN)
1. `Final-[Tên-Sách]/Videos/youtube_metadata/youtube_metadata_{chap_slug}.json`: Tệp JSON chứa đầy đủ Title, Description, Tags, Thumbnails, Default Settings, Pinned Comment đạt chuẩn 100% 5 Quality Gates.
2. `Final-[Tên-Sách]/Videos/.abv_seo_manifest.json`: Tệp manifest nguyên tử theo dõi tiến trình của toàn bộ video.
3. `Final-[Tên-Sách]/Videos/YouTube_SEO_Master_Strategy.md`: Báo cáo tổng thể chiến lược xuất bản, kế hoạch Playlist, ma trận từ khóa và lịch phát hành cho toàn bộ tác phẩm.

---

## 7. PHỦ ĐỊNH & CẤM KỴ (NEGATIVE TRIGGERS & SYSTEM INVARIANTS)
1. **NO-SOLO-BYPASS INVARIANT:** Cấm AI Chính tự ý viết metadata một mình mà không kích hoạt Hội đồng Sub-agents qua `invoke_subagent`.
2. **ATOMIC-RESUME INVARIANT:** Cấm phân tích hoặc ghi đè lại các video đã có status `completed` trong `.abv_seo_manifest.json` trừ khi có cờ `--force`.
3. **CENTRALIZED-STORAGE INVARIANT:** Toàn bộ tệp metadata và manifest bắt buộc phải lưu tập trung tại thư mục Final Video của tác phẩm (`Final-[Tên-Sách]/Videos/`). Tuyệt đối cấm tạo file rác ở thư mục gốc repository.
4. **STRICT-LIMIT INVARIANT:** Cấm tạo Tiêu đề $> 100$ ký tự, Mô tả $> 5.000$ ký tự, Thẻ Tags tổng $> 500$ ký tự hoặc Hashtag $> 60$.
5. **MANDATORY-TIMESTAMPS INVARIANT:** Mô tả bắt buộc phải có Timestamps chính xác bắt đầu từ `00:00`. Cấm mô tả cụt ngủ không có mốc thời gian.
6. **DEFAULT-CONFIG INVARIANT:** Tuyệt đối không thay đổi các thiết lập cốt lõi: Không dành cho trẻ em, Tuyên bố có AI, Cho phép Shorts remix, Category Giải trí (24).
