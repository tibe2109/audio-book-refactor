# 🤖 AGENTS.md — UNIVERSAL AUDIOBOOK PIPELINE (v2.0)
## SPECIFICATION & OPERATIONAL PLAYBOOK FOR AI AGENTS (ANTIGRAVITY, CLAUDE CODE, CODEX, CURSOR)

> **MỤC TIÊU CỐT LÕI DÀNH CHO AI:**  
> File này là tài liệu nạp ngữ cảnh tối cao (Universal Agent Directive) cho mọi mô hình AI khi mở thư mục dự án này. Bất kể bạn là Google Antigravity, Anthropic Claude Code, OpenAI Codex, Cursor hay Gemini Pro: Khi người dùng giao nhiệm vụ liên quan đến sản xuất sách nói, bạn **PHẢI** đọc hiểu và tuân thủ các quy chuẩn dưới đây.

---

## 1. BƯỚC KHỞI ĐỘNG TỰ THÂN CỦA AI (AI SELF-BOOTSTRAPPING PROTOCOL)

Khi bạn (AI) vừa được khởi chạy trong thư mục này trên một máy tính mới:
1. **Kiểm tra Hệ điều hành & Python:**
   - Chạy lệnh kiểm tra: `python --version` (hoặc `python3 --version`).
   - Yêu cầu tối thiểu: Python >= 3.10.
2. **Kiểm tra & Kích hoạt Môi trường ảo (venv):**
   - Nếu chưa có thư mục `venv/`:
     - Trên Windows: Chạy lệnh `setup.bat` hoặc `python -m venv venv && .\venv\Scripts\pip install -r requirements.txt`.
     - Trên Linux/macOS: Chạy lệnh `bash setup.sh` hoặc `python3 -m venv venv && ./venv/bin/pip install -r requirements.txt`.
3. **Kiểm tra Công cụ FFmpeg:**
   - Kiểm tra `ffmpeg` trong PATH hoặc trong `tools/ffmpeg/`.
   - Nếu thiếu, thư viện `imageio-ffmpeg` trong `requirements.txt` sẽ tự động fallback an toàn.

---

## 2. BẢY QUY TẮC THÉP BẤT BIẾN (NON-NEGOTIABLE CONSTRAINTS)

1. **Khóa Cứng Thời Lượng [25 – 35 phút] (Duration Hard-Cap):**
   - Mọi file Audio Full (Bước 09) và Final Master (Bước 10) phải nằm trong khung **[25 – 35 phút]**.
   - **TUYỆT ĐỐI KHÔNG TẠO RA BẤT KỲ FILE NÀO VƯỢT QUÁ 35 PHÚT**. Nếu nội dung dài, giải thuật toán học sẽ tự động chia đều thành nhiều Parts (Part 1, Part 2...).
