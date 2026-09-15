import json
import os
import re

CHAPTER_DIR = "/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/06-Hoi-06"
THEATRICAL_SCRIPT_PATH = os.path.join(CHAPTER_DIR, "theatrical_script.json")
THEATRICAL_BIBLE_PATH = os.path.join(CHAPTER_DIR, ".theatrical_bible.json")
MANIFEST_PATH = "/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/.session_manifest.json"

theatrical_bible = {
    "chapter_folder": "06-Hoi-06",
    "chapter_index": 6,
    "chapter_title": "Hồi 6: Đốt Kim Quyết, Đổng Trác làm càn; Giấu ngọc tỷ, Tôn Kiên trái ước",
    "work_title": "Tam Quốc Diễn Nghĩa",
    "genre": "classical_epic_literature",
    "acoustic_specification": {
        "pitch_scale": {
            "min_pitch": "-8Hz",
            "max_pitch": "+12Hz",
            "contrast_range_hz": 20
        },
        "rate_scale": {
            "min_rate": "-20%",
            "max_rate": "+15%"
        },
        "handoff_matrix": {
            "instant_interruption": "0.30s - 0.35s",
            "urgent_lead_in": "0.35s - 0.40s",
            "natural_dialogue_turn": "0.42s - 0.50s",
            "dialogue_resonance": "0.50s - 0.60s",
            "pensive_lead_in": "0.60s - 0.75s",
            "regal_ceremony": "0.70s - 0.85s",
            "dramatic_silence": "0.85s - 1.20s",
            "poetic_cushion": "0.85s - 1.80s"
        },
        "dsp_presets": {
            "chest_resonance": "Tôn Kiên, Hạ Hầu Đôn, Viên Thiệu (Boost 160Hz +5dB, Boost 300Hz +2.5dB, Dip 3.5kHz -3dB)",
            "warm_authority": "Tào Hồng, Chu Bật, Công Tôn Toản, Lưu Biểu, Chư Hầu (Boost 280Hz +3.5dB, Boost 2.2kHz +2dB, Dip 4.5kHz -2.5dB)",
            "sharp_cunning": "Tào Tháo, Lý Nho, Lý Thôi, Khoái Việt (High-pass 220Hz, Boost 2.8kHz +4.5dB, Boost 5.5kHz +3dB)",
            "aged_gravel": "Trình Phổ, Dương Bưu, Hoàng Uyển, Tuân Sảng (Boost 420Hz +4.5dB, Low-pass 4.2kHz, Dip 1.2kHz -3dB)",
            "tyrant_arrogant": "Đổng Trác, Lã Bố (Boost 190Hz +4.5dB, Boost 1.8kHz +4dB, Boost 4kHz +2dB)",
            "poetic_recitation": "Ngâm vịnh thi ca cổ, đồng dao (Boost 250Hz +3.5dB, Dip 3.5kHz -2dB, Low-pass 7.5kHz)"
        }
    },
    "characters": {
        "Narrator": {
            "name": "Người dẫn chuyện",
            "gender": "male",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "+0Hz",
            "base_rate": "-5%",
            "narrative_modes": [
                "epic_narrator",
                "contemplative_narrator",
                "intimate_narrator",
                "suspense_narrator",
                "dramatic_narrator",
                "poetic_recitation"
            ],
            "timbre_eq": "epic_narrator",
            "dialogue_count": 0
        },
        "Ton_Kien": {
            "name": "Tôn Kiên",
            "gender": "male",
            "age_stage": "trung_nien",
            "temperament": "anh_hung_hao_sang",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "-1Hz",
            "base_rate": "+2%",
            "timbre_eq": "chest_resonance",
            "dialogue_count": 0
        },
        "Dong_Trac": {
            "name": "Đổng Trác",
            "gender": "male",
            "age_stage": "lao_hoa",
            "temperament": "hach_dich_bao_nguoc",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "+3Hz",
            "base_rate": "+4%",
            "timbre_eq": "tyrant_arrogant",
            "dialogue_count": 0
        },
        "Ly_Nho": {
            "name": "Lý Nho",
            "gender": "male",
            "age_stage": "trung_nien",
            "temperament": "giao_hoat_nham_hiem",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "-1Hz",
            "base_rate": "-2%",
            "timbre_eq": "sharp_cunning",
            "dialogue_count": 0
        },
        "Ly_Thoi": {
            "name": "Lý Thôi",
            "gender": "male",
            "age_stage": "trung_nien",
            "temperament": "xun_xoe_don_hen",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "+1Hz",
            "base_rate": "+1%",
            "timbre_eq": "sharp_cunning",
            "dialogue_count": 0
        },
        "Quan_Si": {
            "name": "Quân Sĩ",
            "gender": "male",
            "age_stage": "thanh_xuan",
            "temperament": "trong_sang_thanh_thien",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "+2Hz",
            "base_rate": "+4%",
            "timbre_eq": "warm_authority",
            "dialogue_count": 0
        },
        "Duong_Buu": {
            "name": "Dương Bưu",
            "gender": "male",
            "age_stage": "lao_hoa",
            "temperament": "tram_uat_dan_vat",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "-4Hz",
            "base_rate": "-4%",
            "timbre_eq": "aged_gravel",
            "dialogue_count": 0
        },
        "Hoang_Uyen": {
            "name": "Hoàng Uyển",
            "gender": "male",
            "age_stage": "lao_hoa",
            "temperament": "tram_uat_dan_vat",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "-3Hz",
            "base_rate": "-3%",
            "timbre_eq": "aged_gravel",
            "dialogue_count": 0
        },
        "Tuan_Sang": {
            "name": "Tuân Sảng",
            "gender": "male",
            "age_stage": "lao_hoa",
            "temperament": "tram_uat_dan_vat",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "-3Hz",
            "base_rate": "-3%",
            "timbre_eq": "aged_gravel",
            "dialogue_count": 0
        },
        "Chu_Bat": {
            "name": "Chu Bật",
            "gender": "male",
            "age_stage": "trung_nien",
            "temperament": "tram_uat_dan_vat",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "-1Hz",
            "base_rate": "-2%",
            "timbre_eq": "warm_authority",
            "dialogue_count": 0
        },
        "Tao_Thao": {
            "name": "Tào Tháo",
            "gender": "male",
            "age_stage": "thanh_xuan",
            "temperament": "giao_hoat_nham_hiem",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "+0Hz",
            "base_rate": "+0%",
            "timbre_eq": "sharp_cunning",
            "dialogue_count": 0
        },
        "Vien_Thieu": {
            "name": "Viên Thiệu",
            "gender": "male",
            "age_stage": "trung_nien",
            "temperament": "hach_dich_bao_nguoc",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "+2Hz",
            "base_rate": "+2%",
            "timbre_eq": "chest_resonance",
            "dialogue_count": 0
        },
        "Chu_Hau": {
            "name": "Chư Hầu",
            "gender": "male",
            "age_stage": "trung_nien",
            "temperament": "tram_uat_dan_vat",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "-1Hz",
            "base_rate": "-2%",
            "timbre_eq": "warm_authority",
            "dialogue_count": 0
        },
        "La_Bo": {
            "name": "Lã Bố",
            "gender": "male",
            "age_stage": "thanh_xuan",
            "temperament": "hach_dich_bao_nguoc",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "+3Hz",
            "base_rate": "+5%",
            "timbre_eq": "tyrant_arrogant",
            "dialogue_count": 0
        },
        "Tao_Hong": {
            "name": "Tào Hồng",
            "gender": "male",
            "age_stage": "thanh_xuan",
            "temperament": "anh_hung_hao_sang",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "+1Hz",
            "base_rate": "+3%",
            "timbre_eq": "warm_authority",
            "dialogue_count": 0
        },
        "Ha_Hau_Don": {
            "name": "Hạ Hầu Đôn",
            "gender": "male",
            "age_stage": "thanh_xuan",
            "temperament": "anh_hung_hao_sang",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "+3Hz",
            "base_rate": "+6%",
            "timbre_eq": "chest_resonance",
            "dialogue_count": 0
        },
        "Binh_Si": {
            "name": "Binh Sĩ",
            "gender": "male",
            "age_stage": "thanh_xuan",
            "temperament": "trong_sang_thanh_thien",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "+2Hz",
            "base_rate": "+3%",
            "timbre_eq": "warm_authority",
            "dialogue_count": 0
        },
        "Trinh_Pho": {
            "name": "Trình Phổ",
            "gender": "male",
            "age_stage": "lao_hoa",
            "temperament": "anh_hung_hao_sang",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "-4Hz",
            "base_rate": "-3%",
            "timbre_eq": "aged_gravel",
            "dialogue_count": 0
        },
        "Cac_Tuong": {
            "name": "Các Tướng",
            "gender": "male",
            "age_stage": "trung_nien",
            "temperament": "tram_uat_dan_vat",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "-1Hz",
            "base_rate": "-2%",
            "timbre_eq": "warm_authority",
            "dialogue_count": 0
        },
        "Cong_Ton_Toan": {
            "name": "Công Tôn Toản",
            "gender": "male",
            "age_stage": "trung_nien",
            "temperament": "anh_hung_hao_sang",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "-2Hz",
            "base_rate": "-3%",
            "timbre_eq": "warm_authority",
            "dialogue_count": 0
        },
        "Khoai_Viet": {
            "name": "Khoái Việt",
            "gender": "male",
            "age_stage": "trung_nien",
            "temperament": "giao_hoat_nham_hiem",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "+1Hz",
            "base_rate": "+2%",
            "timbre_eq": "sharp_cunning",
            "dialogue_count": 0
        },
        "Luu_Bieu": {
            "name": "Lưu Biểu",
            "gender": "male",
            "age_stage": "trung_nien",
            "temperament": "tram_uat_dan_vat",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "-1Hz",
            "base_rate": "+0%",
            "timbre_eq": "warm_authority",
            "dialogue_count": 0
        }
    }
}

