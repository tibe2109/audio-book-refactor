---
trigger: always_on
description: Giao thức điều phối Sub-Agents bắt buộc & Ma trận Multi-Agent Swarm (ARF / VRF / ABV).
---

# 🤖 ARF SUBAGENTS: GIAO THỨC ĐIỀU PHỐI MULTI-AGENT SWARM (ARF v2.5)

> **CHỈ THỊ TỐI CAO (ANTIGRAVITY IDE):** Nạp tự động (`always_on`). Bắt buộc kích hoạt Sub-Agents song song, triệt tiêu hoàn toàn thực thi đơn lẻ nhằm tối ưu hóa chất lượng kịch nghệ, tốc độ và chống quá tải ngữ cảnh:

---

## 1. GIAO THỨC PHẢN XẠ BẮT BUỘC (MANDATORY REFLEX PROTOCOL)
Khi nhận bất kỳ nhiệm vụ nào thuộc danh mục sau:
- **Dịch thuật tài liệu dài:** Bước 02 (`arf_02`) khi dung lượng $W_{en} > 1.200$ từ.
- **Biên kịch & Nhịp thở phát thanh:** Bước 05 (`arf_05`) & Bước 06 (`arf_06`) trên $N$ raw chunks.
- **Đạo diễn kịch nghệ phân vai:** Bước 08A (`arf_08a_theatrical_voice_director`).
- **Quy trình tổng thể:** `Make-audio-script-process`, `Make-audio-bgm-process`, hoặc `universal-audiobook`.
- **Xử lý đa chương:** Toàn bộ dự án sách có $M > 1$ chương (`Cross-Chapter Swarm`).
- **Kịch bản Video Storyboard:** Phân tích bảng phân cảnh (`vrf_01_script_to_video_storyboard`).
- **Sản xuất hình ảnh AI:** Tạo ảnh phân cảnh storyboard (`vrf_02_storyboard_to_images`).
- **Dựng video phân cảnh:** Render video MP4 theo shot/kịch bản (`vrf_03_video_renderer`).
- **Master Visual Prompts & Backgrounds:** Thiết lập ý niệm & xuất bản ảnh nền 16:9 (`abv_01_thematic_visual_prompter`).
- **Dựng Video Sách Nói hàng loạt:** Dựng & kết xuất video 1080p hàng loạt (`abv_02_audiobook_video_compiler`).

👉 **LƯỢT GỌI CÔNG CỤ ĐẦU TIÊN CỦA BẠN BẮT BUỘC PHẢI LÀ `invoke_subagent`**.

---

## 2. NGUYÊN TẮC CẤM THỰC THI ĐƠN LẺ (ZERO-SOLO & NO-BYPASS INVARIANT)
1. **Cấm tự sửa file trực tiếp:** Tuyệt đối CẤM AI Chính tự ý dùng `replace_file_content` hoặc `write_to_file` để tự dịch, tự sửa chunks hoặc tự biên soạn `theatrical_script.json` một mình trong phiên chính.
2. **Cấm dùng script Python regex làm tắt:** Tuyệt đối CẤM AI Chính dùng `run_command` chạy các script Python trong `core/` (`process_chapter_scripts`, `theatrical_voice_director.py`) nhằm mục đích sinh kịch bản hay phân vai thay cho Sub-agents. Các script trong `core/` chỉ là công cụ kiểm toán và thư viện kỹ thuật tất định, không có khả năng cảm thụ văn học hay phân vai sống động của LLM.
3. **Chế tài hủy bỏ (Void on Solo Bypass):** Mọi kịch bản, bản dịch hay tệp phân vai JSON thiếu bản ghi tool call `invoke_subagent` ĐỀU BỊ COI LÀ VI PHẠM AN TOÀN HỆ THỐNG VÀ BỊ CỔNG QC BƯỚC 07 / 08 KHÓA CỨNG, TỪ CHỐI XUẤT XƯỞNG.

---

