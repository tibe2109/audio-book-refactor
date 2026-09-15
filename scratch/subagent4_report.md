# BÁO CÁO THIẾT KẾ ĐẠO DIỄN DẪN CHUYỆN & ĐỘNG CƠ THI CA (HỒI 3 - TAM QUỐC DIỄN NGHĨA)
**Người gửi:** Poetic Prosody & Narrator Director (Hội đồng Đạo diễn Kịch nghệ Hồi 3)  
**Người nhận:** Parent Agent (`0f140d22-6976-48ef-af92-d9f37a8c4e48`)  
**Tác phẩm:** *Tam Quốc Diễn Nghĩa* — Hồi 3: *Tiệc Ôn Minh, Đổng Trác mắng Đinh Nguyên / Dùng vàng bạc, Lý Túc dụ Lã Bố*

---

## PHẦN I: KHUNG ĐIỀU BIẾN 8 SẮC THÁI DẪN CHUYỆN THÍCH ỨNG (ADAPTIVE EXPRESSIVE NARRATOR)

Thay vì gán cứng một sắc thái phẳng đơn điệu (`pitch: 0Hz`, `rate: -5%`), Người dẫn chuyện (Narrator) trong Hồi 3 được phân vai thành **Linh hồn dẫn dắt (The Narrative Soul)** với 8 sắc thái âm học thích ứng theo diễn biến kịch tính:

### 1. Bảng Thông Số Kỹ Thuật 8 Sắc Thái Dẫn Chuyện (Acoustic Parameters & ATSE DSP)
| Sắc Thái Dẫn Chuyện | Pitch | Rate | Lead-in Pause | Cấu Hình Formant DSP (ATSE) | Hiệu Ứng Thính Giác & Phân Cảnh Thích Ứng |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **`epic_narrator`** (Hào hùng / Xung trận) | `+1Hz ~ +2Hz` | `-2% ~ 0%` | `0.30s - 0.35s` | Boost $2.5\text{kHz} (+3\text{dB})$, Boost $200\text{Hz} (+2\text{dB})$ | Đanh thép, dồn dập, khí thế ngút trời. Viên Thiệu công thành, Đinh Nguyên đối trận, binh mã Tây Lương rợp đất. |
| **`suspense_narrator`** (Hồi hộp / Rình rập) | `0Hz ~ +1Hz` | `-8% ~ -10%` | `0.40s - 0.48s` | High-pass $150\text{Hz}$, Boost $3.5\text{kHz} (+3\text{dB})$ | Hạ giọng thì thào vi mô, ngắt nhịp sắc sảo rình rập. Hà Tiến vào bẫy, trốn chạy Bắc Mang, Lã Bố ám sát Đinh Nguyên. |
| **`elegiac_narrator`** (Bi tráng / Xót thương) | `-2Hz ~ -3Hz` | `-10% ~ -12%` | `0.55s - 0.65s` | Boost $400\text{Hz} (+2.5\text{dB})$, Dip $3\text{kHz} (-2\text{dB})$ | Chùng lắng, nghẹn ngào, xót xa. Hai vị ấu chúa đói rét ôm nhau khóc trong bụi rậm, vua tôi nhìn nhau rơi lệ. |
| **`contemplative_narrator`** (Hoài cổ / Triết lý) | `-2Hz` | `-12% ~ -15%` | `0.60s - 0.75s` | Boost $250\text{Hz} (+3\text{dB})$, Low-pass $6\text{kHz}$ | Trầm ấm, đĩnh đạc, mênh mang như tiếng chuông đồng. Mở đầu hồi, thế sự hưng vong, Thôi Nghị ẩn cư, kết hồi. |
| **`intimate_narrator`** (Bình nhật / Chuyển tiếp) | `0Hz` | `-5%` | `0.35s - 0.40s` | Flat Studio EQ cân bằng phát thanh | Khách quan, mềm mại, làm nền chuyển giao êm ái giữa các tuyến truyện và đối thoại. |
| **`melancholic_social`** (Lầm than / Đe dọa) | `-3Hz` | `-12%` | `0.55s - 0.65s` | Boost $350\text{Hz} (+3\text{dB})$, Dip $2.5\text{kHz} (-2.5\text{dB})$ | Nặng nề, đè nén. Đổng Trác kéo thiết giáp nghênh ngang thị uy phố phường Lạc Dương, lê dân kinh hoàng. |
| **`satirical_ironic`** (Mỉa mai / Trào phúng) | `+2Hz` | `-6%` | `0.35s - 0.42s` | High-pass $180\text{Hz}$, Boost $2.8\text{kHz} (+3\text{dB})$, Boost $5\text{kHz} (+2\text{dB})$ | Chua cay, châm biếm thói phản phúc tráo trở. Lã Bố chém cha nuôi Đinh Nguyên rồi quỳ lạy nhận giặc làm cha. |
| **`existential_interior`** (Tâm lý / Giằng xé) | `-2Hz` | `-10%` | `0.50s - 0.60s` | Boost $200\text{Hz} (+3\text{dB})$, Dip $4\text{kHz} (-3\text{dB})$ | Sâu thẳm, tiếng dội vọng tâm thức. Lã Bố hổ thẹn khi Lý Túc vạch trần thân phận làm con nuôi, lòng tham trỗi dậy. |