lines = []
current_line_id = 1

def add_line(chunk_id, type_, speaker, text, voice="vi-VN-NamMinhNeural",
             pitch=None, rate=None, lead_in_pause="0.35s", timbre_eq=None,
             emotion=None, character_name=None, narrative_mode=None):
    global current_line_id
    entry = {
        "line_id": current_line_id,
        "chunk_id": chunk_id,
        "type": type_,
        "speaker": speaker
    }
    if type_ == "narrator":
        entry["narrative_mode"] = narrative_mode or "epic"
    elif type_ == "dialogue":
        entry["character_name"] = character_name or theatrical_bible["characters"].get(speaker, {}).get("name", speaker)
        if emotion:
            entry["emotion"] = emotion
    elif type_ == "poem":
        entry["narrative_mode"] = "poetic_recitation"

    entry["text"] = text
    entry["voice"] = voice
    entry["pitch"] = pitch if pitch is not None else "+0Hz"
    entry["rate"] = rate if rate is not None else "-5%"
    entry["lead_in_pause"] = lead_in_pause
    entry["timbre_eq"] = timbre_eq or "intimate_narrator"

    lines.append(entry)
    current_line_id += 1

# ==================== CHUNK 1 ====================
# Line 1: HỒI SÁU
add_line(1, "narrator", "Narrator", "HỒI SÁU", pitch="-2Hz", rate="-12%", lead_in_pause="0.30s", timbre_eq="contemplative_narrator", narrative_mode="contemplative")
# Line 2: . ......
add_line(1, "narrator", "Narrator", ". ......", pitch="-2Hz", rate="-12%", lead_in_pause="1.50s", timbre_eq="contemplative_narrator", narrative_mode="contemplative")
# Line 3: Tiêu đề
add_line(1, "narrator", "Narrator", "ĐỐT KIM QUYẾT, ĐỔNG TRÁC LÀM CÀN,\nGIẤU NGỌC TỶ, TÔN KIÊN TRÁI ƯỚC.", pitch="+1Hz", rate="+0%", lead_in_pause="0.25s", timbre_eq="epic_narrator", narrative_mode="epic")
# Line 4: . ......
add_line(1, "narrator", "Narrator", ". ......", pitch="-2Hz", rate="-12%", lead_in_pause="1.50s", timbre_eq="contemplative_narrator", narrative_mode="contemplative")

# Line 5: Dẫn nhập Tôn Kiên sang trại Viên Thuật
add_line(1, "narrator", "Narrator", "Trương Phi tế ngựa xấn vào cửa quan, nhưng tên và đá bắn xuống như mưa, không thể nào tiến vào được. Phải quay ngựa trở về. Chư hầu tám xứ cùng mời Lưu, Quan, Trương đến mừng công rồi sai người về trại Viên Thiệu báo tin mừng. Thiệu bèn đưa tờ hịch đến Tôn Kiên bảo Kiên tiến binh. Tôn Kiên liền đem Hoàng Cái, Trình Phổ, đến trại Viên Thuật, rồi cầm gậy vạch xuống đất nói rằng.", pitch="+0Hz", rate="-5%", lead_in_pause="0.30s", timbre_eq="epic_narrator", narrative_mode="epic")

# Line 6: Thoại Tôn Kiên với Viên Thuật
add_line(1, "dialogue", "Ton_Kien", "Đổng Trác với tôi thật không có thù hằn gì, nay tôi không nghĩ gì đến thân, xông pha mũi tên hòn đạn để trừ nó. Trước vì nước nhà, sau để báo thù riêng cho nhà tướng quân, trỏ Viên Ngỗi, thế mà tướng quân nghe lời gièm pha. Không phát lương cho tôi, để đến nỗi tôi bị thua, sao tướng quân đành lòng thế được?", pitch="-1Hz", rate="+2%", lead_in_pause="0.45s", timbre_eq="chest_resonance", emotion="cam_phan_trach_moc")

# Line 7: Thuật sợ hãi, người đến báo
add_line(1, "narrator", "Narrator", "Thuật thấy vậy, sợ hãi không biết nói sao, bèn sai đem chém người gièm pha để tạ lỗi Tôn Kiên. Khi ấy, bỗng có người đến báo với Kiên rằng,", pitch="+0Hz", rate="-5%", lead_in_pause="0.35s", timbre_eq="intimate_narrator", narrative_mode="intimate")

# Line 8: Thoại Quân Sĩ báo tin
add_line(1, "dialogue", "Quan_Si", "Trên cửa ải có một tướng cưỡi ngựa đến trại, muốn vào hầu tướng quân.", pitch="+2Hz", rate="+4%", lead_in_pause="0.40s", timbre_eq="warm_authority", emotion="kinh_can_bao_cao")

# Line 9: Kiên về trại, hỏi Lý Thôi
add_line(1, "narrator", "Narrator", "Kiên từ giã Thuật về trại, gọi hỏi ai, hóa ra viên tướng yêu của Đổng Trác, tên là Lý Thôi. Kiên hỏi,", pitch="+0Hz", rate="-5%", lead_in_pause="0.35s", timbre_eq="intimate_narrator", narrative_mode="intimate")

# Line 10: Thoại Tôn Kiên
add_line(1, "dialogue", "Ton_Kien", "Mày lại đây làm gì?", pitch="-1Hz", rate="+3%", lead_in_pause="0.35s", timbre_eq="chest_resonance", emotion="khao_khao_quyet_doan")

# Line 11: Lý Thôi nói
add_line(1, "narrator", "Narrator", "Lý Thôi nói,", pitch="+0Hz", rate="-5%", lead_in_pause="0.30s", timbre_eq="intimate_narrator", narrative_mode="intimate")

# Line 12: Thoại Lý Thôi
add_line(1, "dialogue", "Ly_Thoi", "Thừa tướng chỉ kính trọng tướng quân thôi! Nay thừa tướng muốn kết thân với tướng quân, thừa tướng có một cô con gái muốn gả cho con trai tướng quân.", pitch="+1Hz", rate="+1%", lead_in_pause="0.40s", timbre_eq="sharp_cunning", emotion="xun_xoe_cau_hoa")

# Line 13: Kiên mắng
add_line(1, "narrator", "Narrator", "Tôn Kiên nổi giận mắng rằng,", pitch="+1Hz", rate="+0%", lead_in_pause="0.30s", timbre_eq="dramatic_narrator", narrative_mode="dramatic")

# Line 14: Thoại Tôn Kiên mắng Lý Thôi
add_line(1, "dialogue", "Ton_Kien", "Đổng Trác là thằng nghịch thiên vô đạo, làm xã tắc nghiêng đổ. Ta muốn giết cả chín họ nó đi để tạ thiên hạ, sao lại thèm kết thân với nó! Tao tha chém cho mày, mày về mau đem dâng cửa ải cho tao. Mau mau lên! Chậm thì tao băm xương ra bây giờ!", pitch="+1Hz", rate="+6%", lead_in_pause="0.40s", timbre_eq="chest_resonance", emotion="cuong_no_khinh_bi")

# Line 15: Lý Thôi về, Lý Nho hiến kế
add_line(1, "narrator", "Narrator", "Lý Thôi lủi thủi ra về, kể với Đổng Trác. Trác giận lắm, bèn hỏi Lý Nho. Nho nói,", pitch="+0Hz", rate="-5%", lead_in_pause="0.35s", timbre_eq="intimate_narrator", narrative_mode="intimate")

# Line 16: Thoại Lý Nho dẫn đồng dao
add_line(1, "dialogue", "Ly_Nho", "Lã Ôn Hầu thua trận mới rồi, quân sĩ ngã lòng cả, không có bụng đánh nhau nữa. Nay nên kéo quân về Lạc Dương, đem vua sang Trường An, để ứng vào lời đồng giao mấy hôm nay nói rằng.", pitch="-2Hz", rate="-3%", lead_in_pause="0.42s", timbre_eq="sharp_cunning", emotion="tram_ngam_hien_ke")

# Line 17: . ...... (Đệm thở trước ngâm thơ)
add_line(1, "narrator", "Narrator", ". ......", pitch="-2Hz", rate="-12%", lead_in_pause="1.50s", timbre_eq="contemplative_narrator", narrative_mode="contemplative")

# Line 18-21: Bốn câu đồng dao
add_line(1, "poem", "Narrator", "Mé tây, một nhà Hán,", pitch="-2Hz", rate="-18%", lead_in_pause="0.85s", timbre_eq="poetic_recitation")
add_line(1, "poem", "Narrator", "Mé đông, một nhà Hán.", pitch="-2Hz", rate="-18%", lead_in_pause="0.85s", timbre_eq="poetic_recitation")
add_line(1, "poem", "Narrator", "Hươu chạy, về Trường An,", pitch="-2Hz", rate="-18%", lead_in_pause="0.85s", timbre_eq="poetic_recitation")
add_line(1, "poem", "Narrator", "Mới khỏi, phải gặp nạn.", pitch="-2Hz", rate="-18%", lead_in_pause="0.85s", timbre_eq="poetic_recitation")

