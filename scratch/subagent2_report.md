# 🎭 BÁO CÁO HỒ SƠ NHÂN VẬT & THEATRICAL BIBLE HỒI 3 — TAM QUỐC DIỄN NGHĨA

**Kính gửi:** Hội đồng Đạo diễn Kịch nghệ / Parent Agent  
**Người thực hiện:** Character Arc & Bible Profiler (`arf_08a_theatrical_voice_director`)  
**Tác phẩm:** Tam Quốc Diễn Nghĩa — **Hồi 03:** *Tiệc Ôn Minh, Đổng Trác mắng Đinh Nguyên; Dùng vàng bạc, Lý Túc dụ Lã Bố*  
**Tệp xuất bản:** `/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/03-Hoi-03/.theatrical_bible.json`

---

## 1. TỔNG QUAN HỆ THỐNG & ĐẶC TẢ ÂM HỌC (ACOUSTIC SPECIFICATION)
Đã thiết lập cấu trúc hoàn chỉnh cho `.theatrical_bible.json` tuân thủ nghiêm ngặt **ARF Rules v2.5** và chuẩn kỹ thuật **arf_08a_theatrical_voice_director**:

1. **Dải tương phản Pitch mở rộng (Deep Persona Polarizer):**
   - Giới hạn: `-8Hz` đến `+12Hz` (biên độ tương phản 20Hz).
   - Điểm cực thấp: Lư Thực (`-7Hz`), Sái Ung (`-6Hz`), Đổng Trác (`-4Hz`), Thôi Nghị (`-4Hz`).
   - Điểm cực cao: Trần Lưu Vương (`+9Hz`), Trương Nhượng (`+6Hz` ~ `+8Hz`), Thiếu Đế (`+5Hz`), Đoàn Khuê (`+5Hz`).
   - Phân tầng rõ rệt, triệt tiêu hoàn toàn hiện tượng "nghe như một người đọc".

2. **Thang tốc độ (Rate Scale):**
   - Biến thiên từ `-20%` (ngâm vịnh thi ca cổ, lão tướng trăn trở) đến `+15%` (quát tháo xung trận, báo động binh biến).

3. **Ma trận Chuyển giao Âm học Thích ứng (Dynamic Context-Aware Handoff Matrix):**
   - `instant_interruption` (`0.30s - 0.35s`): Đấu khẩu nảy lửa, cướp lời, quát tháo (Đổng Trác vs Đinh Nguyên, Viên Thiệu vs Đổng Trác, Lã Bố vs Đinh Nguyên).
   - `urgent_lead_in` (`0.35s - 0.40s`): Dẫn nhập thúc giục sang quân lệnh, hò reo, truy đuổi xa giá đêm tối.
   - `natural_dialogue_turn` (`0.42s - 0.50s`): Đối đáp thường nhật, đàm đạo thế sự giữa bạn bè cũ (Lý Túc vs Lã Bố).
   - `dialogue_resonance` (`0.50s - 0.60s`): Ngân rung sau câu thoại chấn động trước khi lời dẫn tiếp tục.
   - `pensive_lead_in` (`0.60s - 0.75s`): Trầm ngâm buông tiếng, thở dài sầu muộn, giãi bày tâm sự bất đắc dĩ.
   - `regal_ceremony` (`0.70s - 0.85s`): Trang nghiêm triều đình, đối đáp thiên tử, tuyên cáo chỉ dụ hoàng gia.
   - `dramatic_silence` (`0.85s - 1.20s`): Chết lặng kịch tính sau lời đe dọa sinh tử hoặc chân lý thế sự rúng động.
   - `poetic_cushion` (`0.85s - 1.80s`): Đệm thở thi ca 3 tầng (0.85s dẫn thơ -> 0.85s liên câu -> 1.50s - 1.80s `. ......` coda).

4. **Khung Dẫn Chuyện Đa Sắc Thái (Adaptive Expressive Narrator Modes):**
   - `epic_narrator`: Hào hùng chiến trận (`pitch: +1Hz`, `rate: +0%`, `lead_in_pause: 0.28s - 0.35s`).
   - `elegiac_narrator`: Bi tráng xót thương (`pitch: -2Hz`, `rate: -10%`, `lead_in_pause: 0.55s - 0.65s`).
   - `contemplative_narrator`: Chiêm nghiệm hoài cổ (`pitch: -2Hz`, `rate: -12%`, `lead_in_pause: 0.60s - 0.75s`).
   - `suspense_narrator`: Hồi hộp rình rập (`pitch: +0Hz`, `rate: -8%`, `lead_in_pause: 0.40s - 0.48s`).
   - `intimate_narrator`: Bình nhật tự nhiên (`pitch: +0Hz`, `rate: -5%`, `lead_in_pause: 0.35s - 0.40s`).
   - `poetic_recitation`: Ngâm vịnh thi ca (`pitch: -2Hz`, `rate: -18%`, `lead_in_pause: 0.85s`).

---

## 2. HỒ SƠ ĐỒNG BỘ 23 NHÂN VẬT & FORMANT DSP PRESETS (ATSE)

