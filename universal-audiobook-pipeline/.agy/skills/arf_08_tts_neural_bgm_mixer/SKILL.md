---
name: arf_08_tts_neural_bgm_mixer
description: "Bước 8 - Chuyên môn hóa: A.I phân tích ngữ âm, tự động chọn giọng đọc bản xứ phù hợp cho thuật ngữ/ngoại ngữ, đồng nhất giới tính và hòa sắc với giọng tiếng Việt, tạo các file audio mini (chunk) liền mạch."
---

# Kỹ năng 08: Universal AI Multilingual TTS & Seamless Dual-Voice Splicing

**TRIẾT LÝ CỐT LÕI:** AI đóng vai trò **Tổng Đạo Diễn Âm Thanh Đa Ngôn Ngữ (Universal Audio Director)**. Không phụ thuộc vào bất kỳ danh sách từ ngữ gán cứng nào, AI tự động phân tích cấu trúc ngữ âm học (Phonology & Morphology) để bóc tách chính xác các thuật ngữ, tên khoa học, từ vựng tiếng nước ngoài, đồng thời tự động lựa chọn giọng đọc bản ngữ đồng nhất về Giới tính (Nam/Nữ) và hòa sắc âm vực (Timbre & Pitch Matching) để mang lại trải nghiệm nghe tự nhiên như một diễn giả song ngữ bản xứ.

## QUY TRÌNH 2 PHA AI-NATIVE TIÊU CHUẨN (TWO-PHASE AI-NATIVE TTS PIPELINE)

Để đảm bảo **tính linh hoạt cao, thông minh và tuyệt đối không gán cứng**, mỗi khi kích hoạt Bước 08, hệ thống vận hành theo chu trình 2 pha tách bạch:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ PHA 8.1: AI PHÂN TÍCH NGỮ NGHĨA & LẬP KẾ HOẠCH BÓC TÁCH (AI SEMANTIC PRE-PASS)│
│  - AI đọc hiểu ngữ cảnh toàn bộ kịch bản Kich-ban-*.txt                      │
│  - Tự động nhận diện 100% thuật ngữ, từ viết tắt, tiêu đề, tên riêng ngoại ngữ │
│  - Không phụ thuộc từ điển gán cứng; tương thích mọi thể loại sách           │
│  - Xuất bảng kế hoạch phân đoạn minh bạch: audio_chunks/.speech_segments.json │
└──────────────────────────────────────┬───────────────────────────────────────┘
                                       │
                                       ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ PHA 8.2: THU ÂM SONG THANH NEURAL CHUẨN PHÒNG THU (DUAL-VOICE SYNTHESIS)     │
│  - Động cơ TTS nạp trực tiếp kế hoạch từ .speech_segments.json               │
│  - Thu âm chuẩn xác Nam Minh (VN) x Brian (EN), đồng nhất giới tính 100%    │
│  - Cắt dead-gap, đệm khẩu hình 40ms, chuẩn hóa EBU R128 (-16 LUFS)           │
│  - Xuất thành phẩm chunk_*.mp3 và bảng đo thời lượng .chunks_duration.json   │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 1. Cơ Chế Nhận Diện Ngôn Ngữ & Thuật Ngữ Thông Minh Đa Tầng (Advanced 4-Tier Language & Acronym Engine)


Hệ thống hoạt động theo nguyên lý **4 Tầng Phân Tích Linh Hoạt Đạt Độ Nhạy & Độ Chuẩn Tuyệt Đối (100% High-Recall Dual-Voice Architecture)**:

### Tầng 1: Bộ Lọc Ngữ Âm Học Tiếng Việt Bất Biến (Vietnamese Phonetic Invariance & Canonical Syllables)
- **Bảo toàn tiếng Việt có dấu 100%:** Quét toàn diện các ký tự mang dấu thanh điệu tiếng Việt (`à, á, ả, ã, ạ, ê, ô, ơ, ư, đ...`). Bất kỳ từ nào chứa dấu tiếng Việt đều lập tức được phân bổ cho giọng đọc tiếng Việt (`vi-VN-NamMinhNeural`).
- **Tập âm tiết tiếng Việt chuẩn hóa (1.894 âm tiết):** Tích hợp trọn vẹn bộ từ điển âm tiết chuẩn tiếng Việt không dấu (`core/vietnamese_syllables.py`). Các từ không dấu như `nhau`, `gian`, `công ty`, `bài`, `hai`, `vai`, `trong` luôn được bảo vệ tối đa, không bị gán nhầm sang tiếng Anh.