# Line 22: . ...... (Đệm thở sau thơ)
add_line(1, "narrator", "Narrator", ". ......", pitch="-2Hz", rate="-12%", lead_in_pause="1.50s", timbre_eq="contemplative_narrator", narrative_mode="contemplative")

# Line 23: Thoại Lý Nho giải thích đồng dao
add_line(1, "dialogue", "Ly_Nho", "Mé tây một nhà Hán nghĩa là, đức Cao Tổ ngày xưa đóng đô ở Trường An, truyền ngôi được mười hai vua. Mé đông một nhà Hán nghĩa là, Vua Quang Vũ đóng đô ở Lạc Dương, cũng truyền ngôi được mười hai vua. Thế là vận trời xoay vần. Nay thừa tướng lại lên thiên đô về Trường An, mới khỏi lo được.", pitch="-1Hz", rate="-2%", lead_in_pause="0.45s", timbre_eq="sharp_cunning", emotion="giai_thich_sau_sac")

# Line 24: Trác mừng
add_line(1, "narrator", "Narrator", "Trác mừng nói rằng,", pitch="+0Hz", rate="-5%", lead_in_pause="0.30s", timbre_eq="intimate_narrator", narrative_mode="intimate")

# Line 25: Thoại Đổng Trác
add_line(1, "dialogue", "Dong_Trac", "Ngươi không nói thì ta không biết!", pitch="+3Hz", rate="+3%", lead_in_pause="0.35s", timbre_eq="tyrant_arrogant", emotion="dac_y_mung_ro")


# ==================== CHUNK 2 ====================
# Line 26: Trác hội quan văn võ
add_line(2, "narrator", "Narrator", "Trác bèn đem Lã Bố về Lạc Dương, rồi hội ngay các quan văn võ để bàn việc thiên đô. Khi các quan đã đến đông, Trác nói rằng,", pitch="+0Hz", rate="-5%", lead_in_pause="0.30s", timbre_eq="epic_narrator", narrative_mode="epic")

# Line 27: Thoại Đổng Trác tuyên bố dời đô
add_line(2, "dialogue", "Dong_Trac", "Nhà Hán ta ở Lạc Dương, hơn hai trăm năm nay, khi số đã hết. Ta xem bây giờ vượng khí tụ ở Trường An. Vậy ta muốn rước vua về đó, các quan nên gấp rút sắm sửa hành trang.", pitch="+3Hz", rate="+2%", lead_in_pause="0.42s", timbre_eq="tyrant_arrogant", emotion="uy_hiep_ra_lenh")

# Line 28: Dương Bưu can ngăn
add_line(2, "narrator", "Narrator", "Tư đồ là Dương Bưu nói rằng,", pitch="+0Hz", rate="-5%", lead_in_pause="0.35s", timbre_eq="intimate_narrator", narrative_mode="intimate")

# Line 29: Thoại Dương Bưu
add_line(2, "dialogue", "Duong_Buu", "Trường An bị tàn phá đã lâu rồi. Nay bỗng dưng ta bỏ cả tôn miếu, hoàng lăng mà đi sang đó, tôi sợ rằng thiên hạ kinh động. Mà thiên hạ kinh động lên thì dễ, yên lại thì khó. Xin thừa tướng hãy xét cho kỹ.", pitch="-4Hz", rate="-4%", lead_in_pause="0.45s", timbre_eq="aged_gravel", emotion="khuyen_can_chinh_truc")

# Line 30: Trác giận mắng Dương Bưu
add_line(2, "narrator", "Narrator", "Trác giận mắng Dương Bưu,", pitch="+1Hz", rate="+0%", lead_in_pause="0.30s", timbre_eq="dramatic_narrator", narrative_mode="dramatic")

# Line 31: Thoại Đổng Trác
add_line(2, "dialogue", "Dong_Trac", "Ngươi lại dám ngăn trở việc lớn nước nhà à?", pitch="+4Hz", rate="+5%", lead_in_pause="0.35s", timbre_eq="tyrant_arrogant", emotion="quat_mang_de_doa")

# Line 32: Hoàng Uyển tiếp lời
add_line(2, "narrator", "Narrator", "Thái úy là Hoàng Uyển cũng nói rằng,", pitch="+0Hz", rate="-5%", lead_in_pause="0.35s", timbre_eq="intimate_narrator", narrative_mode="intimate")

# Line 33: Thoại Hoàng Uyển
add_line(2, "dialogue", "Hoang_Uyen", "Dương tư đồ nói thế phải đấy, Trước kia trong lúc Vương Mãng thoán nghịch. Kế đến Canh Thủy, Xích Mi nổi loạn, Trường An bị đốt cháy thành ra tro sỏi. Vả lại nhân dân xiêu tán, trăm phần không còn một hai phần. Tôi nghĩ không nên bỏ cả cung điện mà đi ra chỗ đất hoang ấy.", pitch="-3Hz", rate="-3%", lead_in_pause="0.45s", timbre_eq="aged_gravel", emotion="can_gian_thiet_tha")

# Line 34: Trác gắt
add_line(2, "narrator", "Narrator", "Trác nói,", pitch="+0Hz", rate="-5%", lead_in_pause="0.30s", timbre_eq="intimate_narrator", narrative_mode="intimate")

# Line 35: Thoại Đổng Trác
add_line(2, "dialogue", "Dong_Trac", "Ở Lạc Dương đây trộm giặc nhiều lắm, nhân dân hoạn lạc, đi mất cả. Trường An có núi Hào, núi Hàm hiểm trở, lại gần Lũng Hữu, đá gỗ và gạch ngói dễ kiếm, sửa sang cung thất. Độ hơn một tháng thì xong, không ai được nói lôi thôi nữa!", pitch="+3Hz", rate="+4%", lead_in_pause="0.42s", timbre_eq="tyrant_arrogant", emotion="chuyen_quyen_doc_doan")

# Line 36: Tuân Sảng can
add_line(2, "narrator", "Narrator", "Tư đồ là Tuân Sảng lại can rằng,", pitch="+0Hz", rate="-5%", lead_in_pause="0.35s", timbre_eq="intimate_narrator", narrative_mode="intimate")

# Line 37: Thoại Tuân Sảng
add_line(2, "dialogue", "Tuan_Sang", "Thừa tướng thiên đô đi thì thiên hạ tất sẽ nhiễu động ngay.", pitch="-3Hz", rate="-3%", lead_in_pause="0.40s", timbre_eq="aged_gravel", emotion="lo_lang_can_gian")

# Line 38: Trác tức mình gắt
add_line(2, "narrator", "Narrator", "Trác tức mình gắt rằng,", pitch="+1Hz", rate="+0%", lead_in_pause="0.30s", timbre_eq="dramatic_narrator", narrative_mode="dramatic")

# Line 39: Thoại Đổng Trác
add_line(2, "dialogue", "Dong_Trac", "Ta vì thiên hạ mà lo việc thiên đô, có xá gì những đứa tiểu dân!", pitch="+4Hz", rate="+5%", lead_in_pause="0.35s", timbre_eq="tyrant_arrogant", emotion="gat_gong_khinh_thi")

# Line 40: Chu Bật can
add_line(2, "narrator", "Narrator", "Ngay hôm ấy Trác cách chức Dương Bưu, Hoàng Uyển, Tuân Sảng, giáng xuống làm thứ dân. Trác trở ra lên xe, thấy có hai người đứng trước vái, trông ra thì là thượng thư Chu Bật và hiệu úy Ngũ Quyền. Trác hỏi có việc gì. Bật nói,", pitch="+0Hz", rate="-5%", lead_in_pause="0.35s", timbre_eq="intimate_narrator", narrative_mode="intimate")

# Line 41: Thoại Chu Bật
add_line(2, "dialogue", "Chu_Bat", "Chúng tôi nghe thừa tướng muốn thiên đô, nên lại can ngăn.", pitch="-1Hz", rate="-2%", lead_in_pause="0.40s", timbre_eq="warm_authority", emotion="khang_khai_can_gian")

# Line 42: Trác giận nói
add_line(2, "narrator", "Narrator", "Trác giận nói,", pitch="+1Hz", rate="+0%", lead_in_pause="0.30s", timbre_eq="dramatic_narrator", narrative_mode="dramatic")

# Line 43: Thoại Đổng Trác
add_line(2, "dialogue", "Dong_Trac", "Trước tao nghe hai chúng bay, dùng thằng Viên Thiệu cho nó làm quan, bây giờ nó làm phản. Thế ra nó với chúng bay cùng một đảng!", pitch="+4Hz", rate="+6%", lead_in_pause="0.35s", timbre_eq="tyrant_arrogant", emotion="cuong_no_nghi_ngo")

# Line 44: Chém Chu Bật, Lý Nho xui
add_line(2, "narrator", "Narrator", "Nói rồi Trác sai võ sĩ đem Chu Bật, Ngũ Quỳnh ra cửa phủ chém, rồi hạ lệnh thiên đô. Hạn đến ngày hôm sau phải đi. Lý Nho xui Đổng Trác,", pitch="+0Hz", rate="-5%", lead_in_pause="0.35s", timbre_eq="suspense_narrator", narrative_mode="suspense")

