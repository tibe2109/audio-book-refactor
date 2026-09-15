---
trigger: always_on
description: Quy tắc cốt lõi & tiêu chuẩn chất lượng không khoan nhượng cho Audio Book Pipeline (ARF Skills 01 - 10).
---

# 📜 ARF RULES: QUY TẮC BẤT BIẾN AUDIOBOOK PIPELINE (ARF v2.5)

> **CHỈ THỊ TỐI CAO (ANTIGRAVITY IDE):** Nạp tự động (`always_on`). Mọi tác vụ bóc tách, dịch thuật, chuẩn hóa, phân đoạn, biên kịch, kiểm toán, thu âm TTS và hòa âm BGM **BẮT BUỘC** tuân thủ 9 nhóm quy tắc:

---

## 1. QUẢN TRỊ HỆ THỐNG, SESSION MANIFEST & VỆ SINH THƯ MỤC
1. **Vị trí kịch bản:** Kịch bản hoàn chỉnh tại `[book]/[chapter]/kich-ban/Kich-ban-N.txt`. File thô `raw_original.txt`, `translated.txt`, `normalized.txt` và `QC_Report.md` nằm tại thư mục gốc của chương.
2. **Lưu trữ tập trung:** Audio Full (không nhạc, B09) gom tại `Full-[tên-sách]/Full_{chap}_{part}.mp3`; Final Master (có nhạc, B10) gom tại `Final-[tên-sách]/Final_Audio_{chap}_{part}.mp3`. **CẤM** lưu Full/Final vào thư mục con của chương.
3. **Vệ sinh thư mục gốc:** Cấm tạo script (.py), audio (.mp3), log (.txt), file tạm tại root. Thử nghiệm phải lưu trong `scratch/` hoặc thư mục riêng của chương.
4. **Tự động dọn dẹp:** Xóa `Kich-ban-raw-*.txt` sau B06; xóa `concat_list.txt`, `.raw_part*.txt`, `.chunk_*.txt` sau B10.
5. **Cơ chế Manifest & Atomic Resume:** File `.session_manifest.json` là la bàn duy nhất. Sau sự cố: SKIP chương đã `completed` (file $> 100$ bytes, $R \ge 0.85$); xử lý chương dang dở. Cập nhật manifest nguyên tử sau mỗi chương.

---

## 2. BẢO TOÀN NGUYÊN TÁC & CHỐNG TÓM TẮT (ZERO-SUMMARIZATION)
1. **Bảo toàn 100%:** Mọi biến đổi văn bản phải bảo toàn trọn vẹn nội dung gốc. Cấm tóm tắt, cắt xén luận điểm, nghiên cứu, số liệu, ví dụ.
2. **Khóa cứng Tỷ lệ Dãn nở Từ vựng ($R = W_{vi} / W_{en}$):**
   - **Bước 02 (`arf_02`):** $0.85 \le R \le 1.50$ (PASSED). Nếu $R < 0.80$: **HARD FAIL (BỊ TÓM TẮT)**, từ chối nghiệm thu, khóa quyền sang Bước 03, kích hoạt Self-Healing dịch lại.
   - **Bước 07 (`arf_07`):** Tổng từ kịch bản so với bản gốc phải đạt $R \ge 0.75$. Nếu $R < 0.75 \to$ Bật RED FLAG, cấm thu âm.