---

### 2. Phân Cảnh & Phân Bổ Sắc Thái Dẫn Chuyện Chi Tiết Qua 10 Chunks Của Hồi 3

| Chunk | Nội Dung Sự Kiện Trọng Tâm | Sắc Thái Dẫn Chuyện Chủ Đạo | Dẫn Giải Chi Tiết Cảm Xúc & Nhịp Điệu |
| :---: | :--- | :--- | :--- |
| **Chunk 1** | Tiêu đề hồi; Tào Tháo, Lư Thực can ngăn Hà Tiến; Đổng Trác dâng biểu dã tâm. | `contemplative_narrator` $\to$ `intimate_narrator` | Khởi đầu đĩnh đạc, chiêm nghiệm sự mục ruỗng triều chính và ván cờ chính trị hiểm độc. |
| **Chunk 2** | Hà Tiến mù quáng vào cung; Trương Nhượng giăng 50 đao phủ mai phục; Thiệu, Tháo đứng ngoài. | `suspense_narrator` $\to$ `intimate_narrator` | Âm mưu cung đình đen tối, không khí ngột ngạt nghẹt thở trước cơn giông bão. |
| **Chunk 3** | Hà Tiến bị chém làm đôi; Thơ than Hà Tiến; Viên Thiệu phóng hỏa đốt thành chém sạch hoạn quan. | `suspense` $\to$ `poem` $\to$ **`epic_narrator`** | Chuyển từ rùng rợn cung cấm sang **hào hùng chiến trận ngút trời**, đại binh công thành, kiếm đao loang loáng, lửa cháy đỏ rực. |
| **Chunk 4** | Hoạn quan ép ấu chúa chạy trốn núi Bắc Mang; nấp bụi cỏ canh tư đói rét; đom đóm dẫn đường. | `suspense_narrator` $\to$ **`elegiac_narrator`** $\to$ `contemplative_narrator` | Điểm rơi cảm xúc sâu sắc nhất: **`elegiac_narrator`** bi tráng, xót xa khi hai vị hoàng đế thơ dại ôm nhau khóc thầm trong sương lạnh giá. |
| **Chunk 5** | Đồng dao Lạc Dương sấm truyền; Đổng Trác đem đại quân thị uy cướp giá; Trác vào thành nghênh ngang. | `poem` $\to$ **`epic_narrator`** $\to$ `melancholic_social` | Đồng dao bí ẩn; Đổng Trác kéo quân bụi bay mờ đất; sắc thái nặng nề khi thiết giáp thị uy gieo sợ hãi cho nhân dân. |
| **Chunk 6** | Tiệc yến vườn Ôn Minh; Đổng Trác rút gươm đòi phế lập; Đinh Nguyên đứng phắt dậy mắng; Lã Bố trừng mắt. | **`suspense_narrator`** $\to$ `epic_narrator` | Căng thẳng tột độ của bữa tiệc quyền lực, gươm tuốt sáng loáng, sinh tử trong chớp mắt. |
| **Chunk 7** | Lư Thực can gián; Đinh Nguyên đối trận Đổng Trác ngoài thành; Lã Bố múa kích đuổi Trác chạy dài. | `contemplative` $\to$ **`epic_narrator`** | **Chiến trận kinh điển**: cờ dong trống mở, Lã Bố xuất trận uy phong lẫm lẫm, đại phá quân Tây Lương lui 30 dặm. |
| **Chunk 8** | Lý Túc hiến kế dụ Bố; Miêu tả ngựa Xích Thố; Thơ vịnh Xích Thố; Túc sang trại Bố tâm tình. | `intimate` $\to$ `contemplative` $\to$ `poem` $\to$ `existential_interior` | Miêu tả thần mã hùng tráng; thơ ngâm trầm vang; đối thoại ngầm thao túng tâm lý Lã Bố. |
| **Chunk 9** | Lã Bố nhận vàng ngựa sa ngã; Hồi canh hai cầm dao lẻn vào trướng Đinh Nguyên chém đầu cha nuôi. | `suspense_narrator` $\to$ `satirical_ironic` | Rùng rợn, rình rập trong đêm đen tĩnh mịch: nhát dao bội phản tàn khốc của Lã Bố. |
| **Chunk 10** | Bố nhận Trác làm cha nuôi; Tiệc yến thứ hai; Viên Thiệu tuốt gươm đối kháng Trác; Câu đối kết hồi. | `satirical` $\to$ **`epic_narrator`** $\to$ `poem` $\to$ `contemplative` | Cao trào đối đầu đỉnh điểm "gươm mày sắc, dễ gươm tao không sắc hay sao"; câu đối đúc kết hồi trang nghiêm, sâu lắng. |