# Line 45: Thoại Lý Nho xui cướp của
add_line(2, "dialogue", "Ly_Nho", "Nay tiền lương thiếu thốn nhiều, ở Lạc Dương nhiều nhà giàu, ta nên tịch thu của cải. Lấy phát lương cho quân. Phàm bao nhiêu môn hạ Viên Thiệu ngày trước, nên đem giết cả đi để lấy của, sẽ thu được vô số.", pitch="-1Hz", rate="-1%", lead_in_pause="0.42s", timbre_eq="sharp_cunning", emotion="doc_ac_hien_ke")


# ==================== CHUNK 3 ====================
# Line 46: Cướp phá Lạc Dương, Tào Tháo đến gặp Viên Thiệu
add_line(3, "narrator", "Narrator", "Trác lập tức sai năm nghìn quân thiết kỵ đi bắt cả những người giàu ở Lạc Dương, cả thảy mấy nghìn hộ. Mỗi người cầm một lá cờ lên đầu, để bốn chữ Phản thần nghịch đảng rồi đem ra ngoài thành chém tuốt. Bao nhiêu của cải lấy sạch. Lý Thôi, Quách Dĩ bắt hết cả dân Lạc Dương, ước mấy trăm vạn, đưa sang Trường An. Cứ mỗi một toán dân lại cho một đội quân đi đàn áp, người chết ở dọc đường không biết bao nhiêu mà kể. Lại cho quân sĩ đi hãm hiếp đàn bà con gái, cướp hết lương thực của dân, tiếng kêu khóc động trời chuyển đất. Người nào đi chậm, đằng sau có quân lính đốc thúc, quân lính cầm dao, giết người ngay ở giữa đường. Lúc Trác ra đi, sai phóng hỏa đốt cả cửa nhà dân chúng, và tôn miếu, cung phủ, Nam, Bắc hai cung, lửa khói mù mịt. Bao nhiêu cung cấm hóa ra tro cả. Trác lại sai Lã Bố khai quật hết cả những lăng tiên hoàng, hậu phi để lấy vàng bạc châu báu. Quân sĩ thấy vậy cũng thừa thế đào mả các nhà quan, nhà dân. Đổng Trác sai xếp những đồ vàng bạc vóc nhiễu được vài nghìn xe, rồi bức thiên tử và hậu phi phải sang Trường An. Tướng Đổng Trác tên là Triệu Xầm, thấy Trác đã bỏ Lạc Dương, bèn dâng ngay cửa Dĩ Thủy cho Tôn Kiên. Kiên kéo binh vào trước, Lưu Bị, Quan Vũ, Trương Phi vào cửa Hổ Lao, chư hầu cũng dẫn quân vào cả. Tôn Kiên đi đến Lạc Dương thấy trong thành lửa cháy ngùn ngụt, ngọn lửa bốc lên tận trời, dưới đất khói đen mù mịt. Trong một quãng hai ba trăm dặm, tịnh không có tiếng gà kêu chó cắn. Đầu tiên Kiên sai quân vào dập lửa, đoạn ra lệnh cho chư hầu đến đóng quân mã ở trên bãi đất hoang. Tào Tháo đến, thấy Viên Thiệu cũng ở đấy, bèn hỏi rằng,", pitch="+0Hz", rate="-5%", lead_in_pause="0.30s", timbre_eq="epic_narrator", narrative_mode="epic")

# Line 47: Thoại Tào Tháo hỏi Viên Thiệu
add_line(3, "dialogue", "Tao_Thao", "Nay Đổng tặc đã kéo về Trường An rồi. Ta nên thừa thế mà đuổi theo bắt nó mới phải, Bản Sơ lại đóng quân ở đây, là ý làm sao?", pitch="+1Hz", rate="+3%", lead_in_pause="0.42s", timbre_eq="sharp_cunning", emotion="hoi_don_chat_van")

# Line 48: Thiệu đáp
add_line(3, "narrator", "Narrator", "Thiệu nói,", pitch="+0Hz", rate="-5%", lead_in_pause="0.30s", timbre_eq="intimate_narrator", narrative_mode="intimate")

# Line 49: Thoại Viên Thiệu
add_line(3, "dialogue", "Vien_Thieu", "Chư hầu đều mỏi mệt cả, đuổi theo, tôi sợ không được việc gì.", pitch="+2Hz", rate="-2%", lead_in_pause="0.40s", timbre_eq="chest_resonance", emotion="do_du_chan_chu")

# Line 50: Tháo giục
add_line(3, "narrator", "Narrator", "Tháo nói,", pitch="+0Hz", rate="-5%", lead_in_pause="0.30s", timbre_eq="intimate_narrator", narrative_mode="intimate")

# Line 51: Thoại Tào Tháo
add_line(3, "dialogue", "Tao_Thao", "Thằng giặc Đổng Trác đốt cung thất, bức vua thiên đô, Trong nước rối động, dân không biết theo ai. Ấy là lúc trời hại nó đấy, nhân lúc này chỉ đánh một trận là yên thiên hạ, sao các ông không đánh?", pitch="+1Hz", rate="+2%", lead_in_pause="0.42s", timbre_eq="sharp_cunning", emotion="hung_hon_thuyet_phuc")

# Line 52: Chư hầu can
add_line(3, "narrator", "Narrator", "Chư hầu đều nói,", pitch="+0Hz", rate="-5%", lead_in_pause="0.30s", timbre_eq="intimate_narrator", narrative_mode="intimate")

# Line 53: Thoại Chư Hầu
add_line(3, "dialogue", "Chu_Hau", "Ta không nên khinh động.", pitch="-1Hz", rate="-2%", lead_in_pause="0.40s", timbre_eq="warm_authority", emotion="ngai_ngan_ru_re")

# Line 54: Tháo mắng
add_line(3, "narrator", "Narrator", "Tháo giận nói rằng,", pitch="+1Hz", rate="+0%", lead_in_pause="0.30s", timbre_eq="dramatic_narrator", narrative_mode="dramatic")

# Line 55: Thoại Tào Tháo mắng chư hầu
add_line(3, "dialogue", "Tao_Thao", "Đồ trẻ con cả, không đáng cùng mưu đồ việc lớn!", pitch="+2Hz", rate="+5%", lead_in_pause="0.35s", timbre_eq="sharp_cunning", emotion="gian_du_khinh_miet")


# ==================== CHUNK 4 ====================
# Line 56: Tháo đuổi theo, Lý Nho hiến kế phục binh
add_line(4, "narrator", "Narrator", "Nói rồi tự dẫn hơn một vạn quân, sai Hạ Hầu Đôn, Hạ Hầu Uyên, Tào Nhân, Tào Hồng, Lý Điển, Nhạc Tiến. Luôn ngày đêm đuổi theo Đổng Trác. Khi Đổng Trác đi đến Vinh Dương, thái thú là Từ Vinh ra tiếp. Lý Nho nói,", pitch="+0Hz", rate="-5%", lead_in_pause="0.30s", timbre_eq="epic_narrator", narrative_mode="epic")

# Line 57: Thoại Lý Nho
add_line(4, "dialogue", "Ly_Nho", "Thừa tướng mới đi khỏi Lạc Dương. Tôi sợ có quân đuổi theo nên sai Từ Vinh phục quân ở bên cạnh núi ngoài thành. Hễ có quân đuổi theo đi qua thì cứ để cho đi, đợi khi nào đi khỏi chỗ quân phục, trong này ta đánh trở ra. Nó tất thua chạy, bấy giờ ông sẽ đánh chen đường, còn quân đi sau tất không dám đuổi nữa.", pitch="-1Hz", rate="-2%", lead_in_pause="0.45s", timbre_eq="sharp_cunning", emotion="muu_sau_ke_doc")

# Line 58: Lã Bố chặn hậu
add_line(4, "narrator", "Narrator", "Trác nghe kế ấy, sai Lã Bố đem tinh binh đi chặn hậu. Bố đang đi bỗng có một toán quân Tào xấn đến. Bố cười nói rằng,", pitch="+0Hz", rate="-5%", lead_in_pause="0.35s", timbre_eq="epic_narrator", narrative_mode="epic")

# Line 59: Thoại Lã Bố
add_line(4, "dialogue", "La_Bo", "Lý Nho đoán không nhầm!", pitch="+3Hz", rate="+3%", lead_in_pause="0.35s", timbre_eq="tyrant_arrogant", emotion="kieu_ngao_dac_y")

# Line 60: Tào Tháo quát
add_line(4, "narrator", "Narrator", "Bố đem quân mã bày dàn, Tào Tháo tế ngựa gọi to,", pitch="+1Hz", rate="+0%", lead_in_pause="0.30s", timbre_eq="dramatic_narrator", narrative_mode="dramatic")

# Line 61: Thoại Tào Tháo
add_line(4, "dialogue", "Tao_Thao", "Nghịch tặc! Bay bức thiên tử và đem trăm họ đi đâu?", pitch="+2Hz", rate="+4%", lead_in_pause="0.35s", timbre_eq="sharp_cunning", emotion="kich_bac_quat_mang")

# Line 62: Lã Bố mắng
add_line(4, "narrator", "Narrator", "Lã Bố mắng rằng,", pitch="+1Hz", rate="+0%", lead_in_pause="0.30s", timbre_eq="dramatic_narrator", narrative_mode="dramatic")