| Nhân Vật | Tuổi Tác | Khí Chất Bản Thể | Pitch | Rate | ATSE Formant DSP | Đặc Trưng Âm Học & Khẩu Khí |
| :--- | :--- | :--- | :---: | :---: | :--- | :--- |
| **Đổng Trác** | Trung niên | Hách dịch bạo ngược | `-4Hz` | `-2%` | `tyrant_arrogant` | Ồm ồm gầm gừ, đanh thép, bạo ngược, áp chế kẻ đối thoại. |
| **Lã Bố** | Thanh xuân | Anh hùng hào sảng | `+2Hz` | `+4%` | `chest_resonance` | Vang lồng ngực sang sảng, kiêu dũng, bồng bột tham lợi, hung tàn. |
| **Đinh Nguyên** | Trung niên | Anh hùng hào sảng | `-3Hz` | `-4%` | `chest_resonance` | Trầm ấm, cương trực, khẩu khí lão tướng sa trường trung liệt. |
| **Viên Thiệu** | Thanh xuân | Hách dịch bạo ngược | `+1Hz` | `+2%` | `chest_resonance` | Kiêu hãnh, tự phụ hào môn vọng tộc, tuốt gươm đanh thép đối kháng. |
| **Hà Tiến** | Trung niên | Hách dịch bạo ngược | `-2Hz` | `+2%` | `chest_resonance` | Ồm ồm thô lỗ, tự phụ, gắt gỏng, mù quáng bỏ ngoài tai lời can. |
| **Vương Doãn** | Trung niên | Khắc khổ lạnh lùng | `-3Hz` | `-6%` | `warm_authority` | Trầm tĩnh, hòa hoãn, cân nhắc từng lời, đại thần lão luyện. |
| **Lư Thực** | Lão hóa | Anh hùng hào sảng | `-7Hz` | `-14%` | `warm_authority` | Giọng già trầm đục, trang nghiêm, cương nghị danh nho, mắng thẳng bạo chúa. |
| **Thôi Nghị** | Lão hóa | Trong sáng thánh thiện | `-4Hz` | `-8%` | `warm_authority` | Ấm áp, từ tốn, nhân hậu chất phác của bậc ẩn sĩ hiền lương. |
| **Mẫn Cống** | Thanh xuân | Anh hùng hào sảng | `-1Hz` | `-2%` | `warm_authority` | Khỏe khoắn, đĩnh đạc, nghĩa sĩ dũng cảm hộ giá ấu chúa. |
| **Trần Lâm** | Thanh xuân | Trong sáng thánh thiện | `+1Hz` | `-2%` | `warm_authority` | Thanh thoát, chuẩn mực, khẩn trương lo lắng cho đại cục. |
| **Trịnh Thái** | Trung niên | Khắc khổ lạnh lùng | `-2Hz` | `-4%` | `warm_authority` | Sắc lạnh, cương quyết, cảnh báo nguy cơ sài lang Đổng Trác. |
| **Bào Tín** | Thanh xuân | Anh hùng hào sảng | `+0Hz` | `+0%` | `warm_authority` | Dứt khoát, mưu lược, quyết đoán đề xuất trừ gian diệt bạo. |
| **Bành Bá** | Trung niên | Khắc khổ lạnh lùng | `-3Hz` | `-4%` | `warm_authority` | Điềm đạm, trang trọng, mềm dẻo can gián cứu danh sĩ. |
| **Lý Nho** | Thanh xuân | Giảo hoạt nham hiểm | `+1Hz` | `-4%` | `sharp_cunning` | The lạnh, sắc nhọn, nói chậm rãi rào đón, mưu mô thâm độc. |
| **Tào Tháo** | Thanh xuân | Giảo hoạt nham hiểm | `+0Hz` | `+0%` | `sharp_cunning` | Sắc sảo, dứt khoát, pha chút châm biếm tự tin của kiêu hùng. |
| **Lý Túc** | Thanh xuân | Giảo hoạt nham hiểm | `+2Hz` | `+4%` | `sharp_cunning` | Ngọt ngào, đon đả, linh hoạt khích tướng, ba tấc lưỡi dụ hàng. |
| **Trương Nhượng**| Trung niên | Xun xoe đớn hèn | `+6Hz` | `+6%` | `servile_flatterer` | The thé, mỏng dính, run rẩy nịnh hót rồi trở mặt độc địa. |
| **Đoàn Khuê** | Trung niên | Xun xoe đớn hèn | `+5Hz` | `+4%` | `servile_flatterer` | The thé hoảng loạn, lắp bắp đớn hèn van xin khi bị bắt. |
| **Trần Lưu Vương**| Ấu thơ | Trong sáng thánh thiện | `+9Hz` | `+4%` | `youth_bright` | Trẻ thơ trong trẻo, đĩnh đạc, khúc chiết, toát lên phong thái thiên tử. |
| **Thiếu Đế** | Thiếu niên | Bi kịch uất nghẹn | `+5Hz` | `+2%` | `youth_bright` | Non nớt, yếu đuối, run rẩy nghẹn ngào, nhu nhược bi kịch. |
| **Hà Thái Hậu** | Trung niên | Bi kịch uất nghẹn | `+2Hz` | `-2%` | `youth_bright` | Giọng nữ quý phái, u sầu, nhu nhược, ôm con than khóc (Hoài My). |
| **Sái Ung** | Lão hóa | Trầm uất dằn vặt | `-6Hz` | `-12%` | `aged_gravel` | Khàn đục, trầm lắng, nặng nỗi ưu tư thế sự và khí chất uyên bác. |
| **Narrator** | — | — | `+0Hz` | `-5%` | `intimate_narrator`| Tròn vành rõ chữ, dẫn dắt linh hoạt 6 narrative modes. |

---

## 3. TRẠNG THÁI FILE VÀ BÀN GIAO TIẾP THEO
- File `.theatrical_bible.json` đã được ghi đè và thẩm định cú pháp JSON 100% hợp lệ tại:  
  `/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/03-Hoi-03/.theatrical_bible.json`
- Sẵn sàng bàn giao cho các Sub-agents tiếp theo trong Hội đồng (`Dramatic Setting & Emotional Dynamics`, `Poetic Prosody & Narrator Director`, `Theatrical Dramaturg & Continuity QC`) để đối soát và tổng hợp kịch bản phân vai `theatrical_script.json`.