2. **Bảo Toàn Thuật Ngữ & Chiến Lược Biên Tập 3 Tầng (NamMinh x Brian & Anti-Auditory Fatigue):**
   - **Tầng 1 (Định vị ban đầu):** Thuật ngữ chuyên ngành tiếng Anh/Latinh (Project Charter, Agile, Stakeholder, Scope Creep...) phải giữ nguyên ký tự quốc tế ở lần giới thiệu đầu tiên hoặc đề mục mới để giọng `en-US-BrianMultilingualNeural` đọc chuẩn xác. Tuyệt đối không phiên âm bồi thô thiển.
   - **Tầng 2 (Nhắc lại có chọn lọc):** Chỉ nhắc lại thuật ngữ ngoại ngữ ở các đề mục lớn (H1/H2) khi thực sự cần thiết để tái định vị ngữ cảnh thính giác.
   - **Tầng 3 (Biên tập thân bài linh hoạt bằng AI):** Trong thân bài diễn giải, AI biên tập viên chủ động chuyển đổi linh hoạt sang tiếng Việt tự nhiên (*Stakeholder* $\to$ *các bên liên quan*, *Project Charter* $\to$ *bản điều lệ dự án*), dùng từ viết tắt tách âm phát thanh (*P-M-I*, *P-M-B-O-K*, *W-B-S*, *K-P-I*) hoặc đại từ thay thế gần gũi ngắn gọn. Tuyệt đối tránh lặp từ ngoại ngữ liên tục gây đảo giọng TTS và mỏi tai người nghe. Phải do AI trực tiếp thẩm định ngữ cảnh, cấm dùng script cứng thay thế mù quáng. Khi tài liệu dài, kích hoạt Sub-agent chuyên trách.
   - **Điều phối nhịp điệu thính giác (Ngắt nghỉ điểm nhấn vs. Đọc liền mạch mềm mại):** Dùng dấu phẩy `, ` tạo nhịp nghỉ phát thanh (~220ms) khi thuật ngữ đi kèm sau tên tiếng Việt giải thích/đề mục để người nghe ghi nhớ; đọc và ghép âm liền mạch 100% êm ái (vùng đệm chuyển giao 80ms, bảo toàn đuôi âm -50dB) không giật cục khi thuật ngữ nằm trong dòng chảy ngữ pháp liên tục (*các Project Manager*, *Tên tôi là Rachel*, *tại Google New York*). Áp dụng thang tốc độ ngoại ngữ thích ứng linh hoạt theo độ dài (1 từ/viết tắt: `-24%`, 2-3 từ: `-18%`, $\ge 4$ từ: `-15%`) để phát âm tròn vành rõ chữ, tuyệt đối không nuốt âm và không buồn ngủ. 100% tiếng Việt do giọng Việt đọc, 100% tiếng nước ngoài do giọng Brian đọc.
3. **Cổng Kiểm Toán Không Nhân Nhượng (Hard QC Gate at Step 07):**
   - Chỉ được phép cấp quyền thu âm TTS (Bước 08) khi tệp `QC_Report.md` được thẩm định **100% 7 Gates PASSED**.
   - Nếu phát hiện lỗi ký tự cấm, câu dài, sót số trần hoặc tỷ lệ từ vựng không đạt ($R < 75\%$), AI phải kích hoạt vòng lặp tự chữa lành (**Self-Healing Loop**) để sửa kịch bản trước khi đi tiếp.
4. **Đánh Giá Thể Loại & Chiến Lược Âm Thanh Linh Hoạt (Adaptive Genre & Audio Strategy):**
   - **Văn học đa thể loại / Kịch nghệ / Sử thi:** Thẩm định sâu sắc trên đa dạng văn học thế giới (Sử thi cổ điển, Hiện thực phê phán, Tâm lý hiện sinh/Trinh thám, Tùy bút hồi ký, Kiếm hiệp huyền huyễn, Triết học). Kích hoạt Phân vai Kịch nghệ Đa thanh (tiến hóa 5 giai đoạn đời người, 10 khí chất bản thể, 12 cảm xúc phân cảnh, dải tương phản Pitch mở rộng -8Hz đến +12Hz). Kết hợp **Khung Dẫn Chuyện Đa Sắc Thái Thích Ứng** (chủ động điều biến Hào hùng chiến trận, Bi tráng xót xa, Hồi hộp rình rập, Chiêm nghiệm hoài cổ, U uất xã hội, Trào phúng mỉa mai, Nội tâm hiện sinh, Bình nhật tự nhiên) và **Động Cơ Tổng Hợp Âm Sắc Thích Ứng (ATSE)** 4 trục formant DSP giải phóng giới hạn preset cứng. Bắt buộc Pre-Review kịch bản lập `.theatrical_bible.json` trước khi thu âm và áp dụng Two-Stage Dynamic Leveling (-16 LUFS, LRA=5-6) chống nhảy vọt âm lượng. Ở các khâu kịch bản (Steps 03 - 06): Bảo tồn 100% âm Hán-Việt (nhân vật, chức danh, địa danh cổ), số hóa cổ kính (*canh ba, ba vạn quân, hai mươi trượng*), bảo toàn trọn vẹn màn đối thoại cao trào gay cấn trong cùng chunk, tiêu đề chương hồi câu đối biền ngẫu viết IN HOA toàn bộ kèm `. ......` (1.8s - 2.0s), giữ trọn khẩu khí và đại từ xưng hô cổ kính (*Chúa công, Quân sư, Thưa Đức ông*). **Acoustic Poetic Calibration & Recitation Engine (Chuẩn hóa thi ca & Zero Robotic Poetics):** Bắt buộc 100% câu thơ bóc tách thành dòng độc lập `type: "poem"`, kết thúc bằng dấu câu; ngắt nhịp vi mô caesura `, ` theo thể thơ; tốc độ ngâm chậm rãi `rate: -18%`, cao độ trầm vang `pitch: -2Hz`, bộ lọc `timbre_eq: "poetic_recitation"`; cấu trúc đệm thở 3 tầng (Lead-in 0.52s - 0.98s, Inter-verse 0.55s, Ending coda 1.00s - 1.20s `. ......`) tạo khoảng lặng ngân vang lắng đọng.
   - **Tự lực / Phát triển bản thân:** Giọng cố vấn truyền cảm hứng (`Tôi - Bạn`), trầm ấm (`Pitch -2Hz`), nhịp đĩnh đạc, nhấn sâu bài học chiêm nghiệm (`. ......` 1.8s). Khóa cứng 1 giới tính xuyên suốt (Nam: 100% Nam Minh x Brian, Nữ: 100% Hoài My x Emma).
   - **Khoa học / Kỹ thuật / Quản trị:** Giọng phát thanh chuyên gia học thuật, khách quan, sắc nét (`Pitch 0Hz`), tách âm viết tắt (*P-M-I*), Brian đọc ngoại ngữ chuẩn. Khóa cứng 1 giới tính.