# Line 63: Thoại Lã Bố
add_line(4, "dialogue", "La_Bo", "Thằng phản chủ kia, sao dám nói càn?", pitch="+3Hz", rate="+5%", lead_in_pause="0.35s", timbre_eq="tyrant_arrogant", emotion="cuong_no_khinh_miet")

# Line 64: Giao tranh dữ dội, Tháo trúng tên gặp Tào Hồng
add_line(4, "narrator", "Narrator", "Hạ Hầu Đôn vác giáo nhảy ngựa, xông thẳng vào để đâm Lã Bố. Đôn với Bố đánh nhau được vài hiệp. Lý Thôi dẫn một đội quân từ bên tả kéo ra. Tháo lại sai Hạ Hầu Uyên ra địch. Lúc bấy giờ lại thấy ở bên hữu có tiếng reo. Quách Dĩ kéo quân ra. Tháo sai Tào Nhân ra địch, nhưng đằng kia ba mặt quân mã đánh dồn lại, thế khó đương nổi. Hạ Hầu Đôn chống với Lã Bố không lại, phi ngựa chạy về. Bố thúc quân vào đánh gấp. Quân Tháo thua chạy kéo về Vinh Dương. Khi chạy đến dưới sườn núi, bấy giờ đã canh hai, trăng sáng như ban ngày. Tháo sắp sửa hội quân lại làm bếp thổi cơm ăn, bỗng nghe thấy bốn mặt tiếng reo ầm ầm. Quân phục của Từ Vinh xông ra. Tào Tháo vội vàng tế ngựa cướp đường chạy trốn, không ngờ gặp ngay Từ Vinh, Tháo lại quay đầu chạy. Vinh giương cung bắn một phát tên trúng ngay vào vai Tháo. Tháo vừa đeo tên vừa chạy, chạy qua một rặng núi, có hai tên lính phục trong đám cỏ, trông thấy ngựa Tháo đi đến. Hai ngọn giáo cùng phóng ra. May đâu một tướng vừa tế ngựa đến, múa dao chém chết hai tên lính, cứu được Tào Tháo. Tháo trông xem ai thì là Tào Hồng. Tháo bảo Hồng rằng,", pitch="+0Hz", rate="-5%", lead_in_pause="0.30s", timbre_eq="epic_narrator", narrative_mode="epic")

# Line 65: Thoại Tào Tháo
add_line(4, "dialogue", "Tao_Thao", "Thôi! Ta đành chết ở đây, hiền đệ nên trốn đi mau.", pitch="-2Hz", rate="-4%", lead_in_pause="0.42s", timbre_eq="sharp_cunning", emotion="tuyet_vong_buong_xuoi")

# Line 66: Hồng đáp
add_line(4, "narrator", "Narrator", "Hồng nói rằng,", pitch="+0Hz", rate="-5%", lead_in_pause="0.30s", timbre_eq="intimate_narrator", narrative_mode="intimate")

# Line 67: Thoại Tào Hồng
add_line(4, "dialogue", "Tao_Hong", "Xin ông lên ngựa ngay. Tôi tình nguyện đi bộ.", pitch="+1Hz", rate="+3%", lead_in_pause="0.38s", timbre_eq="warm_authority", emotion="trung_nghia_qua_quyet")

# Line 68: Tháo hỏi
add_line(4, "narrator", "Narrator", "Tháo hỏi,", pitch="+0Hz", rate="-5%", lead_in_pause="0.30s", timbre_eq="intimate_narrator", narrative_mode="intimate")

# Line 69: Thoại Tào Tháo
add_line(4, "dialogue", "Tao_Thao", "Giặc đuổi đến nơi, ngươi làm thế nào?", pitch="+1Hz", rate="+2%", lead_in_pause="0.38s", timbre_eq="sharp_cunning", emotion="kinh_ngac_lo_lang")

# Line 70: Hồng đáp câu bất hủ
add_line(4, "narrator", "Narrator", "Hồng nói,", pitch="+0Hz", rate="-5%", lead_in_pause="0.30s", timbre_eq="intimate_narrator", narrative_mode="intimate")

# Line 71: Thoại Tào Hồng
add_line(4, "dialogue", "Tao_Hong", "Thiên hạ có thể không có tôi, nhưng không thể không có ông!", pitch="+1Hz", rate="+1%", lead_in_pause="0.42s", timbre_eq="warm_authority", emotion="chi_khi_hao_sang")

# Line 72: Tháo cảm kích
add_line(4, "narrator", "Narrator", "Tháo nói,", pitch="+0Hz", rate="-5%", lead_in_pause="0.30s", timbre_eq="intimate_narrator", narrative_mode="intimate")

# Line 73: Thoại Tào Tháo
add_line(4, "dialogue", "Tao_Thao", "Ta nếu lại được sống, thực là nhờ ngươi đó!", pitch="-1Hz", rate="-2%", lead_in_pause="0.40s", timbre_eq="sharp_cunning", emotion="cam_kich_sau_sac")

# Line 74: Tháo lên ngựa
add_line(4, "narrator", "Narrator", "Tháo lên ngựa.", pitch="+0Hz", rate="-5%", lead_in_pause="0.30s", timbre_eq="intimate_narrator", narrative_mode="intimate")


# ==================== CHUNK 5 ====================
# Line 75: Chạy qua sông, Tháo bi quan
add_line(5, "narrator", "Narrator", "Hồng cởi áo giáp, cắp dao chạy theo sau. Chạy đến độ canh tư, chẹn mất đường đi. Đằng sau nghe thấy tiếng reo hò đã đến nơi. Tháo nói,", pitch="+0Hz", rate="-5%", lead_in_pause="0.30s", timbre_eq="suspense_narrator", narrative_mode="suspense")

# Line 76: Thoại Tào Tháo
add_line(5, "dialogue", "Tao_Thao", "Thôi! Mệnh ta đến thế này, sống sao được nữa!", pitch="-2Hz", rate="-3%", lead_in_pause="0.40s", timbre_eq="sharp_cunning", emotion="bi_phan_tuyet_vong")

# Line 77: Cõng qua sông, Hạ Hầu Đôn cứu viện
add_line(5, "narrator", "Narrator", "Hồng kíp vực Tháo xuống ngựa, cởi áo bào ra, cõng Tháo lội qua sông. Vừa sang đến bờ sông bên kia, quân đuổi cũng vừa đến, tên bắn qua sông như mưa, Tháo cứ mặc cả quần áo ướt. Lướt thướt mà chạy, chạy mãi đến mờ mờ sáng, được ba mươi dặm, đến một gò đất mới tạm ngồi nghỉ hơi một chốc. Bỗng nghe có tiếng reo, một toán quân mã kéo lại. Thì ra Từ Vinh cứ bên kia sông chạy theo lên mạn trên sang đò đuổi kịp. Trong khi Tháo đương hoảng hốt. Hạ Hầu Đôn, Hạ Hầu Uyên vừa đem vài mươi quân kỵ đến, quát to lên rằng,", pitch="+0Hz", rate="-5%", lead_in_pause="0.30s", timbre_eq="epic_narrator", narrative_mode="epic")

# Line 78: Thoại Hạ Hầu Đôn quát Từ Vinh
add_line(5, "dialogue", "Ha_Hau_Don", "Từ Vinh, chớ được hại chủ ta!", pitch="+3Hz", rate="+6%", lead_in_pause="0.35s", timbre_eq="chest_resonance", emotion="hoi_het_xung_tran")

# Line 79: Đôn đâm chết Vinh, Kiên ngắm sao đêm
add_line(5, "narrator", "Narrator", "Vinh xông đến đánh Hạ Hầu Đôn. Đôn vác giáo đâm Vinh ngã xuống ngựa, rồi đánh tan quân Vinh. Đằng sau, Tào Nhân, Lý Điển, Nhạc Tiến cũng dần dần tìm đến, ra mắt Tào Tháo, nửa lo nửa mừng. Tháo thu thập tàn quân, còn độ năm trăm, kéo về Hà Nội. Tàn quân của Trác chạy về Trường An. Đây nói ở Lạc Dương, các chư hầu chia quân đóng trại. Tôn Kiên dập tắt lửa trong cung, đóng quân trong thành. Đặt trướng ngay trên nền đền Kiến Chương rồi sai quân quét dọn những gạch ngói ở các cung điện. Phàm những lăng tẩm mà Đổng Trác đã khai quật lên, Kiên sai chôn cất lại cả. Lại cất ba gian điện, lợp cỏ ở trên nền nhà Thái Miếu, đặt linh vị các vua, giết trâu mổ bò. Mời các chư hầu đến tế. Tế xong rồi, các tướng ai về trại ấy. Kiên về trại, đêm hôm ấy trăng sao vằng vặc, Kiên cầm thanh kiếm ra sân. Ngẩng mặt lên xem thiên văn thấy trong tòa tử vi có khí trắng lờ mờ. Kiên than rằng,", pitch="-1Hz", rate="-8%", lead_in_pause="0.35s", timbre_eq="contemplative_narrator", narrative_mode="contemplative")

# Line 80: Thoại Tôn Kiên than thở
add_line(5, "dialogue", "Ton_Kien", "Đế tinh không được tỏ, cho nên, tặc thần loạn nước, muôn dân phải lầm than, kinh thành không còn gì nữa.", pitch="-2Hz", rate="-4%", lead_in_pause="0.45s", timbre_eq="chest_resonance", emotion="than_tho_bi_trang")

