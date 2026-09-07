# HƯỚNG DẪN ĐIỀU PHỐI DÂY CHUYỀN SÁCH NÓI VẠN NĂNG (ANTIGRAVITY WORKFLOW PLAYBOOK)
## ÁP DỤNG CHO ANTIGRAVITY IDE, ANTIGRAVITY CLI VÀ MULTI-AGENT SWARM v2.0
---

### 1. Giới Thiệu & Bản Quyền Thiết Kế
Tài liệu này là cẩm nang vận hành (Operational Playbook) của **Universal Audiobook Workflow**, được chuẩn hóa cho toàn bộ hệ sinh thái Agent của Google Antigravity:
- **Antigravity IDE:** Tự động kích hoạt thông qua giao diện chat hoặc Slash Commands với giao diện tương tác minh bạch.
- **Antigravity CLI:** Chạy headless qua terminal, background daemon hoặc cron jobs tự động hóa hàng loạt không cần người giám sát.
- **Antigravity v2.0:** Hỗ trợ điều phối đa tác tử (Multi-agent Swarm), phân rã công việc song song và tự phục hồi (Self-Healing).

---

### 2. Ba Quy Tắc Bất Biến (Non-Negotiable Constraints)
Mọi Agent khi thực thi quy trình này **BẮT BUỘC** phải tuân thủ nghiêm ngặt:

1. **Khóa Cứng Thời Lượng (Hard Duration Limit):**
   - Mọi tập Audio Full (Bước 09) và Final Master (Bước 10) phải nằm trong khung **[25 – 35 phút]** (trừ trường hợp tổng thời lượng toàn chương nhỏ hơn 25 phút thì gom thành 1 tập).
   - **TUYỆT ĐỐI KHÔNG TẠO RA BẤT KỲ FILE NÀO VƯỢT QUÁ 35 PHÚT**. Nếu dung lượng kịch bản dài, bắt buộc phải dùng thuật toán cân bằng phân bổ thành nhiều Parts (Part 1, Part 2...).
2. **Bảo Toàn Thuật Ngữ & Ngữ Âm Song Thanh:**
   - 100% thuật ngữ chuyên ngành tiếng Anh/Latinh phải giữ nguyên chữ viết quốc tế để giọng `en-US-BrianMultilingualNeural` đọc chuẩn xác. Tuyệt đối không phiên âm bồi kiểu thô thiển.
   - Viết tắt tách âm phát thanh: `P-M-I`, `P-M-B-O-K`, `W-B-S`, `K-P-I`, `I-T-T-O`.
3. **Cổng Kiểm Toán Không Nhân Nhượng (Hard QC Gate at Step 07):**
   - Chỉ được phép render TTS (Bước 08) khi tệp `QC_Report.md` được thẩm duyệt **100% 7 Gates PASSED**. Nếu phát hiện lỗi ký tự cấm, câu dài hoặc sót số trần, Agent phải tự sửa chữa (Self-Healing) trước khi đi tiếp.

---

### 3. Hướng Dẫn Vận Hành Dành Cho Các Tác Tử (Agent Execution Protocol)

#### A. Khi Chạy Qua Antigravity IDE (Interactive Mode)
Người dùng có thể yêu cầu bằng ngôn ngữ tự nhiên hoặc dùng lệnh:
- Chạy từng bước: `/arf_01` $\rightarrow$ `/arf_10`
- Chạy tự động trọn gói một chương: 
  *"Hãy chạy tự động toàn bộ quy trình từ Bước 01 đến Bước 10 cho Chương X"*
- Chạy tự động một dải chương:
  *"Hãy chạy tự động các chương từ 06 đến 08 theo Universal Workflow"*

#### B. Khi Chạy Qua Antigravity CLI (Headless/Automated Mode)
Các Agent có thể gọi trực tiếp module điều phối bằng terminal:
```powershell
# Chạy tự động trọn gói cho 1 chương cụ thể:
python scripts/antigravity_audiobook_pipeline.py --book_dir "Kich-ban-clipchamp/PMBOK-7th" --chapter "06-performance-domains"

# Chạy tự động tất cả các chương chưa hoàn thành:
python scripts/antigravity_audiobook_pipeline.py --book_dir "Kich-ban-clipchamp/PMBOK-7th" --all

# Chạy một dải chương liên tiếp (ví dụ từ chương 6 đến chương 8):
python scripts/antigravity_audiobook_pipeline.py --book_dir "Kich-ban-clipchamp/PMBOK-7th" --from 6 --to 8

# Xử lý tự động một cuốn sách mới hoàn toàn từ file PDF:
python scripts/antigravity_audiobook_pipeline.py --pdf "D:/Books/Book_Title.pdf" --book_title "Tên Sách"
```

---

### 4. Cấu Trúc Hồ Sơ Dự Án Chuẩn Mực (Directory Layout)
Mỗi dự án sách áp dụng workflow này sẽ tuân thủ cấu trúc sau:
```
D:\Solution\Audio-Book-Refactor\
├── .session_manifest.json          # Cơ sở dữ liệu trạng thái tổng thể (Single Source of Truth)
├── bgm_audio_library/             # Kho nhạc nền bản quyền chất lượng cao
├── scripts/
│   ├── universal_audiobook_workflow.py    # Core Engine
│   ├── antigravity_audiobook_pipeline.py  # CLI Runner
│   └── seamless_dual_voice_splicer.py     # TTS & Phonetics Engine
├── workflows/
│   └── universal-audiobook/
│       ├── workflow.json                  # Machine-readable schema v2.0
│       └── WORKFLOW.md                    # Human & Agent Playbook
├── audio_output/                          # Kho lưu trữ Master Final tập trung
└── Kich-ban-clipchamp/
    └── [Tên-Cuốn-Sách]/
        ├── 00-preface/
        ├── 01-chapter-1/
        │   ├── raw_original.txt           # Bước 01
        │   ├── translated.txt             # Bước 02
        │   ├── normalized.txt             # Bước 03
        │   ├── Kich-ban-raw-*.txt         # Bước 04 & 05
        │   ├── Kich-ban-*.txt             # Bước 06
        │   ├── QC_Report.md               # Bước 07
        │   ├── audio_chunks/              # Bước 08
        │   ├── Full_*.mp3                 # Bước 09
        │   └── Final_Audio_*.mp3          # Bước 10
```