---

## PHẦN II: THIẾT KẾ ĐỘNG CƠ NGÂM VỊNH THI CA (POETIC PROSODY ENGINE)

### 1. Bộ Quy Chuẩn 4 Lớp Cho Thi Ca Cổ (Acoustic Poetic Calibration)
1. **Phân rã dòng độc lập (Line-by-Line Decomposition):** 100% các câu thơ tách thành entry độc lập với `type: "poem"`, tuyệt đối không gộp chung vào đoạn văn xuôi.
2. **Kỹ thuật ngắt nhịp vi mô (Metrical Caesura Injection):** Chèn dấu phẩy `, ` vào điểm ngắt nhịp niêm luật tự nhiên:
   - Thất ngôn: ngắt $4/3$ (*Nhà Hán thương ôi, / vận đã cùng!*) hoặc $2/2/3$ (*Ngàn dặm mù bay, / tịt nẻo xa,*).
   - Tứ ngôn (Đồng dao): ngắt $2/2$ (*Đế chẳng, ra đế,* hoặc câu 4 chữ cân đối *Đế chẳng ra đế,*).
3. **Cấu trúc đệm thở 3 tầng (Three-Tier Cushioning):**
   - **Tầng 1 (Lead-in Cushion):** Đệm **`0.85s - 1.20s`** sau câu dẫn thơ.
   - **Tầng 2 (Inter-Verse Cushion):** Đệm **`0.85s`** (`lead_in_pause: 0.85s`) giữa từng câu thơ để câu trước ngân vang trọn vẹn.
   - **Tầng 3 (Ending Coda Cushion):** Đệm **`1.50s`** (`. ......`) sau khổ thơ tạo khoảng lặng chiêm nghiệm.
4. **Tham số âm học chuẩn ngâm thơ:** `pitch: -2Hz`, `rate: -18%` (khoan thai, nhả chữ tròn vành), `timbre_eq: "poetic_recitation"` (Boost 250Hz +3.5dB ấm áp, Low-pass 7.5kHz triệt tiêu chói).

---

### 2. Chi Tiết Cấu Trúc Kịch Bản Cho 5 Tác Phẩm Thi Ca Trong Hồi 3

#### Tác phẩm 1: Tiêu đề Hồi 3 & Câu đối biền ngẫu đầu hồi (Chunk 1)
- **Hồi hiệu:** `"HỒI BA"` (`type: "narrator"`, `narrative_mode: "contemplative"`, `pitch: "-2Hz"`, `rate: "-12%"`, `lead_in_pause: "0.30s"`)
- **Khoảng lặng Hồi hiệu:** `". ...... "` (`lead_in_pause: "1.50s"`)
- **Câu đối vế trên:**
  ```json
  {
    "type": "poem",
    "speaker": "Narrator",
    "text": "TIỆC ÔN MINH, ĐỔNG TRÁC MẮNG ĐINH NGUYÊN,",
    "voice": "vi-VN-NamMinhNeural",
    "pitch": "-2Hz",
    "rate": "-18%",
    "lead_in_pause": "0.85s",
    "timbre_eq": "poetic_recitation"
  }
  ```
- **Câu đối vế dưới:**
  ```json
  {
    "type": "poem",
    "speaker": "Narrator",
    "text": "DÙNG VÀNG BẠC, LÝ TÚC DỤ LÃ BỐ.",
    "voice": "vi-VN-NamMinhNeural",
    "pitch": "-2Hz",
    "rate": "-18%",
    "lead_in_pause": "0.85s",
    "timbre_eq": "poetic_recitation"
  }
  ```
- **Coda chuyển đoạn:** `". ...... "` (`lead_in_pause: "1.50s"`)

---

