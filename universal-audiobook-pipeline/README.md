# 🎙️ UNIVERSAL AUDIOBOOK PIPELINE (v2.0)
## GÓI NGUỒN PHÂN PHỐI ĐỘC LẬP & TỰ ĐỘNG HÓA VẬN HÀNH TOÀN DIỆN (CROSS-PLATFORM)

[![Platform](https://img.shields.io/badge/Platform-Windows_%7C_Linux_%7C_macOS-blue.svg)]()
[![Python](https://img.shields.io/badge/Python-3.10%2B-green.svg)](https://python.org)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-7.0%2B_or_Auto--Fallback-orange.svg)](https://ffmpeg.org)
[![AI Ready](https://img.shields.io/badge/AI_Agents-Antigravity_%7C_Claude_%7C_Codex_%7C_Cursor-purple.svg)]()
[![Standard](https://img.shields.io/badge/Audio_Standard-EBU_R128_%28--16LUFS%29-red.svg)]()

Thư mục này là **Gói Nguồn Phân Phối Độc Lập (Self-Contained Standalone Package)** của dự án **Universal Audiobook Pipeline v2.0**. 

Gói này được tối ưu để bạn có thể sao chép, nén zip hoặc chuyển giao sang bất kỳ máy tính nào khác mà vẫn hoạt động 100%, không bị phụ thuộc vào đường dẫn của máy tính ban đầu.

---

## 🚀 CÁCH CÀI ĐẶT 1-CHẠM (QUICKSTART)

### Trên Windows:
Nhấp đúp chuột vào file:
👉 **`setup.bat`**  
*(Hệ thống sẽ tự tạo môi trường ảo Python `venv`, cài đặt thư viện và tải FFmpeg nếu máy tính chưa có).*

Sau đó, nhấp đúp chuột vào file:
👉 **`run.bat`**  
*(Để mở Menu điều khiển tiếng Việt trực quan).*

### Trên Linux / macOS:
Mở Terminal tại thư mục này và chạy:
```bash
chmod +x setup.sh run.sh
./setup.sh
./run.sh
```

---

## 📁 CẤU TRÚC GÓI NGUỒN (PACKAGE ARCHITECTURE)

```text
universal-audiobook-pipeline/
├── AGENTS.md                          # Hướng dẫn quy chuẩn tối cao cho mọi Agent (Antigravity, Claude, Codex, Cursor)
├── AI_ONBOARDING.md                   # Hướng dẫn AI tự phân tích môi trường, tự setup và tự sửa lỗi
├── README.md                          # Tài liệu kỹ thuật tổng quan này
├── HUONG_DAN_SU_DUNG.md               # Sổ tay tiếng Việt cho người dùng phổ thông
├── requirements.txt                   # Danh sách thư viện Python (Cross-Platform)
│
├── setup.bat                          # Cài đặt tự động 1-click cho Windows
├── setup.sh                           # Cài đặt tự động 1-click cho Linux / macOS
├── run.bat                            # Menu điều khiển nhanh 1-click cho Windows
├── run.sh                             # Menu điều khiển nhanh 1-click cho Linux / macOS
│
├── core/                              # Động cơ Python cốt lõi sạch (Zero-hardcode)
│   ├── __init__.py
│   ├── config.py                      # Tự nhận diện PROJECT_ROOT & Dò tìm FFmpeg 5 tầng
│   ├── universal_audiobook_workflow.py# Engine điều phối Bước 07 -> Bước 10
│   ├── antigravity_audiobook_pipeline.py # CLI Runner chính
│   ├── seamless_dual_voice_splicer.py # Động cơ TTS song thanh (NamMinh x Brian)
│   └── swarm_orchestrator.py          # Bộ điều phối Swarm 10 bước
│
├── .agy/skills/                       # 10 Kỹ năng ARF chuẩn Antigravity
├── skills/                            # 10 Kỹ năng ARF cho Claude Code, Codex, Cursor
│   ├── arf_01_pdf_structure_extractor
│   ├── arf_02_author_style_translator
│   ├── arf_03_text_phonetics_normalizer
│   ├── arf_04_smart_audiobook_rechunker
│   ├── arf_05_script_structure_formatter
│   ├── arf_06_llm_script_refiner
│   ├── arf_07_audiobook_qc_auditor
│   ├── arf_08_tts_neural_bgm_mixer
│   ├── arf_09_audio_smart_aggregator
│   └── arf_10_bgm_dynamic_mixer
│
├── workflows/                         # Cấu hình máy đọc và playbook
│   └── universal-audiobook/
│       ├── workflow.json              # Schema v2.0
│       └── WORKFLOW.md                # Human & Agent Playbook
│
├── bgm_audio_library/                 # 6 Bản nhạc nền bản quyền chất lượng cao
│   ├── mood_baroque_classical_focus.mp3
│   ├── mood_deep_focus_insight_positive.mp3
│   ├── mood_epic_motivation_cinematic.mp3
│   ├── mood_ghibli_anime_piano.mp3
│   ├── mood_lofi_chill_relax_study.mp3
│   └── mood_neutral_default_piano.mp3
│
├── tools/                             # Công cụ ngoại vi
│   └── download_ffmpeg.py             # Script tự động kéo bản FFmpeg Portable
│
├── input_books/                       # Thư mục lưu trữ sách đầu vào và kịch bản
│
└── audio_output/                      # Thư viện xuất bản Master Audio tập trung
```

---

## 🎯 ĐẶC TÍNH VƯỢT TRỘI

1. **Zero-Hardcode & Cross-Platform:** Hoạt động hoàn hảo trên Windows, Linux, macOS. Tự động nhận diện thư mục cài đặt thông qua `core/config.py`.
2. **Khóa Cứng Thời Lượng [25 – 35 phút]:** Không bao giờ tạo file âm thanh quá 35 phút, đảm bảo chuẩn phân phối trên YouTube, Podcast, Spotify.
3. **Thu Âm Song Thanh (Dual-Voice TTS):** Giọng đọc Nam Minh (Tiếng Việt) kết hợp Brian (Tiếng Anh quốc tế), bảo toàn 100% thuật ngữ gốc không bị đọc méo tiếng.
4. **Hòa Âm Nghệ Thuật (Dynamic BGM):** Tự động chuyển đổi 3 phân cảnh cảm xúc theo thời lượng tập, hạ nhạc nền -20dB dưới lời nói để giọng đọc luôn nổi bật.
5. **AI Self-Bootstrapping:** Bất kỳ mô hình AI nào (Google Antigravity, Claude, ChatGPT, Cursor) khi mở thư mục này đều sẽ đọc `AGENTS.md` và `AI_ONBOARDING.md` để tự biết cách cài đặt và vận hành mà không cần người dùng chỉ dẫn.
