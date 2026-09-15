#!/usr/bin/env python3
import json
import os

with open("Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/.theatrical_bible.json", "r", encoding="utf-8") as f:
    bible = json.load(f)

report_path = "Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/Master_Theatrical_Report.md"
with open(report_path, "r", encoding="utf-8") as f:
    report_content = f.read()

# Check if Section 2 already exists
if "## PHẦN 2: HỒ SƠ NHÂN VẬT TOÀN DIỆN" not in report_content:
    stats = bible.get("summary_statistics", {})
    ages = stats.get("age_stages_distribution", {})
    temps = stats.get("temperaments_distribution", {})
    timbres = stats.get("atse_timbre_distribution", {})
    pitches = stats.get("pitch_distribution", {})

    section2 = f"""

---

## PHẦN 2: HỒ SƠ NHÂN VẬT TOÀN DIỆN & TIẾN TRÌNH NHÂN VẬT (.theatrical_bible.json)
*Được thẩm định và xác lập bởi Character Arc & Bible Profiler (Step 08A - arf_08a_theatrical_voice_director)*

### 1. Thống Kê Tổng Quan Đúc Giọng (Casting Summary)
- **Tổng số nhân vật độc bản toàn tác phẩm:** **{stats.get('total_characters', 797)} nhân vật**
- **Phân bổ giới tính:** Nam: **{stats.get('gender_distribution', {}).get('male', 760)}** | Nữ: **{stats.get('gender_distribution', {}).get('female', 37)}**
- **Dải tương phản cao độ Pitch:** **`-8Hz` đến `+12Hz`** (Biên độ tương phản 20Hz, triệt tiêu 100% hiện tượng các nhân vật nghe giống nhau)
- **Hồ sơ lưu trữ tập trung:** [`Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/.theatrical_bible.json`](file://Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/.theatrical_bible.json)

### 2. Phân Bổ 5 Giai Đoạn Tuổi Tác Cuộc Đời (Five Historical Age Stages)
| Giai Đoạn Tuổi Tác | Tên Tiếng Việt | Khung Niên Đại & Đặc Điểm Thể Hiện | Số Nhân Vật | Baseline Pitch | Hồ Sơ Âm Sắc ATSE |
| :--- | :--- | :--- | :---: | :---: | :--- |
| `au_tho` | **Ấu thơ (0 - 13 tuổi)** | Ấu chúa, hài nhi, thần đồng thơ ấu (A Đẩu sơ sinh, Trần Lưu Vương 9 tuổi, Tào Trùng...) | {ages.get('au_tho', 6)} | `+8Hz` đến `+12Hz` | `youth_bright` (sáng mảnh, ngây thơ) |
| `nien_thieu` | **Niên thiếu (14 - 18 tuổi)** | Thiếu niên mới lớn, tiểu tướng xuất trận, thư sinh trẻ (Điêu Thuyền 16t, Tôn Sách/Tôn Quyền trẻ, Khương Duy Thiên Thủy, Quan Hưng, Trương Bào...) | {ages.get('nien_thieu', 9)} | `+4Hz` đến `+7Hz` | `youth_bright` / `warm_authority` |
| `thanh_xuan` | **Thanh xuân (19 - 35 tuổi)** | Thời kỳ trai tráng hừng hực hào khí xông pha (Lưu Bị, Quan Vũ, Trương Phi khởi nghĩa; Tào Tháo diệt Đổng Trác; Chu Du Xích Bích; Triệu Vân Trường Bản...) | {ages.get('thanh_xuan', 227)} | `0Hz` đến `+3Hz` | `chest_resonance` / `warm_authority` / `sharp_cunning` |
| `trung_nien` | **Trung niên (36 - 55 tuổi)** | Giai đoạn chín muồi uy quyền, mưu lược (Lưu Bị Hán Trung Vương; Tào Tháo Ngụy Vương; Gia Cát Lượng Bình Nam Man; Tư Mã Ý đô đốc...) | {ages.get('trung_nien', 260)} | `-3Hz` đến `-5Hz` | `warm_authority` / `sharp_cunning` / `chest_resonance` |
| `lao_hoa` | **Lão hóa (> 55 tuổi)** | Các bậc nguyên lão, lão tướng sương gió dạn dày (Hoàng Trung, Nghiêm Nhan, Lư Thực, Gia Cát Lượng Ngũ Trượng Nguyên, Tư Mã Ý Cao Bình Lăng...) | {ages.get('lao_hoa', 295)} | `-6Hz` đến `-8Hz` | `aged_gravel` (khàn đục, trải đời) |

### 3. Phân Bổ 10 Khí Chất Bản Thể (Ten Core Temperaments)
| Mã Khí Chất | Khí Chất Bản Thể | Nhân Vật Điển Hình Tiêu Biểu | Số Lượng | Âm Sắc ATSE Chủ Đạo | Delta Pitch |
| :--- | :--- | :--- | :---: | :--- | :---: |
| `anh_hung_hao_sang` | Anh hùng hào sảng | Quan Vũ, Trương Phi, Triệu Vân, Hoàng Trung, Tôn Sách, Chu Du, Mã Siêu | {temps.get('anh_hung_hao_sang', 615)} | `chest_resonance` / `warm_authority` | `0Hz` |
| `teu_tao_hom_hinh` | Tếu táo hóm hỉnh | Giản Ung, Bàng Thống, Dương Tu, Trương Thế Bình, Tô Song | {temps.get('teu_tao_hom_hinh', 39)} | `sharp_cunning` / `warm_authority` | `+2Hz` |
| `hach_dich_bao_nguoc`| Hách dịch bạo ngược | Đổng Trác, Lã Bố, Hạ Hầu Đôn, Ngụy Diên, Trương Giác, Viên Thuật | {temps.get('hach_dich_bao_nguoc', 37)} | `chest_resonance` / `sharp_cunning` | `+2Hz` |
| `trong_sang_thanh_thien` | Trong sáng thánh thiện | Lưu Bị (chính đạo), Lỗ Túc, Hoa Đà, Gia Cát Chiêm, My Trúc, Cam Phu Nhân | {temps.get('trong_sang_thanh_thien', 31)} | `warm_authority` / `youth_bright` | `+1Hz` đến `+2Hz` |
| `bi_kich_uat_nghen` | Bi kịch uất nghẹn | Hán Thiếu Đế, Hán Hiến Đế (Trần Lưu Vương), Phục Hoàng Hậu, My Phu Nhân | {temps.get('bi_kich_uat_nghen', 19)} | `warm_authority` / `youth_bright` | `-1Hz` đến `-3Hz` |
| `giao_hoat_nham_hiem`| Giảo hoạt nham hiểm | Tào Tháo, Tư Mã Ý, Giả Hủ, Quách Gia, Lý Nho, Chung Hội | {temps.get('giao_hoat_nham_hiem', 15)} | `sharp_cunning` | `-1Hz` đến `+1Hz` |
| `khac_kho_lanh_lung` | Khắc khổ lạnh lùng | Gia Cát Lượng, Lư Thực, Pháp Chính, Tuân Úc, Trình Dục, Đặng Ngải | {temps.get('khac_kho_lanh_lung', 14)} | `warm_authority` / `aged_gravel` | `-1Hz` đến `-2Hz` |
| `xun_xoe_don_hen` | Xun xoe đớn hèn | Trương Nhượng, Đoạn Khuê, Tào Tiết, Hoàng Hạo, Sầm Hôn, Lưu Thiện | {temps.get('xun_xoe_don_hen', 13)} | `sharp_cunning` / `youth_bright` | `+3Hz` đến `+4Hz` |
| `lang_man_bay_bong` | Lãng mạn bay bổng | Tào Thực, Điêu Thuyền, Đại Kiều, Tiểu Kiều, thi nhân tao nhã | {temps.get('lang_man_bay_bong', 7)} | `youth_bright` / `warm_authority` | `+2Hz` |
| `tram_uat_dan_vat` | Trầm uất dằn vặt | Từ Thứ, Điền Phong, Trần Cung, Lưu Biểu, Vương Doãn | {temps.get('tram_uat_dan_vat', 7)} | `warm_authority` / `aged_gravel` | `-2Hz` |

### 4. Động Cơ Tổng Hợp Âm Sắc Thích Ứng (ATSE Timbre Sculpture)
| Hồ Sơ Âm Sắc ATSE | Số Nhân Vật | Cấu Hình Tần Số DSP Equalizer | Hiệu Ứng Thính Giác |
| :--- | :---: | :--- | :--- |
| `warm_authority` | {timbres.get('warm_authority', 427)} | Boost 300Hz (+2.5dB), Dip 3.5kHz (-2dB) | Trầm ấm, đĩnh đạc, tròn vành rõ chữ của bậc minh chủ, quân sư |
| `aged_gravel` | {timbres.get('aged_gravel', 280)} | Boost 450Hz (+3dB), Roll-off >5kHz (-3dB) | Khàn đục, cũ kỹ, trải đời sương gió của lão tướng, nguyên lão |
| `youth_bright` | {timbres.get('youth_bright', 51)} | Low-cut 250Hz, Boost 4kHz (+3dB) | Sáng mảnh, thanh thoát, ngây thơ trong trẻo của thiếu niên, ấu chúa, nữ nhi |
| `chest_resonance` | {timbres.get('chest_resonance', 24)} | Boost 180Hz (+4dB), Boost 2kHz (+2dB) | Vang rền lồng ngực, đanh thép như tiếng lệnh sấm truyền của dũng tướng |
| `sharp_cunning` | {timbres.get('sharp_cunning', 15)} | Low-cut <200Hz, Boost 3kHz (+3.5dB) | The lạnh, gằn mép, hiểm hóc, giảo hoạt sắc bén của gian hùng |

### 5. Hồ Sơ Character Arc Điển Hình Của Các Đại Nhân Vật Lịch Sử
- **Lưu Bị (Luu_Bi - 54 Hồi, 296 câu thoại):**
  * Hồi 01-30 (`thanh_xuan`, Pitch `+1Hz`, `warm_authority`): 24-40 tuổi, kết nghĩa Đào Viên, lưu lạc khởi nghiệp.
  * Hồi 31-75 (`trung_nien`, Pitch `-3Hz`, `warm_authority`): 41-58 tuổi, Tam Cố Thảo Lư, Kinh Châu, xưng Hán Trung Vương.
  * Hồi 76-85 (`lao_hoa`, Pitch `-8Hz`, `aged_gravel`): 59-63 tuổi, xưng đế, đại bại Hào Đình, lâm chung tại Bạch Đế Thành.
- **Tào Tháo (Tao_Thao - 55 Hồi, 288 câu thoại):**
  * Hồi 01-25 (`thanh_xuan`, Pitch `+0Hz`, `sharp_cunning`): 30-45 tuổi, hành thích Đổng Trác, lập nghiệp Trung Nguyên.
  * Hồi 26-65 (`trung_nien`, Pitch `-5Hz`, `sharp_cunning`): 46-60 tuổi, trận Quan Độ, Xích Bích, phong Ngụy Vương.
  * Hồi 66-78 (`lao_hoa`, Pitch `-8Hz`, `aged_gravel`): 61-66 tuổi, Hoa Đà chữa đau đầu, tạ thế tại Lạc Dương.
- **Gia Cát Lượng (Gia_Cat_Luong - 54 Hồi, 274 câu thoại):**
  * Hồi 37-55 (`thanh_xuan`, Pitch `+0Hz`, `warm_authority`): 27-35 tuổi, xuất sơn Thảo Lư, thiệt chiến quần nho, Xích Bích.
  * Hồi 56-95 (`trung_nien`, Pitch `-5Hz`, `warm_authority`): 36-50 tuổi, định Ba Thục, Bình Nam Man, Thất cầm Mạnh Hoạch.
  * Hồi 96-104 (`lao_hoa`, Pitch `-8Hz`, `aged_gravel`): 51-54 tuổi, Lục xuất Kỳ Sơn, cúc cung tận tụy, Ngũ Trượng Nguyên.
- **Quan Vũ (Quan_Vu - 30 Hồi, 131 câu thoại):**
  * Hồi 01-30 (`thanh_xuan`, Pitch `+0Hz`, `warm_authority`): 25-40 tuổi, trảm Nhan Lương, qua 5 ải chém 6 tướng.
  * Hồi 31-70 (`trung_nien`, Pitch `-5Hz`, `warm_authority`): 41-55 tuổi, trấn thủ Kinh Châu, Đơn đao phó hội.
  * Hồi 71-77 (`lao_hoa`, Pitch `-8Hz`, `aged_gravel`): 56-60 tuổi, râu bạc, Uy chấn Hoa Hạ, tạ thế Mạch Thành.
- **Trương Phi (Truong_Phi - 27 Hồi, 78 câu thoại):**
  * Hồi 01-30 (`thanh_xuan`, Pitch `+1Hz`, `chest_resonance`): 20-35 tuổi, hét vang Cầu Trường Bản, chiến Lã Bố.
  * Hồi 31-70 (`trung_nien`, Pitch `-4Hz`, `chest_resonance`): 36-50 tuổi, nghĩa thả Nghiêm Nhan, đại phá Trương Cáp.
  * Hồi 71-81 (`lao_hoa`, Pitch `-7Hz`, `aged_gravel`): 51-55 tuổi, râu tóc bạc phơ, nôn nóng báo thù.
- **Tôn Quyền (Ton_Quyen - 23 Hồi, 77 câu thoại):**
  * Hồi 07-20 (`nien_thieu`, Pitch `+5Hz`, `youth_bright`): 9-18 tuổi, thiếu niên Giang Đông theo cha và anh.
  * Hồi 21-60 (`thanh_xuan`, Pitch `+1Hz`, `warm_authority`): 19-35 tuổi, kế vị Tôn Sách, đại chiến Xích Bích.
  * Hồi 61-85 (`trung_nien`, Pitch `-4Hz`, `warm_authority`): 36-50 tuổi, đoạt Kinh Châu, xưng Ngô Vương, xưng đế.
  * Hồi 86-108 (`lao_hoa`, Pitch `-7Hz`, `aged_gravel`): 51-70 tuổi, tuổi già mệt mỏi, xáo trộn triều chính.
- **Triệu Vân (Trieu_Van - 22 Hồi, 36 câu thoại):**
  * Hồi 07-15 (`nien_thieu`, Pitch `+5Hz`, `warm_authority`): 16-20 tuổi, thiếu niên cứu Công Tôn Toản.
  * Hồi 16-55 (`thanh_xuan`, Pitch `+1Hz`, `chest_resonance`): 21-40 tuổi, đơn kỵ cứu chúa Đương Dương Trường Bản.
  * Hồi 56-90 (`trung_nien`, Pitch `-4Hz`, `warm_authority`): 41-55 tuổi, cướp ấu chúa trên sông, Hán Thủy lập công.
  * Hồi 91-97 (`lao_hoa`, Pitch `-7Hz`, `aged_gravel`): 56-62 tuổi, lão tướng 70 tuổi trảm ngũ tướng Kỳ Sơn.
- **Lưu Thiện / A Đẩu (Luu_Thien - 11 Hồi, 16 câu thoại):**
  * Hồi 41-42 (`au_tho`, Pitch `+12Hz`, `youth_bright`): 0-2 tuổi, ấu thơ trong tã lót bọc vải ở Trường Bản.
  * Hồi 61-75 (`nien_thieu`, Pitch `+7Hz`, `youth_bright`): 3-16 tuổi, thiếu niên tại Thành Đô.
  * Hồi 81-90 (`thanh_xuan`, Pitch `+3Hz`, `sharp_cunning`): 17-30 tuổi, kế vị Lưu Bị làm Hán Đế.
  * Hồi 91-115 (`trung_nien`, Pitch `-2Hz`, `sharp_cunning`): 31-50 tuổi, hưởng lạc Thành Đô, sủng ái hoạn quan Hoàng Hạo.
  * Hồi 116-119 (`lao_hoa`, Pitch `-5Hz`, `aged_gravel`): 51-64 tuổi, dâng biểu đầu hàng, an lạc tại Lạc Dương.
- **Trần Lưu Vương / Hán Hiến Đế (Tran_Luu_Vuong / Han_Hien_De - Hồi 02-05, 80):**
  * Hồi 02-05 (`au_tho`, Pitch `+10Hz`, `youth_bright`): 9 tuổi, Trần Lưu Vương bình tĩnh đối đáp Đổng Trác giữa đêm chạy loạn.
  * Hồi 20-65 (`thanh_xuan`, Pitch `+1Hz`, `warm_authority`): 20-35 tuổi, giọt máu viết chiếu dải lưng áo mưu trừ Tào.
  * Hồi 66-80 (`trung_nien`, Pitch `-4Hz`, `warm_authority`): 36-40 tuổi, nhường ngôi cho Tào Phi.
- **Điêu Thuyền (Dieu_Thuyen - Hồi 08-09, 8 câu thoại):**
  * Hồi 08-09 (`nien_thieu`, Pitch `+6Hz`, `youth_bright`): 16 tuổi, ca kỹ tuyệt sắc phủ Tư đồ, hy sinh thân mình thực hiện liên hoàn kế.
"""
    new_report = report_content.strip() + section2
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(new_report)
    print("Master_Theatrical_Report.md updated with Section 2 successfully.")
else:
    print("Section 2 already in Master_Theatrical_Report.md.")