5. **Kỷ Luật Quản Lý Tệp Tin & Giữ Vững Thư Mục Gốc (Root Cleanliness & File Hygiene):**
   - **Tuyệt đối KHÔNG tạo file tạm ở thư mục gốc (Root):** Cấm mọi hành vi tạo script thử nghiệm (.py), file audio nháp (.mp3), file log (.txt) hoặc file cờ không đuôi trực tiếp tại thư mục gốc. Mọi tệp thử nghiệm ngắn hạn phải nằm trong `scratch/` hoặc thư mục riêng của từng chương.
   - **Tổ chức theo dự án biệt lập & Lưu trữ tập trung:** Dữ liệu sách nằm trong `Kich-ban-clipchamp/<Tên-Sách>/` hoặc `input_books/<Tên-Sách>/`. Từ điển riêng (`custom_phonetics.json` / `pmbok_custom_phonetics.json`) phải đặt bên trong thư mục của cuốn sách đó. Toàn bộ file Full (không nhạc) xuất xưởng của các chương được gom tập trung vào thư mục `Full-[tên-sách]/`, và toàn bộ file Final Master (có nhạc) xuất xưởng được gom tập trung vào `Final-[tên-sách]/`. Tuyệt đối KHÔNG lưu file Full hoặc Final vào từng thư mục con của chương.
   - **Tự động dọn dẹp sau khi hoàn thành:** Sau khi Bước 10 xuất xưởng file `Final_Audio_*.mp3` đạt chuẩn, hệ thống tự động dọn sạch các tệp trung gian (`concat_list.txt`, `.chunk_*.txt`, `.raw_part*.txt`) để không gian làm việc luôn gọn gàng và tối ưu bộ nhớ.