3. **Phân đoạn Tiền Dịch Thuật:** Khi $W_{raw} > 1.200$ từ tiếng Anh, bắt buộc chia khối 800 – 1.200 từ theo tiêu đề hoặc `\n\n` trước khi dịch để triệt tiêu nguy cơ LLM tóm tắt ngầm.
4. **Khóa Văn Phong, Dual-Engine & Ngữ Cảnh Gối Đầu (Rolling Context):**
   - **Phân định Dual-Engine:** Profile 2A (Phi hư cấu/Kinh doanh: ngôi `Tôi - Bạn`, súc tích, chuẩn thuật ngữ); Profile 2B (Văn học kinh điển: 5 trụ cột kịch nghệ, đa thanh, độc thoại nội tâm, bảo tồn khẩu khí nhân vật).
   - **Rolling Context:** Dịch đoạn $k \ge 2$, prompt bắt buộc kèm 1 câu tóm tắt ý trước + **3 câu tiếng Việt cuối đoạn $k-1$** (`trailing_context`) để bắt trọn nhịp văn và liên từ.
   - **Terminology Lock:** Toàn bộ phân đoạn nạp chung từ điển `custom_phonetics.json` để thuật ngữ đồng nhất 100%.
   - **Seam Smoothing:** Sau khi nối thành `translated.txt`, rà soát câu ranh giới tiếp giáp để liên từ (`mặt khác,`, `do đó,`) tiếp nối tự nhiên, không lộ vết cắt ghép.
5. **Khóa Độ Lệch Từ Vựng khi Tinh chỉnh (Bước 06):** $|\Delta W| / W \le 3\%$. Cấm tự ý paraphrase làm thay đổi câu chữ gốc.

---

## 3. CHIẾN LƯỢC BIÊN TẬP THUẬT NGỮ 3 TẦNG & TRẢI NGHIỆM THÍNH GIÁC
Triệt tiêu mỏi thính giác do đảo giọng (Voice Switching) liên tục giữa Nam Minh (VN) và Brian (EN):
1. **Tầng 1 (Định vị):** Giữ chữ quốc tế ở lần đầu xuất hiện kèm diễn giải tiếng Việt (*Stakeholder - các bên liên quan*).
2. **Tầng 2 (Nhắc lại chọn lọc):** Chỉ nhắc lại ngoại ngữ ở đề mục lớn (H1/H2) khi cần tái định vị ngữ cảnh.
3. **Tầng 3 (Thân bài linh hoạt):** Dùng tiếng Việt tự nhiên, từ viết tắt tách âm (*P-M-I*, *W-B-S*) hoặc đại từ thay thế; cấm lặp ngoại ngữ $\ge 3$ lần/đoạn.
4. **Phân luồng nhịp điệu:**
   - **Điểm nhấn (`pause_type: emphasis`):** Sau tiêu đề hoặc giải nghĩa $\to$ Dùng `, `, nghỉ vi mô 220ms (`apad=0.22`).
   - **Liền mạch (`pause_type: seamless`):** Trong dòng ngữ pháp $\to$ Không chèn chấm giả, đuôi âm `-50dB`, đệm khẩu hình 80ms (`apad=0.08`), ghép êm ái 100%.
5. **Bảo tồn cổ phong & văn học kinh điển:** Giữ trọn 100% âm Hán-Việt (nhân vật, chức danh phong kiến, địa danh cổ), số hóa cổ kính (*canh ba*, *năm Kiến An thứ năm*, *ba vạn quân*, *hai mươi trượng*), giữ trọn vần điệu thi ca.

---

