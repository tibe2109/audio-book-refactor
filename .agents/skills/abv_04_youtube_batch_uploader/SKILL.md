---
name: abv_04_youtube_batch_uploader
description: "Kỹ năng điều phối đăng tải video và kịch bản SEO YouTube hàng loạt lên YouTube (Audiobook YouTube Batch Uploader & Asset Synchronizer). Tiếp nhận nguồn video final của tác phẩm, ảnh bìa thumbnails và kịch bản mô tả SEO; sở hữu trí tuệ tự động tìm kiếm (Smart Auto-Discovery) phân giải toàn bộ các thư mục liên quan (Videos, backgrounds, youtube_metadata) khi người dùng chỉ cung cấp đường link source chung chung. Sử dụng thông tin xác thực OAuth 2.0 tại tools/client_secret.json và token tại tools/token.json. Tích hợp phân tích chuyên sâu về giới hạn hạn ngạch (YouTube Daily Quota 10.000 điểm/ngày, 1.650 điểm/video) và số luồng upload đồng thời tối ưu (2–3 luồng song song để chống nghẽn băng thông, tránh lỗi 429 Too Many Requests và TimeoutError). Trang bị cơ chế Khóa tiến trình chống chạy đè (Concurrency Process Lock .upload.lock với fcntl.flock & PID inspection), Kiểm tra trùng lặp trước khi upload 2 tầng (Pre-Upload Deduplication: Local Manifest + Remote YouTube Playlist/Channel Cache Check), và Tự phục hồi retry với exponential backoff khi gặp lỗi 429 lúc đặt ảnh bìa thumbnail. Bắt buộc kích hoạt tối đa mảng Sub-agents chuyên môn song song (invoke_subagent) phân chia công việc theo từng lô video (Batch Processing: 2-3 video/agent) để tối đa hóa tốc độ tải lên toàn tác phẩm (> 100 video). Toàn bộ tiến trình được kiểm soát nguyên tử qua tệp .abv_upload_manifest.json đặt ngay tại thư mục Final Video, tự động bỏ qua các video đã đăng thành công (Atomic Resume & Skip Uploaded) và tiếp tục công việc ngay lập tức nếu bị gián đoạn giữa chừng."
---

# 🚀 ABV-04: AUDIOBOOK YOUTUBE BATCH UPLOADER & ASSET SYNCHRONIZER
## QUY TRÌNH THAO TÁC CHUẨN (SOP) TỰ ĐỘNG ĐĂNG TẢI VIDEO SÁCH NÓI, THUMBNAIL VÀ METADATA SEO LÊN YOUTUBE HÀNG LOẠT

---

## 1. SOP / ĐẶC TẢ KỸ THUẬT (SPECIFICATION)
`abv_04_youtube_batch_uploader` là kỹ năng bước 4 (khâu phát hành cuối cùng) trong chuỗi sản xuất và phát hành Video Sách Nói (ABV Pipeline), đảm nhiệm vai trò **Kỹ Sư Điều Phối Đăng Tải YouTube Hàng Loạt (YouTube Batch Uploader & Asset Synchronizer)**. Kỹ năng chịu trách nhiệm:

### A. Yêu Cầu Đầu Vào & Cơ Chế Tự Động Tìm Kiếm (Smart Auto-Discovery)
Kỹ năng yêu cầu người dùng cung cấp 3 thành phần tài nguyên (hoặc chỉ cần cung cấp đường link source chung của tác phẩm):
1. **Source Video Final:** Tệp `Final_Video_*.mp4` (chuẩn 1080p từ kỹ năng ABV-02).
2. **Thumbnails:** Thư mục ảnh bìa (chuẩn 16:9, tự động nén $\le 2\text{MB}$ từ ABV-01 hoặc thư viện `backgrounds/`).
3. **Kịch bản Mô Tả SEO YouTube:** Tệp `youtube_metadata_*.json` (chuẩn SEO từ kỹ năng ABV-03).

> 💡 **Khả năng Tự Động Phân Giải (Smart Auto-Discovery):**  
> Khi người dùng chỉ gửi đường dẫn dự án chung chung (ví dụ: `/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia`), kỹ năng tự động quét và định vị chính xác:
> - `final_video_dir`: `Final-[Tên-Sách]/Videos/`
> - `metadata_dir`: `Final-[Tên-Sách]/Videos/youtube_metadata/` (hoặc `Final-[Tên-Sách]/youtube_metadata/`)
> - `backgrounds_dir`: `Final-[Tên-Sách]/backgrounds/`
> - `client_secrets`: `tools/client_secret.json`
> - `token_file`: `tools/token.json`
> - `lock_file`: `Final-[Tên-Sách]/Videos/.upload.lock`