### Tầng 2: Tập Từ Vựng Quản Trị - Công Nghệ & Đại Từ Điển Hệ Thống (Built-in Glossaries & System Lexicon)
- **Tập từ vựng Quản trị & Công nghệ tích hợp sẵn (`BUILTIN_PM_TERMS`):** Tự động nhận diện tức thì và trọn vẹn mọi thuật ngữ chuyên môn: `project`, `management`, `manager`, `charter`, `scope`, `deliverables`, `stakeholder`, `agile`, `scrum`, `sprint`, `kanban`, `waterfall`, `lean`, `telehealth`, `unique`, `endeavor`, `temporary`, `pursuit`, `what`, `why`, `how`, `career`, `embarking`, `effective`, `organizational`, `culture`, `structure`, `framework`, `lifecycle`, `tailoring`, `baseline`, `milestone`, `burndown`, `roadmap`, `dashboard`, `governance`, `procurement`, `kickoff`, `retrospective`, `jira`, `confluence`, `coursera`, `google`...
- **Đại từ điển Anh ngữ hệ thống (104.000+ từ vựng):** Tự động truy xuất danh mục `/usr/share/dict/words` để đối chiếu các từ vựng tiếng Anh học thuật xuất hiện trong giáo trình quốc tế.
- **Từ điển tùy biến cuốn sách:** Nạp file `custom_phonetics.json` hoặc `pmbok_custom_phonetics.json` trong thư mục dự án sách.

### Tầng 3: Nhận Diện Cấu Trúc Ngữ Âm & Từ Viết Tắt Chuẩn Quốc Tế (Phonetic & Morphological Engine)
1. **Từ viết tắt tách âm phát thanh (Hyphenated Acronyms):** Nhận diện 100% các từ viết tắt có gạch nối: `P-M-I`, `W-B-S`, `K-P-I`, `P-M-B-O-K`, `S-W-O-T`, `A-I`, `I-T`, `E-V-M`... phân bổ hoàn toàn cho giọng quốc tế `en-US-BrianMultilingualNeural` đọc tách chữ chuẩn xác.
2. **Từ viết tắt viết hoa toàn bộ (All-Caps Acronyms):** `PMI`, `PMBOK`, `WBS`, `KPI`, `SLA`, `SWOT`, `PMP`, `PMO`, `CAPM`, `RACI`, `SMART`, `MVP`, `API`, `UI`, `UX`, `ROI`, `ERP`, `CRM`...
3. **Hình thái học hậu tố (Morphological Suffixes - Đơn & Số nhiều):** `(tion|sion|ment|ance|ence|able|ible|tive|sive|ship|ing|ed|al|ic|ical|ous|ity|ism|ist|logy|graphy|ture|ure|est|less|ness|hood|wise|ward|ful|fully|ly)s?` (ví dụ: `management`, `development`, `governance`, `predictive`, `leadership`, `embarking`, `planning`, `tailoring`, `methodology`, `structure`...).
4. **Ký tự ngoại lai đặc thù:** Chứa `w, W, z, Z, j, J, f, F` (ví dụ: `framework`, `workflow`, `view`, `focus`, `feedback`, `knowledge`, `size`...).
5. **Cụm phụ âm đầu & đuôi chuẩn quốc tế:**
   - Đầu ngoại ngữ: `str, spr, scr, spl, squ, shr, thr, fl, fr, gl, gr, pl, pr, bl, br, cl, cr, dr, sk, sp, st, sm, sn, sc, sw, wr, kn, ps, rh, sch...`
   - Đuôi ngoại ngữ: `ct, ft, pt, lt, rt, st, sk, sp, mp, nd, nt, nk, rk, lk, rd, ld, rn, rm, lm, sm, ts, ks, ps, nce, nse, rce, rse, tch, dge, que, the, ble, ple, fle, gle, kle, tle, dle, ght, sh, th, ph` hoặc kết thúc bằng `b, d, f, k, l, r, s, v, w, x, z`.
