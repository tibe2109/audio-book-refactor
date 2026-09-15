import os
import shutil

SKILL_08A_CONTENT = """---
name: arf_08a_theatrical_voice_director
description: "Bước 08A trong Dây chuyền Sách nói Toàn năng (Universal Audiobook Pipeline): Tổng Đạo diễn Kịch nghệ & Phân vai Diễn đọc Thính kịch Đa thanh (Chief Theatrical Voice & Casting Director). Tiếp nhận kịch bản đạt 100% 7 Quality Gates từ Bước 07, tiến hành thẩm định thể loại linh hoạt tránh áp đặt cứng nhắc: với Văn học kinh điển/Sử thi, kích hoạt Động cơ Phân vai Đa thanh theo dõi tiến hóa 5 giai đoạn tuổi tác cuộc đời (Ấu thơ, Vỡ giọng, Thanh xuân, Trung niên, Lão hóa), 10 khí chất bản thể và 12 cung bậc cảm xúc phân cảnh; tích hợp Động cơ Thẩm định Thi ca & Nghệ thuật Ngâm vịnh Đa thể loại (Song thất lục bát, Lục bát, Thất ngôn Đường luật, Từ khúc, Ngũ ngôn) với kỹ thuật ngắt nhịp vi mô và phân hóa sâu sắc giữa Người dẫn chuyện hoài cổ và Nhân vật ngâm vịnh theo bối cảnh kịch tính. Bắt buộc kích hoạt và điều phối mảng đa tác tử tối thiểu 4 - 5 Subagents chuyên môn song song (Council of Theatrical Directors): bóc tách thoại Lời dẫn vs Nhân vật, lập hồ sơ nhân vật .theatrical_bible.json, giải mã bối cảnh và cảm xúc, phân tích thi ca và nhịp thở kịch nghệ, điều chế thông số âm học (Pitch Delta, Rate Delta, Lead-in Pause), và tổng duyệt kịch nghệ trước khi chuyển giao sang phòng thu âm Bước 08B. Kích hoạt khi kịch bản đạt chuẩn Bước 07 hoặc khi cần đạo diễn phân vai và ngâm vịnh thi ca cho tác phẩm văn học."
---

# Kỹ năng 08A: Đạo Diễn Kịch Nghệ & Phân Vai Đa Thanh (Theatrical Voice Director)

## 1. Đặc Tả Quy Trình Thao Tác Chuẩn (Specification - SOP)

Kỹ năng `arf_08a_theatrical_voice_director` giữ vai trò **Tổng Đạo Diễn Nghệ Thuật Tiền Kỳ (Chief Dramaturg & Casting Master)**. Để kịch bản audio truyền tải sâu sắc linh hồn, bối cảnh tâm lý, cảm xúc nhân vật và nhạc điệu thi ca, kỹ năng thiết lập cơ chế **Bắt buộc kích hoạt & điều phối mảng tối thiểu 4 - 5 Subagents chuyên môn song song**.

### 1.1 Thẩm Định Thể Loại & Chiến Lược Diễn Đọc
| Thể Loại Tác Phẩm | Bản Chất Truyền Tải | Chiến Lược Đạo Diễn | Thiết Lập Âm Học Cốt Lõi |
| :--- | :--- | :--- | :--- |
| **Văn học / Kịch / Sử thi** | Xung đột kịch tính, đối thoại đan xen, thi ca ngâm vịnh. | **Hội đồng Đạo diễn $\\ge 4-5$ Subagents:** 8 Nhóm tuổi, 10 Khí chất, 12 Cảm xúc, Động cơ Thi ca Đa thể loại. | Dynamic: `Pitch -6Hz ~ +10Hz`, `Rate -20% ~ +15%`, `lead_in_pause: 0.18s ~ 0.50s` (Thơ: 0.8s - 1.8s). |
| **Tự lực / Kỹ năng sống** | Đối thoại 1-1 giữa Tác giả và Độc giả (`Tôi - Bạn`). | **Cố Vấn Tri Kỷ (Inspirational Mentor):** Trầm ấm, chân thành, đĩnh đạc, lắng đọng. | `Pitch -2Hz`, `Rate -3%`, nhấn sâu đúc kết triết lý (`. ......` 1.8s). |
| **Khoa học / PMBOK** | Tri thức học thuật khách quan, phân cấp H1/H2. | **Phát Thanh Học Thuật (Academic Broadcast):** Chuẩn xác, sắc sảo, kỷ luật chuyên gia. | `Pitch 0Hz`, `Rate 0%`, tách âm viết tắt (*P-M-I*), Brian đọc ngoại ngữ. |

### 1.2 Động Cơ Phân Vai Kịch Nghệ Đa Thanh (Dành Cho Nhân Vật)
$$\\text{Tone Thoại Cuối} = \\text{Cốt Giọng Theo Tuổi} + \\Delta_{\\text{Khí Chất}} + \\Delta_{\\text{Cảm Xúc Phân Cảnh}}$$
- **5 Giai đoạn tiến hóa đời người:** Ấu thơ (5-10t: `+8Hz ~ +10Hz`), Vỡ giọng (12-17t: `+4Hz ~ +6Hz`), Thanh xuân (18-30t: `0Hz ~ +3Hz`), Trung niên (35-55t: `-2Hz ~ -4Hz`), Lão hóa (65-80+t: `-6Hz ~ -8Hz`).
- **10 Khí chất bản thể:** Anh hùng hào sảng, Trầm uất dằn vặt, Giảo hoạt nham hiểm, Hách dịch bạo ngược, Xun xoe đớn hèn, Trong sáng thánh thiện, Bi kịch uất nghẹn, Lãng mạn bay bổng, Khắc khổ lạnh lùng, Tếu táo hóm hỉnh.
- **12 Cung bậc cảm xúc tức thời:** Cuồng nộ (`+5Hz`), Đau đớn trăng trối (`-4Hz`), Đe dọa thâm hiểm (`-4Hz`), Nịnh bợ van xin (`+5Hz`), Hồi hộp thì thào (`+1Hz`), Độc thoại dằn vặt (`-2Hz`), Ghen tuông cay đắng (`+2Hz`), Ngượng ngùng tình đầu (`+3Hz`), Bàng hoàng chết lặng (`0Hz`), Hoan ca đắc thắng (`+3Hz`), Mỉa mai châm biếm (`+2Hz`), Mệt mỏi buông xuôi (`-4Hz`).

### 1.3 Động Cơ Thẩm Định Thi Ca & Ngâm Vịnh Đa Thể Loại (Poetic Prosody Engine)
Trí tuệ văn học linh hoạt, tự động nhận diện cấu trúc thể thơ và điều chế nhịp thở diễn ngâm:

| Thể Thơ Nhận Diện | Cấu Trúc Khổ & Ngắt Nhịp (Caesura) | Kỹ Thuật Diễn Ngâm / Luyến Láy | Thiết Lập Âm Học Diễn Ngâm |
| :--- | :--- | :--- | :--- |
| **Song thất lục bát** *(7-7-6-8)* | Cặp 7 ngắt nhịp $3/4$ hoặc $2/2/3$; cặp 6-8 ngắt nhịp chẵn ($2/4, 4/4$). | Cặp 7 ngâm cao giọng ở nhịp đầu, buông chùng và ngân dài ở tiếng thứ 7; cặp 6-8 chuyển trầm ấm tâm tình. Điển hình khúc *Lâm giang tiên* (*Trường Giang cuồn cuộn*). | `Pitch: -1Hz ~ +1Hz`, `Rate: -12% ~ -18%`, chèn dấu phẩy nhịp thở vi mô sau từng vế nhịp. |
| **Lục bát** *(6-8)* | Nhịp $2/2/2, 4/4$ êm đềm, nhịp nhàng. | Đọc mềm mại, lướt êm, ngân vang tự nhiên ở các tiếng vần (tiếng 6, tiếng 8). | `Pitch: 0Hz`, `Rate: -10% ~ -14%`, đệm êm dịu. |
| **Thất ngôn Đường luật** *(Tứ tuyệt / Bát cú)* | Nhịp $4/3$ hoặc $2/2/3$ trang trọng. | Ngắt nhịp dứt khoát tại tiếng thứ 4, kéo dài âm vang tại tiếng thứ 7, giọng đĩnh đạc cổ kính. | `Pitch: +1Hz` (câu đề/thực) $\\to$ `-2Hz` (câu kết), `Rate: -12%`. |
| **Ngũ ngôn** *(5 chữ)* | Nhịp $2/3$, dứt khoát, cô đọng. | Thanh thoát, gãy gọn, nhấn mạnh sức nặng của từng hình ảnh biểu tượng. | `Pitch: 0Hz`, `Rate: -8% ~ -12%`. |
| **Từ khúc / Phú / Biền văn** | Nhịp câu dài ngắn tự do uyển chuyển. | Biến hóa theo nhạc điệu điệu từ, giàu tính biểu cảm và nhạc tính. | Dynamic thích ứng theo cung bậc phân cảnh. |
| **Thơ tự do / Hiện đại** | Nhịp điệu theo dòng cảm xúc nội tâm. | Tự nhiên, chân thành, ngắt nghỉ theo trường liên tưởng thi ảnh. | `Pitch: -1Hz`, `Rate: -8% ~ -12%`. |

- **Phân hóa Chủ thể & Bối cảnh Diễn ngâm:**
  - *Người kể chuyện (Narrator):* Đề từ đầu chương, bình sử hoài cổ $\\to$ Không gian mênh mang, chiêm nghiệm buông bỏ, buông chùng hơi thở, tốc độ chậm rãi (`Rate -15%`).
  - *Nhân vật ngâm vịnh:* Hào sảng chí lớn (Tào Tháo *Đoản ca hành* $\\to$ âm vực lồng ngực hào hùng); Uất hận bi ai (Tào Thực *Thất bộ thi* $\\to$ nghẹn ngào, nấc nhịp); Khóc hận tế điệu (Khổng Minh tế Chu Du $\\to$ trầm buồn, buông tiếng nấc).
- **Quy chuẩn Âm học Thi ca (Acoustic Poetic Calibration):**
  - Chèn breathing commas `, ` đúng vế nhịp thơ để tạo khoảng nghỉ phát thanh vi mô (~220ms).
  - Chèn khoảng lặng dẫn nhập `0.8s - 1.5s` sau lời dẫn thơ (*\"Có bài từ rằng,\"*, *\"Cất giọng ngâm rằng,\"*).
  - Chèn khoảng lặng lắng đọng `1.5s - 1.8s` (`. ......`) sau câu thơ kết bài để dư ba ngân vang.

### 1.4 Hội Đồng Đạo Diễn Kịch Nghệ 5 Subagents Bắt Buộc (Council of Theatrical Directors)
AI Chính **bắt buộc kích hoạt đồng thời mảng tối thiểu 4 - 5 Subagents chuyên môn song song**:

| Subagent | Vai Trò Chuyên Biệt | Trọng Tâm Nhiệm Vụ | Đầu Ra Cam Kết |
| :---: | :--- | :--- | :--- |
| **SA 1** | **Speaker Attribution & Dialogue Boundary** | Quét triệt để ranh giới Lời dẫn (Narrator) vs Lời thoại (Dialogue) vs Khối thi ca ngâm vịnh. | Phân đoạn thoại & thơ kèm Speaker ID chuẩn hóa. |
| **SA 2** | **Character Arc & Archetype Profiler** | Thẩm định tuổi tác 5 giai đoạn, 10 khí chất bản thể, khóa tính nhất quán nhân vật toàn tác phẩm. | Xuất bản hồ sơ nhân vật `.theatrical_bible.json`. |
| **SA 3** | **Dramatic Setting & Power Dynamics Analyst** | Phân tích bối cảnh phân cảnh, vị thế quyền lực (Vua-Tôi, Huynh-Đệ, Kẻ thù), giải mã stage directions. | Gán nhãn 1 trong 12 cung bậc cảm xúc tức thời. |
| **SA 4** | **Poetic Prosody & Scansion Specialist** | Phân tích thể thơ, vế nhịp (Caesura), bối cảnh người ngâm (hoài cổ vs bi tráng), chèn breathing commas. | Ma trận âm học ngâm thơ (`Pitch`, `Rate`, `Lead-in Pause`). |
| **SA 5** | **Theatrical Dramaturg & Continuity QC** | Tổng duyệt kịch nghệ, kiểm tra độ mượt chuyển giao giữa Lời dẫn, Thoại và Thơ, triệt tiêu xung đột vai. | Nghiệm thu và chốt bản `theatrical_script.json`. |

---

## 2. Điều Kiện Kích Hoạt & Cụm Từ Khóa (When to Use & Triggers)

### 2.1 Bối Cảnh Sử Dụng
- Khi các tệp `Kich-ban-*.txt` đã đạt 100% 7 Quality Gates tại Bước 07.
- Khi tác phẩm văn học, tiểu thuyết, sử thi có đối thoại đan xen hoặc chứa các đoạn thơ ca, từ khúc ngâm vịnh.
- Trước khi chuyển sang phòng thu âm `arf_08_tts_neural_bgm_mixer`.

### 2.2 Câu Lệnh Người Dùng Điển Hình (User Prompt Triggers)
- *"Phân vai kịch nghệ và đạo diễn ngâm thơ cho chương này: `01-chuong-1`"*
- *"Kích hoạt hội đồng đạo diễn đa tác tử để lên kịch bản thu âm và diễn ngâm thi ca"*
- *"Bóc tách lời thoại, gán cảm xúc kịch tính và ngắt nhịp ngâm thơ cho đúng thể thơ"*
- *"Tạo kịch bản phân vai theatrical_script.json với 5 subagents chuyên môn"*
- *"Chạy Bước 08A đạo diễn thính kịch đa thanh"*

---

## 3. Trình Tự Thực Thi Từng Bước (Step-by-Step Execution)

```mermaid
flowchart TD
    P1["Pha 1: Tiền Đánh Giá & Phân Cảnh (AI Chính)\\n- Thẩm định thể loại tác phẩm\\n- Quét sự hiện diện của đối thoại và thi ca\\n- Phân rã kịch bản thành Phân cảnh (Scenes)"] --> P2["Pha 2: Điều Phối Mảng Tối Thiểu 4-5 Subagents Song Song\\n- SA1: Speaker Attribution\\n- SA2: Character Arc Profiler\\n- SA3: Emotion & Power Dynamics\\n- SA4: Poetic Prosody & Scansion Specialist\\n- SA5: Theatrical Dramaturg & QC"]
    P2 --> P3["Pha 3: Tổng Hợp & Xuất Bản Kịch Bản Phân Vai\\n- Ghép nối JSON toàn chương\\n- Xuất theatrical_script.json & .theatrical_bible.json\\n- Cập nhật manifest & chuyển giao sang B08B"]
```

### Pha 1: Tiền đánh giá & Phân cảnh (Pre-checks)
1. Xác nhận `QC_Report.md` đã đạt 100% 7/7 Gates PASSED.
2. AI Chính đánh giá thể loại tác phẩm: phân rã thành các Phân cảnh kịch nghệ và đánh dấu các khối thi ca (nếu có).

### Pha 2: Điều phối mảng Sub-agents chuyên môn song song (Core Multi-Agent Swarm)
AI Chính bắt buộc kích hoạt đồng thời mảng **tối thiểu 4 - 5 Subagents** chuyên môn:
```python
invoke_subagent(
    Subagents=[
        {"TypeName": "self", "Role": "Speaker Attribution Specialist", "Prompt": "Bóc tách Lời dẫn vs Thoại vs Thơ, gán Speaker ID."},
        {"TypeName": "self", "Role": "Character Bible Master", "Prompt": "Xác lập tuổi tác 5 giai đoạn, 10 khí chất bản thể, xuất .theatrical_bible.json."},
        {"TypeName": "self", "Role": "Emotion & Dynamics Director", "Prompt": "Phân tích bối cảnh, quan hệ quyền lực, gán 1 trong 12 cảm xúc tức thời."},
        {"TypeName": "self", "Role": "Poetic Prosody Specialist", "Prompt": "Thẩm định thể thơ (Song thất lục bát, Lục bát, Đường luật...), gán nhịp ngắt vi mô và thông số âm học ngâm vịnh."},
        {"TypeName": "self", "Role": "Theatrical Dramaturg & QC", "Prompt": "Tổng duyệt kịch nghệ, rà soát tính biểu cảm và hoàn tất theatrical_script.json."}
    ]
)
```

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
└── theatrical_script.json          # Danh sách câu thoại & đoạn thơ kèm thông số âm học
```

### Mẫu `theatrical_script.json` (Bao Gồm Thoại & Thơ Ngâm):
```json
[
  {
    "line_id": 1,
    "chunk_id": 1,
    "type": "poetry",
    "poetic_form": "song_that_luc_bat",
    "speaker": "Narrator",
    "recitation_style": "hoai_co_chiem_nghiem",
    "text": "Trường Giang, cuồn cuộn chảy về đông,\nSóng vùi dập, hết anh hùng,\nĐược, thua, phải, trái, thoắt thành không,\nNon xanh nguyên vẻ cũ,\nMấy độ bóng tà hồng!",
    "voice": "vi-VN-NamMinhNeural",
    "pitch": "-1Hz",
    "rate": "-15%",
    "lead_in_pause": "1.50s"
  },
  {
    "line_id": 2,
    "chunk_id": 1,
    "type": "dialogue",
    "speaker": "Truong_Phi",
    "character_name": "Trương Phi",
    "text": "Hai vị ca ca! Trương Phi này xin thề sống chết có nhau cùng hai huynh!",
    "age_stage": "thanh_xuan",
    "temperament": "anh_hung_hao_sang",
    "emotion": "hao_hung_phan_khich",
    "voice": "vi-VN-NamMinhNeural",
    "pitch": "+4Hz",
    "rate": "+6%",
    "lead_in_pause": "0.22s"
  }
]
```

---

## 5. Cơ Chế Phủ Định & Điều Cấm Kỵ (Negative Triggers & Constraints)

- **CẤM ĐỌC DỒN DẬP THI CA NHƯ VĂN XUÔI:** Bắt buộc chèn breathing commas `, ` đúng vế nhịp của thể thơ và khoảng lặng dẫn nhập/kết thúc để tạo dư ba ngân vang.
- **CẤM ÉP CỨNG MỌI THỂ THƠ VÀO MỘT KHUÔN NHỊP DUY NHẤT:** AI phải thẩm định linh hoạt từng thể thơ (Song thất lục bát khác Lục bát, khác Thất ngôn Đường luật).
- **CẤM TUYỆT ĐỐI HÀNH VI CHỈ DÙNG 1 HOẶC 2 SUBAGENTS ĐỐI PHÓ:** Bắt buộc kích hoạt tối thiểu 4 – 5 Subagents chuyên môn song song.
- **TUYỆT ĐỐI KHÔNG THU ÂM TRONG BƯỚC 08A:** Bước này chỉ chịu trách nhiệm đạo diễn kịch nghệ và xuất kịch bản JSON.
- **CẤM ÁP ĐẶT CƯỜNG ĐIỆU KỊCH NGHỆ LÊN SÁCH PHI HƯ CẤU:** Sách tự lực, khoa học, PMBOK phải giữ giọng cố vấn hoặc chuyên gia chuẩn mực.
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

print("Update 08A with Poetic Prosody completed successfully!")