## 4. QUY CHUẨN KỸ THUẬT KỊCH BẢN TTS & ZERO-DIGIT POLICY
1. **Zero-Digit 100%:** Tuyệt đối không sót `0-9`. Số đếm, %, thập phân, năm, tiền tệ phải viết bằng chữ tiếng Việt (`15` $\to$ `mười lăm`, `50%` $\to$ `năm mươi phần trăm`).
2. **Khử sạch ký tự cấm TTS:** Khử ngoặc kép `""“”`, `()[]`, `:`, gạch dài `—–`, markdown `#*_~|/\\`, icons/bullets (`▶●★✓•...`). Thay bằng `, ` hoặc khoảng trắng.
3. **Độ dài chunk:** Mỗi file `Kich-ban-N.txt` tối ưu **2.200 – 2.800 ký tự** (giới hạn cứng $\le 3.000$). Cắt tại cuối câu/đoạn trọn nghĩa do AI quyết định.
4. **Nhịp thở phát thanh chuẩn (`. ......`):** Dấu `. ......` (chấm, cách, 6 chấm) tạo khoảng lặng 1.5 – 2.0s sau tiêu đề IN HOA và kết luận sâu sắc. Cấm dùng `...`.
5. **Câu ngắn & Breathing Commas:** Câu $\le 30$ từ; thêm breathing commas `, ` sau liên từ (`tuy nhiên,`, `do đó,`) và mệnh đề dài $> 12$ từ để TTS lấy hơi tự nhiên.
6. **Đặc tả kịch bản văn học kinh điển & Acoustic Poetic Calibration (Steps 04 - 06):** Giữ trọn vẹn màn đối thoại cao trào gay cấn và khối độc thoại nội tâm trong cùng chunk ($\le 3.000$ ký tự); tiêu đề chương hồi câu đối biền ngẫu viết IN HOA toàn bộ kèm `. ......` (1.8s - 2.0s); bảo tồn khẩu khí và đại từ xưng hô cổ kính (*Chúa công, Quân sư, Thưa Đức ông*); đặt dấu phẩy lấy hơi phân định lời dẫn chuyện và lời thoại. **Quy chuẩn thi ca cổ (Zero Poetic Run-on):** 100% dòng thơ phải kết thúc bằng dấu câu (phẩy `, ` hoặc chấm `. `) để ngăn TTS đọc dồn dập như văn xuôi; chèn `. ......` sau lời dẫn thơ (*Có bài từ rằng,*, *Đó chính là,*), giữa các khổ thơ và sau câu thơ kết bài để tạo khoảng lặng ngân vang lắng đọng.

---

## 5. CỔNG KIỂM TOÁN KHÔNG KHOAN NHƯỢNG (STEP 07 HARD QC GATE)
1. **Điều kiện mở khóa thu âm:** Chỉ cấp quyền chạy Bước 08 khi `QC_Report.md` đạt **100% 7 Quality Gates PASSED**:
   - **G1:** Thư mục/File chuẩn `^[a-zA-Z0-9\-]+$` | **G2:** Chunk $\le 3.000$ ký tự, không rỗng.
   - **G3:** Sạch ký tự cấm | **G4:** Zero-digit 100% bằng chữ tiếng Việt (chấp nhận số cổ phong *canh ba, ba vạn quân* với văn học kinh điển).
   - **G5:** Cú pháp nhịp nghỉ `. ......` chuẩn | **G6:** $R \ge 0.75$ (Zero-summarization).
   - **G7:** Tuân thủ Chiến lược 3 tầng & chống lặp ngoại ngữ (hoặc bảo tồn 100% danh xưng/âm Hán-Việt cổ phong với văn học kinh điển).
2. **Vòng lặp tự chữa lành (Self-Healing Loop):** Gate nào FAIL: AI bắt buộc tự sửa trực tiếp kịch bản và audit lại. Cấm bypass sang Bước 08 khi chưa đạt 100% PASSED.

---