6. **Nguyên âm đôi & Phụ âm kép:** `ea, ee, oo, ou, ei, ey, oy, au, aw, ow, ew`, và phụ âm lặp `bb, cc, dd, ff, gg, ll, mm, nn, pp, rr, ss, tt, vv, zz`.

### Tầng 4: Phân Tích Mệnh Đề Không Lệch Chỉ Mục & Gom Cụm Ngữ Cảnh (Zero-Drift Clause & Multi-Token Bridging)
1. **Phân tích mệnh đề mức ngữ đoạn (Zero-Drift Clause-Level Detection):**
   - Tự động bóc tách các mệnh đề phân cách bởi dấu ngắt câu (`.,;:?!`).
   - Nếu một mệnh đề có >= 2 từ, chứa thuật ngữ tiếng Anh chuẩn, không có dấu tiếng Việt, và các từ còn lại đều tương thích với từ nối Anh ngữ (kể cả khi mở đầu bằng mạo từ như `The`, `A`, `An`, `How`, `What`): toàn bộ mệnh đề được chuyển sang giọng tiếng Anh (ví dụ: `THE ROLE OF THE PROJECT MANAGER`, `EMBARKING ON A CAREER IN PROJECT MANAGEMENT`, `WHAT IS PROJECT MANAGEMENT?`).
2. **Gom cụm liên kết đa từ (Multi-Token Connector Bridging):**
   - Khi có từ 1 đến 4 từ nối/mạo từ tiếng Anh (`on a`, `in the`, `of the`, `for a`, `and the`, `as a`, `to the`, `by the`, `from the`, `is`, `are`) nằm giữa các thuật ngữ ngoại ngữ, hệ thống tự động gom toàn bộ thành một phân đoạn liền mạch, ngăn chặn triệt để việc ngắt giọng vụn vặt.
3. **Thời gian chờ streaming động (Dynamic Streaming Timeout):**
   - Thiết lập thời gian timeout linh hoạt `max(60.0, len(text) * 0.08 + 30.0)` giây, xóa bỏ hoàn toàn hiện tượng timeout giả khi tổng hợp các đoạn văn tiếng Việt dài trên 1.000 ký tự.


---

## 2. Ma Trận Ghép Cặp Giọng Đọc Đồng Nhất Giới Tính (Gender Consistency Matrix)

Để đảm bảo người nghe có cảm giác chỉ có **MỘT người diễn giả thông thái duy nhất** đang thuyết minh:

```
                  ┌──────────────────────────────────────────────────────────┐
                  │          MA TRẬN HÒA SẮC ĐỒNG NHẤT GIỚI TÍNH             │
                  └──────────────────────────────────────────────────────────┘
                                                │
                 ┌──────────────────────────────┴──────────────────────────────┐
                 ▼                                                             ▼
     [ HỒ SƠ GIỌNG NAM - MALE PROFILE ]                           [ HỒ SƠ GIỌNG NỮ - FEMALE PROFILE ]
  Giọng chính: vi-VN-NamMinhNeural (Rate: -10%)               Giọng chính: vi-VN-HoaiMyNeural (Rate: -10%)
  Chất giọng: Trầm ấm, đĩnh đạc, học thuật                    Chất giọng: Trong trẻo, truyền cảm, trang nhã
                 │                                                             │
   ┌─────────────┴─────────────┐                                 ┌─────────────┴─────────────┐
   ▼                           ▼                                 ▼                           ▼
Tiếng Anh/Khoa học:         Các ngoại ngữ khác:               Tiếng Anh/Khoa học:         Các ngoại ngữ khác:
en-US-BrianMultilingual     Pháp: fr-FR-HenriNeural           en-US-EmmaMultilingual      Pháp: fr-FR-DeniseNeural
(Rate: -5%)                 Đức:  de-DE-ConradNeural          (Rate: -5%)                 Đức:  de-DE-KatjaNeural
                            TBN:  es-ES-AlvaroNeural                                      TBN:  es-ES-ElviraNeural
                            Nhật: ja-JP-KeitaNeural                                       Nhật: ja-JP-NanamiNeural
                            Trung: zh-CN-YunxiNeural                                      Trung: zh-CN-XiaoxiaoNeural
                 │                                                             │
   Parametric EQ Harmonization (Nam):                            Parametric EQ Harmonization (Nữ):
   - Nâng dải trầm ấm: +2.5dB tại 300Hz                          - Nâng dải ấm: +2.0dB tại 300Hz
   - Giảm chói gắt: -2.0dB tại 4000Hz                            - Làm dịu sibilance: -2.0dB tại 4500Hz
```

