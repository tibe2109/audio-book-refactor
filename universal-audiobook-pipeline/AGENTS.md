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

## 2. BA QUY TẮC THÉP BẤT BIẾN (NON-NEGOTIABLE CONSTRAINTS)

1. **Khóa Cứng Thời Lượng [25 – 35 phút] (Duration Hard-Cap):**
   - Mọi file Audio Full (Bước 09) và Final Master (Bước 10) phải nằm trong khung **[25 – 35 phút]**.
   - **TUYỆT ĐỐI KHÔNG TẠO RA BẤT KỲ FILE NÀO VƯỢT QUÁ 35 PHÚT**. Nếu nội dung dài, giải thuật toán học sẽ tự động chia đều thành nhiều Parts (Part 1, Part 2...).
2. **Bảo Toàn Thuật Ngữ & Chiến Lược Biên Tập 3 Tầng (NamMinh x Brian & Anti-Auditory Fatigue):**
   - **Tầng 1 (Định vị ban đầu):** Thuật ngữ chuyên ngành tiếng Anh/Latinh (Project Charter, Agile, Stakeholder, Scope Creep...) phải giữ nguyên ký tự quốc tế ở lần giới thiệu đầu tiên hoặc đề mục mới để giọng `en-US-BrianMultilingualNeural` đọc chuẩn xác. Tuyệt đối không phiên âm bồi thô thiển.
   - **Tầng 2 (Nhắc lại có chọn lọc):** Chỉ nhắc lại thuật ngữ ngoại ngữ ở các đề mục lớn (H1/H2) khi thực sự cần thiết để tái định vị ngữ cảnh thính giác.
   - **Tầng 3 (Biên tập thân bài linh hoạt bằng AI):** Trong thân bài diễn giải, AI biên tập viên chủ động chuyển đổi linh hoạt sang tiếng Việt tự nhiên (*Stakeholder* $\to$ *các bên liên quan*, *Project Charter* $\to$ *bản điều lệ dự án*), dùng từ viết tắt tách âm phát thanh (*P-M-I*, *P-M-B-O-K*, *W-B-S*, *K-P-I*) hoặc đại từ thay thế gần gũi ngắn gọn. Tuyệt đối tránh lặp từ ngoại ngữ liên tục gây đảo giọng TTS và mỏi tai người nghe. Phải do AI trực tiếp thẩm định ngữ cảnh, cấm dùng script cứng thay thế mù quáng. Khi tài liệu dài, kích hoạt Sub-agent chuyên trách.
   - **Điều phối nhịp điệu thính giác (Ngắt nghỉ điểm nhấn vs. Đọc liền mạch):** Dùng dấu phẩy `, ` tạo nhịp nghỉ nhẹ (~200ms) khi thuật ngữ đi kèm sau tên tiếng Việt giải thích/đề mục để người nghe ghi nhớ; đọc và ghép âm liền mạch 100% không khựng tiếng khi thuật ngữ nằm trong dòng chảy ngữ pháp liên tục (*các Project Manager*, *Tên tôi là Rachel*, *tại Google New York*). 100% tiếng Việt do giọng Việt đọc, 100% tiếng nước ngoài do giọng Brian đọc.
3. **Cổng Kiểm Toán Không Nhân Nhượng (Hard QC Gate at Step 07):**
   - Chỉ được phép cấp quyền thu âm TTS (Bước 08) khi tệp `QC_Report.md` được thẩm định **100% 7 Gates PASSED**.
   - Nếu phát hiện lỗi ký tự cấm, câu dài hoặc sót số trần, AI phải kích hoạt vòng lặp tự chữa lành (**Self-Healing Loop**) để sửa kịch bản trước khi đi tiếp.
4. **Bảo Toàn Nhất Quán Giới Tính Người Diễn Đọc (Gender Consistency Invariance):**
   - Tuyệt đối giữ nguyên giới tính xuyên suốt toàn bộ các chunks trong chương và các tập sách (Nếu Nam thì 100% Nam Minh, Nữ thì 100% Hoài My). Cấm mọi cơ chế retry tự động tráo đổi sang giọng đối lập khi gặp sự cố mạng.