## 6. CHIẾN LƯỢC ÂM THANH LINH HOẠT THEO THỂ LOẠI & DUAL-VOICE TTS (STEPS 08A & 08B)
1. **Đánh giá Thể loại & Đạo diễn Kịch nghệ Tiền kỳ (Bước 08A - `arf_08a_theatrical_voice_director`):** AI Chính trực tiếp review kịch bản đã qua QC, phân loại linh hoạt:
   - **Văn học / Kịch nghệ đa thể loại:** Thẩm định sâu sắc 6 thể loại lớn (Sử thi cổ điển, Hiện thực phê phán, Tâm lý hiện sinh/Noir trinh thám, Tùy bút hồi ký, Kiếm hiệp huyền huyễn, Phi hư cấu). Kích hoạt Phân vai Đa thanh (tiến hóa 5 giai đoạn đời người, 10 khí chất bản thể, 12 cảm xúc phân cảnh, dải tương phản Pitch mở rộng -8Hz đến +12Hz).
   - **Khung Dẫn Chuyện Đa Sắc Thái Thích Ứng:** Điều biến 8 sắc thái linh hoạt theo dòng cảm xúc phân cảnh (Hào hùng chiến trận, Bi tráng xót xa, Hồi hộp rình rập, Chiêm nghiệm hoài cổ, U uất xã hội, Trào phúng mỉa mai, Nội tâm hiện sinh, Bình nhật tự nhiên).
   - **Động Cơ Thẩm Định Thi Ca & Ngâm Vịnh Chuyên Sâu (Zero Robotic Poetics):** Bắt buộc 100% dòng thơ bóc tách thành các entry độc lập `type: "poem"`, chèn nhịp vi mô caesura `, `, tốc độ chậm rãi `rate: -18%`, cao độ trầm vang `pitch: -2Hz`, bộ lọc `timbre_eq: "poetic_recitation"` và cấu trúc đệm thở 3 tầng (Lead-in 0.8s - 1.5s, Inter-verse 0.85s, Ending coda 1.5s - 1.8s `. ......`).
   - **Động Cơ Tổng Hợp Âm Sắc Thích Ứng (ATSE):** Điêu khắc 4 trục formant DSP (Body, Nasal, Presence, Air), giải phóng giới hạn preset cứng nhắc, cho phép kết hợp tự do hoặc truyền chuỗi FFmpeg parametric equalizer strings.
   - **Tự lực / Phát triển bản thân:** Giọng cố vấn truyền cảm hứng (`Tôi - Bạn`), trầm ấm (`Pitch -2Hz`), nhịp đĩnh đạc, nhấn sâu đúc kết triết lý (`. ......` 1.8s). Khóa cứng 1 giới tính.
   - **Khoa học / Kỹ thuật / Quản trị:** Giọng phát thanh chuyên gia học thuật, khách quan, sắc nét (`Pitch 0Hz`), tách âm viết tắt (*P-M-I*), Brian đọc ngoại ngữ chuẩn. Khóa cứng 1 giới tính.
   - **Điều phối Hội đồng $\ge 4-5$ Subagents song song:** Bóc tách thoại nhân vật vs lời dẫn vs thơ ca, tính toán handoff êm ái, xuất bản `theatrical_script.json` và `.theatrical_bible.json`.
2. **Kỹ Sư Phòng Thu Neural TTS (Bước 08B - `arf_08_tts_neural_bgm_mixer`):**
   - Tiếp nhận trực tiếp `theatrical_script.json` từ B08A, không phân tích lại kịch nghệ, triệt tiêu hoàn toàn xung đột.
   - Phân bổ ngôn ngữ: 100% tiếng Việt do giọng Việt đọc; 100% ngoại ngữ/viết tắt quốc tế do giọng Brian/Emma đọc. Cấm đổi giọng khi retry.
   - Cân bằng âm học 2 tầng (Two-Stage Leveling): Cắt dead-gap, giữ đuôi âm khẽ `-50dB`. Đệm chuyển giao khẩu hình 80ms (`pad_dur=0.08`). Áp dụng Two-Stage Dynamic Leveling (-16 LUFS, LRA=5-6) cho từng câu thoại và toàn chunk, triệt tiêu nhảy âm lượng khi đổi tone. Tốc độ ngoại ngữ: 1 từ/viết tắt: `-18%`, 2-3 từ: `-15%`, $\ge 4$ từ: `-12%`.

---

## 7. KHÓA CỨNG THỜI LƯỢNG [25 – 35 PHÚT] & CÂN BẰNG TOÁN HỌC (STEP 09)
1. **Khóa cứng thời lượng:** Audio Full (B09) và Final Master (B10) bắt buộc nằm trong **[25 – 35 phút]** ($\le 35$ phút). CẤM TẠO FILE > 35 PHÚT.
2. **Chia đều cân bằng & Thích ứng thể loại:** Gom chunk bám sát target [25 - 35 phút]. Văn học ưu tiên tính toàn vẹn của Hồi/Chương hoặc cao trào kịch tính; Phi hư cấu ưu tiên gom theo Miền Hiệu Suất / Cụm nguyên tắc. Với $T_{total} > 35$ phút: $N = \max(1, \text{round}(T_{total} / 30))$, mục tiêu $Target = T_{total} / N$.
3. **Đối soát thời lượng:** Chênh lệch thời lượng thực tế file Full so với tổng chunk phải đạt $\Delta t \le 2.0s$.

