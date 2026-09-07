# DÂY CHUYỀN SẢN XUẤT SÁCH NÓI VẠN NĂNG (UNIVERSAL END-TO-END AUDIOBOOK WORKFLOW)
## TỰ ĐỘNG HÓA TỪ TÀI LIỆU GỐC (PDF/DOCX/TEXT) ĐẾN MASTER SÁCH NÓI CHUẨN PHÁT THANH
---

### 1. Triết Lý Thiết Kế (Core Architectural Philosophy)
- **Độc lập Ngữ cảnh (Context Isolation):** Mỗi chương được xử lý trong một phiên/tiến trình con sạch sẽ, loại bỏ hoàn toàn hiện tượng thoái hóa ngữ cảnh (Context Degradation) và ảo giác (Hallucination) khi xử lý sách dày hàng trăm trang.
- **Cổng Chặn Cứng Chất Lượng (Hard Quality Gates):** Không cho phép lỗi đi qua. Nếu Bước 07 (QC) chưa đạt 100% 7 Cổng chất lượng, hệ thống sẽ tự động kích hoạt vòng lặp khắc phục lỗi (Self-Healing Loop) trước khi chuyển sang khâu sinh giọng đọc.
- **Khóa Cứng Thời Lượng An Toàn (Duration Hard-Cap):** Thuật toán phân bổ cân bằng toán học ở Bước 09 & 10 bắt buộc mọi tập phát thanh đều nằm trong khung [25 – 35 phút], **tuyệt đối không có bất kỳ tập nào vượt quá 35 phút**.
- **Tính Phổ Quát & Đa Năng (Universal Portability):** Áp dụng cho bất kỳ cuốn sách, bất kỳ ngôn ngữ hay lĩnh vực nào thông qua cấu hình `book_literary_profile.json` và `glossary.json`.

---

### 2. Sơ Đồ Quy Trình 10 Bước Chuẩn Hóa

```
[ BƯỚC 01: PDF STRUCTURE EXTRACTOR ]
  • Bóc tách cấu trúc PDF, loại bỏ số trang giấy in, Header, Footer, nối liền Drop-cap gãy dòng.
  • Đầu ra: raw_original.txt
       │
       ▼
[ BƯỚC 02: AUTHOR PERSONA TRANSLATOR ]
  • Nhập vai tác giả/chuyên gia, chuyển thể văn phong tự nhiên, giữ nguyên 100% tri thức và thuật ngữ Latinh.
  • Đầu ra: translated.txt
       │
       ▼
[ BƯỚC 03: CONTEXTUAL PHONETIC NORMALIZER ]
  • Chuẩn hóa số học (12 -> mười hai), tách âm phát thanh viết tắt (P-M-I, W-B-S), bảo toàn thuật ngữ quốc tế.
  • Đầu ra: normalized.txt
       │
       ▼
[ BƯỚC 04: SMART AUDIOBOOK RECHUNKER ]
  • Phân rã văn bản thành các chunks đệm tối ưu cho AI phát thanh (2.500 - 3.500 ký tự) theo ranh giới đoạn văn.
  • Đầu ra: Kich-ban-raw-1.txt -> Kich-ban-raw-N.txt
       │
       ▼
[ BƯỚC 05: SCRIPT STRUCTURE FORMATTER ]
  • Phân tầng tiêu đề IN HOA, chèn khoảng lặng phát thanh sâu ". ......" (1.5 - 2.0s) tại ranh giới chuyển ý.
  • Đầu ra: Kịch bản có cấu trúc nhịp thở
       │
       ▼
[ BƯỚC 06: LLM SCRIPT REFINER ]
  • Tinh chỉnh câu chữ diễn đọc trôi chảy, thêm dấu phẩy ngắt hơi tự nhiên (Breathing Commas), khử ký tự cấm TTS.
  • Đầu ra: Kich-ban-1.txt -> Kich-ban-N.txt
       │
       ▼
[ BƯỚC 07: SEMANTIC QC AUDITOR (HARD GATE) ]
  • Kiểm toán tự động 7 Quality Gates (Cú pháp, Giấy in, Ký tự cấm, Số trần, Latinh, Nhịp thở, Tri thức).
  • Điều kiện: 100% PASSED -> Xuất bản QC_Report.md và mở khóa sang Bước 08.
       │
       ▼
[ BƯỚC 08: UNIVERSAL NEURAL DUAL-VOICE TTS ]
  • Thu âm song thanh NamMinh Neural (VN) x Brian Multilingual Neural (EN), khử dead-gap, đệm khẩu hình 40ms.
  • Đầu ra: audio_chunks/chunk_1.mp3 -> chunk_N.mp3
       │
       ▼
[ BƯỚC 09: AUDIO SMART AGGREGATOR ]
  • Toán học cân bằng thời lượng, tự động phân nhóm các chunks thành các tập từ [25 - 35 phút].
  • Đầu ra: Full_ChapterX_PartY.mp3
       │
       ▼
[ BƯỚC 10: DYNAMIC BGM SCENE-SCORING MASTER ]
  • Lên timeline 3 Scenes cảm xúc, Volume Ducking -20dB, Acrossfade 3s, xuất bản bản quyền Master.
  • Đầu ra: Final_Audio_ChapterX_PartY.mp3 (Lưu tại thư mục chương & release hub audio_output/)
```

---

### 3. Hướng Dẫn Vận Hành Engine Điều Phối
- Chạy tự động từng chương:
  ```powershell
  python scripts/universal_audiobook_workflow.py --chapter 05-pmbok-introduction
  ```
- Chạy tự động cả cuốn sách hoặc một dải chương:
  ```powershell
  python scripts/universal_audiobook_workflow.py --from 5 --to 15
  ```