6. **Bảo Toàn Nội Dung Gốc Tuyệt Đối (End-to-End Content Fidelity & Zero-Loss Invariant):**
   - **Bảo toàn thông tin toàn diện:** Mọi bước biến đổi văn bản (Bóc tách PDF $\to$ Dịch thuật AI $\to$ Chuẩn hóa ngữ âm $\to$ Chia đoạn $\to$ Tinh chỉnh câu $\to$ Thu âm $\to$ Ghép Master) bắt buộc phải là các phép biến đổi **bảo toàn thông tin (Information-Preserving)**. Tuyệt đối không được bỏ sót, cắt xén bất kỳ phân đoạn, giai thoại, ví dụ, công thức hay số liệu nào của tác giả gốc.
   - **Khóa cứng Tỷ lệ Giãn nở Từ vựng (Expansion Ratio Check):** Tỷ lệ từ vựng giữa bản dịch tiếng Việt so với bản gốc tiếng Anh ($R = \frac{\text{Số từ Tiếng Việt}}{\text{Số từ Tiếng Anh}}$) bắt buộc phải đạt $R \ge 0.85$ ở Bước 02 và $R \ge 0.75$ ở Bước 07. Bất kỳ kết quả nào thấp hơn ngưỡng này đều bị coi là **hành vi tự ý tóm tắt bất hợp lệ (Invalid Summarization)** và bị từ chối xuất xưởng.
   - **Đồng nhất văn phong & Ngữ cảnh gối đầu khi phân đoạn (Rolling Context & Persona Anchor):** Khi chương dài ($> 1.200$ từ) được chia thành nhiều đoạn hoặc giao Subagents xử lý, bắt buộc áp dụng cơ chế khóa cứng ngôi xưng (`Tôi - Bạn`), nạp chung từ điển thuật ngữ (`custom_phonetics.json`) và truyền kèm 3 câu dịch cuối cùng của đoạn trước (`trailing_context`) làm điểm gối đầu ngữ cảnh. Đảm bảo toàn bộ các phân đoạn ăn khớp hoàn hảo về văn phong, nhịp điệu và không lộ vết cắt ghép.
   - **Bảo toàn cấu trúc âm thanh:** Ký hiệu nhịp thở `. ......` bắt buộc phải tạo khoảng lặng phát thanh đúng 1.5 giây sau các tiêu đề in hoa; quá trình khử khoảng lặng (silenceremove) phải bảo toàn đuôi âm khẽ (-50dB) để không nuốt chữ. Ghép nối file Full phải đối soát thời lượng thực tế với tổng thời lượng chunk ($\Delta t \le 2.0s$).