---

### B. Phân Tích Giới Hạn Quota, Số Luồng Tối Ưu & Khóa Tiến Trình (Concurrency & Quota Analysis)
1. **Phân Tích Hạn Ngạch Điểm Hàng Ngày (YouTube Daily Quota):**
   - Hạn mức mặc định của Google Cloud: **10.000 Quota Units / ngày** (tự động làm mới lúc 14:00 - 15:00 giờ VN).
   - Chi phí điểm của từng thao tác:
     - Khởi tạo & Upload Video (`videos.insert`): **1.600 units**.
     - Đặt ảnh bìa tùy chỉnh (`thumbnails.set`): **50 units**.
     - Thêm vào Playlist (`playlistItems.insert`): **50 units**.
     - **Tổng cộng 1 video hoàn chỉnh:** $\approx \mathbf{1.650\text{ units}}$.
   - **Năng lực đăng tải an toàn mỗi ngày:** **5 – 6 video / ngày** trên hạn ngạch mặc định.  
     *(Đối với dự án quy mô lớn $> 100$ video, người dùng có thể gửi đơn xin Google nâng Quota lên 50.000 – 100.000 units/ngày để đăng 30 – 60 video/ngày).*

2. **Phân Tích Số Luồng Upload Đồng Thời Tối Ưu (Concurrency Sweet Spot):**
   - Mặc dù Google hỗ trợ đa luồng HTTP, việc upload các tệp video sách nói dung lượng lớn (100MB – 300MB/tệp) qua giao thức Resumable Upload (chunks 8MB) nếu mở quá nhiều luồng ($> 4$ luồng trên 1 IP/token) sẽ gây:
     - Tranh chấp băng thông dẫn đến lỗi ngắt kết nối mạng (`TimeoutError`).
     - Google trả về mã lỗi `429 Too Many Requests` hoặc `uploadRateLimitExceeded`.
   - **Số luồng tối ưu (Sweet Spot):** **2 đến 3 luồng song song (2–3 Parallel Sub-agents)**.
     - Mỗi Sub-agent phụ trách 1 batch nhỏ (2–3 video), upload tuần tự trong batch của mình.
     - Giữa các Sub-agent chạy song song độc lập. Tổng tốc độ đẩy dữ liệu đạt **12 – 18 MB/s**, vừa tối đa hóa đường truyền vừa an toàn tuyệt đối 100%.

3. **Cơ Chế Khóa Tiến Trình Chống Trùng Lặp (Concurrency Process Lock — `.upload.lock`):**
   - Để triệt tiêu hoàn toàn nguy cơ chạy đè nhiều tiến trình upload lên cùng một tác phẩm gây trùng lặp video và cạn kiệt Quota, hệ thống bắt buộc sử dụng cơ chế Process Lock tại `final_video_dir / ".upload.lock"`.
   - **Khóa kép tầng hạt nhân & PID (Dual-Layer Kernel Flock & PID Inspection):**
     - Sử dụng `fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)` để khóa độc quyền ở cấp độ Kernel Linux.
     - Ghi nhận PID và metadata tiến trình vào file lock. Kết hợp kiểm tra trạng thái sống của tiến trình (`psutil.pid_exists` / `os.kill(pid, 0)`) để loại bỏ hoàn toàn hiện tượng khóa chết (Stale Lock) khi tiến trình trước bị ngắt đột ngột (`SIGKILL` hoặc mất điện).
   - **Thoát an toàn khi có xung đột:** Nếu phát hiện đã có tiến trình khác đang giữ khóa, tiến trình mới sẽ in cảnh báo chi tiết (PID đang chạy, đường dẫn lockfile) và dừng lại an toàn (`sys.exit(0)`) thay vì cố chạy song song gây xung đột.
   - **Tự động giải phóng (Auto-Release Lifecycle):** File lock được tự động giải phóng và dọn sạch khi tiến trình kết thúc (dù thành công hay gặp ngoại lệ) thông qua context manager và `atexit`.

---

