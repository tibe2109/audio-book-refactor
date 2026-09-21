---
trigger: always_on
description: Quy tắc kỹ thuật & tiêu chuẩn âm học Audio Book Pipeline (ARF Skills 01 - 10).
---

# 📜 ARF RULES: QUY TẮC KỸ THUẬT & CHẤT LƯỢNG ÂM HỌC (ARF v2.5)

> **CHỈ THỊ TỐI CAO:** Nạp tự động (`always_on`). Bắt buộc tuân thủ 8 quy chuẩn kỹ thuật âm học dưới đây (điều phối Sub-agents quy định tại `arf-subagents.md`):

---

## 1. QUẢN TRỊ HỆ THỐNG, MANIFEST & VỆ SINH THƯ MỤC
1. **Lưu trữ kịch bản:** Kịch bản hoàn chỉnh tại `[book]/[chapter]/kich-ban/Kich-ban-N.txt`. File thô `raw_original.txt`, `translated.txt`, `normalized.txt`, `QC_Report.md` tại gốc chapter.
2. **Kho tập trung:** File Full (không nhạc, B09) gom tại `Full-[tên-sách]/Full_{chap}_{part}.mp3`; Final Master (có nhạc, B10) gom tại `Final-[tên-sách]/Final_Audio_{chap}_{part}.mp3`. **CẤM** lưu Full/Final vào thư mục con chapter.
3. **Vệ sinh root:** Cấm tạo script (.py), audio (.mp3), log (.txt), file tạm tại root. Mọi tệp thử nghiệm phải nằm trong `scratch/` hoặc thư mục riêng của chương.
4. **Tự động dọn dẹp:** Xóa `Kich-ban-raw-*.txt` sau B06; xóa `concat_list.txt`, `.raw_part*.txt`, `.chunk_*.txt` sau B10.
5. **Manifest & Resume:** `.session_manifest.json` là la bàn duy nhất. Skip chapter `completed` (>100 bytes, $R \ge 0.85$); chỉ xử lý chapter dang dở. Cập nhật manifest nguyên tử sau mỗi chương.

---

## 2. BẢO TOÀN NGUYÊN TÁC & CHỐNG TÓM TẮT (ZERO-SUMMARIZATION)
1. **Bảo toàn 100%:** Giữ trọn vẹn nội dung gốc, luận điểm, dẫn chứng, số liệu, ví dụ. Cấm tóm tắt hoặc cắt xén.
2. **Khóa cứng Tỷ lệ Dãn nở Từ vựng ($R = W_{vi} / W_{en}$):**
   - *Bước 02 (`arf_02`):* $0.85 \le R \le 1.50$ (PASSED). Nếu $R < 0.80$: **HARD FAIL (BỊ TÓM TẮT)**, khóa sang B03, kích hoạt Self-Healing dịch lại.
   - *Bước 07 (`arf_07`):* Tổng từ kịch bản so với bản gốc $R \ge 0.75$. Nếu $R < 0.75 \to$ Bật RED FLAG, cấm thu âm.
3. **Phân đoạn Tiền Dịch Thuật:** Khi $W_{raw} > 1.200$ từ EN, bắt buộc chia khối 800 – 1.200 từ theo heading hoặc `\n\n` trước khi dịch để triệt tiêu tóm tắt ngầm.
4. **Dual-Engine & Rolling Context:**
   - *Profile 2A (Phi hư cấu/Kinh doanh):* Ngôi xưng `Tôi - Bạn`, súc tích, chuẩn hóa thuật ngữ.
   - *Profile 2B (Văn học/Kịch nghệ):* 5 trụ cột kịch nghệ, đa thanh, độc thoại nội tâm, bảo tồn khẩu khí nhân vật.
   - *Rolling Context:* Dịch đoạn $k \ge 2$, prompt bắt buộc kèm 1 câu tóm tắt ý trước + **3 câu tiếng Việt cuối đoạn $k-1$** (`trailing_context`).
   - *Terminology Lock & Seam Smoothing:* Nạp chung `custom_phonetics.json`; rà soát liên từ tiếp giáp sau khi nối `translated.txt`.