---

## 8. ĐẠO DIỄN ÂM NHẠC & HÒA ÂM BGM PHÁT THANH (STEP 10)
1. **AI Dynamic Scene-Scoring & Thích ứng thể loại:** AI chia 3 phân cảnh (Mở đầu $\to$ Kể chuyện $\to$ Đúc kết). Chọn màu sắc BGM thích ứng: Giao hưởng thính phòng/dân tộc cho văn học kinh điển; Acoustic/Piano truyền cảm hứng cho tự lực; Baroque 60 BPM/Deep Focus cho khoa học/quản trị. Cấm nhạc u ám.
2. **Volume Ducking & Crossfade:** BGM giảm mức $10\% - 12\%$ (`volume=0.10` - `0.12`) để tôn giọng đọc. Chuyển Scene dùng acrossfade 3s.
3. **True Seamless Part Cut:** Fade-in đúng 3s ở đầu Part 1; Fade-out đúng 5s ở cuối Part cuối. Điểm nối giữa các Part kế tiếp **bắt buộc cắt thô (Raw cut)** khớp thời gian, cấm chèn Fade-in/out làm gián đoạn người nghe.

---

## 9. ĐIỀU KHOẢN KHÓA CỨNG: BẮT BUỘC KÍCH HOẠT SUB-AGENTS & TRIỆT TIÊU THỰC THI ĐƠN LẺ (MANDATORY SUBAGENT DISPATCH & ZERO-SOLO ENFORCEMENT)

Áp dụng **Giao Thức Phản Xạ Bắt Buộc Kích Hoạt Sub-Agent** nhằm nâng cao chất lượng nghệ thuật, tốc độ thực thi vượt trội và triệt tiêu hoàn toàn nguy cơ quá tải ngữ cảnh (Context Exhaustion) hoặc suy giảm tư duy khi làm một mình:

1. **Giao Thức Phản Xạ Bắt Buộc (Mandatory Reflex Protocol):**
   - Khi nhận bất kỳ nhiệm vụ nào liên quan đến:
     * Dịch thuật tài liệu dài (Bước 02 khi $W_{en} > 1.200$ từ);
     * Định dạng cấu trúc nhịp thở & ngắt nhịp thi ca (Bước 05);
     * Tinh chỉnh câu ngắn $\le 30$ từ và breathing commas (Bước 06);
     * Đạo diễn kịch nghệ phân vai, ngâm thơ và điều biến dẫn chuyện (Bước 08A);
     * Thực hiện quy trình `Make-audio-script-process`, `Make-audio-bgm-process`, hoặc `universal-audiobook`;
     * Xử lý song song nhiều chương độc lập (`Cross-Chapter Swarm`).
   - 👉 **LƯỢT GỌI CÔNG CỤ ĐẦU TIÊN CỦA BẠN BẮT BUỘC PHẢI LÀ `invoke_subagent`**.

2. **Nguyên Tắc Cấm Thực Thi Đơn Lẻ & Cấm Script Python Làm Tắt (Zero-Solo & No-Bypass Invariant):**
   - **CẤM TỰ SỬA FILE TRỰC TIẾP:** Tuyệt đối CẤM AI Chính tự ý dùng `replace_file_content` hoặc `write_to_file` để tự dịch, tự sửa chunks hoặc tự biên soạn `theatrical_script.json` một mình trong phiên chính.
   - **CẤM DÙNG SCRIPT PYTHON REGEX LÀM TẮT:** Tuyệt đối CẤM AI Chính dùng `run_command` để chạy các script Python trong `core/` (`process_chapter_scripts`, `theatrical_voice_director.py`) nhằm mục đích sinh kịch bản hay phân vai thay cho Sub-agents. Các script Python trong `core/` CHỈ là thư viện kỹ thuật tất định và bộ kiểm toán, hoàn toàn không có khả năng cảm thụ văn học, thấu hiểu ngữ cảnh và phân vai sống động của LLM.
   - **Chế tài hủy bỏ (Void on Solo Bypass):** Bất kỳ kịch bản, bản dịch hay tệp phân vai JSON nào do AI Chính tự làm một mình hoặc chạy script Python regex làm tắt mà không có bản ghi tool call `invoke_subagent` ĐỀU BỊ COI LÀ VI PHẠM ĐIỀU KHOẢN AN TOÀN HỆ THỐNG VÀ BỊ CỔNG QC BƯỚC 07 / 08 KHÓA CỨNG, TỪ CHỐI XUẤT XƯỞNG.