### C. Quản Lý Tiến Trình Nguyên Tử, Chống Trùng Lặp & Tự Phục Hồi
1. **Vị trí tệp Manifest:** Lưu trực tiếp tại `Final-[Tên-Sách]/Videos/.abv_upload_manifest.json`.
2. **Cấu trúc Manifest:**
   ```json
   {
     "book_name": "Tam-Quoc-Dien-Nghia",
     "final_video_dir": "/path/to/Final-Tam-Quoc-Dien-Nghia/Videos",
     "total_videos": 120,
     "uploaded_count": 1,
     "pending_count": 119,
     "failed_count": 0,
     "videos": {
       "Final_Video_01-Hoi-01_Part1.mp4": {
         "video_file": "Final_Video_01-Hoi-01_Part1.mp4",
         "chapter_slug": "01-Hoi-01",
         "status": "uploaded",
         "video_id": "OUkuc46XzU0",
         "youtube_url": "https://youtu.be/OUkuc46XzU0",
         "uploaded_at": "2026-09-18T18:15:50Z"
       },
       "Final_Video_02-Hoi-02_Part1.mp4": {
         "video_file": "Final_Video_02-Hoi-02_Part1.mp4",
         "chapter_slug": "02-Hoi-02",
         "status": "pending",
         "video_id": null,
         "youtube_url": null,
         "uploaded_at": null
       }
     }
   }
   ```
3. **Cơ Chế Kiểm Tra Trùng Lặp Trước Khi Upload (Pre-Upload Deduplication & Atomic Resume):**
   Trước khi tiến hành upload bất kỳ video nào (`Final_Video_XX.mp4`), hệ thống thực hiện kiểm tra 2 tầng nghiêm ngặt:
   - **Tầng 1 (Local Manifest Check):** Kiểm tra entry trong manifest: nếu `status in ("uploaded", "completed")` và có `video_id` hợp lệ $\to$ **LẬP TỨC BỎ QUA (`⏭️ [SKIP DUPLICATE]`)**, không upload lại gây lãng phí Quota!
   - **Tầng 2 (Remote YouTube Playlist & Channel Cache Check):** Truy vấn trước danh sách video từ Playlist mục tiêu và Uploads playlist của Channel để lập bộ nhớ đệm (Deduplication Cache, chỉ tiêu tốn 1–2 Quota Units). Đối soát video theo:
     1. Tiêu đề video (khớp chính xác hoặc chuẩn hóa).
     2. Chapter slug (ví dụ: `02-Hoi-02`).
     3. Số thứ tự Hồi/Chương (ví dụ: `Hồi 2:`, `Hồi 02:`, `Chương 2:`).
   - **Tự động đồng bộ ngược:** Nếu phát hiện video đã tồn tại trên YouTube nhưng manifest chưa cập nhật, hệ thống tự động ghi nhận `video_id`, `youtube_url`, cập nhật trạng thái `uploaded` vào manifest nguyên tử và BỎ QUA (`⏭️ [SKIP DUPLICATE]`).
   - Cập nhật manifest nguyên tử sau mỗi video bằng tệp tạm và `os.replace`.

4. **Cơ Chế Tự Phục Hồi & Thử Lại Thumbnail (Thumbnail 429 Retry & Exponential Backoff):**
   - Khi đặt ảnh bìa tùy chỉnh (`thumbnails.set`), nếu gặp mã lỗi `429 Too Many Requests`, lỗi mạng hoặc lỗi server 5xx, hệ thống tự động kích hoạt cơ chế retry với thuật toán **Exponential Backoff**:
     $$\text{Delay} = \text{base\_backoff} \times 2^{\text{attempt}} \quad (3\text{s}, 6\text{s}, 12\text{s}, 24\text{s})$$
     thử lại tối đa 5 lần.
   - **Không làm gián đoạn upload video:** Nếu sau 5 lần thử lại mà YouTube vẫn trả về 429 (do chạm trần giới hạn thumbnail hàng ngày), hệ thống ghi nhận cảnh báo an toàn và vẫn công nhận video upload thành công (`status: "uploaded"`), cho phép người dùng đồng bộ lại ảnh bìa sau bằng lệnh `--sync_thumbnails`.

---