5. **Khóa Độ Lệch Từ Vựng (B06):** $|\Delta W| / W \le 3\%$. Cấm tự ý paraphrase làm thay đổi câu chữ gốc.

---

## 3. CHIẾN LƯỢC THUẬT NGỮ 3 TẦNG & TRẢI NGHIỆM THÍNH GIÁC
Chống mỏi thính giác do voice-switching Nam Minh (VN) - Brian (EN):
1. **Tầng 1 (Định vị):** Giữ chữ quốc tế ở lần đầu xuất hiện kèm diễn giải tiếng Việt (*Stakeholder - các bên liên quan*).
2. **Tầng 2 (Nhắc lại chọn lọc):** Chỉ nhắc lại ngoại ngữ ở đề mục lớn (H1/H2) khi cần tái định vị ngữ cảnh.
3. **Tầng 3 (Thân bài linh hoạt):** Dùng tiếng Việt tự nhiên, từ viết tắt tách âm (*P-M-I*, *W-B-S*) hoặc đại từ thay thế; cấm lặp ngoại ngữ $\ge 3$ lần/đoạn.
4. **Phân luồng nhịp điệu & Thang tốc độ ngoại ngữ:**
   - *Điểm nhấn (`pause_type: emphasis`):* Sau tiêu đề/giải nghĩa $\to$ Dùng `, `, nghỉ vi mô 220ms (`apad=0.22`).
   - *Liền mạch (`pause_type: seamless`):* Trong dòng ngữ pháp $\to$ Không chấm giả, đuôi âm `-50dB`, đệm khẩu hình 80ms (`apad=0.08`), ghép êm 100%.
   - *Thang tốc độ ngoại ngữ:* 1 từ/viết tắt: `-24%`, 2-3 từ: `-18%`, $\ge 4$ từ: `-15%`.
5. **Bảo tồn cổ phong & văn học:** Giữ trọn 100% âm Hán-Việt (nhân vật, chức danh, địa danh), số hóa cổ kính (*canh ba*, *năm Kiến An thứ năm*, *ba vạn quân*, *hai mươi trượng*), giữ trọn vần điệu thi ca.

---

## 4. QUY CHUẨN KỸ THUẬT KỊCH BẢN TTS & ZERO-DIGIT POLICY
1. **Zero-Digit 100%:** Tuyệt đối không sót `0-9`. Số đếm, %, thập phân, năm, tiền tệ viết bằng chữ tiếng Việt (`15` $\to$ `mười lăm`, `50%` $\to$ `năm mươi phần trăm`).
2. **Khử sạch ký tự cấm TTS:** Khử `""“”`, `()[]`, `:`, `—–`, markdown `#*_~|/\\`, icons/bullets `▶●★✓•...` $\to$ Thay bằng `, ` hoặc khoảng trắng.
3. **Độ dài chunk:** Mỗi file `Kich-ban-N.txt` tối ưu **2.200 – 2.800 ký tự** (giới hạn cứng $\le 3.000$). Cắt tại cuối câu/đoạn trọn nghĩa.
4. **Nhịp thở chuẩn (`. ......`):** Ký hiệu `. ......` (chấm, cách, 6 chấm) tạo khoảng lặng 1.5 – 2.0s sau tiêu đề IN HOA và kết luận sâu sắc. Cấm dùng `...`.
5. **Câu ngắn & Breathing Commas:** Câu $\le 30$ từ; thêm `, ` sau liên từ (`tuy nhiên,`, `do đó,`) và mệnh đề dài $> 12$ từ để lấy hơi tự nhiên.
6. **Văn học kinh điển & Thi ca cổ (Steps 04 - 06):**
   - Giữ trọn đối thoại kịch tính & độc thoại nội tâm trong cùng chunk ($\le 3.000$ ký tự).
   - Tiêu đề chương hồi câu đối biền ngẫu viết IN HOA toàn bộ kèm `. ......` (1.8s - 2.0s).
   - Giữ khẩu khí, xưng hô cổ kính (*Chúa công, Quân sư, Thưa Đức ông*); đặt `, ` phân định dẫn chuyện và thoại.
   - *Zero Poetic Run-on & Acoustic Calibration:* 100% dòng thơ kết thúc bằng dấu câu (`,` hoặc `. `); chèn `. ......` sau lời dẫn thơ (*Có bài từ rằng,*, *Đó chính là,*), giữa các khổ thơ và sau câu thơ kết bài để tạo khoảng lặng ngân vang.