# Line 81: Binh sĩ trỏ giếng
add_line(5, "narrator", "Narrator", "Vừa nói vừa rỏ nước mắt khóc. Bên cạnh có tên lính trỏ tay bảo Kiên rằng,", pitch="+0Hz", rate="-5%", lead_in_pause="0.35s", timbre_eq="intimate_narrator", narrative_mode="intimate")

# Line 82: Thoại Binh Sĩ
add_line(5, "dialogue", "Binh_Si", "Kia, ở phía nam điện này có hào quang năm sắc. Từ dưới đáy giếng bốc lên.", pitch="+2Hz", rate="+3%", lead_in_pause="0.38s", timbre_eq="warm_authority", emotion="kinh_ngac_phat_hien")

# Line 83: Kiên sai tìm
add_line(5, "narrator", "Narrator", "Kiên liền sai quân sĩ đốt đuốc xuống giếng tìm xem.", pitch="+0Hz", rate="-5%", lead_in_pause="0.30s", timbre_eq="intimate_narrator", narrative_mode="intimate")


# ==================== CHUNK 6 ====================
# Line 84: Vớt được ngọc tỷ, hỏi Trình Phổ
add_line(6, "narrator", "Narrator", "Một lát quân mò đem lên được một cái thây người đàn bà chết đã lâu ngày nhưng chưa nát. Người này mặc theo lối của cung đình, dưới cổ có đeo một cái túi gấm. Mở túi ra xem thấy có một cái hộp nhỏ son son, khóa vàng, mở ra thấy một cái ấn bằng ngọc, vuông bốn tấc. Trên núm dấu chạm năm con rồng, bên cạnh có sứt một miếng phải lấy vàng bịt lại, mặt dấu khắc tám chữ triện. Phụ mệnh vu thiên, ký thọ vĩnh xương, Kiên được ấn ngọc ấy, hỏi Trình Phổ. Phổ nói,", pitch="+0Hz", rate="-5%", lead_in_pause="0.35s", timbre_eq="suspense_narrator", narrative_mode="suspense")

# Line 85: Thoại Trình Phổ kể lai lịch ngọc tỷ
add_line(6, "dialogue", "Trinh_Pho", "Đấy là ngọc tỳ truyền quốc. Ngày xưa, Biện Hòa ở dưới núi Kinh Sơn trông thấy chim phượng hoàng đậu ở trên hòn đá. Đem đá ấy về tiến vua Văn Vương nước Sở. Lúc phá đá ra trong có hòn ngọc. Đến đời nhà Tần, năm thứ hai mươi sáu, hai trăm hai mươi mốt trước công nguyên. Vua Tần sai thợ ngọc giũa ra làm ấn quốc bảo. Tám chữ triện viết ở trên mặt ấn là chữ Lý Tư. Năm thứ hai mươi tám Tần Thủy Hoàng đi tuần đến hồ Động Đình, gặp sóng to gió lớn, thuyền sắp đắm. Vua vội vàng ném ngọc tỷ ấy xuống hồ mới không việc gì. Đến năm thứ ba mươi tám, Thủy Hoàng đi tuần đến núi Hoa Âm, đương đi gặp một người tay cầm ngọc tỷ đứng đón đường. Đưa cho quân hầu nói rằng, Đem cái này về trả Tổ Long. Nói xong rồi biến mất. Ấn ngọc ấy lại về nhà Tần. Đến năm sau, Thủy Hoàng mất. Tử Anh đem ngọc tỷ dâng vua Cao Tổ nhà Hán. Đến lúc Vương Mãng khởi loạn, Hoàng hậu, vua Hiếu Nguyên cầm ngọc ấy đánh Vương Tâm. Tô Hiến sứt mất một góc, phải lấy vàng bịt vào. Vua Quang Vũ được ấn ngọc ấy ở Nghi Dương, truyền đến bây giờ. Khi mười tên hoạn quan làm loạn, bức đem Thiếu Đế ra Bắc Mang, lúc về thấy mất ngọc tỷ. Nay tướng quân lại tìm được, tất là trời cho tướng quân đó. Điềm này là điềm báo tướng quân sẽ làm vua. Vậy tướng quân không nên ở lâu chốn này, mà nên về ngay Giang Đông để mưu toan việc lớn!", pitch="-4Hz", rate="-3%", lead_in_pause="0.45s", timbre_eq="aged_gravel", emotion="triet_ly_khuyen_giai")

# Line 86: Thoại Tôn Kiên đồng ý lui binh
add_line(6, "dialogue", "Ton_Kien", "Ngươi nói chính hợp ý ta. Ngày mai ta sẽ cáo bệnh về.", pitch="-1Hz", rate="+2%", lead_in_pause="0.40s", timbre_eq="chest_resonance", emotion="dong_tinh_quyet_doan")

# Line 87: Lẻn báo Viên Thiệu, Kiên sang từ biệt
add_line(6, "narrator", "Narrator", "Bàn định xong, Kiên truyền quân sĩ không được nói hở cho ai biết. Không ngờ trong đám quân sĩ có một người cùng làng với Viên Thiệu, biết việc đó, muốn nhân dịp tiến thân. Ngay đêm hôm ấy lẻn sang báo với Viên Thiệu. Thiệu thưởng cho người ấy rồi giữ lại ở trong quân. Hôm sau Tôn Kiên sang trại Viên Thiệu để cáo từ, nói rằng,", pitch="+0Hz", rate="-5%", lead_in_pause="0.35s", timbre_eq="intimate_narrator", narrative_mode="intimate")

# Line 88: Thoại Tôn Kiên cáo từ
add_line(6, "dialogue", "Ton_Kien", "Tôi hơi khó ở, xin phép về Trường Sa.", pitch="-1Hz", rate="-1%", lead_in_pause="0.38s", timbre_eq="chest_resonance", emotion="gia_vo_tu_ta")

# Line 89: Thiệu cười nói
add_line(6, "narrator", "Narrator", "Thiệu cười nói rằng,", pitch="+0Hz", rate="-5%", lead_in_pause="0.30s", timbre_eq="intimate_narrator", narrative_mode="intimate")

# Line 90: Thoại Viên Thiệu
add_line(6, "dialogue", "Vien_Thieu", "Tôi đã biết bệnh ông rồi.", pitch="+2Hz", rate="+0%", lead_in_pause="0.38s", timbre_eq="chest_resonance", emotion="mia_mai_hiem_hiem")


# ==================== CHUNK 7 ====================
# Line 91: Thoại Viên Thiệu vạch trần
add_line(7, "dialogue", "Vien_Thieu", "Bệnh ấy là bệnh ngọc tỷ!", pitch="+3Hz", rate="+2%", lead_in_pause="0.38s", timbre_eq="chest_resonance", emotion="vach_tran_che_gieu")

# Line 92: Kiên thất sắc hỏi
add_line(7, "narrator", "Narrator", "Kiên thất sắc, hỏi rằng,", pitch="+0Hz", rate="-5%", lead_in_pause="0.30s", timbre_eq="suspense_narrator", narrative_mode="suspense")

# Line 93: Thoại Tôn Kiên
add_line(7, "dialogue", "Ton_Kien", "Ai nói với ông thế?", pitch="+1Hz", rate="+3%", lead_in_pause="0.35s", timbre_eq="chest_resonance", emotion="giat_minh_hoi_don")

# Line 94: Thiệu nói
add_line(7, "narrator", "Narrator", "Thiệu nói,", pitch="+0Hz", rate="-5%", lead_in_pause="0.30s", timbre_eq="intimate_narrator", narrative_mode="intimate")

# Line 95: Thoại Viên Thiệu đòi ngọc tỷ
add_line(7, "dialogue", "Vien_Thieu", "Nay chúng ta vì nước đánh giặc. Ngọc tỷ là của báu triều đình. Ông bắt được, nên ở chỗ minh chủ, đợi khi nào giết được Đổng Trác, thì đem trả lại nhà vua. Nay ông giấu ấn ấy mà bỏ đi, định làm gì?", pitch="+2Hz", rate="+1%", lead_in_pause="0.42s", timbre_eq="chest_resonance", emotion="ap_dat_hach_hoi")

# Line 96: Kiên chối
add_line(7, "narrator", "Narrator", "Kiên cứ chối,", pitch="+0Hz", rate="-5%", lead_in_pause="0.30s", timbre_eq="intimate_narrator", narrative_mode="intimate")

# Line 97: Thoại Tôn Kiên
add_line(7, "dialogue", "Ton_Kien", "Ngọc tỷ làm gì có ở tôi?", pitch="-1Hz", rate="+1%", lead_in_pause="0.35s", timbre_eq="chest_resonance", emotion="choi_quanh_cung_ran")

# Line 98: Thiệu ép
add_line(7, "narrator", "Narrator", "Thiệu nói,", pitch="+0Hz", rate="-5%", lead_in_pause="0.30s", timbre_eq="intimate_narrator", narrative_mode="intimate")

# Line 99: Thoại Viên Thiệu
add_line(7, "dialogue", "Vien_Thieu", "Cái gì bắt được ở dưới giếng đền Kiến Chương, bây giờ đâu?", pitch="+3Hz", rate="+3%", lead_in_pause="0.38s", timbre_eq="chest_resonance", emotion="hoi_ep_don_dap")

# Line 100: Kiên phản bác
add_line(7, "narrator", "Narrator", "Kiên nói,", pitch="+0Hz", rate="-5%", lead_in_pause="0.30s", timbre_eq="intimate_narrator", narrative_mode="intimate")

