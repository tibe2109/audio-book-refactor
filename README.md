# 🎙️ UNIVERSAL AUDIOBOOK ENGINE (v2.0)
## DÂY CHUYỀN SẢN XUẤT SÁCH NÓI VẠN NĂNG TỰ ĐỘNG HÓA TỪ PDF ĐẾN MASTER ĐA PHÂN CẢNH

[![Antigravity](https://img.shields.io/badge/Antigravity-v2.0_Ready-blue.svg)](https://antigravity.google.com)
[![Python](https://img.shields.io/badge/Python-3.10%2B-green.svg)](https://python.org)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-7.0%2B-orange.svg)](https://ffmpeg.org)
[![Quality Gate](https://img.shields.io/badge/Quality_Gate-7_Hard_Gates-red.svg)]()
[![Standard](https://img.shields.io/badge/Audio_Standard-EBU_R128_%28--16LUFS%29-purple.svg)]()

**Universal Audiobook Engine** là giải pháp toàn diện chuẩn công nghiệp biến đổi mọi tài liệu (PDF, Word, Text — kể cả sách chuyên khảo chứa bảng biểu, đồ thị, công thức, mã code) thành các tác phẩm Sách Nói (Audiobook) chuẩn phát thanh quốc tế.

Hệ thống được thiết kế theo triết lý **Zero-Hardcode (Không phụ thuộc đường dẫn cứng)**, cho phép cài đặt "1-Click" và vận hành mượt mà trên bất kỳ máy tính nào (Windows, macOS, Linux).

---

## 📑 MỤC LỤC
1. [Bốn Trụ Cột Triết Lý Thiết Kế](#1-bốn-trụ-cột-triết-lý-thiết-kế)
2. [Sơ Đồ Dây Chuyền 10 Bước Chuẩn Hóa](#2-sơ-đồ-dây-chuyền-10-bước-chuẩn-hóa)
3. [Cấu Trúc Thư Mục Dự Án (Directory Layout)](#3-cấu-trúc-thư-mục-dự-án)
4. [Động Cơ Thu Âm Song Thanh (Seamless Dual-Voice TTS)](#4-động-cơ-thu-âm-song-thanh)
5. [7 Cổng Kiểm Toán Chất Lượng Cứng (Hard Quality Gates)](#5-7-cổng-kiểm-toán-chất-lượng-cứng)
6. [Hòa Âm Đạo Diễn Đa Phân Cảnh (Dynamic BGM Scene-Scoring)](#6-hòa-âm-đạo-diễn-đa-phân-cảnh)
7. [Cài Đặt Nhanh & Vận Hành Hệ Thống](#7-cài-đặt-nhanh--vận-hành-hệ-thống)
8. [Tích Hợp AI Agent & Hệ Thống 10 Skills](#8-tích-hợp-ai-agent--hệ-thống-10-skills)

---

## 1. BỐN TRỤ CỘT TRIẾT LÝ THIẾT KẾ

1. **Context Isolation (Độc lập Ngữ cảnh):** Mỗi chương và từng phân đoạn được xử lý độc lập trong một phiên làm việc riêng. Triệt tiêu hoàn toàn hiện tượng thoái hóa ngữ cảnh (Context Degradation) và ảo giác (Hallucination) trên sách dày hàng trăm trang.
2. **Hard Quality Gates (Cổng Chặn Cứng Bước 07):** Tuyệt đối không để lọt lỗi. Nếu kịch bản chưa đạt 100% 7 tiêu chuẩn kiểm toán kỹ thuật, hệ thống tự động kích hoạt vòng lặp tự phục hồi (*Self-Healing Loop*) trước khi mở khóa cho động cơ TTS.
3. **Duration Hard-Cap [25 – 35 phút]:** Thuật toán phân bổ cân bằng toán học (Bước 09 & 10) bắt buộc mọi tập xuất bản đều nằm trong khung [25 – 35 phút], **tuyệt đối không có bất kỳ tập nào vượt quá 35 phút** (tối ưu cho trải nghiệm nghe tập trung và dung lượng phát hành YouTube/Podcast).
4. **Universal Portability (Tính Di Động Vạn Năng):** Tự động phân giải đường dẫn gốc qua `scripts/config.py`, tự tìm kiếm FFmpeg 5 tầng an toàn, sẵn sàng chạy ngay trên mọi máy tính chỉ sau 1 cú nhấp chuột.

---

## 2. SƠ ĐỒ DÂY CHUYỀN 10 BƯỚC CHUẨN HÓA

```
[ BƯỚC 01: PDF STRUCTURE EXTRACTOR ]
  • Bóc tách cấu trúc PDF, loại bỏ Header/Footer, số trang, hàn gắn Drop-Cap gãy dòng.
  👉 Đầu ra: raw_original.txt & .session_manifest.json
       │
       ▼
[ BƯỚC 02: AUTHOR PERSONA TRANSLATOR ]
  • Nhập vai tác giả, chuyển thể bảng biểu/sơ đồ/công thức thành văn xuôi phát thanh.
  👉 Đầu ra: translated.txt
       │
       ▼
[ BƯỚC 03: CONTEXTUAL PHONETIC NORMALIZER ]
  • Chuyển hóa 100% số tự nhiên thành chữ, tách âm viết tắt (P-M-I, W-B-S), giữ nguyên Latinh.
  👉 Đầu ra: normalized.txt
       │
       ▼
[ BƯỚC 04: SMART AUDIOBOOK RECHUNKER ]
  • Phân rã kịch bản thành các khối đệm phát thanh tối ưu 2.500 - 3.500 ký tự theo đoạn văn.
  👉 Đầu ra: Kich-ban-raw-1.txt ... Kich-ban-raw-N.txt
       │
       ▼
[ BƯỚC 05: SCRIPT STRUCTURE FORMATTER ]
  • Phân tầng tiêu đề IN HOA độc lập, chèn marker khoảng lặng phát thanh sâu ". ......" (1.5 - 2.0s).
  👉 Đầu ra: Kịch bản phân tầng cấu trúc nhịp thở
       │
       ▼
[ BƯỚC 06: LLM SCRIPT REFINER ]
  • Khống chế câu <= 30 từ, thêm dấu phẩy lấy hơi (Breathing Commas), quét sạch ký tự cấm.
  👉 Đầu ra: Kich-ban-1.txt ... Kich-ban-N.txt
       │
       ▼
[ BƯỚC 07: SEMANTIC QC AUDITOR (HARD GATE) ]
  • Kiểm toán tự động 7 Quality Gates. 100% PASSED mới mở khóa bước tiếp theo.
  👉 Đầu ra: QC_Report.md
       │
       ▼
[ BƯỚC 08: UNIVERSAL NEURAL DUAL-VOICE TTS ]
  • Thu âm song thanh NamMinh (VN) x Brian (EN), cắt dead-gap, đệm khẩu hình 40ms, chuẩn EBU R128 (-16 LUFS).
  👉 Đầu ra: audio_chunks/chunk_1.mp3 ... chunk_N.mp3
       │
       ▼
[ BƯỚC 09: AUDIO SMART AGGREGATOR ]
  • Cân bằng thời lượng toán học, gom thành các tập chuẩn [25 - 35 phút]. Khóa cứng <= 35p.
  👉 Đầu ra: Full_ChapterX_PartY.mp3
       │
       ▼
[ BƯỚC 10: DYNAMIC BGM SCENE-SCORING MASTER ]
  • Hòa âm 3 phân cảnh cảm xúc (Khởi nguồn 35% -> Chiều sâu 40% -> Đúc kết 25%), Ducking -20dB, Acrossfade 3s.
  👉 Đầu ra: Final_Audio_ChapterX_PartY.mp3 (lưu tại chương và audio_output/)
```

---

## 3. CẤU TRÚC THƯ MỤC DỰ ÁN

```text
Audio-Book-Refactor/
├── .session_manifest.json          # Cơ sở dữ liệu trạng thái tiến trình (Single Source of Truth)
├── requirements.txt                # Thư viện Python phụ thuộc chuẩn hóa
├── setup_environment.bat           # Script cài đặt tự động 1-click cho Windows
├── setup_environment.ps1           # Script cài đặt PowerShell
├── run_audiobook.bat               # Menu khởi chạy nhanh giao diện tương tác
├── README.md                       # Cẩm nang kỹ thuật & kiến trúc
├── HUONG_DAN_SU_DUNG.md            # Hướng dẫn dễ hiểu cho người dùng phổ thông
├── AI_AGENT_PROMPT_PRESET.md       # Bộ Prompt chuẩn mẫu nạp cho mọi AI
│
├── bgm_audio_library/             # Kho nhạc nền bản quyền chất lượng cao
│   ├── mood_baroque_classical_focus.mp3
│   ├── mood_deep_focus_insight_positive.mp3
│   ├── mood_epic_motivation_cinematic.mp3
│   ├── mood_ghibli_anime_piano.mp3
│   ├── mood_lofi_chill_relax_study.mp3
│   └── mood_neutral_default_piano.mp3
│
├── audio_output/                  # Thư viện xuất bản Master Audio tập trung
│
├── scripts/                       # Bộ động cơ thực thi Python cốt lõi
│   ├── config.py                  # Quản lý ROOT, PATH, FFmpeg & Constants
│   ├── universal_audiobook_workflow.py   # Core Workflow Engine (Step 07 - 10)
│   ├── antigravity_audiobook_pipeline.py # Autonomous CLI Runner
│   ├── seamless_dual_voice_splicer.py    # Dual-Voice TTS & DSP Engine
│   └── swarm_orchestrator.py             # Multi-agent Swarm Coordinator (10 Steps)
│
├── .agy/skills/                   # Hệ thống 10 Skills chuẩn Antigravity (arf_01 -> arf_10)
│   ├── arf_01_pdf_structure_extractor/
│   ├── arf_02_author_style_translator/
│   ├── arf_03_text_phonetics_normalizer/
│   ├── arf_04_smart_audiobook_rechunker/
│   ├── arf_05_script_structure_formatter/
│   ├── arf_06_llm_script_refiner/
│   ├── arf_07_audiobook_qc_auditor/
│   ├── arf_08_tts_neural_bgm_mixer/
│   ├── arf_09_audio_smart_aggregator/
│   └── arf_10_bgm_dynamic_mixer/
│
├── tools/                         # Công cụ phụ trợ ngoại vi
│   ├── download_ffmpeg.py         # Tự động kéo bản FFmpeg portable cho Windows
│   └── ffmpeg/                    # Chứa binary ffmpeg.exe & ffprobe.exe
│
└── Kich-ban-clipchamp/            # Vùng lưu trữ kịch bản & file trung gian từng tác phẩm
    └── [Tên-Cuốn-Sách]/
        ├── 00-preface/
        └── 01-chapter-1/
            ├── raw_original.txt          # Bước 01
            ├── translated.txt            # Bước 02
            ├── normalized.txt            # Bước 03
            ├── Kich-ban-raw-*.txt        # Bước 04 & 05
            ├── Kich-ban-*.txt            # Bước 06
            ├── QC_Report.md              # Bước 07
            ├── audio_chunks/             # Bước 08
            ├── Full_*.mp3                # Bước 09
            └── Final_Audio_*.mp3         # Bước 10
```

---

## 4. ĐỘNG CƠ THU ÂM SONG THANH (SEAMLESS DUAL-VOICE TTS)

Động cơ `seamless_dual_voice_splicer.py` giải quyết hiện tượng giọng đọc tiếng Việt đọc từ tiếng Anh bị méo tiếng hoặc phát âm sai bằng ma trận hòa sắc đa ngữ:

| Đặc tính | Cấu hình Giọng Nam (Mặc định) | Cấu hình Giọng Nữ |
| :--- | :--- | :--- |
| **Giọng tiếng Việt** | `vi-VN-NamMinhNeural` (Rate: -10%) | `vi-VN-HoaiMyNeural` (Rate: -10%) |
| **Giọng ngoại ngữ (EN)** | `en-US-BrianMultilingualNeural` (Rate: -5%) | `en-US-EmmaMultilingualNeural` (Rate: -5%) |
| **Âm sắc (Timbre)** | Trầm ấm, uyên bác, đĩnh đạc | Truyền cảm, thanh thoát, trang nhã |
| **Xử lý EQ** | Bass-Heavy Academic (+2.5dB@300Hz, -2.0dB@4kHz) | Scholarly Gentle (+2.0dB@300Hz, -2.0dB@4.5kHz) |
| **Khử Dead-Gap** | `silenceremove` dưới ngưỡng **-42dB** | `silenceremove` dưới ngưỡng **-42dB** |
| **Đệm khẩu hình** | **40ms** Natural Cadence Buffer | **40ms** Natural Cadence Buffer |
| **Chuẩn âm lượng** | **EBU R128 (-16 LUFS)** | **EBU R128 (-16 LUFS)** |

---

## 5. 7 CỔNG KIỂM TOÁN CHẤT LƯỢNG CỨNG (HARD QUALITY GATES)

Tại **Bước 07**, hệ thống kích hoạt bộ đối soát nghiêm ngặt trước khi cấp phép thu âm:

1. **Gate 1 - Cú pháp phi văn bản:** Không còn cú pháp Markdown Table (`|`), LaTeX Math (`$`, `\frac`, `\sum`), hoặc ký tự code máy tính (`{`, `}`, `;`).
2. **Gate 2 - Dấu vết giấy in:** Xóa sạch mọi cụm từ: *"xem hình"*, *"xem bảng"*, *"trang bên"*, *"nhìn vào hình vẽ"*.
3. **Gate 3 - Ký tự cấm phát thanh:** Quét sạch 100% các ký tự: `()`, `""`, `“`, `”`, `:`, `;`, `—`, `–`, `[]`, `{}`, `_`, `*`, `#`, `\`, `/`, `<>`.
4. **Gate 4 - Số trần (Raw Digits):** 100% số nguyên, số thập phân, phần trăm, năm, chương phải được chuyển hóa thành chữ cái tiếng Việt (Ví dụ: `15` $\rightarrow$ `mười lăm`, `2026` $\rightarrow$ `năm hai nghìn không trăm hai mươi sáu`).
5. **Gate 5 - Bảo toàn Latinh:** Thuật ngữ quốc tế giữ nguyên chữ cái Latinh để giọng Brian đọc bản ngữ. Viết tắt phát thanh tách âm có gạch nối (`P-M-I`, `W-B-S`).
6. **Gate 6 - Nhịp thở & Tiêu đề:** Tiêu đề IN HOA đứng riêng một dòng; chèn khoảng lặng sâu `. ......` (1.5 - 2.0s) tại ranh giới chuyển ý.
7. **Gate 7 - Tính trọn vẹn tri thức:** Không cắt xén, không tóm tắt tùy tiện, bảo toàn toàn vẹn tri thức của tài liệu gốc.

---

## 6. HÒA ÂM ĐẠO DIỄN ĐA PHÂN CẢNH (DYNAMIC BGM SCENE-SCORING)

Mỗi tập phát thanh [25 - 35 phút] tại **Bước 10** được hòa âm tự động theo 3 phân cảnh cảm xúc:

| Phân Cảnh | Tỷ Lệ | Nhạc Nền Khuyến Nghị | Cảm Xúc / Mood |
| :--- | :--- | :--- | :--- |
| **Scene 1: Khởi nguồn & Đặt vấn đề** | 35% đầu | `mood_baroque_classical_focus.mp3` | Trang trọng, kích thích tư duy, học thuật |
| **Scene 2: Đột phá & Chiều sâu** | 40% giữa | `mood_deep_focus_insight_positive.mp3` | Tích cực, sáng tỏ, tập trung cao độ |
| **Scene 3: Đúc kết & Tầm nhìn** | 25% cuối | `mood_neutral_default_piano.mp3` | Sâu lắng, chiêm nghiệm, khai phóng |

- **Kỹ thuật hòa âm DSP:**
  - `acrossfade=d=3.0`: Chuyển đoạn nhạc nền mượt mà trong 3 giây.
  - `volume=0.10`: Ducking nhạc nền xuống -20dB dưới giọng đọc để giọng chính luôn nổi bật.
  - `afade=t=in:d=3.0`: Hòa âm vào êm dịu ở đầu Part 1.
  - `afade=t=out:d=5.0`: Giảm âm dần trang trọng ở cuối Part cuối.

---

## 7. CÀI ĐẶT NHANH & VẬN HÀNH HỆ THỐNG

### Cách 1: Cài đặt 1-Click (Dành cho Windows)
Chỉ cần nhấp đúp chuột vào file:
👉 **`setup_environment.bat`**

Hệ thống sẽ tự động:
1. Kiểm tra phiên bản Python (yêu cầu >= 3.10).
2. Tạo môi trường ảo `venv`.
3. Tải và cài đặt toàn bộ dependencies trong `requirements.txt`.
4. Tự động kiểm tra và tải FFmpeg portable nếu máy chưa có.

### Cách 2: Vận hành nhanh bằng dòng lệnh (CLI Runner)
```powershell
# Kích hoạt venv:
.\venv\Scripts\Activate.ps1

# Chạy tự động 1 chương cụ thể:
python scripts/antigravity_audiobook_pipeline.py --chapter "06-performance-domains"

# Chạy một dải chương liên tiếp (từ chương 6 đến chương 8):
python scripts/antigravity_audiobook_pipeline.py --from_chap 6 --to_chap 8

# Chạy tự động toàn bộ các chương chưa hoàn thành:
python scripts/antigravity_audiobook_pipeline.py --all
```

---

## 8. TÍCH HỢP AI AGENT & HỆ THỐNG 10 SKILLS

Hệ thống cung cấp trọn bộ 10 Agent Skills trong `.agy/skills/`:
- Người dùng có thể yêu cầu AI trong Antigravity IDE:
  - *"Hãy chạy Bước 01 đến Bước 10 cho chương 01-chuong-1"*
  - *"Kiểm toán QC kịch bản chương này theo 7 Quality Gates"*
  - *"Tự động điều phối Swarm Agents cho cả cuốn sách"*

Để biết thêm chi tiết cách sử dụng dành cho người mới bắt đầu, vui lòng đọc cẩm nang **[HUONG_DAN_SU_DUNG.md](HUONG_DAN_SU_DUNG.md)**!
