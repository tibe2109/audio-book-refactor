# Báo Cáo Kiểm Toán Chất Lượng (QC Audit Report) — 120-Hoi-120
**Trạng Thái Thẩm Định:** ✅ PASSED (100% 7 GATES PASSED)
**Thời Điểm Kiểm Toán:** `2026-09-15T04:10:29.312502+00:00`

| Gate | Tiêu Chí Kiểm Toán | Kết Quả | Chi Tiết Đối Soát |
| :--- | :--- | :---: | :--- |
| **Gate 1: Tên Thư Mục Chuẩn** | Tên Thư Mục Chuẩn | ✅ PASS | Thư mục: '120-Hoi-120' |
| **Gate 2: Dung Lượng Chunk <= 3000 ký tự** | Dung Lượng Chunk <= 3000 ký tự | ✅ PASS | 13 chunks đạt chuẩn (Min: 1637, Max: 2321, Avg: 2131 ký tự) |
| **Gate 3: Khử Sạch Ký Tự Cấm TTS** | Khử Sạch Ký Tự Cấm TTS | ✅ PASS | 100% Sạch ký tự cấm |
| **Gate 4: Viết Chữ Số Toàn Diện (Zero-digit)** | Viết Chữ Số Toàn Diện (Zero-digit) | ✅ PASS | 100% Viết chữ tự nhiên (0 chữ số thô) |
| **Gate 5: Định Dạng Nhịp Thở (. ......)** | Định Dạng Nhịp Thở (. ......) | ✅ PASS | Đạt chuẩn (6 markers ngắt nghỉ phát thanh) |
| **Gate 6: Word Count Delta (Chống Tóm Tắt)** | Word Count Delta (Chống Tóm Tắt) | ✅ PASS | Tham chiếu (normalized.txt): 6108 từ | Kịch bản: 6116 từ | Độ lệch: 0.13% (Ngưỡng $\le$ 5%) | Tỷ lệ dịch/gốc: 99.3% |
| **Gate 7: Cấp Quyền Thu Âm TTS (Step 08 Clearance)** | Cấp Quyền Thu Âm TTS (Step 08 Clearance) | ✅ PASS | ĐỦ ĐIỀU KIỆN THU ÂM TTS (100% 7 GATES PASSED) |

### Bảng Thống Kê Chi Tiết Từng File Kịch Bản:
| Tên File | Dung Lượng Ký Tự (Chars) | Số Từ (Words) | Trạng Thái Gate 2 (<= 3000) |
| :--- | :---: | :---: | :---: |
| `Kich-ban-1.txt` | 2321 | 523 | ✅ PASS |
| `Kich-ban-2.txt` | 2174 | 488 | ✅ PASS |
| `Kich-ban-3.txt` | 2202 | 486 | ✅ PASS |
| `Kich-ban-4.txt` | 2189 | 483 | ✅ PASS |
| `Kich-ban-5.txt` | 2139 | 470 | ✅ PASS |
| `Kich-ban-6.txt` | 2162 | 475 | ✅ PASS |
| `Kich-ban-7.txt` | 2019 | 446 | ✅ PASS |
| `Kich-ban-8.txt` | 2192 | 489 | ✅ PASS |
| `Kich-ban-9.txt` | 2179 | 478 | ✅ PASS |
| `Kich-ban-10.txt` | 2141 | 471 | ✅ PASS |
| `Kich-ban-11.txt` | 2153 | 466 | ✅ PASS |
| `Kich-ban-12.txt` | 2199 | 491 | ✅ PASS |
| `Kich-ban-13.txt` | 1637 | 350 | ✅ PASS |

---
*Báo cáo được khởi tạo tự động bởi Audiobook QC Auditor Engine (Step 07)*
