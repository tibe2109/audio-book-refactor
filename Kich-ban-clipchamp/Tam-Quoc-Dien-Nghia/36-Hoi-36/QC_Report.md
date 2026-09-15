# Báo Cáo Kiểm Toán Chất Lượng (QC Audit Report) — 36-Hoi-36
**Trạng Thái Thẩm Định:** ✅ PASSED (100% 7 GATES PASSED)
**Thời Điểm Kiểm Toán:** `2026-09-15T04:10:25.347667+00:00`

| Gate | Tiêu Chí Kiểm Toán | Kết Quả | Chi Tiết Đối Soát |
| :--- | :--- | :---: | :--- |
| **Gate 1: Tên Thư Mục Chuẩn** | Tên Thư Mục Chuẩn | ✅ PASS | Thư mục: '36-Hoi-36' |
| **Gate 2: Dung Lượng Chunk <= 3000 ký tự** | Dung Lượng Chunk <= 3000 ký tự | ✅ PASS | 8 chunks đạt chuẩn (Min: 1460, Max: 2330, Avg: 2089 ký tự) |
| **Gate 3: Khử Sạch Ký Tự Cấm TTS** | Khử Sạch Ký Tự Cấm TTS | ✅ PASS | 100% Sạch ký tự cấm |
| **Gate 4: Viết Chữ Số Toàn Diện (Zero-digit)** | Viết Chữ Số Toàn Diện (Zero-digit) | ✅ PASS | 100% Viết chữ tự nhiên (0 chữ số thô) |
| **Gate 5: Định Dạng Nhịp Thở (. ......)** | Định Dạng Nhịp Thở (. ......) | ✅ PASS | Đạt chuẩn (5 markers ngắt nghỉ phát thanh) |
| **Gate 6: Word Count Delta (Chống Tóm Tắt)** | Word Count Delta (Chống Tóm Tắt) | ✅ PASS | Tham chiếu (normalized.txt): 3724 từ | Kịch bản: 3724 từ | Độ lệch: 0.00% (Ngưỡng $\le$ 5%) | Tỷ lệ dịch/gốc: 98.5% |
| **Gate 7: Cấp Quyền Thu Âm TTS (Step 08 Clearance)** | Cấp Quyền Thu Âm TTS (Step 08 Clearance) | ✅ PASS | ĐỦ ĐIỀU KIỆN THU ÂM TTS (100% 7 GATES PASSED) |

### Bảng Thống Kê Chi Tiết Từng File Kịch Bản:
| Tên File | Dung Lượng Ký Tự (Chars) | Số Từ (Words) | Trạng Thái Gate 2 (<= 3000) |
| :--- | :---: | :---: | :---: |
| `Kich-ban-1.txt` | 2330 | 509 | ✅ PASS |
| `Kich-ban-2.txt` | 2191 | 481 | ✅ PASS |
| `Kich-ban-3.txt` | 2112 | 479 | ✅ PASS |
| `Kich-ban-4.txt` | 2133 | 483 | ✅ PASS |
| `Kich-ban-5.txt` | 2154 | 491 | ✅ PASS |
| `Kich-ban-6.txt` | 2209 | 491 | ✅ PASS |
| `Kich-ban-7.txt` | 2129 | 469 | ✅ PASS |
| `Kich-ban-8.txt` | 1460 | 321 | ✅ PASS |

---
*Báo cáo được khởi tạo tự động bởi Audiobook QC Auditor Engine (Step 07)*