---

## 5. CỔNG KIỂM TOÁN KHÔNG KHOAN NHƯỢNG (STEP 07 HARD QC GATE)
1. **Điều kiện mở khóa Bước 08:** `QC_Report.md` phải đạt **100% 7 Quality Gates PASSED**:
   - **G1:** Thư mục/File chuẩn `^[a-zA-Z0-9\-]+$`.
   - **G2:** Chunk $\le 3.000$ ký tự, không rỗng.
   - **G3:** Sạch 100% ký tự cấm TTS.
   - **G4:** Zero-digit 100% bằng chữ tiếng Việt (chấp nhận số cổ phong văn học).
   - **G5:** Cú pháp nhịp nghỉ `. ......` chuẩn phát thanh.
   - **G6:** $R \ge 0.75$ (Bảo toàn nguyên tác, chống tóm tắt).
   - **G7:** Tuân thủ Chiến lược 3 tầng & chống lặp ngoại ngữ / bảo tồn 100% Hán-Việt cổ phong.
2. **Vòng lặp tự chữa lành (Self-Healing Loop):** Gate nào FAIL: AI bắt buộc tự sửa trực tiếp kịch bản và audit lại đến khi 100% PASSED. Cấm bypass sang Bước 08.

---

## 6. CHIẾN LƯỢC ÂM THANH THEO THỂ LOẠI & DUAL-VOICE TTS (STEPS 08A & 08B)
1. **Đạo diễn Kịch nghệ Tiền kỳ (Bước 08A - `arf_08a_theatrical_voice_director`):**
   - *Văn học / Kịch nghệ (6 thể loại):* Sử thi cổ điển, Hiện thực phê phán, Tâm lý hiện sinh/Noir, Tùy bút hồi ký, Kiếm hiệp huyền huyễn, Phi hư cấu.
   - *Phân vai đa thanh:* 5 giai đoạn đời người, 10 khí chất bản thể, 12 cảm xúc phân cảnh, dải Pitch mở rộng $-8\text{Hz} \to +12\text{Hz}$.
   - *Khung Dẫn chuyện 8 sắc thái:* Hào hùng chiến trận, Bi tráng xót xa, Hồi hộp rình rập, Chiêm nghiệm hoài cổ, U uất xã hội, Trào phúng mỉa mai, Nội tâm hiện sinh, Bình nhật tự nhiên.
   - *Acoustic Poetic Calibration:* 100% dòng thơ là entry độc lập `type: "poem"`, caesura `, `, `rate: -18%`, `pitch: -2Hz`, `timbre_eq: "poetic_recitation"`, đệm thở 3 tầng (Lead-in 0.52-0.98s, Inter-verse 0.55s, Ending coda 1.00-1.20s `. ......`).
   - *Động cơ ATSE:* 4 trục formant DSP (Body, Nasal, Presence, Air), hỗ trợ chuỗi FFmpeg parametric equalizer.
   - *Tự lực / Phát triển bản thân:* Giọng cố vấn (`Tôi - Bạn`), trầm ấm (`Pitch -2Hz`), `. ......` 1.8s, khóa 1 giới tính (Nam: Nam Minh x Brian; Nữ: Hoài My x Emma).
   - *Khoa học / Quản trị:* Giọng chuyên gia, sắc nét (`Pitch 0Hz`), tách âm viết tắt (*P-M-I*), Brian đọc ngoại ngữ, khóa 1 giới tính.
   - *Xuất bản:* `theatrical_script.json` và `.theatrical_bible.json`, handoff êm ái khóa cứng trong dải `[0.45s – 1.20s]`.
