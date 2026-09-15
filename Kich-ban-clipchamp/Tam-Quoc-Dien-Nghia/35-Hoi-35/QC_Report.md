# Báo Cáo Kiểm Toán Chất Lượng (QC Audit Report) — 35-Hoi-35
**Trạng Thái Thẩm Định:** ✅ PASSED (100% 7 GATES PASSED)
**Thời Điểm Kiểm Toán:** `2026-09-15T04:10:25.338210+00:00`

| Gate | Tiêu Chí Kiểm Toán | Kết Quả | Chi Tiết Đối Soát |
| :--- | :--- | :---: | :--- |
| **Gate 1: Tên Thư Mục Chuẩn** | Tên Thư Mục Chuẩn | ✅ PASS | Thư mục: '35-Hoi-35' |
| **Gate 2: Dung Lượng Chunk <= 3000 ký tự** | Dung Lượng Chunk <= 3000 ký tự | ✅ PASS | 7 chunks đạt chuẩn (Min: 1630, Max: 2283, Avg: 2111 ký tự) |
| **Gate 3: Khử Sạch Ký Tự Cấm TTS** | Khử Sạch Ký Tự Cấm TTS | ✅ PASS | 100% Sạch ký tự cấm |
| **Gate 4: Viết Chữ Số Toàn Diện (Zero-digit)** | Viết Chữ Số Toàn Diện (Zero-digit) | ✅ PASS | 100% Viết chữ tự nhiên (0 chữ số thô) |
| **Gate 5: Định Dạng Nhịp Thở (. ......)** | Định Dạng Nhịp Thở (. ......) | ✅ PASS | Đạt chuẩn (3 markers ngắt nghỉ phát thanh) |
| **Gate 6: Word Count Delta (Chống Tóm Tắt)** | Word Count Delta (Chống Tóm Tắt) | ✅ PASS | Tham chiếu (normalized.txt): 3241 từ | Kịch bản: 3241 từ | Độ lệch: 0.00% (Ngưỡng $\le$ 5%) | Tỷ lệ dịch/gốc: 97.8% |
| **Gate 7: Cấp Quyền Thu Âm TTS (Step 08 Clearance)** | Cấp Quyền Thu Âm TTS (Step 08 Clearance) | ✅ PASS | ĐỦ ĐIỀU KIỆN THU ÂM TTS (100% 7 GATES PASSED) |

### Bảng Thống Kê Chi Tiết Từng File Kịch Bản:
| Tên File | Dung Lượng Ký Tự (Chars) | Số Từ (Words) | Trạng Thái Gate 2 (<= 3000) |
| :--- | :---: | :---: | :---: |
| `Kich-ban-1.txt` | 2283 | 497 | ✅ PASS |
| `Kich-ban-2.txt` | 2203 | 480 | ✅ PASS |
| `Kich-ban-3.txt` | 2102 | 461 | ✅ PASS |
| `Kich-ban-4.txt` | 2212 | 482 | ✅ PASS |
| `Kich-ban-5.txt` | 2192 | 489 | ✅ PASS |
| `Kich-ban-6.txt` | 2160 | 479 | ✅ PASS |
| `Kich-ban-7.txt` | 1630 | 353 | ✅ PASS |

---
*Báo cáo được khởi tạo tự động bởi Audiobook QC Auditor Engine (Step 07)*