# Line 101: Thoại Tôn Kiên
add_line(7, "dialogue", "Ton_Kien", "Tôi không có của ấy. Cưỡng bức nhau làm gì thế?", pitch="-1Hz", rate="+2%", lead_in_pause="0.38s", timbre_eq="chest_resonance", emotion="cuong_nghinh_phan_bac")

# Line 102: Thiệu đe dọa
add_line(7, "narrator", "Narrator", "Thiệu nói,", pitch="+0Hz", rate="-5%", lead_in_pause="0.30s", timbre_eq="intimate_narrator", narrative_mode="intimate")

# Line 103: Thoại Viên Thiệu
add_line(7, "dialogue", "Vien_Thieu", "Mau mau bỏ ra đây, kẻo vạ đến thân bây giờ?", pitch="+3Hz", rate="+4%", lead_in_pause="0.38s", timbre_eq="chest_resonance", emotion="de_doa_gat_gong")

# Line 104: Kiên chỉ trời thề
add_line(7, "narrator", "Narrator", "Kiên trỏ tay lên trời thề rằng,", pitch="+1Hz", rate="+0%", lead_in_pause="0.35s", timbre_eq="dramatic_narrator", narrative_mode="dramatic")

# Line 105: Thoại Tôn Kiên thề
add_line(7, "dialogue", "Ton_Kien", "Tôi được của ấy mà giấu đi, thì sẽ chết dưới mũi tên hòn đạn.", pitch="-1Hz", rate="+3%", lead_in_pause="0.42s", timbre_eq="chest_resonance", emotion="the_doc_quyet_liet")

# Line 106: Các tướng can
add_line(7, "narrator", "Narrator", "Các tướng đều nói rằng,", pitch="+0Hz", rate="-5%", lead_in_pause="0.30s", timbre_eq="intimate_narrator", narrative_mode="intimate")

# Line 107: Thoại Các Tướng
add_line(7, "dialogue", "Cac_Tuong", "Văn Đài đã thề như thế, chắc là không bắt được ngọc tỷ.", pitch="-1Hz", rate="-2%", lead_in_pause="0.40s", timbre_eq="warm_authority", emotion="can_ngan_phan_tran")

# Line 108: Thiệu gọi người làm chứng
add_line(7, "narrator", "Narrator", "Thiệu gọi người làm chứng ra, hỏi Tôn Kiên rằng,", pitch="+0Hz", rate="-5%", lead_in_pause="0.30s", timbre_eq="intimate_narrator", narrative_mode="intimate")

# Line 109: Thoại Viên Thiệu
add_line(7, "dialogue", "Vien_Thieu", "Lúc mò được ngọc, có người này ở đấy không?", pitch="+2Hz", rate="+2%", lead_in_pause="0.38s", timbre_eq="chest_resonance", emotion="hach_hoi_thach_thuc")

# Line 110: Rút gươm toan chém
add_line(7, "narrator", "Narrator", "Kiên giận lắm, rút ngay gươm ra, định chém người ấy. Thiệu cũng rút gươm ra bảo rằng,", pitch="+1Hz", rate="+0%", lead_in_pause="0.30s", timbre_eq="dramatic_narrator", narrative_mode="dramatic")

# Line 111: Thoại Viên Thiệu
add_line(7, "dialogue", "Vien_Thieu", "Hễ mày chém nó thì đúng là mày dối tao.", pitch="+3Hz", rate="+4%", lead_in_pause="0.35s", timbre_eq="chest_resonance", emotion="quat_thao_chan_dung")

# Line 112: Hai bên tuốt gươm, Kiên bỏ đi, Tháo về tiệc rượu than
add_line(7, "narrator", "Narrator", "Nhan Lương, Văn Sú đứng sau lưng Viên Thiệu, cũng rút gươm ra. Sau lưng Tôn Kiên, Trình Phổ, Hoàng Cái, Hàn Dương cũng cầm dao lăm lăm ở tay. Các tướng đều xúm lại can đôi bên. Kiên lập tức trở ra, lên ngựa về phổ trại, bỏ Lạc Dương đi. Thiệu giận lắm, liền viết một lá thư, sai người tâm phúc ngay đêm hôm ấy đem sang Linh Châu. Đưa cho quan thứ sử là Lưu Biểu, sai Biểu chẹn đường Kiên, lấy lại ngọc tỷ. Hôm sau có người báo rằng, Tào Tháo đuổi Đổng Trác, đánh nhau ở Linh Dương thua to trở về. Thiệu bèn sai người đón Tháo vào trại, mở tiệc rượu cùng với Tháo giải phiền. Trong khi uống rượu, Tào Tháo than rằng,", pitch="-1Hz", rate="-8%", lead_in_pause="0.35s", timbre_eq="contemplative_narrator", narrative_mode="contemplative")

# Line 113: Thoại Tào Tháo than thở trách chư hầu
add_line(7, "dialogue", "Tao_Thao", "Ta trước kia khởi nghĩa lớn, cốt là muốn vì nước trừ hại. Các ông đã có bụng trượng nghĩa mà đến với tôi, ý tôi muốn phiền Bản Sơ đem quân Hà Nội sang đóng ở Mạch Tân. Còn các quân Toan, Tào cứ giữ vững Thành Cao, giữ cửa ải Ngao Thương, ngăn Hoàn Viên, Đại Cốc, khống chế những nơi hiểm yếu. Còn Công Lộ đem quân Nam Dương sang đóng ở Đan Triết, tiến vào cửa Vũ Quan. Để cho cái uy thế ở Tam Phu to lên. Nơi nào cũng thành cao, hào sâu, không đánh nhau, chỉ giữ làm nghi binh, để cho thiên hạ trông rõ hình thế. Cho ta là kẻ thuận đi trừ kẻ gian, thì việc lớn có thể định ngay được. Thế mà các ông dùng dằng mãi chẳng tiến quân, làm mất cả lòng mong đợi của thiên hạ, tôi lấy làm xấu hổ quá!", pitch="-1Hz", rate="-2%", lead_in_pause="0.45s", timbre_eq="sharp_cunning", emotion="than_tho_cay_dang")


# ==================== CHUNK 8 ====================
# Line 114: Chư hầu tan rã, Công Tôn Toản chán nản
add_line(8, "narrator", "Narrator", "Lũ Thiệu không ai nói câu gì. Một chốc tiệc tan. Tháo thấy lũ Thiệu mỗi người một bụng, nghĩ cũng không làm được việc lớn, bèn tự kéo quân về Dương Châu. Công Tôn Toản thấy tình cảnh thế, cũng chán. Một bữa, Toản bảo với Lưu, Quan, Trương,", pitch="-1Hz", rate="-8%", lead_in_pause="0.35s", timbre_eq="contemplative_narrator", narrative_mode="contemplative")

# Line 115: Thoại Công Tôn Toản
add_line(8, "dialogue", "Cong_Ton_Toan", "Tôi xem Viên Thiệu không làm nên được trò trống gì đâu. Ở lâu tất sinh biến. Chi bằng chúng ta hãy về.", pitch="-2Hz", rate="-3%", lead_in_pause="0.42s", timbre_eq="warm_authority", emotion="chan_chuong_that_vong")

# Line 116: Lưu Biểu sai chặn Kiên, Khoái Việt ra trận
add_line(8, "narrator", "Narrator", "Bèn nhổ trại về phía bắc. Đi đến huyện Bình Nguyên, Toản sai Lưu Bị làm tướng ở đó, giữ lấy đất, nuôi lấy quân. Thái thú Duyên Châu Lưu Đại, thiếu lương hỏi vay thái thú Đông Quận là Kiều Mạo. Mạo không cho vay, Đại đem quân xông vào dinh Mạo, giết Mạo đi rồi thu phục quân sĩ và thu hết quân lương. Viên Thiệu thấy chư hầu mỗi người đi một ngả, cũng rời Lạc Dương kéo quân về Quan Đông. Thứ sử kinh Châu là Lưu Biểu, bắt được thư của Viên Thiệu xin đem quân chẹn đường Tôn Kiên. Liền sai ngay Khoái Việt và Sái Mạo dẫn một vạn quân ra đón đường đánh Kiên. Lưu Biểu, tên chữ là Cảnh Thăng, quê ở Cao Bình, đất Sơn Dương, cũng là tôn thân nhà Hán. Lúc còn nhỏ Biểu kết bạn với bảy danh sĩ, bấy giờ người ta gọi là Giang hạ bát tuấn. Trong tám người ấy thì một người là Lưu Biểu, còn bảy người nữa là, một, Trần Tường hai, Phạm Phang ba, Khổng Giực bốn. Phạm Khang năm, Đàn Phu sáu, Trương Kiệm bảy, Sầm Hinh. Biểu cùng với bảy người ấy kết làm bạn, nhưng ngoài ra, còn có mấy người phù tá. Một là Khoái Lương, người ở Diên Bình, hai là Khoái Việt cũng người Diên Bình, ba là Sái Mạo người ở Tương Dương. Khoái Việt, Sái Mạo dẫn một vạn quân ra chẹn đường. Tôn Kiên vừa đến đó, Khoái Việt bày trận rồi nhảy ngựa ra. Kiên thấy Việt, hỏi rằng,", pitch="+0Hz", rate="-5%", lead_in_pause="0.30s", timbre_eq="epic_narrator", narrative_mode="epic")