5. **Kỷ Luật Quản Lý Tệp Tin & Giữ Vững Thư Mục Gốc (Root Cleanliness & File Hygiene):**
   - **Tuyệt đối KHÔNG tạo file tạm ở thư mục gốc (Root):** Cấm mọi hành vi tạo script thử nghiệm (.py), file audio nháp (.mp3), file log (.txt) hoặc file cờ không đuôi trực tiếp tại thư mục gốc. Mọi tệp thử nghiệm ngắn hạn phải nằm trong `scratch/` hoặc thư mục riêng của từng chương.
   - **Tổ chức theo dự án biệt lập & Lưu trữ tập trung:** Dữ liệu sách nằm trong `Kich-ban-clipchamp/<Tên-Sách>/` hoặc `input_books/<Tên-Sách>/`. Từ điển riêng (`custom_phonetics.json` / `pmbok_custom_phonetics.json`) phải đặt bên trong thư mục của cuốn sách đó. Toàn bộ file Full (không nhạc) xuất xưởng của các chương được gom tập trung vào thư mục `Full-[tên-sách]/`, và toàn bộ file Final Master (có nhạc) xuất xưởng được gom tập trung vào `Final-[tên-sách]/`. Tuyệt đối KHÔNG lưu file Full hoặc Final vào từng thư mục con của chương.
   - **Tự động dọn dẹp sau khi hoàn thành:** Sau khi Bước 10 xuất xưởng file `Final_Audio_*.mp3` đạt chuẩn, hệ thống tự động dọn sạch các tệp trung gian (`concat_list.txt`, `.chunk_*.txt`, `.raw_part*.txt`) để không gian làm việc luôn gọn gàng và tối ưu bộ nhớ.

---

## 3. SƠ ĐỒ DÂY CHUYỀN 10 BƯỚC KHÉP KÍN

| Bước | Mã Kỹ Năng / Module | Nhiệm Vụ Của AI | File Đầu Ra |
| :---: | :--- | :--- | :--- |
| **01** | `arf_01_pdf_structure_extractor` | Bóc tách cấu trúc PDF, khử Header/Footer/số trang, nối Drop-Cap. | `raw_original.txt` |
| **02** | `arf_02_author_style_translator` | Nhập vai tác giả, chuyển thể bảng/biểu đồ/công thức thành văn xuôi. | `translated.txt` |
| **03** | `arf_03_text_phonetics_normalizer` | Chuẩn hóa số học (100% viết chữ), tách âm viết tắt, bảo toàn Latinh. | `normalized.txt` |
| **04** | `arf_04_smart_audiobook_rechunker` | Phân rã khối đệm 2.500 - 3.500 ký tự theo ranh giới đoạn văn. | `Kich-ban-raw-*.txt` |
| **05** | `arf_05_script_structure_formatter` | Tiêu đề IN HOA đứng riêng, chèn khoảng lặng phát thanh `. ......` (1.5-2s). | Kịch bản có nhịp thở |
| **06** | `arf_06_llm_script_refiner` | Câu <= 30 từ, thêm phẩy lấy hơi (Breathing Commas), quét sạch ký tự cấm. | `Kich-ban-*.txt` |
| **07** | `arf_07_audiobook_qc_auditor` | Kiểm toán 7 Quality Gates. 100% PASSED mới mở khóa bước 08. | `QC_Report.md` |
| **08** | `arf_08_tts_neural_bgm_mixer` | Thu âm song thanh NamMinh (VN) x Brian (EN), cắt dead-gap, EBU R128. | `audio_chunks/*.mp3` |
| **09** | `arf_09_audio_smart_aggregator` | Ghép chunk thành tập cân bằng thời lượng [25-35 phút]. Khóa cứng <= 35p. | `Full-[tên-sách]/Full_*.mp3` |
| **10** | `arf_10_bgm_dynamic_mixer` | Hòa âm 3 phân cảnh (Baroque 35% -> Focus 40% -> Piano 25%), Ducking -20dB. | `Final-[tên-sách]/Final_Audio_*.mp3` |

---

## 4. CÂU LỆNH ĐIỀU PHỐI DÀNH CHO AI (AGENT EXECUTION COMMANDS)

Khi thực thi trên Terminal / Command Line, AI sử dụng các lệnh chuẩn sau (đã tự động xử lý cross-platform):

```bash
# 1. Chạy tự động trọn gói 1 chương từ Bước 07 đến Bước 10:
python core/antigravity_audiobook_pipeline.py --book_dir "input_books/Tên-Sách" --chapter "01-chuong-1"

# 2. Chạy tự động toàn bộ các chương chưa hoàn thành:
python core/antigravity_audiobook_pipeline.py --book_dir "input_books/Tên-Sách" --all

# 3. Chạy theo dải chương:
python core/antigravity_audiobook_pipeline.py --book_dir "input_books/Tên-Sách" --from_chap 1 --to_chap 5

# 4. Kiểm toán 7 Quality Gates độc lập bằng Python:
python -c "import sys; sys.path.insert(0, 'core'); from universal_audiobook_workflow import UniversalAudiobookWorkflow; wf = UniversalAudiobookWorkflow('input_books/Tên-Sách', '01-chuong-1'); print(wf.audit_quality_gates())"
```

---

## 5. THƯ VIỆN KỸ NĂNG CÓ SẴN (SKILLS DIRECTORY)
Dự án lưu trữ sẵn 10 kỹ năng chuẩn ở 2 vị trí để mọi AI đều đọc được:
- `.agy/skills/` (Tương thích Google Antigravity)
- `skills/` (Tương thích Claude Code, Cursor, Codex)

Mỗi kỹ năng đều có tài liệu `SKILL.md` hướng dẫn chi tiết prompt, input/output contract và kịch bản kích hoạt Subagent.
