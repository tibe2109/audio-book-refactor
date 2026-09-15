import os
import shutil

SKILL_08A_CONTENT = """---
name: arf_08a_theatrical_voice_director
description: "Bước 08A trong Dây chuyền Sách nói Toàn năng (Universal Audiobook Pipeline): Tổng Đạo diễn Kịch nghệ & Phân vai Diễn đọc Thính kịch Đa thanh (Chief Theatrical Voice & Casting Director). Tiếp nhận kịch bản đạt 100% 7 Quality Gates từ Bước 07, tiến hành thẩm định thể loại linh hoạt tránh áp đặt cứng nhắc: với Văn học kinh điển/Sử thi, kích hoạt Động cơ Phân vai Đa thanh theo dõi tiến hóa 5 giai đoạn tuổi tác cuộc đời (Ấu thơ, Vỡ giọng, Thanh xuân, Trung niên, Lão hóa), 10 khí chất bản thể và 12 cung bậc cảm xúc phân cảnh; tích hợp Động cơ Thẩm định Thi ca & Ngâm vịnh Đa thể loại (Song thất lục bát, Lục bát, Đường luật, Từ khúc) với kỹ thuật ngắt nhịp vi mô. Đặc biệt tích hợp Bộ Best Practices 5 Trụ cột phân hóa sắc nét từng nhân vật (dù cùng một giọng đọc nền vi-VN-NamMinhNeural) thông qua mở rộng dải tương phản cao độ (-7Hz đến +8Hz), định hình âm sắc Formant EQ (Vang rền lồng ngực, Trầm ấm uy nghiêm, Sắc lạnh thâm hiểm, Khàn đục lão niên), chữ ký nhịp điệu riêng biệt và cơ chế chuyển giao âm học mượt mà (Seamless Handoff Transition đệm thở 0.28s - 0.35s, Micro-fade 25ms triệt tiêu 100% tiếng giật cục). Bắt buộc kích hoạt và điều phối mảng đa tác tử tối thiểu 4 - 5 Subagents chuyên môn song song trước khi xuất bản kịch bản phân vai theatrical_script.json và hồ sơ .theatrical_bible.json chuyển giao sang phòng thu âm Bước 08B. Kích hoạt khi kịch bản đạt chuẩn Bước 07 hoặc khi cần đạo diễn phân vai nghệ thuật thính kịch."
---

# Kỹ năng 08A: Đạo Diễn Kịch Nghệ & Phân Vai Đa Thanh (Theatrical Voice Director)

## 1. Đặc Tả Quy Trình Thao Tác Chuẩn (Specification - SOP)

Kỹ năng `arf_08a_theatrical_voice_director` giữ vai trò **Tổng Đạo Diễn Nghệ Thuật Tiền Kỳ (Chief Dramaturg & Casting Master)**. Để kịch bản audio truyền tải sâu sắc linh hồn tác phẩm, phân hóa sắc nét từng nhân vật (dù cùng chung giọng nền `vi-VN-NamMinhNeural`) và chuyển giao mượt mà không giật cục, kỹ năng áp dụng **Bộ Best Practices 5 Trụ Cột Đột Phá** kết hợp **Hội Đồng Đạo Diễn $\\ge 4-5$ Subagents Chuyên Môn Song Song**.

### 1.1 Thẩm Định Thể Loại & Chiến Lược Diễn Đọc
| Thể Loại Tác Phẩm | Bản Chất Truyền Tải | Chiến Lược Đạo Diễn | Thiết Lập Âm Học Cốt Lõi |
| :--- | :--- | :--- | :--- |
| **Văn học / Kịch / Sử thi** | Xung đột kịch tính, đối thoại đan xen, thi ca ngâm vịnh. | **Hội đồng $\\ge 4-5$ Subagents:** 5 Trụ cột âm sắc, 8 Nhóm tuổi, 10 Khí chất, 12 Cảm xúc, Động cơ Thi ca. | Dynamic: `Pitch -7Hz ~ +8Hz`, `Rate -20% ~ +15%`, `lead_in_pause: 0.20s ~ 0.50s` (Thơ: 0.8s - 1.8s). |
| **Tự lực / Kỹ năng sống** | Đối thoại 1-1 giữa Tác giả và Độc giả (`Tôi - Bạn`). | **Cố Vấn Tri Kỷ (Inspirational Mentor):** Trầm ấm, chân thành, đĩnh đạc, lắng đọng. | `Pitch -2Hz`, `Rate -3%`, nhấn sâu đúc kết triết lý (`. ......` 1.8s). |
| **Khoa học / PMBOK** | Tri thức học thuật khách quan, phân cấp H1/H2. | **Phát Thanh Học Thuật (Academic Broadcast):** Chuẩn xác, sắc sảo, kỷ luật chuyên gia. | `Pitch 0Hz`, `Rate 0%`, tách âm viết tắt (*P-M-I*), Brian đọc ngoại ngữ. |

### 1.2 Động Cơ Phân Vai Kịch Nghệ: Dải Tương Phản Cao Độ Mở Rộng
$$\\text{Tone Thoại Cuối} = \\text{Cốt Giọng Theo Tuổi} + \\Delta_{\\text{Khí Chất}} + \\Delta_{\\text{Cảm Xúc Phân Cảnh}}$$
Khắc phục hiện tượng \"nghe như một người nói\" bằng cách mở rộng biên độ Pitch tương phản rõ rệt:
- **5 Giai đoạn tuổi tác:** Ấu thơ (`+8Hz ~ +12Hz`), Vỡ giọng (`+4Hz ~ +6Hz`), Thanh xuân (`0Hz ~ +3Hz`), Trung niên (`-3Hz ~ -5Hz`), Lão niên (`-6Hz ~ -8Hz`).
- **10 Khí chất bản thể:** Anh hùng hào sảng, Trầm uất dằn vặt, Giảo hoạt nham hiểm, Hách dịch bạo ngược, Xun xoe đớn hèn, Trong sáng thánh thiện, Bi kịch uất nghẹn, Lãng mạn bay bổng, Khắc khổ lạnh lùng, Tếu táo hóm hỉnh.
- **12 Cung bậc cảm xúc tức thời:** Cuồng nộ (`+5Hz`), Đau đớn trăng trối (`-4Hz`), Đe dọa thâm hiểm (`-4Hz`), Nịnh bợ van xin (`+5Hz`), Hồi hộp thì thào (`+1Hz`), Độc thoại dằn vặt (`-2Hz`), Ghen tuông cay đắng (`+2Hz`), Ngượng ngùng tình đầu (`+3Hz`), Bàng hoàng chết lặng (`0Hz`), Hoan ca đắc thắng (`+3Hz`), Mỉa mai châm biếm (`+2Hz`), Mệt mỏi buông xuôi (`-4Hz`).

### 1.3 Ma Trận Định Hình Âm Sắc Formant EQ (Vocal Timbre Profiling)
Cùng 1 voice gốc, gán trường `timbre_eq` vào JSON để định hình màu giọng đặc trưng qua bộ lọc DSP:
| Nhãn `timbre_eq` | Nhân Vật Đại Diện | Cấu Hình Tần Số EQ Mục Tiêu | Hiệu Ứng Thính Giác |
| :--- | :--- | :--- | :--- |
| `chest_resonance` | Trương Phi, Hứa Chử, Điển Vi | Boost $180\\text{Hz} (+4\\text{dB})$, $2\\text{kHz} (+2\\text{dB})$ | Giọng vang rền lồng ngực, đanh thép, tiếng vang như sấm. |
| `warm_authority` | Quan Vũ, Lưu Bị, Gia Cát Lượng | Boost $300\\text{Hz} (+2.5\\text{dB})$, Dip $3.5\\text{kHz} (-2\\text{dB})$ | Giọng trầm ấm, tròn vành, đĩnh đạc của bậc đại trượng phu/quân sư. |
| `sharp_cunning` | Tào Tháo, Tư Mã Ý, Bọn hoạn quan | Low-cut dưới $200\\text{Hz}$, Boost $3\\text{kHz} (+3.5\\text{dB})$ | Giọng the lạnh, gằn mép, hiểm hóc, giảo hoạt sắc bén. |
| `aged_gravel` | Hoàng Trung, Kiều Quốc Lão, Lão tiều | Boost $450\\text{Hz} (+3\\text{dB})$, Roll-off trên $5\\text{kHz} (-3\\text{dB})$ | Giọng khàn đục, cũ kỹ, trải đời của bậc lão tướng/trưởng lão. |
| `youth_bright` | Thiếu niên, Đồng tử, Nữ cải trang | Low-cut $250\\text{Hz}$, Boost $4\\text{kHz} (+3\\text{dB})$ | Giọng sáng mảnh, thanh thoát, ngây thơ. |
| `intimate_narrator` | Người kể chuyện (Narrator) | Flat Studio EQ, cân bằng âm học phát thanh | Khách quan, truyền cảm, đĩnh đạc, rõ nét. |

### 1.4 Quy Chuẩn Chuyển Giao Âm Học Mượt Mà (Seamless Handoff Transition)
Triệt tiêu hoàn toàn hiện tượng khựng giật khi đổi giọng giữa Người dẫn và Nhân vật:
- **Chuẩn hóa nhịp đệm thở sinh học (`lead_in_pause`):**
  - *Lời dẫn $\\to$ Thoại nhân vật:* Bắt buộc chèn đệm thở **`0.28s - 0.35s`** (vừa đủ 1 nhịp thở sinh học, không đè tiếng và không hụt hơi).
  - *Nhân vật A $\\to$ Nhân vật B (đối đáp):* Đệm kịch tính **`0.20s - 0.25s`** (tạo độ chan chát, sắc bén).
  - *Thoại $\\to$ Ngâm thơ / Chiêm nghiệm:* Đệm sâu lắng **`0.80s - 1.20s`**.
- **Hạ giọng lời dẫn tiếp giáp (Lead-in Voice Softening):** Các cụm từ dẫn thoại (*\"nói,\"\*, *\"quát rằng,\"\*, *\"thầm nghĩ,\"\*) kết thúc bằng dấu phẩy `, ` để giọng dẫn hạ cao độ buông hơi trước khi nhường lời cho nhân vật.
- **Micro-fade 25ms:** Kỹ sư phòng thu tự động fade-in/out 25ms ở hai đầu ranh giới câu thoại để xóa bỏ 100% tiếng pop/click hoặc xung đột biên độ sóng âm khi đổi EQ.

### 1.5 Động Cơ Thẩm Định Thi Ca & Ngâm Vịnh Đa Thể Loại (Poetic Prosody Engine)
- **Nhận diện 6 thể thơ:** Song thất lục bát (7-7-6-8 ngắt $3/4$ hoặc $2/2/3$, câu 6-8 ngắt chẵn $2/4, 4/4$, hoài niệm mênh mang như khúc *Lâm giang tiên*), Lục bát ($2/2/2, 4/4$), Thất ngôn Đường luật ($4/3, 2/2/3$), Ngũ ngôn ($2/3$), Từ khúc/Phú, Thơ tự do.
- **Phân hóa người ngâm:** Người dẫn chuyện (hoài cổ thế sự, `Rate -15%`, buông chùng ngân tàn) vs Nhân vật ngâm (Tào Tháo hào hùng chí lớn vs Tào Thực uất hận bi ai vs Khổng Minh khóc tế bạn hữu).
- **Nhịp thở thi ca:** Breathing commas sau từng vế nhịp, khoảng lặng dẫn nhập 0.8s - 1.5s, khoảng lặng lắng đọng kết bài 1.5s - 1.8s (`. ......`).

### 1.6 Hội Đồng Đạo Diễn Kịch Nghệ 5 Subagents Bắt Buộc (Council of Theatrical Directors)
AI Chính **bắt buộc kích hoạt đồng thời mảng tối thiểu 4 - 5 Subagents chuyên môn song song**:
- **SA 1 (Speaker Attribution):** Bóc tách Lời dẫn vs Thoại vs Thơ, gán Speaker ID.
- **SA 2 (Character Arc & Bible Profiler):** Thẩm định tuổi tác, 10 khí chất, xuất bản `.theatrical_bible.json`.
- **SA 3 (Dramatic Setting & Dynamics):** Phân tích bối cảnh, quan hệ quyền lực, gán 1 trong 12 cảm xúc.
- **SA 4 (Poetic & Prosody Modulator):** Thẩm định thể thơ, gán nhịp vi mô, tính `pitch`, `rate`, `lead_in_pause`, `timbre_eq`.
- **SA 5 (Theatrical Dramaturg & Continuity QC):** Tổng duyệt tính liền mạch, kiểm tra độ mượt chuyển giao, chốt bản `theatrical_script.json`.

---

## 2. Điều Kiện Kích Hoạt & Cụm Từ Khóa (When to Use & Triggers)

### 2.1 Bối Cảnh Sử Dụng
- Khi các tệp `Kich-ban-*.txt` đã đạt 100% 7 Quality Gates tại Bước 07.
- Khi tác phẩm văn học, tiểu thuyết, sử thi có nhiều nhân vật đối thoại hoặc chứa các đoạn thơ ca, từ khúc ngâm vịnh.
- Trước khi chuyển sang phòng thu âm `arf_08_tts_neural_bgm_mixer`.

### 2.2 Câu Lệnh Người Dùng Điển Hình (User Prompt Triggers)
- *"Phân vai kịch nghệ và tạo âm sắc rõ nét cho các nhân vật: `01-chuong-1`"*
- *"Tối ưu hóa độ mượt khi chuyển giọng và gán EQ âm sắc cho từng nhân vật"*
- *"Kích hoạt hội đồng đạo diễn đa tác tử để lên kịch bản thu âm đa nhân vật và ngâm thơ"*
- *"Tạo kịch bản phân vai theatrical_script.json với 5 subagents chuyên môn"*
- *"Chạy Bước 08A đạo diễn thính kịch đa thanh"*

---

## 3. Trình Tự Thực Thi Từng Bước (Step-by-Step Execution)

```mermaid
flowchart TD
    P1["Pha 1: Tiền Đánh Giá & Phân Cảnh (AI Chính)\\n- Thẩm định thể loại tác phẩm\\n- Quét đối thoại, thi ca & nhân vật\\n- Phân rã kịch bản thành Phân cảnh (Scenes)"] --> P2["Pha 2: Điều Phối Mảng Tối Thiểu 4-5 Subagents Song Song\\n- SA1: Speaker Attribution\\n- SA2: Character Profiler (.theatrical_bible.json)\\n- SA3: Dramatic Setting & Emotion Dynamics\\n- SA4: Prosody & Timbre EQ Modulator\\n- SA5: Theatrical Dramaturg & Continuity QC"]
    P2 --> P3["Pha 3: Tổng Hợp & Xuất Bản Kịch Bản Phân Vai\\n- Ghép nối JSON toàn chương\\n- Kiểm tra Seamless Handoff (đệm thở 0.28s - 0.35s)\\n- Xuất theatrical_script.json & chuyển B08B"]
```

### Pha 1: Tiền đánh giá & Phân cảnh (Pre-checks)
1. Xác nhận `QC_Report.md` đã đạt 100% 7/7 Gates PASSED.
2. AI Chính phân rã tác phẩm thành các Phân cảnh kịch nghệ, lập danh sách nhân vật và đánh dấu các đoạn thơ.

### Pha 2: Điều phối mảng Sub-agents chuyên môn song song (Core Multi-Agent Swarm)
AI Chính bắt buộc kích hoạt đồng thời mảng **tối thiểu 4 - 5 Subagents** chuyên môn qua `invoke_subagent`:
- Tính toán đầy đủ: `voice`, `pitch`, `rate`, `lead_in_pause`, `timbre_eq`.
- Đảm bảo biên độ tương phản Pitch đạt chuẩn rõ nét ($-7\\text{Hz} \\to +8\\text{Hz}$).

### Pha 3: Nghiệm thu & Xuất bản tệp phân vai (Verification & Export)
1. AI Chính nghiệm thu và ghép nối kết quả thành tệp `theatrical_script.json` đồng nhất.
2. Lưu hồ sơ nhân vật toàn chương vào `.theatrical_bible.json`.
3. Cập nhật `.session_manifest.json` ghi nhận `step_8a_status: "completed"`.

---

## 4. Ràng Buộc Đầu Ra (Output Contract)

Mọi chương hoàn thành Bước 08A phải có 2 file dữ liệu kịch nghệ chuẩn mực:
```text
[chapter_folder]/
├── .theatrical_bible.json          # Hồ sơ nhân vật toàn chương
└── theatrical_script.json          # Danh sách câu thoại & thơ kèm EQ và âm học
```

### Mẫu `theatrical_script.json` Chuẩn Hóa:
```json
[
  {
    "line_id": 1,
    "chunk_id": 1,
    "type": "narrator",
    "speaker": "Narrator",
    "text": "Bấy giờ, Huyền Đức đọc bảng văn rồi thở dài. Có một người đứng phía sau nói lớn lên rằng,",
    "voice": "vi-VN-NamMinhNeural",
    "pitch": "0Hz",
    "rate": "-5%",
    "lead_in_pause": "0.18s",
    "timbre_eq": "intimate_narrator"
  },
  {
    "line_id": 2,
    "chunk_id": 1,
    "type": "dialogue",
    "speaker": "Truong_Phi",
    "character_name": "Trương Phi",
    "text": "Đại trượng phu như ông, không ra giúp nước, đứng thở dài đó, được việc chi!",
    "age_stage": "thanh_xuan",
    "temperament": "anh_hung_hao_sang",
    "emotion": "cuong_no_hao_hung",
    "voice": "vi-VN-NamMinhNeural",
    "pitch": "+5Hz",
    "rate": "+6%",
    "lead_in_pause": "0.32s",
    "timbre_eq": "chest_resonance"
  },
  {
    "line_id": 3,
    "chunk_id": 1,
    "type": "dialogue",
    "speaker": "Luu_Bi",
    "character_name": "Lưu Bị",
    "text": "Tôi đây vốn dòng dõi nhà Hán, họ Lưu tên Bị, nay thấy giặc Khăn Vàng nổi loạn, muốn giúp nước yên dân mà sức bất tòng tâm.",
    "age_stage": "thanh_xuan",
    "temperament": "trong_sang_thanh_thien",
    "emotion": "tram_ngam_than_tho",
    "voice": "vi-VN-NamMinhNeural",
    "pitch": "-3Hz",
    "rate": "-6%",
    "lead_in_pause": "0.28s",
    "timbre_eq": "warm_authority"
  }
]
```

---

## 5. Cơ Chế Phủ Định & Điều Cấm Kỵ (Negative Triggers & Constraints)

- **CẤM DẢI CAO ĐỘ CO CỤM DƯỚI 2HZ:** Không được gán pitch hời hợt $\\pm 1\\text{Hz} \\sim \\pm 2\\text{Hz}$ cho các tuyến nhân vật đối lập; phải mở rộng tương phản rõ rệt theo bảng ma trận.
- **CẤM KHOẢNG ĐỆM CHUYỂN TIẾP QUÁ NGẮN ($< 0.15\\text{S}$):** Khi chuyển từ Lời dẫn sang Thoại, bắt buộc đệm thở `0.28s - 0.35s` để triệt tiêu giật cục.
- **CẤM TUYỆT ĐỐI HÀNH VI CHỈ DÙNG 1 HOẶC 2 SUBAGENTS ĐỐI PHÓ:** Bắt buộc kích hoạt tối thiểu 4 – 5 Subagents chuyên môn song song.
- **TUYỆT ĐỐI KHÔNG THU ÂM TRONG BƯỚC 08A:** Bước này chỉ chịu trách nhiệm đạo diễn kịch nghệ và xuất kịch bản JSON.
- **CẤM ĐỔI TÊN SPEAKER BẤT NHẤT:** Nhân vật `Luu_Bi` phải giữ nguyên ID xuyên suốt toàn bộ phân cảnh.
"""

mirrors = [
    ".agent/skills",
    ".agents/skills",
    ".gemini/skills",
    ".agy/skills"
]

for mirror in mirrors:
    path_08a = os.path.join(mirror, "arf_08a_theatrical_voice_director", "SKILL.md")
    os.makedirs(os.path.dirname(path_08a), exist_ok=True)
    with open(path_08a, "w", encoding="utf-8") as f:
        f.write(SKILL_08A_CONTENT.strip() + "\n")
    print(f"[OK] Written {path_08a}")

print("Update 08A with distinction best practices completed successfully!")
