import os
import shutil

SKILL_08A_CONTENT = """---
name: arf_08a_theatrical_voice_director
description: "Bước 08A trong Dây chuyền Sách nói Toàn năng (Universal Audiobook Pipeline): Tổng Đạo diễn Kịch nghệ & Phân vai Diễn đọc Thính kịch Đa thanh (Chief Theatrical Voice & Casting Director). Tiếp nhận kịch bản đạt 100% 7 Quality Gates từ Bước 07, tiến hành thẩm định thể loại linh hoạt tránh áp đặt cứng nhắc: với Văn học kinh điển/Sử thi, kích hoạt Động cơ Phân vai Đa thanh (Polyphonic Casting Engine) theo dõi tiến hóa 5 giai đoạn tuổi tác cuộc đời (Ấu thơ, Vỡ giọng, Thanh xuân, Trung niên, Lão hóa), 10 khí chất bản thể và 12 cung bậc cảm xúc phân cảnh; với Sách tự lực, định hình phong cách Cố vấn tri kỷ; với Sách khoa học/quản trị, định hình phong cách Chuyên gia học thuật. Bắt buộc kích hoạt và điều phối mảng đa tác tử tối thiểu 4 - 5 Subagents chuyên môn song song (Council of Theatrical Directors): Subagent 1 bóc tách thoại Narrator vs Dialogue, Subagent 2 lập hồ sơ nhân vật .theatrical_bible.json, Subagent 3 giải mã bối cảnh và cảm xúc tức thời, Subagent 4 điều chế thông số âm học (Pitch Delta, Rate Delta, Lead-in Pause), và Subagent 5 tổng duyệt kịch nghệ và tính liền mạch cảm xúc. Xuất bản kịch bản phân vai hoàn chỉnh theatrical_script.json dứt điểm trước khi chuyển sang phòng thu âm Bước 08B. Kích hoạt khi kịch bản đạt chuẩn Bước 07 hoặc khi cần đạo diễn phân vai chuyên sâu cho tác phẩm kịch nghệ tiểu thuyết."
---

# Kỹ năng 08A: Đạo Diễn Kịch Nghệ & Phân Vai Đa Thanh (Theatrical Voice Director)

## 1. Đặc Tả Quy Trình Thao Tác Chuẩn (Specification - SOP)

Kỹ năng `arf_08a_theatrical_voice_director` giữ vai trò **Tổng Đạo Diễn Nghệ Thuật Tiền Kỳ (Chief Dramaturg & Casting Master)**. Để kịch bản audio truyền tải sâu sắc linh hồn, bối cảnh tâm lý và cảm xúc của nhân vật, kỹ năng thiết lập cơ chế **Bắt buộc kích hoạt & điều phối mảng tối thiểu 4 - 5 Subagents chuyên môn song song**.

### 1.1 Thẩm Định Thể Loại & Chiến Lược Diễn Đọc
| Thể Loại Tác Phẩm | Bản Chất Truyền Tải | Chiến Lược Đạo Diễn | Thiết Lập Âm Học Cốt Lõi |
| :--- | :--- | :--- | :--- |
| **Văn học / Kịch / Sử thi** | Xung đột kịch tính, đối thoại đan xen, số phận nhân vật. | **Hội đồng Đạo diễn $\\ge 4-5$ Subagents:** 8 Nhóm tuổi, 10 Khí chất, 12 Cảm xúc biến thiên. | Dynamic: `Pitch -6Hz ~ +10Hz`, `Rate -20% ~ +15%`, `lead_in_pause: 0.18s ~ 0.50s`. |
| **Tự lực / Kỹ năng sống** | Đối thoại 1-1 giữa Tác giả và Độc giả (`Tôi - Bạn`). | **Cố Vấn Tri Kỷ (Inspirational Mentor):** Trầm ấm, chân thành, đĩnh đạc, lắng đọng. | `Pitch -2Hz`, `Rate -3%`, nhấn sâu đúc kết triết lý (`. ......` 1.8s). |
| **Khoa học / PMBOK** | Tri thức học thuật khách quan, phân cấp H1/H2. | **Phát Thanh Học Thuật (Academic Broadcast):** Chuẩn xác, sắc sảo, kỷ luật chuyên gia. | `Pitch 0Hz`, `Rate 0%`, tách âm viết tắt (*P-M-I*), Brian đọc ngoại ngữ. |

### 1.2 Động Cơ Phân Vai Kịch Nghệ Đa Thanh (Dành Cho Văn Học)
$$\\text{Tone Thoại Cuối} = \\text{Cốt Giọng Theo Tuổi} + \\Delta_{\\text{Khí Chất}} + \\Delta_{\\text{Cảm Xúc Phân Cảnh}}$$
- **5 Giai đoạn tiến hóa đời người:**
  1. *Ấu thơ (5-10t):* `Pitch +8Hz ~ +10Hz`, `Rate +8% ~ +12%` (ngây thơ, mỏng).
  2. *Vỡ giọng / Niên thiếu (12-17t):* `Pitch +4Hz ~ +6Hz`, `Rate +5% ~ +8%` (bất an, khàn).
  3. *Thanh xuân (18-30t):* `Pitch 0Hz ~ +3Hz`, `Rate 0% ~ +5%` (sáng khỏe, nhiệt huyết).
  4. *Trung niên (35-55t):* `Pitch -2Hz ~ -4Hz`, `Rate -5% ~ -10%` (dày ngực, uy lực).
  5. *Lão hóa (65-80+t):* `Pitch -6Hz ~ -8Hz`, `Rate -15% ~ -20%` (khàn đục, chậm rãi).
- **10 Khí chất bản thể:** Anh hùng hào sảng, Trầm uất dằn vặt, Giảo hoạt nham hiểm, Hách dịch bạo ngược, Xun xoe đớn hèn, Trong sáng thánh thiện, Bi kịch uất nghẹn, Lãng mạn bay bổng, Khắc khổ lạnh lùng, Tếu táo hóm hỉnh.
- **12 Cung bậc cảm xúc tức thời:** Cuồng nộ (`+5Hz`), Đau đớn trăng trối (`-4Hz`), Đe dọa thâm hiểm (`-4Hz`), Nịnh bợ van xin (`+5Hz`), Hồi hộp thì thào (`+1Hz`), Độc thoại dằn vặt (`-2Hz`), Ghen tuông cay đắng (`+2Hz`), Ngượng ngùng tình đầu (`+3Hz`), Bàng hoàng chết lặng (`0Hz`), Hoan ca đắc thắng (`+3Hz`), Mỉa mai châm biếm (`+2Hz`), Mệt mỏi buông xuôi (`-4Hz`).

### 1.3 Hội Đồng Đạo Diễn Kịch Nghệ 5 Subagents Bắt Buộc (Council of Theatrical Directors)
Khi xử lý tác phẩm văn học / kịch nghệ, AI Chính **bắt buộc kích hoạt đồng thời mảng tối thiểu 4 - 5 Subagents**:

| Subagent | Vai Trò Chuyên Biệt | Trọng Tâm Nhiệm Vụ | Đầu Ra Cam Kết |
| :---: | :--- | :--- | :--- |
| **SA 1** | **Speaker Attribution & Dialogue Boundary** | Quét triệt để ranh giới Lời dẫn (Narrator) vs Lời thoại (Dialogue); không bỏ sót câu thoại lồng trong văn xuôi. | Danh sách phân đoạn thoại kèm Speaker ID chuẩn hóa. |
| **SA 2** | **Character Arc & Archetype Profiler** | Thẩm định tuổi tác, xác lập 10 khí chất bản thể, bảo đảm nhất quán nhân vật xuyên suốt tác phẩm. | Xuất bản hồ sơ nhân vật `.theatrical_bible.json`. |
| **SA 3** | **Dramatic Setting & Power Dynamics Analyst** | Phân tích bối cảnh phân cảnh, vị thế thứ bậc (Vua-Tôi, Huynh-Đệ, Kẻ thù), giải mã stage directions ẩn. | Gán nhãn 1 trong 12 cung bậc cảm xúc tức thời. |
| **SA 4** | **Acoustic Prosody & Micro-timing Modulator** | Tính toán ma trận số học `Pitch Delta (Hz)`, `Rate Delta (%)`, chèn khoảng lặng kịch tính `lead_in_pause (0.18s - 0.50s)`. | Thông số âm học chi tiết cho từng dòng thoại. |
| **SA 5** | **Theatrical Dramaturg & Continuity QC Auditor** | Tổng duyệt tính biểu cảm, kiểm tra độ mượt chuyển giao giữa Người dẫn và Nhân vật, triệt tiêu xung đột vai. | Nghiệm thu và chốt bản `theatrical_script.json`. |

*Ghi chú:* Với chương dài nhiều phân cảnh, có thể luân chuyển sang mô hình **Scene Swarm**: 4 Subagents đạo diễn 4 Phân cảnh song song + 1 Subagent Tổng trưởng quản Bible & Thẩm định tính liền mạch.

---

## 2. Điều Kiện Kích Hoạt & Cụm Từ Khóa (When to Use & Triggers)

### 2.1 Bối Cảnh Sử Dụng
- Khi các tệp `Kich-ban-*.txt` đã đạt 100% 7 Quality Gates tại Bước 07.
- Khi tác phẩm thuộc thể loại văn học, tiểu thuyết kinh điển, sử thi, kịch truyền thanh có nhiều nhân vật đối thoại.
- Trước khi chuyển sang phòng thu âm `arf_08_tts_neural_bgm_mixer`.

### 2.2 Câu Lệnh Người Dùng Điển Hình (User Prompt Triggers)
- *"Phân vai kịch nghệ cho chương này: `01-chuong-1`"*
- *"Kích hoạt hội đồng đạo diễn đa tác tử để lên kịch bản thu âm nhiều nhân vật"*
- *"Bóc tách lời thoại và gán cảm xúc kịch tính cho các nhân vật"*
- *"Tạo kịch bản phân vai theatrical_script.json với 5 subagents chuyên môn"*
- *"Chạy Bước 08A đạo diễn kịch truyền thanh đa thanh"*

---

## 3. Trình Tự Thực Thi Từng Bước (Step-by-Step Execution)

```mermaid
flowchart TD
    P1["Pha 1: Tiền Đánh Giá & Phân Cảnh (AI Chính)\\n- Thẩm định thể loại tác phẩm\\n- Phân rã kịch bản thành các Phân cảnh (Scenes)\\n- Lập danh sách nhân vật xuất hiện"] --> P2["Pha 2: Điều Phối Mảng Tối Thiểu 4-5 Sub-Agents Song Song\\n- SA1: Speaker Attribution\\n- SA2: Character Profiler\\n- SA3: Emotion & Power Dynamics\\n- SA4: Prosody & Micro-timing\\n- SA5: Theatrical Dramaturg & QC"]
    P2 --> P3["Pha 3: Tổng Hợp & Xuất Bản Kịch Bản Phân Vai\\n- Ghép nối JSON toàn chương\\n- Xuất theatrical_script.json & .theatrical_bible.json\\n- Cập nhật manifest & chuyển giao sang B08B"]
```

### Pha 1: Tiền đánh giá & Phân cảnh (Pre-checks)
1. Xác nhận `QC_Report.md` đã đạt 100% 7/7 Gates PASSED.
2. AI Chính đánh giá thể loại tác phẩm. Với sách phi hư cấu/PMBOK: gán kịch bản đơn giọng chuẩn trong 2 giây. Với văn học: phân rã tác phẩm thành các Phân cảnh kịch nghệ (Scenes).

### Pha 2: Điều phối mảng Sub-agents chuyên môn song song (Core Multi-Agent Swarm)
AI Chính bắt buộc kích hoạt đồng thời mảng **tối thiểu 4 - 5 Subagents** chuyên môn:
```python
invoke_subagent(
    Subagents=[
        {
            "TypeName": "self",
            "Role": "Speaker Attribution Specialist",
            "Prompt": "Bóc tách Lời dẫn (Narrator) vs Thoại nhân vật, gán Speaker ID cho từng câu."
        },
        {
            "TypeName": "self",
            "Role": "Character Bible Master",
            "Prompt": "Xác lập tuổi tác 5 giai đoạn, 10 khí chất bản thể, xuất bản .theatrical_bible.json."
        },
        {
            "TypeName": "self",
            "Role": "Emotion & Dynamics Director",
            "Prompt": "Phân tích bối cảnh, quan hệ thứ bậc quyền lực, gán 1 trong 12 cảm xúc phân cảnh."
        },
        {
            "TypeName": "self",
            "Role": "Prosody & Micro-timing Engineer",
            "Prompt": "Tính Pitch Delta, Rate Delta, Lead-in Pause (0.18s - 0.50s) cho từng câu thoại."
        },
        {
            "TypeName": "self",
            "Role": "Theatrical Dramaturg & Continuity QC",
            "Prompt": "Tổng duyệt kịch nghệ, rà soát xung đột và hoàn tất theatrical_script.json."
        }
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
└── theatrical_script.json          # Danh sách câu thoại kèm thông số âm học
```

### Mẫu `theatrical_script.json`:
```json
[
  {
    "line_id": 1,
    "chunk_id": 1,
    "type": "narrator",
    "speaker": "Narrator",
    "text": "Lại nói về ba người Lưu Bị, Quan Vũ và Trương Phi cùng kết nghĩa tại vườn đào.",
    "voice": "vi-VN-NamMinhNeural",
    "pitch": "0Hz",
    "rate": "-5%",
    "lead_in_pause": "0.18s"
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

- **CẤM TUYỆT ĐỐI HÀNH VI CHỈ DÙNG 1 HOẶC 2 SUBAGENTS ĐỐI PHÓ:** Bắt buộc kích hoạt tối thiểu 4 – 5 Subagents chuyên môn song song để bảo đảm chiều sâu nghệ thuật và cảm xúc.
- **TUYỆT ĐỐI KHÔNG THU ÂM TRONG BƯỚC 08A:** Bước này chỉ chịu trách nhiệm đạo diễn kịch nghệ và xuất kịch bản JSON. Toàn bộ khâu thu âm thuộc Bước 08B.
- **CẤM ÁP ĐẶT CƯỜNG ĐIỆU KỊCH NGHỆ LÊN SÁCH PHI HƯ CẤU:** Sách tự lực, khoa học, PMBOK phải giữ giọng cố vấn hoặc chuyên gia chuẩn mực, không gán cảm xúc gào thét.
- **CẤM ĐỔI TÊN SPEAKER BẤT NHẤT:** Nhân vật `Luu_Bi` phải giữ nguyên ID xuyên suốt toàn bộ các phân cảnh, không đổi sang `Luu_Huyen_Duc` hay `Luu_De`.
- **CẤM SỬ DỤNG KHI KỊCH BẢN CHƯA QUA BƯỚC 07:** Phải có `QC_Report.md` đạt 100% PASSED trước khi phân vai.
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

print("Update 08A completed successfully!")