# Line 117: Thoại Tôn Kiên hỏi Khoái Việt
add_line(8, "dialogue", "Ton_Kien", "Khoái Việt cớ sao chẹn đường ta?", pitch="-1Hz", rate="+2%", lead_in_pause="0.38s", timbre_eq="chest_resonance", emotion="chat_van_nghi_hoac")

# Line 118: Việt đáp
add_line(8, "narrator", "Narrator", "Việt nói,", pitch="+0Hz", rate="-5%", lead_in_pause="0.30s", timbre_eq="intimate_narrator", narrative_mode="intimate")

# Line 119: Thoại Khoái Việt đòi ngọc tỷ
add_line(8, "dialogue", "Khoai_Viet", "Ngươi đã làm tôi nhà Hán, sao được giấu ngọc tỷ truyền quốc? Đưa ngay ra đây, ta sẽ cho đi", pitch="+1Hz", rate="+2%", lead_in_pause="0.40s", timbre_eq="sharp_cunning", emotion="hach_dich_doi_hoi")

# Line 120: Hoàng Cái đánh Sái Mạo, Lưu Biểu tới
add_line(8, "narrator", "Narrator", "Kiên tức lắm, sai ngay Hoằng Cái ra đánh. Sái Mạo múa dao lại địch. Được vài hiệp, Cái hoa ngọn roi, đánh trúng ngay miếng kính che ngực Mạo. Mạo quay đầu ngựa chạy. Kiên thừa thế đuổi đánh khỏi cửa ô. Lúc bấy giờ, ở trong núi bỗng thấy chiêng trống khua rầm lên. Thì ra Lưu Biểu vừa dẫn quân đến. Kiên ngồi trên ngựa chào hỏi tử tế, rồi nói với Lưu Biểu rằng,", pitch="+0Hz", rate="-5%", lead_in_pause="0.30s", timbre_eq="epic_narrator", narrative_mode="epic")

# Line 121: Thoại Tôn Kiên nói với Lưu Biểu
add_line(8, "dialogue", "Ton_Kien", "Ta với Cảnh Thăng là láng giềng với nhau. Sao Cảnh Thăng lại nỡ tin lời Viên Thiệu và xử tệ với ta vậy?", pitch="-1Hz", rate="-1%", lead_in_pause="0.42s", timbre_eq="chest_resonance", emotion="on_hoa_trach_moc")


# ==================== CHUNK 9 ====================
# Line 122: Biểu nói
add_line(9, "narrator", "Narrator", "Biểu nói,", pitch="+0Hz", rate="-5%", lead_in_pause="0.30s", timbre_eq="intimate_narrator", narrative_mode="intimate")

# Line 123: Thoại Lưu Biểu
add_line(9, "dialogue", "Luu_Bieu", "Nhà ngươi giấu quốc bảo, muốn làm phản à?", pitch="-1Hz", rate="+1%", lead_in_pause="0.38s", timbre_eq="warm_authority", emotion="nghi_ngo_buoc_toi")

# Line 124: Kiên lại thề
add_line(9, "narrator", "Narrator", "Kiên lại thề,", pitch="+0Hz", rate="-5%", lead_in_pause="0.30s", timbre_eq="intimate_narrator", narrative_mode="intimate")

# Line 125: Thoại Tôn Kiên thề lần hai
add_line(9, "dialogue", "Ton_Kien", "Ta mà có của ấy ở trong mình, xin chết ở dưới mũi tên viên đạn.", pitch="-1Hz", rate="+3%", lead_in_pause="0.40s", timbre_eq="chest_resonance", emotion="the_thot_qua_quyet")

# Line 126: Biểu ép khám hành lý
add_line(9, "narrator", "Narrator", "Biểu nói,", pitch="+0Hz", rate="-5%", lead_in_pause="0.30s", timbre_eq="intimate_narrator", narrative_mode="intimate")

# Line 127: Thoại Lưu Biểu
add_line(9, "dialogue", "Luu_Bieu", "Muốn cho ta tin, nhà ngươi phải để cho ta khám cả đồ hành lý.", pitch="-1Hz", rate="+0%", lead_in_pause="0.38s", timbre_eq="warm_authority", emotion="doi_hoi_ep_uong")

# Line 128: Kiên nổi khùng
add_line(9, "narrator", "Narrator", "Kiên nổi khùng, mắng Lưu Biểu rằng,", pitch="+1Hz", rate="+0%", lead_in_pause="0.30s", timbre_eq="dramatic_narrator", narrative_mode="dramatic")

# Line 129: Thoại Tôn Kiên mắng Lưu Biểu
add_line(9, "dialogue", "Ton_Kien", "Tài sức mày thấm vào đâu, mà dám khinh tao!", pitch="+1Hz", rate="+5%", lead_in_pause="0.35s", timbre_eq="chest_resonance", emotion="cuong_no_khinh_thi")

# Line 130: Binh phục ập ra, Tôn Kiên bị vây khốn, dẫn nhập câu đối kết
add_line(9, "narrator", "Narrator", "Hai bên sắp sửa giao binh đánh nhau, Lưu Biểu lui ngay. Kiên thấy vậy thả ngựa sấn lại. Bấy giờ quân phục ở sau hai rặng núi kéo ồ ra, sau lưng Khoái Việt, Sái Mạo ập lại. Vây bọc lấy Tôn Kiên ở giữa trận. Thế rõ thực là,", pitch="+0Hz", rate="-5%", lead_in_pause="0.35s", timbre_eq="suspense_narrator", narrative_mode="suspense")

# Line 131: . ...... (Đệm thở trước câu đối kết)
add_line(9, "narrator", "Narrator", ". ......", pitch="-2Hz", rate="-12%", lead_in_pause="1.50s", timbre_eq="contemplative_narrator", narrative_mode="contemplative")

# Line 132-133: Hai câu đối kết hồi
add_line(9, "poem", "Narrator", "Ngọc tỷ đem về, không dùng được,", pitch="-2Hz", rate="-18%", lead_in_pause="0.85s", timbre_eq="poetic_recitation")
add_line(9, "poem", "Narrator", "Lại vì của ấy, động binh đao.", pitch="-2Hz", rate="-18%", lead_in_pause="0.85s", timbre_eq="poetic_recitation")

# Line 134: . ...... (Đệm thở sau câu đối kết)
add_line(9, "narrator", "Narrator", ". ......", pitch="-2Hz", rate="-12%", lead_in_pause="1.50s", timbre_eq="contemplative_narrator", narrative_mode="contemplative")

# Line 135: Câu chốt kết hồi
add_line(9, "narrator", "Narrator", "Chưa biết Tôn Kiên làm thế nào mà thoát được, xem hồi sau sẽ rõ.", pitch="-2Hz", rate="-12%", lead_in_pause="0.50s", timbre_eq="contemplative_narrator", narrative_mode="contemplative")


# Count statistics
total_lines = len(lines)
dialogue_lines = [l for l in lines if l["type"] == "dialogue"]
narrator_lines = [l for l in lines if l["type"] == "narrator"]
poem_lines = [l for l in lines if l["type"] == "poem"]

char_counts = {}
for d in dialogue_lines:
    spk = d["speaker"]
    char_counts[spk] = char_counts.get(spk, 0) + 1

for char_id, count in char_counts.items():
    if char_id in theatrical_bible["characters"]:
        theatrical_bible["characters"][char_id]["dialogue_count"] = count

theatrical_bible["characters"]["Narrator"]["dialogue_count"] = len(narrator_lines)
theatrical_bible["total_theatrical_lines"] = total_lines
theatrical_bible["narrator_lines"] = len(narrator_lines)
theatrical_bible["poem_lines"] = len(poem_lines)
theatrical_bible["dialogue_lines"] = len(dialogue_lines)
theatrical_bible["characters_cast_count"] = len(theatrical_bible["characters"])

print(f"Total Lines: {total_lines}")
print(f"Narrator Lines: {len(narrator_lines)}")
print(f"Poem Lines: {len(poem_lines)}")
print(f"Dialogue Lines: {len(dialogue_lines)}")
print(f"Characters Cast: {len(theatrical_bible['characters'])}")
print("Character dialogue counts:")
for k, v in sorted(char_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"  {k}: {v}")

# Save JSON files
with open(THEATRICAL_SCRIPT_PATH, "w", encoding="utf-8") as f:
    json.dump(lines, f, ensure_ascii=False, indent=2)

with open(THEATRICAL_BIBLE_PATH, "w", encoding="utf-8") as f:
    json.dump(theatrical_bible, f, ensure_ascii=False, indent=2)

print(f"Saved: {THEATRICAL_SCRIPT_PATH}")
print(f"Saved: {THEATRICAL_BIBLE_PATH}")

# Update .session_manifest.json
with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
    manifest = json.load(f)

for chap in manifest.get("chapters", []):
    if chap.get("folder") == "06-Hoi-06":
        chap["step_8a_status"] = "completed"
        chap["theatrical_script_file"] = "06-Hoi-06/theatrical_script.json"
        chap["theatrical_bible_file"] = "06-Hoi-06/.theatrical_bible.json"
        chap["total_theatrical_lines"] = total_lines
        chap["total_poem_lines"] = len(poem_lines)
        chap["total_dialogue_lines"] = len(dialogue_lines)
        chap["total_characters_cast"] = len(theatrical_bible["characters"])
        print("Updated 06-Hoi-06 in manifest successfully!")
        break

with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

print("Saved manifest!")
