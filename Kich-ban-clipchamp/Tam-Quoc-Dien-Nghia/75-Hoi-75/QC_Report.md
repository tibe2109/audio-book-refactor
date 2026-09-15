# Báo Cáo Kiểm Toán Chất Lượng (QC Audit Report) — 75-Hoi-75
**Trạng Thái Thẩm Định:** ✅ PASSED (100% 7 GATES PASSED)
**Thời Điểm Kiểm Toán:** `2026-09-15T04:10:28.922497+00:00`

| Gate | Tiêu Chí Kiểm Toán | Kết Quả | Chi Tiết Đối Soát |
| :--- | :--- | :---: | :--- |
| **Gate 1: Tên Thư Mục Chuẩn** | Tên Thư Mục Chuẩn | ✅ PASS | Thư mục: '75-Hoi-75' |
| **Gate 2: Dung Lượng Chunk <= 3000 ký tự** | Dung Lượng Chunk <= 3000 ký tự | ✅ PASS | 8 chunks đạt chuẩn (Min: 1173, Max: 2284, Avg: 2053 ký tự) |
| **Gate 3: Khử Sạch Ký Tự Cấm TTS** | Khử Sạch Ký Tự Cấm TTS | ✅ PASS | 100% Sạch ký tự cấm |
| **Gate 4: Viết Chữ Số Toàn Diện (Zero-digit)** | Viết Chữ Số Toàn Diện (Zero-digit) | ✅ PASS | 100% Viết chữ tự nhiên (0 chữ số thô) |
| **Gate 5: Định Dạng Nhịp Thở (. ......)** | Định Dạng Nhịp Thở (. ......) | ✅ PASS | Đạt chuẩn (5 markers ngắt nghỉ phát thanh) |
| **Gate 6: Word Count Delta (Chống Tóm Tắt)** | Word Count Delta (Chống Tóm Tắt) | ✅ PASS | Tham chiếu (normalized.txt): 3647 từ | Kịch bản: 3651 từ | Độ lệch: 0.11% (Ngưỡng $\le$ 5%) | Tỷ lệ dịch/gốc: 98.8% |
| **Gate 7: Cấp Quyền Thu Âm TTS (Step 08 Clearance)** | Cấp Quyền Thu Âm TTS (Step 08 Clearance) | ✅ PASS | ĐỦ ĐIỀU KIỆN THU ÂM TTS (100% 7 GATES PASSED) |

### Bảng Thống Kê Chi Tiết Từng File Kịch Bản:
| Tên File | Dung Lượng Ký Tự (Chars) | Số Từ (Words) | Trạng Thái Gate 2 (<= 3000) |
| :--- | :---: | :---: | :---: |
| `Kich-ban-1.txt` | 2284 | 502 | ✅ PASS |
| `Kich-ban-2.txt` | 2153 | 475 | ✅ PASS |
| `Kich-ban-3.txt` | 2123 | 472 | ✅ PASS |
| `Kich-ban-4.txt` | 2169 | 489 | ✅ PASS |
| `Kich-ban-5.txt` | 2189 | 486 | ✅ PASS |
| `Kich-ban-6.txt` | 2210 | 487 | ✅ PASS |
| `Kich-ban-7.txt` | 2128 | 480 | ✅ PASS |
| `Kich-ban-8.txt` | 1173 | 260 | ✅ PASS |

---
*Báo cáo được khởi tạo tự động bởi Audiobook QC Auditor Engine (Step 07)*