7. **Giao Thức Phản Xạ Bắt Buộc Kích Hoạt Sub-Agents & Triệt Tiêu Thực Thi Đơn Lẻ (Mandatory Subagent Dispatch & Zero-Solo Enforcement):**
   - **GIAO THỨC PHẢN XẠ BẮT BUỘC (MANDATORY REFLEX PROTOCOL):** Khi nhận bất kỳ nhiệm vụ nào liên quan đến:
     * Dịch thuật tài liệu dài (Bước 02 khi $W_{en} > 1.200$ từ)
     * Biên kịch cấu trúc nhịp thở & tinh chỉnh câu (Bước 05 & Bước 06 trên $N$ raw chunks)
     * Đạo diễn kịch nghệ phân vai & ngâm thơ (Bước 08A)
     * Toàn bộ quy trình kịch bản (`Make-audio-script-process`) hoặc quy trình toàn năng (`universal-audiobook`)
     * Xử lý đa chương song song (`Cross-Chapter Swarm`)
     * Phân tích kịch bản video storyboard & thiết lập bảng phân cảnh (`vrf_01_script_to_video_storyboard`)
     * Sản xuất hình ảnh AI phân cảnh storyboard (`vrf_02_storyboard_to_images`)
     * Điều phối dựng video phân cảnh hàng loạt (`vrf_03_video_renderer`)
     * Thiết lập ý niệm & xuất bản 10 Master Prompts ảnh nền video (`abv_01_thematic_visual_prompter`)
     * Điều phối dựng và kết xuất Video Sách Nói chuẩn 1080p hàng loạt (`abv_02_audiobook_video_compiler`)
     * Nghiên cứu thị trường thính giả & xuất bản YouTube SEO Metadata chuẩn mực (`abv_03_youtube_seo_publisher`)
     * Điều phối đăng tải video và kịch bản SEO hàng loạt lên YouTube (`abv_04_youtube_batch_uploader`)
     👉 **LƯỢT GỌI CÔNG CỤ ĐẦU TIÊN CỦA BẠN BẮT BUỘC PHẢI LÀ `invoke_subagent`**.
   - **TUYỆT ĐỐI CẤM THỰC THI ĐƠN LẺ & CẤM DÙNG SCRIPT PYTHON REGEX LÀM TẮT (ZERO-SOLO & NO-BYPASS INVARIANT):**
     * **CẤM** AI Chính tự ý dùng `replace_file_content` hoặc `write_to_file` để tự dịch, tự sửa chunks hoặc tự viết `theatrical_script.json` một mình trong phiên chính.
     * **CẤM** AI Chính dùng `run_command` để chạy các script Python trong `core/` (`process_chapter_scripts`, `theatrical_voice_director.py`) nhằm mục đích sinh kịch bản hay phân vai thay cho Sub-agents. Các file Python trong `core/` CHỈ là thư viện kỹ thuật và công cụ kiểm toán, tuyệt đối không có tư duy ngôn ngữ và xúc cảm nghệ thuật của LLM.
     * **Chế tài hủy bỏ (Void on Solo Bypass):** Bất kỳ kịch bản hay file phân vai nào được tạo ra đơn lẻ mà không có dấu vết tool call `invoke_subagent` trong phiên làm việc ĐỀU BỊ COI LÀ VI PHẠM AN TOÀN HỆ THỐNG VÀ BỊ CỔNG QC BƯỚC 07 / BƯỚC 08 KHÓA CỨNG, TỪ CHỐI XUẤT XƯỞNG.
   - **Phân bổ năng lực cụ thể cho từng bước:**
     * **Bước 02 ($W > 1.200$ từ):** Bắt buộc chia 800 - 1.200 từ/đoạn và kích hoạt đồng thời 2-3 Sub-agents (`Role: "Author Style Translator [Part X]"`) dịch song song kèm Rolling Context 3 câu cuối.
     * **Bước 05 & 06 ($N$ chunks):** Sau khi AI chính phân rã $N$ raw chunks, kích hoạt **ĐỒNG LOẠT mảng Sub-agents chuyên môn song song** qua `invoke_subagent(Subagents=[...])`. Mỗi Sub-agent phụ trách đúng 1-2 chunks độc lập (áp dụng nhịp thở `. ......`, caesura thi ca, câu $\le 30$ từ, breathing commas). Toàn bộ chunks hoàn thành chỉ trong 1 - 1.5 phút!
     * **Bước 08A:** Bắt buộc kích hoạt **ĐỒNG THỜI Hội đồng tối thiểu 4 - 5 Sub-agents chuyên môn song song** (`Speaker Attribution Director`, `Character Arc & Bible Profiler`, `Dramatic Setting & Emotional Dynamics`, `Poetic Prosody & Narrator Director`, `Theatrical Dramaturg & Continuity QC`) xuất bản `theatrical_script.json` & `.theatrical_bible.json`.
     * **VRF-01 (Kịch bản Video Storyboard):** Bắt buộc kích hoạt **ĐỒNG THỜI Hội đồng tối thiểu 3 - 4 Sub-agents chuyên môn song song** (`Narrative & Pacing Beat Director`, `Cinematographer & Camera Movement Director`, `Visual Prompt Engineer & Art Stylist`, `Continuity & Visual QC Lead`) xuất bản `storyboard_video/Kich-ban-N.md`.
     * **VRF-02 (Sản xuất Hình ảnh AI):** Bắt buộc kích hoạt song song các Sub-agents theo từng lô shot (Batch 2-3 shots/agent) gọi `generate_image` với tỷ lệ 16:9 hoặc fallback đồng bộ sang thư mục `storyboard_video/kich-ban-N/images/`.
     * **VRF-03 (Biên dịch & Kết xuất Video MP4):** Khi kết xuất hàng loạt nhiều kịch bản/nhiều chương, kích hoạt Sub-agents song song theo từng kịch bản hoặc chương độc lập (`Video Compiler Coordinator [Kich-ban-N]`).
     * **ABV-01 (Master Visual Prompts & Backgrounds):** Bắt buộc kích hoạt Hội đồng Sub-agents chuyên môn (`Visual Concept Director`, `Historical & Cultural Stylist`, `Visual Prompt Engineer`) khi phân tích tác phẩm xuất bản 10 Master Prompts và thư viện backgrounds 16:9.
     * **ABV-02 (Dựng Video Sách Nói Hàng Loạt):** Khi kết xuất video cho toàn bộ tác phẩm gồm nhiều chương, bắt buộc kích hoạt mảng Sub-agents song song (`Video Batch Renderer Coordinator [Batch X]`) phân chia theo từng lô chương (2-4 video/agent) để tăng tốc gấp 3-5 lần.
     * **ABV-03 (Nghiên cứu Thị trường & YouTube SEO Publisher):** Bắt buộc kích hoạt Hội đồng Sub-agents chuyên môn (`Audience & Market Research Strategist`, `Chapter Literary & Narrative Analyst`, `YouTube SEO Copywriter & Prompt Architect`, `Upload Strategy & Series Batch Coordinator`, `SEO Quality Gate & Compliance Auditor`) khi xây dựng bộ Metadata YouTube chuẩn SEO và điều phối chiến lược xuất bản toàn tác phẩm (> 100 video).
     * **ABV-04 (Đăng tải Video & Kịch bản SEO Hàng Loạt):** Bắt buộc kích hoạt mảng Sub-agents song song (`Upload Batch Worker [Batch X]`, `Thumbnail & Asset Integrity Linker`, `Quota & Rate Limit Auditor`) phân chia theo từng lô video (2-3 video/agent) chạy song song (2–3 luồng tối ưu) để tải lên YouTube an toàn, tránh nghẽn mạng và kiểm soát Quota.
     * **Xử lý toàn sách ($M > 1$ chương):** AI chính điều phối song song mảng Sub-agents theo từng chương (`Cross-Chapter Swarm`).
   - **Tác vụ kỹ thuật tất định AI Chính tự chạy bằng script (< 2 giây):** Bước 01 (Extract PDF), Bước 03 (Số hóa num2words/regex), Bước 04 (Semantic chunking), Bước 07 (Kiểm toán QC 7 Gates), Bước 08B (Phòng thu TTS), Bước 09 & 10 (Ghép file & Hòa âm BGM), VRF-03 khi chạy đơn lẻ cho 1 kịch bản cụ thể (`core/vrf_video_compiler.py`), ABV-01 / ABV-02 khi chạy đơn lẻ cho 1 chương cụ thể (`core/abv_video_compiler.py`), ABV-03 khi chạy kiểm toán / sinh template kỹ thuật (`core/abv_youtube_seo_generator.py`), ABV-04 khi chạy kiểm tra trạng thái / upload đơn lẻ (`core/abv_youtube_uploader.py`).