> [!IMPORTANT]
> **QUY TẮC BẢO TOÀN GIỚI TÍNH BẤT BIẾN (GENDER INVARIANCE RULE):**
> - **Tuyệt đối không tự ý tráo đổi giọng giữa Nam và Nữ:** Nếu hồ sơ được chỉ định là `male`, 100% các đoạn tiếng Việt trong toàn bộ các chương và các tập sách PHẢI là `vi-VN-NamMinhNeural`. Khi xảy ra sự cố nghẽn mạng hoặc retry (lần 1 đến 7), hệ thống áp dụng cơ chế giãn cách lũy tiến (*Exponential Backoff*) nhưng **TUYỆT ĐỐI KHÔNG chuyển sang giọng nữ `HoaiMy`**.
> - Tương tự, nếu hồ sơ là `female`, toàn bộ file luôn trung thành với `vi-VN-HoaiMyNeural`.

---

## 3. Quy Chuẩn Phòng Thu Đã Kiểm Nghiệm (Studio Best Practices)

Toàn bộ các best practices nền tảng tiếp tục được bảo toàn nghiêm ngặt:
1. **Khử Sạch Silence Padding (Zero Dead Gap):**
   - Quét và cắt triệt để khoảng lặng nhân tạo ở đầu và đuôi mỗi phân đoạn audio bằng bộ lọc `silenceremove` (ngưỡng `-42dB`), xóa bỏ hoàn toàn khoảng ngắt chết gây khựng tiếng.
2. **Nhịp Thở Đàm Thoại Tự Nhiên (Natural Cadence Buffer 40ms):**
   - Đệm một khoảng chuyển khẩu hình siêu nhỏ 40 mili-giây (`apad=pad_dur=0.04`) giữa tiếng Việt và ngoại ngữ, tái hiện chính xác nhịp chuyển giọng tự nhiên của người thật.
3. **Chuẩn Hóa Âm Lượng EBU R128 (-16 LUFS):**
   - Áp dụng bộ lọc `loudnorm=I=-16:TP=-1.5:LRA=11` để bảo đảm năng lượng âm thanh giữa các phân đoạn đồng nhất tuyệt đối, không có hiện tượng chênh lệch âm lượng.
4. **Bộ Đệm Chống Nghẽn & Bộ Nhớ Đệm Phân Đoạn (Part-Level Caching & Auto-Backoff):**
   - Tự động lưu cache các phân đoạn con đã sinh thành công; không bao giờ gọi lại API vô nghĩa khi xảy ra sự cố mạng.
   - Cơ chế giãn cách lũy tiến thông minh (Exponential Backoff `3.0s * attempt`) khi Microsoft Edge TTS tạm thời bận, đảm bảo pipeline chạy xuyên suốt tới 100% hoàn thành mà không crash.

---

## 4. Ràng Buộc & Phạm Vi Áp Dụng
- **Tính độc lập & Khả chuyển:** Module `seamless_dual_voice_splicer.py` được thiết kế linh hoạt, nhận diện văn bản tự động, có thể tái sử dụng cho mọi chương, mọi cuốn sách, mọi lĩnh vực mà không cần cấu hình thủ công lại.
- **Phạm vi bước 08:** Chỉ phụ trách tạo các tệp mini chunk chuẩn mực (`chunk_*.mp3`). Khâu ghép nối thành file dài thuộc Bước 09 và lồng nhạc nền thuộc Bước 10.