## 2. GIAO THỨC BẮT BUỘC KÍCH HOẠT MẢNG SUB-AGENTS (MANDATORY SWARM PROTOCOL)
> ⚠️ **CHỈ THỊ KHÔNG THỰC THI ĐƠN LẺ (ZERO-SOLO ENFORCEMENT):**  
> Tuyệt đối cấm AI Chính tự ý chạy upload tuần tự từng video một mình khi tác phẩm có nhiều video mà không kích hoạt mảng Sub-agents qua `invoke_subagent`.  
> 👉 **LƯỢT GỌI CÔNG CỤ ĐẦU TIÊN CỦA BẠN BẮT BUỘC PHẢI LÀ `invoke_subagent`**.

### Ma Trận Hội Đồng Sub-Agents Chuyên Môn Bắt Buộc:
1. **Subagent 1: `Upload Batch Worker [Batch 1: Hồi 02-04]`**
   - *Nhiệm vụ:* Đảm nhiệm tải lên song song nhóm video từ Hồi 02 đến Hồi 04. Tuân thủ Process Lock và Pre-Upload Deduplication.
2. **Subagent 2: `Upload Batch Worker [Batch 2: Hồi 05-07]`**
   - *Nhiệm vụ:* Đảm nhiệm tải lên song song nhóm video từ Hồi 05 đến Hồi 07. Tuân thủ Process Lock và Pre-Upload Deduplication.
3. **Subagent 3: `Thumbnail & Asset Integrity Linker`**
   - *Nhiệm vụ:* Rà soát đối chiếu 1-1 giữa Video MP4, Thumbnail tương ứng (`Background-1_thumb.jpg` / `Background-N.png`), đảm bảo ảnh bìa đã được tối ưu hóa $\le 2\text{MB}$, và tệp Metadata SEO JSON tương ứng trước khi đẩy vào hàng đợi upload.
4. **Subagent 4: `Quota & Rate Limit Auditor`**
   - *Nhiệm vụ:* Giám sát số lượng Quota tiêu thụ trong ngày, kiểm soát tốc độ request, theo dõi lockfile `.upload.lock`, phát hiện sớm các cảnh báo rate limit 429 để kích hoạt exponential backoff kịp thời.

---

## 3. TRÌNH TỰ TỪNG BƯỚC THỰC THI (STEP-BY-STEP WORKFLOW)

### Bước 3.1: Tiếp Nhận Nguồn & Tự Động Định Vị Tài Nguyên (Auto-Discovery)
- Tiếp nhận đường dẫn nguồn từ người dùng.
- Tự động phân giải các thư mục `Videos`, `youtube_metadata`, `backgrounds`.
- Kiểm tra sự tồn tại của `tools/client_secret.json` và `tools/token.json`.

### Bước 3.2: Kiểm Tra Tiến Trình Upload Hiện Tại
Chạy lệnh kiểm tra trạng thái manifest (không kích hoạt lock):
```bash
.venv/bin/python core/abv_youtube_uploader.py --source "Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia" --status
```
Kết quả hiển thị:
```text
=======================================================
📊 ABV-04 UPLOAD PROGRESS: 0.8% (1/120)
=======================================================
  ✅ Uploaded Videos : 1
  ⏳ Pending Videos  : 119
  ❌ Failed Videos   : 0
=======================================================
```

### Bước 3.3: Điều Phối Mảng Sub-Agents Song Song (2–3 Luồng)
AI Chính kích hoạt mảng Sub-agents chuyên trách qua `invoke_subagent`:
```python
invoke_subagent(Subagents=[
    {
        "TypeName": "self",
        "Role": "Upload Batch Worker [Batch 1: Hoi 02-04]",
        "Prompt": "Chạy tải lên YouTube Hồi 02-04 bằng lệnh: .venv/bin/python core/abv_youtube_uploader.py --source 'Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia' --batch_start 2 --batch_end 4"
    },
    {
        "TypeName": "self",
        "Role": "Upload Batch Worker [Batch 2: Hoi 05-07]",
        "Prompt": "Chạy tải lên YouTube Hồi 05-07 bằng lệnh: .venv/bin/python core/abv_youtube_uploader.py --source 'Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia' --batch_start 5 --batch_end 7"
    },
    {
        "TypeName": "self",
        "Role": "Thumbnail & Asset Integrity Linker",
        "Prompt": "Kiểm tra tính sẵn sàng của file video MP4, ảnh bìa Backgrounds (<=2MB) và file metadata JSON cho các hồi từ 02 đến 07."
    }
])
```