#### Tác phẩm 2: Bài thơ than Hà Tiến (Chunk 3)
- **Câu dẫn nhập:** `"Đời sau có thơ than rằng,"` (`type: "narrator"`, `narrative_mode: "contemplative"`, `pitch: "-2Hz"`, `rate: "-12%"`, `lead_in_pause: "0.85s"`)
- **Đệm tầng 1:** `". ...... "` (`lead_in_pause: "1.00s"`)
- **4 dòng thơ bóc tách độc lập (Caesura 4/3):**
  ```json
  [
    {
      "type": "poem",
      "speaker": "Narrator",
      "text": "Nhà Hán thương ôi, vận đã cùng!",
      "voice": "vi-VN-NamMinhNeural",
      "pitch": "-2Hz",
      "rate": "-18%",
      "lead_in_pause": "0.85s",
      "timbre_eq": "poetic_recitation"
    },
    {
      "type": "poem",
      "speaker": "Narrator",
      "text": "Mưu gì Hà Tiến, lại tam công?",
      "voice": "vi-VN-NamMinhNeural",
      "pitch": "-2Hz",
      "rate": "-18%",
      "lead_in_pause": "0.85s",
      "timbre_eq": "poetic_recitation"
    },
    {
      "type": "poem",
      "speaker": "Narrator",
      "text": "Mấy phen chẳng biết, nghe lời phải,",
      "voice": "vi-VN-NamMinhNeural",
      "pitch": "-2Hz",
      "rate": "-18%",
      "lead_in_pause": "0.85s",
      "timbre_eq": "poetic_recitation"
    },
    {
      "type": "poem",
      "speaker": "Narrator",
      "text": "Thoát khỏi làm sao, họa cửa cung?",
      "voice": "vi-VN-NamMinhNeural",
      "pitch": "-2Hz",
      "rate": "-18%",
      "lead_in_pause": "0.85s",
      "timbre_eq": "poetic_recitation"
    }
  ]
  ```
- **Đệm tầng 3 (Coda):** `". ...... "` (`lead_in_pause: "1.50s"`)
- **Chuyển tiếp sau thơ:** Viên Thiệu gọi tướng quân ra về $\to$ chuyển sang nhịp dẫn khẩn cấp `suspense` $\to$ `epic_narrator`.

---

#### Tác phẩm 3: Bài đồng dao kinh thành Lạc Dương (Chunk 5)
- **Câu dẫn nhập:** `"Trước đây ít lâu, trẻ con ở kinh thành Lạc Dương thường hát mấy câu sau,"` (`type: "narrator"`, `narrative_mode: "contemplative"`, `pitch: "-2Hz"`, `lead_in_pause: "0.85s"`)
- **Đệm tầng 1:** `". ...... "` (`lead_in_pause: "1.00s"`)
- **4 dòng đồng dao sấm truyền (Nhịp điệu cổ kính):**
  ```json
  [
    {
      "type": "poem",
      "speaker": "Narrator",
      "text": "Đế chẳng ra đế,",
      "voice": "vi-VN-NamMinhNeural",
      "pitch": "-2Hz",
      "rate": "-18%",
      "lead_in_pause": "0.85s",
      "timbre_eq": "poetic_recitation"
    },
    {
      "type": "poem",
      "speaker": "Narrator",
      "text": "Vương chẳng ra vương,",
      "voice": "vi-VN-NamMinhNeural",
      "pitch": "-2Hz",
      "rate": "-18%",
      "lead_in_pause": "0.85s",
      "timbre_eq": "poetic_recitation"
    },
    {
      "type": "poem",
      "speaker": "Narrator",
      "text": "Xe xe, ngựa ngựa,",
      "voice": "vi-VN-NamMinhNeural",
      "pitch": "-2Hz",
      "rate": "-18%",
      "lead_in_pause": "0.85s",
      "timbre_eq": "poetic_recitation"
    },
    {
      "type": "poem",
      "speaker": "Narrator",
      "text": "Chạy ra Bắc Mang.",
      "voice": "vi-VN-NamMinhNeural",
      "pitch": "-2Hz",
      "rate": "-18%",
      "lead_in_pause": "0.85s",
      "timbre_eq": "poetic_recitation"
    }
  ]
  ```
- **Đệm tầng 3 (Coda):** `". ...... "` (`lead_in_pause: "1.50s"`)
- **Lời bình sấm truyền:** `"Đến bây giờ, quả là ứng nghiệm."` (`type: "narrator"`, `narrative_mode: "contemplative"`, `pitch: "-2Hz"`, `lead_in_pause: "0.85s"`)

---