2. **Kỹ Sư Phòng Thu Neural TTS (Bước 08B - `arf_08_tts_neural_bgm_mixer`):**
   - Tiếp nhận trực tiếp `theatrical_script.json` từ B08A, không phân tích lại kịch nghệ.
   - Phân bổ giọng: 100% tiếng Việt giọng Việt; 100% ngoại ngữ/viết tắt giọng Brian/Emma. Cấm đổi giọng khi retry.
   - Two-Stage Dynamic Leveling: Cắt dead-gap, giữ đuôi âm khẽ `-50dB`. Đệm chuyển giao khẩu hình 80ms (`pad_dur=0.08`). Áp dụng Two-Stage Dynamic Leveling (-16 LUFS, LRA=5-6) cho từng câu thoại và toàn chunk.

---

## 7. KHÓA CỨNG THỜI LƯỢNG [25 – 35 PHÚT] & CÂN BẰNG TOÁN HỌC (STEP 09)
1. **Khóa cứng thời lượng:** Audio Full (B09) và Final Master (B10) bắt buộc nằm trong **[25 – 35 phút]** ($\le 35$ phút). CẤM TẠO FILE > 35 PHÚT.
2. **Chia đều cân bằng & Thích ứng thể loại:** Gom chunk bám sát target [25 - 35 phút]. Văn học ưu tiên tính toàn vẹn của Hồi/Chương hoặc cao trào; Phi hư cấu gom theo Miền Hiệu Suất/Cụm nguyên tắc. Với $T_{total} > 35$ phút: $N = \max(1, \text{round}(T_{total} / 30))$, mục tiêu $Target = T_{total} / N$.
3. **Đối soát thời lượng:** Chênh lệch thời lượng thực tế file Full so với tổng chunk phải đạt $\Delta t \le 2.0s$.

---

## 8. ĐẠO DIỄN ÂM NHẠC, TUYỂN CHỌN BGM & HÒA ÂM MASTER (STEP 10)
1. **BGM thích ứng văn hóa/thể loại:** Cổ phong Đông Á (Đàn Tranh, Cổ Cầm, Tiêu Sáo mộc); Văn học VN (Sáo Trúc, Đàn Bầu, Acoustic); Phương Tây (Solo Piano, Solo Cello); Tự lực (Ambient Piano, Warm Guitar); Khoa học/Quản trị (Baroque 60 BPM). Cấm nhạc dồn dập, sôi nổi, trống trận, đục âm. Chỉ dùng nhạc Public Domain / CC0 / Royalty-Free. Tự động tải qua `core/bgm_downloader.py` (yt-dlp) khi kho nhạc chưa phù hợp.
2. **Vocal Foreground Priority & Vocal Pocket Carving EQ:** BGM giảm mức $6.5\% - 7.5\%$ (`volume=0.065` - `0.075`, tương đương $-24\text{dB}$ đến $-22\text{dB}$, tối đa $0.10$) tôn giọng đọc sáng rõ. Áp dụng bộ lọc khoét tần số `equalizer=f=2500:t=q:w=1.5:g=-3.0` nhường dải phụ âm cho giọng đọc. Cân chỉnh chuẩn phát thanh EBU R128 (`loudnorm=I=-16:TP=-1.5:LRA=6`).
3. **True Seamless Part Cut:** Fade-in đúng 3s ở đầu Part 1; Fade-out đúng 5s ở cuối Part cuối. Điểm nối giữa các Part kế tiếp **bắt buộc cắt thô (Raw cut)**, cấm chèn Fade-in/out.

---
> 💡 **Quy Chuẩn Điều Phối Sub-Agents:** Xem chi tiết giao thức bắt buộc, quy định Zero-Solo và ma trận Swarm ARF/VRF/ABV tại `arf-subagents.md`.