### Bước 3.4: Tải Lên Dữ Liệu, Khóa Tiến Trình & Khử Trùng Lặp
- Khởi tạo `ProcessLock` tại `.upload.lock`. Nếu có tiến trình khác đang chạy, dừng an toàn.
- Quét và xây dựng bộ nhớ đệm kiểm tra trùng lặp từ YouTube (Playlist & Channel).
- Bỏ qua các video đã đăng theo kết quả đối soát manifest và remote YouTube (`⏭️ [SKIP DUPLICATE]`).
- Từng Worker tải dữ liệu lên YouTube qua giao thức Resumable Upload (8MB chunks).
- Đặt ảnh bìa với cơ chế Exponential Backoff khi gặp lỗi 429.
- Đính kèm toàn bộ Tiêu đề, Mô tả (kèm Timestamps), Tags, Category 24, và Privacy (`unlisted`).
- Ghi nhận `youtube_url` và cập nhật nguyên tử vào `.abv_upload_manifest.json`.

### Bước 3.5: Xuất Bản Báo Cáo Phát Hành (Master Upload Report)
- Xuất bản báo cáo tổng hợp tại: `Final-[Tên-Sách]/Videos/Master_Upload_Report.md` thống kê toàn bộ link video YouTube đã phát hành của tác phẩm.

---

## 4. OUTPUT CONTRACT (CHUẨN ĐẦU RA & RÀNG BUỘC TỆP TIN)
1. `Final-[Tên-Sách]/Videos/.abv_upload_manifest.json`: Tệp manifest quản lý tiến trình đăng tải của toàn bộ video, lưu trữ video ID và URL YouTube.
2. `Final-[Tên-Sách]/Videos/.upload.lock`: Tệp khóa tiến trình tạm thời (tự động giải phóng khi hoàn thành).
3. `Final-[Tên-Sách]/Videos/Master_Upload_Report.md`: Báo cáo bảng Markdown tổng kết danh sách các video đã upload thành công kèm link YouTube trực tiếp.

---

## 5. PHỦ ĐỊNH & CẤM KỴ (NEGATIVE TRIGGERS & SYSTEM INVARIANTS)
1. **NO-SOLO-BYPASS INVARIANT:** Cấm AI Chính tự ý chạy upload tuần tự một mình khi tác phẩm có nhiều video mà không kích hoạt mảng Sub-agents qua `invoke_subagent`.
2. **CONCURRENCY-CAP INVARIANT:** Tuyệt đối không mở quá 3 luồng upload song song cùng lúc để tránh nghẽn băng thông và lỗi `429 Too Many Requests`.
3. **CONCURRENCY-LOCK INVARIANT:** Bắt buộc thiết lập và duy trì `ProcessLock` (`.upload.lock`) trong suốt quá trình upload; cấm chạy đè tiến trình khi một tiến trình khác đang xử lý cùng tác phẩm.
4. **PRE-UPLOAD-DEDUPLICATION INVARIANT:** Bắt buộc thực hiện kiểm tra trùng lặp 2 tầng (Manifest + Remote YouTube Playlist/Channel) trước khi upload bất kỳ video nào; tự động bỏ qua (Skip) ngay lập tức nếu video đã tồn tại.
5. **THUMBNAIL-RETRY-BACKOFF INVARIANT:** Bắt buộc áp dụng cơ chế retry với exponential backoff khi gặp mã lỗi 429 lúc đặt ảnh bìa; tuyệt đối không đánh rớt trạng thái thành công của video chỉ vì giới hạn thumbnail.
6. **SKIP-UPLOADED INVARIANT:** Bắt buộc bỏ qua các video đã có status `uploaded` hoặc `completed` trong manifest, cấm upload lại gây lãng phí Quota.
7. **THUMBNAIL-SIZE INVARIANT:** Bắt buộc nén ảnh bìa $\le 2\text{MB}$ trước khi gọi API `thumbnails.set`. Cấm gửi ảnh $> 2\text{MB}$ gây lỗi 400/403.
8. **ROOT-CLEANLINESS INVARIANT:** Mọi tệp manifest, lock và báo cáo phải lưu đúng tại thư mục Final Video của tác phẩm (`Final-[Tên-Sách]/Videos/`). Cấm tạo tệp rác tại thư mục gốc repository.