## 3. MA TRẬN PHÂN BỔ SUB-AGENTS BẮT BUỘC THEO MODULE
### A. Audiobook Pipeline (ARF Skills 01 - 10)
- **Bước 02 (Dịch thuật $W_{en} > 1.200$ từ):** Chia nhỏ 800 – 1.200 từ/đoạn. Kích hoạt ĐỒNG THỜI mảng 2 – 3 Subagents (`Role: "Author Style Translator [Part X]"`) dịch song song kèm Rolling Context (1 câu tóm tắt + 3 câu tiếng Việt cuối đoạn trước).
- **Bước 05 & 06 (Biên kịch $N$ Raw Chunks):** AI chính phân rã $N$ raw chunks, kích hoạt ĐỒNG THỜI mảng Subagents (`Role: "Audiobook Script & Breathing Refiner [Chunk X]"`) xử lý song song. Mỗi Sub-agent phụ trách 1-2 chunks độc lập (nhịp thở `. ......`, caesura thi ca, câu $\le 30$ từ, breathing commas, sạch ký tự cấm).
- **Bước 08A (Đạo diễn Kịch nghệ):** Bắt buộc kích hoạt ĐỒNG THỜI Hội đồng tối thiểu 4 – 5 Subagents:
  1. `Speaker Attribution Director`: Bóc tách ranh giới thoại nhân vật vs lời dẫn chuyện vs thơ ca.
  2. `Character Bible Profiler`: Thiết lập `.theatrical_bible.json` (5 độ tuổi, 10 khí chất, dải Pitch $-8\text{Hz} \to +12\text{Hz}$).
  3. `Dramatic Setting & Emotional Dynamics`: Phân tích bối cảnh quyền lực & gán 12 cảm xúc phân cảnh.
  4. `Poetic Prosody & Narrator Director`: Đạo diễn Người dẫn chuyện 8 sắc thái & ngâm vịnh thi ca caesura (`rate: -18%`, `pitch: -2Hz`, đệm thở 3 tầng).
  5. `Theatrical Dramaturg & Continuity QC`: Thẩm định handoff êm ái khóa cứng `[0.45s – 1.20s]`, tính nhất quán và chốt `theatrical_script.json`.

### B. Video Storyboard Pipeline (VRF Skills 01 - 03)
- **VRF-01 (Kịch bản Video Storyboard):** Kích hoạt ĐỒNG THỜI Hội đồng tối thiểu 3 – 4 Subagents:
  1. `Narrative & Pacing Beat Director`: Bóc tách mạch kịch tính theo Acts/Beats, tính pacing [15s – 28s/ảnh], bao phủ 100% câu chữ audio.
  2. `Cinematographer & Camera Movement Director`: Cự ly khung hình (EWS/WS/MS/CU), góc máy, chuyển động Ken Burns & transition.
  3. `Visual Prompt Engineer & Art Stylist`: Master English Prompts 7 tầng chi tiết cho Midjourney/FLUX/SDXL, phục trang, bối cảnh, Negative Prompts.
  4. `Continuity & Visual QC Lead`: Thẩm định tính liên tục thị giác, đối soát 100% audio vs ảnh, xuất bản `storyboard_video/Kich-ban-N.md`.
- **VRF-02 (Sản xuất Hình ảnh AI):** Kích hoạt song song theo từng batch 2-3 shots/agent gọi `generate_image` tỷ lệ 16:9 $\to$ lưu tại `storyboard_video/kich-ban-N/images/`.
- **VRF-03 (Biên dịch & Render Video MP4):** Khi render hàng loạt nhiều kịch bản/chương, kích hoạt Sub-agents song song theo từng kịch bản/chương độc lập (`Video Compiler Coordinator [Kich-ban-N]`).

### C. Audiobook Video Pipeline (ABV Skills 01 - 02)
- **ABV-01 (Master Prompts & Backgrounds):** Hội đồng Sub-agents (`Visual Concept Director`, `Historical & Cultural Stylist`, `Visual Prompt Engineer`) phân tích tác phẩm xuất bản 10 Master Prompts và thư viện backgrounds 16:9.
- **ABV-02 (Dựng Video Sách Nói Hàng Loạt):** Mảng Sub-agents song song (`Video Batch Renderer Coordinator [Batch X]`) phân chia theo từng lô chương (2-4 video/agent).

### D. Cross-Chapter Swarm (Toàn sách $M > 1$ chương)
- AI Chính điều phối song song mảng Sub-agents theo từng chương độc lập (`Chapter Coordinator [Chap X]`).

---

## 4. BẢNG PHÂN ĐỊNH THẨM QUYỀN THỰC THI TUYỆT ĐỐI
| Loại Tác Vụ | Phương Thức Thực Thi | Các Bước Cụ Thể |
| :--- | :--- | :--- |
| **Kỹ thuật tất định (< 2s)** | AI Chính tự chạy script Python | Bước 01 (Extract PDF), Bước 03 (Số hóa), Bước 04 (Chunking), Bước 07 (QC 7 Gates), Bước 08B (TTS rendering), Bước 09 & 10 (Ghép Full & Hòa âm BGM), VRF-03/ABV-01/ABV-02 khi chạy đơn lẻ cho 1 kịch bản/chương. |
| **Tư duy nghệ thuật & Đa chương** | BẮT BUỘC 100% qua `invoke_subagent` | Bước 02 ($W > 1.200$), Bước 05 & 06 (Biên kịch chunks), Bước 08A (Hội đồng kịch nghệ), VRF-01 (Hội đồng Storyboard), VRF-02 (Tạo ảnh batch), VRF-03 hàng loạt, ABV-01, ABV-02 hàng loạt, Cross-Chapter Swarm. |