3. **Ma Trận Phân Bổ Sub-agents Bắt Buộc Theo Từng Bước:**
   - **Bước 02 (Dịch thuật $W_{en} > 1.200$ từ):** Chia nhỏ 800 – 1.200 từ/đoạn, kích hoạt ĐỒNG THỜI mảng 2 – 3 Subagents (`TypeName: "self"`, `Role: "Author Style Translator [Part X]"`) dịch song song kèm Rolling Context 3 câu cuối.
   - **Bước 05 & 06 (Biên kịch $N$ Raw Chunks):** Sau khi AI chính phân rã $N$ raw chunks, BẮT BUỘC kích hoạt ĐỒNG THỜI mảng Subagents (`TypeName: "self"`, `Role: "Audiobook Script & Breathing Refiner [Chunk X]"`) xử lý song song từng chunk (nhịp thở `. ......`, caesura thi ca, câu $\le 30$ từ, breathing commas, Zero Poetic Run-on). Hoàn tất toàn bộ chunks trong 1 - 1.5 phút!
   - **Bước 08A (Đạo diễn Kịch nghệ Phân vai):** BẮT BUỘC kích hoạt ĐỒNG THỜI **Hội đồng tối thiểu 4 – 5 Subagents** (`TypeName: "self"`):
     1. `Speaker Attribution Director`: Bóc tách ranh giới thoại vs lời dẫn vs thơ ca.
     2. `Character Bible Profiler`: Lập hồ sơ `.theatrical_bible.json` (5 độ tuổi, 10 khí chất, dải Pitch $-8\text{Hz} \to +12\text{Hz}$).
     3. `Dramatic Setting & Emotional Dynamics`: Phân tích bối cảnh quyền lực & gán 12 cảm xúc phân cảnh.
     4. `Poetic Prosody & Narrator Director`: Đạo diễn Người dẫn chuyện 8 sắc thái & ngâm vịnh thi ca caesura (`rate: -18%`, `pitch: -2Hz`, đệm thở 3 tầng).
     5. `Theatrical Dramaturg & Continuity QC`: Thẩm định handoff êm ái `0.28s - 0.35s`, tính nhất quán và chốt `theatrical_script.json`.
   - **Xử lý Toàn Sách Đa Chương ($M > 1$):** BẮT BUỘC kích hoạt Subagents song song theo từng chương độc lập (`Cross-Chapter Swarm`).

4. **Bảng Phân Định Thẩm Quyền Thực Thi Tuyệt Đối:**
   - **Tác vụ AI Chính tự làm bằng Python script (< 2 giây):** Bước 01 (PDF extraction), Bước 03 (Số hóa num2words & Regex ngữ âm), Bước 04 (Semantic chunking), Bước 07 (Kiểm toán QC 7 Gates), Bước 08B (TTS studio rendering), Bước 09 & 10 (Ghép Part & Hòa âm BGM).
   - **Tác vụ BẮT BUỘC 100% GỌI `invoke_subagent`:** Bước 02 ($W > 1.200$), Bước 05-06 (Tinh chỉnh chunks song song), Bước 08A (Hội đồng 4-5 subagents kịch nghệ), Xử lý đồng thời đa chương.