---

## 3. SƠ ĐỒ DÂY CHUYỀN 10 BƯỚC KHÉP KÍN

| Bước | Mã Kỹ Năng / Module | Nhiệm Vụ Của AI | File Đầu Ra |
| :---: | :--- | :--- | :--- |
| **01** | `arf_01_pdf_structure_extractor` | Bóc tách cấu trúc PDF, khử Header/Footer/số trang, nối Drop-Cap. | `raw_original.txt` |
| **02** | `arf_02_author_style_translator` | Dual-Engine: 2A Phi hư cấu / 2B Văn học kinh điển. Kích hoạt mảng Sub-agents song song khi $W > 1.200$. | `translated.txt` |
| **03** | `arf_03_text_phonetics_normalizer` | Chuẩn hóa số học (100% viết chữ), tách âm viết tắt, bảo toàn Latinh. | `normalized.txt` |
| **04** | `arf_04_smart_audiobook_rechunker` | Phân rã khối đệm 2.500 - 3.500 ký tự theo ranh giới đoạn văn. | `Kich-ban-raw-*.txt` |
| **05** | `arf_05_script_structure_formatter` | Tiêu đề IN HOA đứng riêng, chèn `. ......`, phân tách thi ca & caesura. Điều phối Sub-agents song song. | Kịch bản có nhịp thở |
| **06** | `arf_06_llm_script_refiner` | Câu <= 30 từ, thêm breathing commas, sạch ký tự cấm. Điều phối Sub-agents song song theo từng chunk. | `Kich-ban-*.txt` |
| **07** | `arf_07_audiobook_qc_auditor` | Kiểm toán 7 Quality Gates & Thẩm định nguồn gốc Sub-agents. 100% PASSED mới mở khóa bước 08. | `QC_Report.md` |
| **08A** | `arf_08a_theatrical_voice_director` | Đạo diễn kịch nghệ: Phân vai đa thanh, ngâm vịnh thi ca, BẮT BUỘC điều phối Hội đồng $\ge 4-5$ Subagents song song. | `theatrical_script.json` & `.theatrical_bible.json` |
| **08B** | `arf_08_tts_neural_bgm_mixer` | Kỹ sư phòng thu TTS: Song thanh NamMinh x Brian, đệm 80ms, giữ đuôi âm -50dB, Two-Stage Leveling (-16 LUFS). | `audio_chunks/*.mp3` |
| **09** | `arf_09_audio_smart_aggregator` | Ghép chunk thành tập cân bằng thời lượng [25-35 phút]. Khóa cứng <= 35p. | `Full-[tên-sách]/Full_*.mp3` |
| **10** | `arf_10_bgm_dynamic_mixer` | Đạo diễn BGM thích ứng văn hóa/thể loại, tự động tải nhạc công quyền (yt-dlp), Vocal Pocket Carving EQ, Master EBU R128 (-16 LUFS). | `Final-[tên-sách]/Final_Audio_*.mp3` |