#### Tác phẩm 4: Bài thơ vịnh ngựa Xích Thố (Chunk 8)
- **Câu dẫn nhập:** `"Đời sau có người vịnh thơ khen ngựa xích thố rằng,"` (`type: "narrator"`, `narrative_mode: "contemplative"`, `pitch: "-2Hz"`, `lead_in_pause: "0.85s"`)
- **Đệm tầng 1:** `". ...... "` (`lead_in_pause: "1.00s"`)
- **4 dòng thơ ngợi ca thần mã (Caesura 4/3):**
  ```json
  [
    {
      "type": "poem",
      "speaker": "Narrator",
      "text": "Ngàn dặm mù bay, tịt nẻo xa,",
      "voice": "vi-VN-NamMinhNeural",
      "pitch": "-2Hz",
      "rate": "-18%",
      "lead_in_pause": "0.85s",
      "timbre_eq": "poetic_recitation"
    },
    {
      "type": "poem",
      "speaker": "Narrator",
      "text": "Trèo non vượt nước, khéo xông pha.",
      "voice": "vi-VN-NamMinhNeural",
      "pitch": "-2Hz",
      "rate": "-18%",
      "lead_in_pause": "0.85s",
      "timbre_eq": "poetic_recitation"
    },
    {
      "type": "poem",
      "speaker": "Narrator",
      "text": "Cương tơ chặt đứt, rung chuông ngọc,",
      "voice": "vi-VN-NamMinhNeural",
      "pitch": "-2Hz",
      "rate": "-18%",
      "lead_in_pause": "0.85s",
      "timbre_eq": "poetic_recitation"
    },
    {
      "type": "poem",
      "speaker": "Narrator",
      "text": "Rồng đỏ trên trời, hẳn mới sa?",
      "voice": "vi-VN-NamMinhNeural",
      "pitch": "-2Hz",
      "rate": "-18%",
      "lead_in_pause": "0.85s",
      "timbre_eq": "poetic_recitation"
    }
  ]
  ```
- **Đệm tầng 3 (Coda):** `". ...... "` (`lead_in_pause: "1.50s"`)

---

#### Tác phẩm 5: Câu đối kết hồi & Lời dẫn hồi sau (Chunk 10)
- **Lời dẫn kết:** `"Thế rõ thực là,"` (`type: "narrator"`, `narrative_mode: "contemplative"`, `pitch: "-2Hz"`, `lead_in_pause: "0.85s"`)
- **Đệm tầng 1:** `". ...... "` (`lead_in_pause: "1.00s"`)
- **Cặp câu đối thất ngôn tổng kết bi kịch & xung đột:**
  ```json
  [
    {
      "type": "poem",
      "speaker": "Narrator",
      "text": "Đinh Nguyên trượng nghĩa, thân vừa chết,",
      "voice": "vi-VN-NamMinhNeural",
      "pitch": "-2Hz",
      "rate": "-18%",
      "lead_in_pause": "0.85s",
      "timbre_eq": "poetic_recitation"
    },
    {
      "type": "poem",
      "speaker": "Narrator",
      "text": "Viên Thiệu tranh hùng, thế cũng nguy.",
      "voice": "vi-VN-NamMinhNeural",
      "pitch": "-2Hz",
      "rate": "-18%",
      "lead_in_pause": "0.85s",
      "timbre_eq": "poetic_recitation"
    }
  ]
  ```
- **Đệm tầng 3 (Coda):** `". ...... "` (`lead_in_pause: "1.50s"`)
- **Câu Coda dứt hồi:** `"Chưa biết tính mạng Viên Thiệu thế nào, xem hồi sau thì biết rõ."` (`type: "narrator"`, `narrative_mode: "contemplative"`, `pitch: "-2Hz"`, `rate: "-12%"`, `lead_in_pause: "1.20s"`, `timbre_eq: "contemplative_narrator"`)

---

## KẾT LUẬN & KIẾN NGHỊ BÀN GIAO CHO CONTINUITY QC (SA5)
1. Hồ sơ thiết kế 8 sắc thái dẫn chuyện và toàn bộ 5 tác phẩm thi ca đã được chuẩn hóa 100% âm học (bóc tách từng dòng `type: "poem"`, caesura `, `, đệm 3 tầng `0.85s - 1.20s / 0.85s / 1.50s`, `rate: -18%`, `pitch: -2Hz`, `timbre_eq: "poetic_recitation"`).
2. Đề nghị Subagent 5 (`Theatrical Dramaturg & Continuity QC`) tích hợp toàn bộ các cấu trúc này vào tệp `theatrical_script.json`, bóc tách dứt điểm các dòng thơ đang bị dính liền vào đoạn dẫn văn xuôi ở Chunk 3, 5, 8, 10 để phòng thu TTS Bước 08B xuất xưởng bản thu thính kịch hoàn hảo nhất.