---

## 4. CÂU LỆNH ĐIỀU PHỐI DÀNH CHO AI (AGENT EXECUTION COMMANDS)

Khi thực thi trên Terminal / Command Line, AI sử dụng các lệnh chuẩn sau (Lưu ý: Các bước kỹ thuật 01, 07, 08B, 09, 10 do script chạy tự động; Các bước tư duy nghệ thuật 02, 05, 06, 08A do AI Chính điều phối mảng Sub-agents qua `invoke_subagent` trước khi mở khóa phòng thu):

```bash
# 1. Kiểm toán 7 Quality Gates độc lập bằng Python (Bước 07):
python -c "import sys; sys.path.insert(0, 'core'); from universal_audiobook_workflow import UniversalAudiobookWorkflow; wf = UniversalAudiobookWorkflow('input_books/Tên-Sách', '01-chuong-1'); print(wf.audit_quality_gates())"

# 2. Chạy phòng thu âm & hoàn thiện BGM (Bước 08B đến 10) sau khi kịch bản đã qua Sub-agents và QC:
python core/antigravity_audiobook_pipeline.py --book_dir "input_books/Tên-Sách" --chapter "01-chuong-1"

# 3. Chạy hậu kỳ âm thanh toàn bộ các chương đã đạt QC:
python core/antigravity_audiobook_pipeline.py --book_dir "input_books/Tên-Sách" --all
```

---

## 5. THƯ VIỆN KỸ NĂNG CÓ SẴN (SKILLS DIRECTORY)
Dự án lưu trữ sẵn toàn bộ các kỹ năng chuẩn ở 4 hệ thống mirror đồng bộ 100% để mọi AI đều nạp được:
- `.agent/skills/` (Tương thích Cursor, Claude Code, Cline)
- `.agents/skills/` (Tương thích Google Antigravity Workspace Root)
- `.gemini/skills/` (Tương thích Google Gemini CLI & IDE)
- `.agy/skills/` (Tương thích Antigravity Swarm Core)

Mỗi kỹ năng đều có tài liệu `SKILL.md` hướng dẫn chi tiết prompt, input/output contract và kịch bản kích hoạt Subagent.
