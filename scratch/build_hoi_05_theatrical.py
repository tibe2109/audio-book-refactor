import json
import os
import re

# Destination files
CHAPTER_DIR = "/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/05-Hoi-05"
THEATRICAL_SCRIPT_PATH = os.path.join(CHAPTER_DIR, "theatrical_script.json")
THEATRICAL_BIBLE_PATH = os.path.join(CHAPTER_DIR, ".theatrical_bible.json")

# 1. Define Theatrical Bible
theatrical_bible = {
    "chapter_folder": "05-Hoi-05",
    "chapter_index": 5,
    "chapter_title": "Hồi 5: Phát hiệu triệu, các trấn hưởng ứng Tào Công; Phá cửa quan, ba anh hùng đánh Lã Bố",
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
            "chest_resonance": "Trương Phi, Quan Vũ, Tôn Kiên, Hoa Hùng (Boost 160Hz +5dB, Boost 300Hz +2.5dB, Dip 3.5kHz -3dB)",
            "warm_authority": "Lưu Bị, Công Tôn Toản, Vệ Hoằng (Boost 280Hz +3.5dB, Boost 2.2kHz +2dB, Dip 4.5kHz -2.5dB)",
            "sharp_cunning": "Tào Tháo, Lý Nho, Lý Túc (High-pass 220Hz, Boost 2.8kHz +4.5dB, Boost 5.5kHz +3dB)",
            "aged_gravel": "Tào Tung (Boost 420Hz +4.5dB, Low-pass 4.2kHz, Dip 1.2kHz -3dB)",
            "tyrant_arrogant": "Đổng Trác, Lã Bố, Viên Thuật (Boost 190Hz +4.5dB, Boost 1.8kHz +4dB, Boost 4kHz +2dB)",
            "poetic_recitation": "Ngâm vịnh thi ca cổ (Boost 250Hz +3.5dB, Dip 3.5kHz -2dB, Low-pass 7.5kHz)"
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
                "elegiac_narrator",
                "suspense_narrator"
            ],
            "timbre_eq": "epic_narrator",
            "dialogue_count": 52
        },
        "Tran_Cung": {
            "name": "Trần Cung",
            "gender": "male",
            "age_stage": "trung_nien",
            "temperament": "tram_uat_dan_vat",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "-3Hz",
            "base_rate": "-6%",
            "timbre_eq": "warm_authority",
            "dialogue_count": 1
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
            "dialogue_count": 10
        },
        "Tao_Tung": {
            "name": "Tào Tung",
            "gender": "male",
            "age_stage": "lao_hoa",
            "temperament": "khac_kho_lanh_lung",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "-6Hz",
            "base_rate": "-14%",
            "timbre_eq": "aged_gravel",
            "dialogue_count": 1
        },
        "Ve_Hoang": {
            "name": "Vệ Hoằng",
            "gender": "male",
            "age_stage": "trung_nien",
            "temperament": "anh_hung_hao_sang",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "-2Hz",
            "base_rate": "-2%",
            "timbre_eq": "warm_authority",
            "dialogue_count": 1
        },
        "Cong_Ton_Toan": {
            "name": "Công Tôn Toản",
            "gender": "male",
            "age_stage": "trung_nien",
            "temperament": "anh_hung_hao_sang",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "-2Hz",
            "base_rate": "+0%",
            "timbre_eq": "warm_authority",
            "dialogue_count": 5
        },
        "Luu_Bi": {
            "name": "Lưu Bị",
            "gender": "male",
            "age_stage": "thanh_xuan",
            "temperament": "trong_sang_thanh_thien",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "+1Hz",
            "base_rate": "-3%",
            "timbre_eq": "warm_authority",
            "dialogue_count": 4
        },
        "Truong_Phi": {
            "name": "Trương Phi",
            "gender": "male",
            "age_stage": "thanh_xuan",
            "temperament": "anh_hung_hao_sang",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "+5Hz",
            "base_rate": "+8%",
            "timbre_eq": "chest_resonance",
            "dialogue_count": 4
        },
        "Quan_Vu": {
            "name": "Quan Vũ",
            "gender": "male",
            "age_stage": "thanh_xuan",
            "temperament": "anh_hung_hao_sang",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "-1Hz",
            "base_rate": "+0%",
            "timbre_eq": "chest_resonance",
            "dialogue_count": 4
        },
        "Vuong_Khuong": {
            "name": "Vương Khuông",
            "gender": "male",
            "age_stage": "trung_nien",
            "temperament": "anh_hung_hao_sang",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "-3Hz",
            "base_rate": "-2%",
            "timbre_eq": "warm_authority",
            "dialogue_count": 1
        },
        "Vien_Thieu": {
            "name": "Viên Thiệu",
            "gender": "male",
            "age_stage": "trung_nien",
            "temperament": "hach_dich_bao_nguoc",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "-4Hz",
            "base_rate": "-4%",
            "timbre_eq": "warm_authority",
            "dialogue_count": 9
        },
        "Chu_Hau": {
            "name": "Chư hầu đồng thanh",
            "gender": "male",
            "age_stage": "trung_nien",
            "temperament": "anh_hung_hao_sang",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "+1Hz",
            "base_rate": "+4%",
            "timbre_eq": "warm_authority",
            "dialogue_count": 1
        },
        "Cac_Tuong": {
            "name": "Các tướng tuân lệnh",
            "gender": "male",
            "age_stage": "trung_nien",
            "temperament": "anh_hung_hao_sang",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "+0Hz",
            "base_rate": "+2%",
            "timbre_eq": "warm_authority",
            "dialogue_count": 1
        },
        "La_Bo": {
            "name": "Lã Bố",
            "gender": "male",
            "age_stage": "thanh_xuan",
            "temperament": "hach_dich_bao_nguoc",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "+3Hz",
            "base_rate": "+6%",
            "timbre_eq": "tyrant_arrogant",
            "dialogue_count": 1
        },
        "Dong_Trac": {
            "name": "Đổng Trác",
            "gender": "male",
            "age_stage": "trung_nien",
            "temperament": "hach_dich_bao_nguoc",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "-5Hz",
            "base_rate": "-6%",
            "timbre_eq": "tyrant_arrogant",
            "dialogue_count": 1
        },
        "Hoa_Hung": {
            "name": "Hoa Hùng",
            "gender": "male",
            "age_stage": "trung_nien",
            "temperament": "hach_dich_bao_nguoc",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "+2Hz",
            "base_rate": "+4%",
            "timbre_eq": "chest_resonance",
            "dialogue_count": 2
        },
        "Ton_Kien": {
            "name": "Tôn Kiên",
            "gender": "male",
            "age_stage": "trung_nien",
            "temperament": "anh_hung_hao_sang",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "-2Hz",
            "base_rate": "+2%",
            "timbre_eq": "chest_resonance",
            "dialogue_count": 1
        },
        "Muu_Si_Vien_Thuat": {
            "name": "Mưu sĩ Viên Thuật",
            "gender": "male",
            "age_stage": "trung_nien",
            "temperament": "giao_hoat_nham_hiem",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "+1Hz",
            "base_rate": "-4%",
            "timbre_eq": "sharp_cunning",
            "dialogue_count": 1
        },
        "Ly_Tuc": {
            "name": "Lý Túc",
            "gender": "male",
            "age_stage": "trung_nien",
            "temperament": "giao_hoat_nham_hiem",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "+0Hz",
            "base_rate": "-2%",
            "timbre_eq": "sharp_cunning",
            "dialogue_count": 1
        },
        "To_Mau": {
            "name": "Tổ Mậu",
            "gender": "male",
            "age_stage": "thanh_xuan",
            "temperament": "anh_hung_hao_sang",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "+0Hz",
            "base_rate": "+4%",
            "timbre_eq": "warm_authority",
            "dialogue_count": 1
        },
        "Quan_Do_Tham": {
            "name": "Quân do thám",
            "gender": "male",
            "age_stage": "thanh_xuan",
            "temperament": "kinh_hai",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "+3Hz",
            "base_rate": "+6%",
            "timbre_eq": "intimate_narrator",
            "dialogue_count": 1
        },
        "Du_Thiep": {
            "name": "Du Thiệp",
            "gender": "male",
            "age_stage": "thanh_xuan",
            "temperament": "anh_hung_hao_sang",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "+1Hz",
            "base_rate": "+2%",
            "timbre_eq": "chest_resonance",
            "dialogue_count": 1
        },
        "Quan_Bao": {
            "name": "Quân báo",
            "gender": "male",
            "age_stage": "thanh_xuan",
            "temperament": "kinh_hoang",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "+4Hz",
            "base_rate": "+8%",
            "timbre_eq": "intimate_narrator",
            "dialogue_count": 1
        },
        "Han_Phuc": {
            "name": "Hàn Phức",
            "gender": "male",
            "age_stage": "trung_nien",
            "temperament": "anh_hung_hao_sang",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "-2Hz",
            "base_rate": "+0%",
            "timbre_eq": "warm_authority",
            "dialogue_count": 1
        },
        "Vien_Thuat": {
            "name": "Viên Thuật",
            "gender": "male",
            "age_stage": "trung_nien",
            "temperament": "hach_dich_bao_nguoc",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "+4Hz",
            "base_rate": "+8%",
            "timbre_eq": "tyrant_arrogant",
            "dialogue_count": 3
        },
        "Ly_Nho": {
            "name": "Lý Nho",
            "gender": "male",
            "age_stage": "trung_nien",
            "temperament": "giao_hoat_nham_hiem",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "-2Hz",
            "base_rate": "-5%",
            "timbre_eq": "sharp_cunning",
            "dialogue_count": 1
        }
    }
}

# 2. Build full theatrical lines
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
# Line 1: HỒI NĂM
add_line(1, "narrator", "Narrator", "HỒI NĂM", pitch="-2Hz", rate="-12%", lead_in_pause="0.30s", timbre_eq="contemplative_narrator", narrative_mode="contemplative")
# Line 2: . ......
add_line(1, "narrator", "Narrator", ". ......", pitch="-2Hz", rate="-12%", lead_in_pause="1.50s", timbre_eq="contemplative_narrator", narrative_mode="contemplative")
# Line 3: Title
add_line(1, "narrator", "Narrator", "PHÁT HIỆU TRIỆU, CÁC TRẤN HƯỞNG ỨNG TÀO CÔNG,\nPHÁ CỬA QUAN, BA ANH HÙNG ĐÁNH LÃ BỐ.", pitch="+1Hz", rate="+0%", lead_in_pause="0.25s", timbre_eq="epic_narrator", narrative_mode="epic")
# Line 4: . ......
add_line(1, "narrator", "Narrator", ". ......", pitch="-2Hz", rate="-12%", lead_in_pause="1.50s", timbre_eq="contemplative_narrator", narrative_mode="contemplative")
# Line 5: Trần Cung lead-in
add_line(1, "narrator", "Narrator", "Trần Cung muốn giết Tào Tháo, nhưng lại nghĩ rằng,", pitch="0Hz", rate="-5%", lead_in_pause="0.35s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 6: Trần Cung monologue
add_line(1, "dialogue", "Tran_Cung", "Mình theo hắn cũng là vì nước, bây giờ giết hắn e mang tiếng bất nghĩa. Chi bằng bỏ hắn đi nơi khác là hơn.", pitch="-3Hz", rate="-6%", lead_in_pause="0.45s", timbre_eq="warm_authority", emotion="doc_thoai_dan_vat")
# Line 7: Tháo dậy lead-in
add_line(1, "narrator", "Narrator", "Nghĩ rồi lại cài gươm, lên ngựa, không đợi trời sáng, đi thẳng về Đông Quân. Tháo dậy, không thấy Trần Cung, nghĩ bụng,", pitch="0Hz", rate="-5%", lead_in_pause="0.40s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 8: Tào Tháo monologue
add_line(1, "dialogue", "Tao_Thao", "Người này thấy ta nói mấy câu, tưởng ta là đứa bất nhân, nên bỏ ta mà đi. Ta nên đi ngay, không thể ở đây lâu.", pitch="+0Hz", rate="+0%", lead_in_pause="0.42s", timbre_eq="sharp_cunning", emotion="doc_thoai_dan_vat")
# Line 9: Tào Tung lead-in
add_line(1, "narrator", "Narrator", "Suốt đêm hôm ấy Tháo đi đến Trần Lưu, tìm thấy bố, thuật lại sự tình với bố. Muốn đem gia tài bán đi để mộ nghĩa binh. Tào Tung nói,", pitch="0Hz", rate="-5%", lead_in_pause="0.40s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 10: Tào Tung
add_line(1, "dialogue", "Tao_Tung", "Gia tư nhà ta không có mấy tí, cha e không đủ để kham nổi việc lớn. Ở đây có ông Vệ Hoằng, đỗ khoa hiếu liêm, là người khinh tài trọng nghĩa, nhà giàu, nếu được ông ấy giúp. Thì việc lớn có thể mưu đồ được.", pitch="-6Hz", rate="-14%", lead_in_pause="0.45s", timbre_eq="aged_gravel", emotion="binh_than_tu_nhien")
# Line 11: Tháo bèn đặt tiệc lead-in
add_line(1, "narrator", "Narrator", "Tháo bèn đặt một tiệc rượu, mời Vệ Hoằng đến nhà nói với Hoằng rằng,", pitch="0Hz", rate="-5%", lead_in_pause="0.42s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 12: Tào Tháo nói với Vệ Hoằng
add_line(1, "dialogue", "Tao_Thao", "Nay nhà Hán vô chủ. Đổng Trác lộng quyền, dối vua hại dân, thiên hạ ai ai cũng nghiến răng tức giận. Tôi muốn hết lòng giúp nước, hiềm vì sức không đủ. Ngài là người trung nghĩa, rất mong ngài giúp đỡ cho.", pitch="+1Hz", rate="+0%", lead_in_pause="0.45s", timbre_eq="sharp_cunning", emotion="anh_hung_hao_sang")
# Line 13: Vệ Hoằng lead-in
add_line(1, "narrator", "Narrator", "Vệ Hoằng nói,", pitch="0Hz", rate="-5%", lead_in_pause="0.35s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 14: Vệ Hoằng
add_line(1, "dialogue", "Ve_Hoang", "Tôi có lòng ấy đã lâu, giận rằng chưa gặp ai là người anh hùng. Nay Mạnh đã có chí lớn, tôi xin đem hết của cải ra giúp.", pitch="-2Hz", rate="-2%", lead_in_pause="0.42s", timbre_eq="warm_authority", emotion="anh_hung_hao_sang")
# Line 15: Chiêu tập binh mã
add_line(1, "narrator", "Narrator", "Tào Tháo mừng lắm, làm ngay tờ kêu gọi phát đi các đạo, rồi dựng một lá cờ trắng, đề hai chữ. Trung nghĩa để chiêu tập binh mã. Không được mấy ngày, thiên hạ kéo đến ứng mộ đông như nước chảy. Một bữa có người ở Dương Bình, nước Vệ, tên là Nhạc Tiến, tự là Văn Khiêm, lại có người ở Cư Lộc huyện Sơn Dương. Là Lý Điển, tự là Man Thành, cùng đến xin theo. Tháo đều cho làm chân tay dưới trướng. Lại có người nữa, người ở nước Thùy nước Bái, tên là Hạ Hầu Đông tự là Nguyên Nhượng. Nguyên là dòng dõi Hạ Hầu Anh ngày xưa, từ khi còn nhỏ đã tập đánh gậy. Đến năm mười bốn tuổi đã theo thầy học võ. Có người chửi thầy. Đôn giết người ấy rồi trốn sang nơi khác ở. Bây giờ nghe thấy Tào Tháo khởi binh, Đôn cùng với một người em họ, tên là Hạ Hầu Uyên. Đem một nghìn tráng sĩ lại họp với quân Tháo. Hai người ấy vốn là anh em cùng họ với Tào Tháo, vì Tháo nguyên cũng là họ Hạ Hầu. Tại bố Tháo là Tào Tung vào làm con nuôi họ Tào, nên mới đổi ra là họ Tào. Được vài ngày nữa, lại có hai người họ Tào, Tào Nhân, Tào Hồng cũng đem hơn một nghìn quân lại giúp.", pitch="+1Hz", rate="+0%", lead_in_pause="0.40s", timbre_eq="epic_narrator", narrative_mode="epic")

# ==================== CHUNK 2 ====================
# Line 16: Narrator lead into Hịch
add_line(2, "narrator", "Narrator", "Tào Nhân, tự là Tử Hiếu, Tào Hồng tự là Tử Liêm, hai người cung mã đều thạo, võ nghệ tinh thông. Tháo mừng lắm, ngày ngày ở trong thôn, luyện tập quân mã. Vệ Hoằng đem hết cả gia tài, sắm sửa cờ quạt và may áo giáp. Bốn phương lại đưa lương thực đến, không biết ngần nào mà kể. Bấy giờ, Viên Thiệu bắt được tờ kêu gọi của Tào Tháo, bèn tụ hội văn vũ. Đem ba vạn quân ở Bột Hải sang hội với quân Tào Tháo. Tháo bèn làm một bài hịch gửi đi các quận. Hịch rằng,", pitch="+1Hz", rate="+0%", lead_in_pause="0.35s", timbre_eq="epic_narrator", narrative_mode="epic")
# Line 17: Bài Hịch Tào Tháo
add_line(2, "dialogue", "Tao_Thao", "Anh em Tào Tháo chúng tôi kính đem nghĩa lớn, bá cáo cả nước, Tặc thần Đổng Trác, lừa đất dối trời. Giết vua phá nước ô uế chốn cung cấm, tàn hại kẻ dân lành. Bạo ngược bất nhân, tội ác chồng chất! Nay vâng tờ mật chiếu của thiên tử, họp quân nghĩa binh thề quét sạch cả Hoa Hạ, tiểu trừ mọi quân hung bạo. Rất mong các nơi đều dấy nghĩa binh, cùng hả lòng công phẫn để giúp vua cứu chúng. Hịch này đến nơi, lập tức thi hành!.", pitch="+1Hz", rate="-2%", lead_in_pause="0.45s", timbre_eq="sharp_cunning", emotion="cuong_no")
# Line 18: Danh sách 17 chư hầu
add_line(2, "narrator", "Narrator", "Tờ hịch của Tào đã phát đi, chư hầu các trấn đều khởi binh hưởng ứng, một. Viên Thuật, hậu tướng quân, thái thú Nam Dương. hai. Hàn Phức, thứ sử Ký Châu. ba. Khổng Du, thứ sử Dự Châu. bốn. Lưu Đại, thứ sử Duyện Châu. năm. Vương Khuông, thái thú quận Hà Nội. sáu. Trương Mặc, thái thú Trần Lưu. bảy. Kiều Mạo, thái thú Đông Quận. tám. Viên Di, thái thú Sơn Dương. chín. Pháo Tín, tướng ở Tế Bắc. mười. Khổng Dung, thái thú Bắc Hải. mười một. Trương Siêu, thái thú Quảng Lăng. mười hai. Đào Khiêm, thứ sử Từ Châu. mười ba. Mã Đằng, thái thú Tây Lương. mười bốn. Công Tôn Toản, thái thú Bắc Bình. mười lăm. Trương Dương, thái thú Thượng Đảng. mười sáu. Tôn Kiên, Ô trình hầu, thái thú Trường Sa. mười bảy. Viên Thiệu, Kỳ hương hầu, thái thú Bột Hải. Quân mã các trấn, nơi nhiều nơi ít, trấn thì ba vạn, trấn thì một hai vạn, đều đem các văn quan võ tướng. Kéo đến Lạc Dương. Đây nói chuyện thái thú Bắc Bình là Công Tôn Toản đem một vạn rưỡi quân, khi đi qua huyện Bình Nguyên, ở Châu Đức. Trông thấy ở đằng xa, trong đám cây dâu, có một lá cờ vàng, với vài người kỵ mã đến đón. Toản trông xem ai hóa ra Lưu Bị. Toản hỏi,", pitch="+1Hz", rate="+0%", lead_in_pause="0.40s", timbre_eq="epic_narrator", narrative_mode="epic")
# Line 19: Công Tôn Toản hỏi
add_line(2, "dialogue", "Cong_Ton_Toan", "Hiền đệ sao lại ở đây?", pitch="-2Hz", rate="+0%", lead_in_pause="0.35s", timbre_eq="warm_authority", emotion="binh_than_tu_nhien")
# Line 20: Lưu Bị thưa lead-in
add_line(2, "narrator", "Narrator", "Lưu Bị thưa,", pitch="0Hz", rate="-5%", lead_in_pause="0.35s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 21: Lưu Bị
add_line(2, "dialogue", "Luu_Bi", "Ngày trước em nhờ anh được cử làm huyện lệnh Bình Nguyên, nay nghe thấy đại quân qua đây, nên em lại hầu. Xin mời anh hãy vào thành nghỉ.", pitch="+1Hz", rate="-2%", lead_in_pause="0.42s", timbre_eq="warm_authority", emotion="binh_than_tu_nhien")
# Line 22: Toản trỏ hỏi
add_line(2, "narrator", "Narrator", "Toản thấy có mấy người đi theo Lưu Bị, trỏ hỏi mấy người ấy là ai.", pitch="0Hz", rate="-5%", lead_in_pause="0.40s", timbre_eq="intimate_narrator", narrative_mode="intimate")

# ==================== CHUNK 3 ====================
# Line 23: Lưu Bị nói lead-in
add_line(3, "narrator", "Narrator", "Lưu Bị nói,", pitch="0Hz", rate="-5%", lead_in_pause="0.35s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 24: Lưu Bị
add_line(3, "dialogue", "Luu_Bi", "Đây là Quan Vũ, Trương Phi, hai người anh em kết nghĩa với tôi đó.", pitch="+1Hz", rate="-2%", lead_in_pause="0.42s", timbre_eq="warm_authority", emotion="binh_than_tu_nhien")
# Line 25: Toản hỏi lead-in
add_line(3, "narrator", "Narrator", "Toản hỏi có phải hai người ấy là hai người cùng phá giặc Khăn Vàng hay không, Huyền Đức nói.", pitch="0Hz", rate="-5%", lead_in_pause="0.38s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 26: Lưu Bị
add_line(3, "dialogue", "Luu_Bi", "Phá giặc Khăn Vàng chính là công hai người này cả!", pitch="+1Hz", rate="+0%", lead_in_pause="0.40s", timbre_eq="warm_authority", emotion="anh_hung_hao_sang")
# Line 27: Toản hỏi chức gì lead-in
add_line(3, "narrator", "Narrator", "Toản hỏi hiện bây giờ hai người làm chức gì? Huyền Đức thưa,", pitch="0Hz", rate="-5%", lead_in_pause="0.38s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 28: Lưu Bị
add_line(3, "dialogue", "Luu_Bi", "Quan Vũ làm tay mã cung, Trương Phi làm tay bộ cung.", pitch="0Hz", rate="-3%", lead_in_pause="0.42s", timbre_eq="warm_authority", emotion="bi_kich_uat_nghen")
# Line 29: Toản than rằng lead-in
add_line(3, "narrator", "Narrator", "Toản than rằng,", pitch="0Hz", rate="-5%", lead_in_pause="0.35s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 30: Công Tôn Toản
add_line(3, "dialogue", "Cong_Ton_Toan", "Như thế quả là mai một anh hùng! Nay Đổng Trác làm loạn, chư hầu cùng dấy binh đến đánh. Hiền đệ bỏ quách một chức quan quèn này, cùng với tôi đi đánh giặc giúp nhà Hán, nên không?", pitch="-2Hz", rate="+2%", lead_in_pause="0.45s", timbre_eq="warm_authority", emotion="anh_hung_hao_sang")
# Line 31: Lưu Bị vâng xin đi lead-in
add_line(3, "narrator", "Narrator", "Lưu Bị vâng xin đi ngay. Trương Phi nghe thấy tên Đổng Trác, nói rằng.", pitch="0Hz", rate="-5%", lead_in_pause="0.38s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 32: Trương Phi
add_line(3, "dialogue", "Truong_Phi", "Khi trước giá để tôi giết ngay thằng giặc ấy đi thì không phải rắc rối như ngày nay.", pitch="+5Hz", rate="+8%", lead_in_pause="0.30s", timbre_eq="chest_resonance", emotion="cuong_no")
# Line 33: Quan Vũ nói lead-in
add_line(3, "narrator", "Narrator", "Quan Vũ nói,", pitch="0Hz", rate="-5%", lead_in_pause="0.35s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 34: Quan Vũ
add_line(3, "dialogue", "Quan_Vu", "Bây giờ việc đã như thế, ta nên thu xếp đi ngay thôi.", pitch="-1Hz", rate="-2%", lead_in_pause="0.40s", timbre_eq="warm_authority", emotion="binh_than_tu_nhien")
# Line 35: Chư hầu hội quân lead-in
add_line(3, "narrator", "Narrator", "Lưu Bị cùng Quan, Trương liền đem vài ba người lính kỵ, theo Công Tôn Toản đi. Tào Tháo ra tiếp. Các chư hầu cũng lục tục kéo đến cả, mỗi người đóng trại một chỗ, liên tiếp nhau hơn hai trăm dặm đất. Tào Tháo giết trâu mổ ngựa, hội cả mười tám chư hầu bàn việc tiến binh. Thái thú Vương Khuông nói,", pitch="+1Hz", rate="+0%", lead_in_pause="0.40s", timbre_eq="epic_narrator", narrative_mode="epic")
# Line 36: Vương Khuông
add_line(3, "dialogue", "Vuong_Khuong", "Nay làm việc đại nghĩa, nên lập minh chủ, để mọi người vâng theo hiệu lệnh, rồi sẽ tiến binh.", pitch="-3Hz", rate="-2%", lead_in_pause="0.42s", timbre_eq="warm_authority", emotion="binh_than_tu_nhien")
# Line 37: Tháo nói lead-in
add_line(3, "narrator", "Narrator", "Tháo nói,", pitch="0Hz", rate="-5%", lead_in_pause="0.35s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 38: Tào Tháo
add_line(3, "dialogue", "Tao_Thao", "Viên Bản Sơ nhà bốn đời làm tam công, lại có nhiều thủ hạ cũ, nguyên là con cháu danh tướng nhà Hán. Nên tôn làm minh chủ.", pitch="+0Hz", rate="+0%", lead_in_pause="0.42s", timbre_eq="sharp_cunning", emotion="binh_than_tu_nhien")
# Line 39: Mọi người đều nói lead-in
add_line(3, "narrator", "Narrator", "Thiệu hai ba lần từ chối, nhưng mọi người đều nói,", pitch="0Hz", rate="-5%", lead_in_pause="0.38s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 40: Chư hầu đồng thanh
add_line(3, "dialogue", "Chu_Hau", "Phi Bản Sơ không xong!", pitch="+1Hz", rate="+4%", lead_in_pause="0.35s", timbre_eq="warm_authority", emotion="hoan_ca_dac_thang")
# Line 41: Lập đàn tế lễ lead-in
add_line(3, "narrator", "Narrator", "Thiệu mới vâng lời. Hôm sau lập một cái đàn ba tầng, chung quanh cắm cờ ngũ phương, tầng trên dựng một lá cờ tuyết mao trắng. Một cây hoàng việt, binh phù tướng ấn đủ cả, chư hầu mời Thiệu lên đàn. Thiệu mặc áo chỉnh tề, đeo gươm đầu hàng, đốt hương lễ hai lễ, rồi đọc lời thề,", pitch="+1Hz", rate="+0%", lead_in_pause="0.45s", timbre_eq="epic_narrator", narrative_mode="epic")
# Line 42: Lời thề Viên Thiệu
add_line(3, "dialogue", "Vien_Thieu", "Nhà Hán chẳng may, phép vua lơi lỏng. Tặc thần Đổng Trác, thừa kế làm ác, vạ đến ngôi vua, hại ra trăm họ. Anh em chúng tôi là Thiệu Sợ rằng xã tắc đắm mất nên phải tụ họp nghĩa binh, cùng nhau cứu nạn nước. Phàm đã là người đồng minh, ai cũng phải dốc lòng hết sức để giữ lấy đạo làm tôi không được hai lòng. Ai trái lời thề này, sẽ chết mất mạng, tiệt tự cháu con. Xin trời đất tổ tôn chứng giám cho!.", pitch="-4Hz", rate="-6%", lead_in_pause="0.50s", timbre_eq="warm_authority", emotion="trang_nghiem")
# Line 43: Uống máu ăn thề
add_line(3, "narrator", "Narrator", "Thiệu đọc xong, các tướng đều uống máu ăn thề. Mọi người nghe thấy lời nói khảng khái, ai cũng nước mắt chứa chan.", pitch="-1Hz", rate="-6%", lead_in_pause="0.40s", timbre_eq="contemplative_narrator", narrative_mode="contemplative")

# ==================== CHUNK 4 ====================
# Line 44: Xuống đàn uống rượu lead-in
add_line(4, "narrator", "Narrator", "Thề xong xuống đàn, Thiệu lên trướng ngồi, chư hầu hai bên theo chức tước và tuổi chia định ngôi thứ. Tháo đứng dậy mời rượu. Rượu uống được vài tuần, Tháo nói,", pitch="0Hz", rate="-5%", lead_in_pause="0.40s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 45: Tào Tháo
add_line(4, "dialogue", "Tao_Thao", "Nay đã lập minh chủ rồi, chúng ta đều phải vâng nghe điều khiển, cùng giúp việc nước. Không ai được cậy khỏe cậy tài, ganh tỵ nhau.", pitch="+0Hz", rate="+0%", lead_in_pause="0.42s", timbre_eq="sharp_cunning", emotion="trang_nghiem")
# Line 46: Viên Thiệu nói lead-in
add_line(4, "narrator", "Narrator", "Viên Thiệu nói,", pitch="0Hz", rate="-5%", lead_in_pause="0.35s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 47: Viên Thiệu
add_line(4, "dialogue", "Vien_Thieu", "Thiệu tuy bất tài, nhưng đã được các quan cắt làm minh chủ, xin hết sức công minh, ai có công phải thưởng. Ai có tội phải phạt. Nước có hình luật quân có phép tắc, nên cùng giữ gìn, đừng ai vi phạm.", pitch="-3Hz", rate="-4%", lead_in_pause="0.45s", timbre_eq="warm_authority", emotion="trang_nghiem")
# Line 48: Các tướng đều nói lead-in
add_line(4, "narrator", "Narrator", "Các tướng đều nói,", pitch="0Hz", rate="-5%", lead_in_pause="0.35s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 49: Các tướng
add_line(4, "dialogue", "Cac_Tuong", "Chúng tôi xin tuân lệnh.", pitch="+0Hz", rate="+2%", lead_in_pause="0.38s", timbre_eq="warm_authority", emotion="dong_long")
# Line 50: Thiệu cắt cử lead-in
add_line(4, "narrator", "Narrator", "Thiệu lại nói,", pitch="0Hz", rate="-5%", lead_in_pause="0.35s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 51: Viên Thiệu
add_line(4, "dialogue", "Vien_Thieu", "Em ta là Viên Thuật, coi việc lương thảo, ứng cấp các trại không được thiếu thốn. Sau nữa xin chọn lấy một người làm tiên phong, đi thẳng ngay vào cửa Dĩ Thủy khiêu chiến. Còn các tướng khác phải chia nhau giữ các chốn hiểm yếu, để làm tiếp ứng.", pitch="-3Hz", rate="-4%", lead_in_pause="0.45s", timbre_eq="warm_authority", emotion="trang_nghiem")
# Line 52: Tôn Kiên xin đi tiên phong lead-in
add_line(4, "narrator", "Narrator", "Thái thú Trường Sa là Tôn Kiên, bước lên, xin đi tiên phong. Thiệu nói,", pitch="0Hz", rate="-5%", lead_in_pause="0.38s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 53: Viên Thiệu
add_line(4, "dialogue", "Vien_Thieu", "Phải đấy! Văn Đài hùng mạnh, có thể đảm đang chức ấy.", pitch="-2Hz", rate="+0%", lead_in_pause="0.40s", timbre_eq="warm_authority", emotion="hoan_hi")
# Line 54: Lã Bố thưa lead-in
add_line(4, "narrator", "Narrator", "Kiên liền dẫn quân bản hộ của mình, kéo đến cửa Dĩ Thủy. Quân canh cửa vội vàng phi ngựa về Lạc Dương vào phủ thừa tướng cáo cấp. Đổng Trác từ khi chuyên quyền, ngày nào cũng yến tiệc vui say. Lý Nho tiếp được tờ cáo cấp, vào bẩm với Trác. Trác thất kinh vội vàng họp các tướng sĩ bàn bạc. Lã Bố thưa rằng,", pitch="+1Hz", rate="+0%", lead_in_pause="0.40s", timbre_eq="epic_narrator", narrative_mode="epic")
# Line 55: Lã Bố
add_line(4, "dialogue", "La_Bo", "Phụ thân đừng lo, các chư hầu đóng ngoài cửa ải, con coi như cỏ rác. Con xin đem quân hổ lang, chém hết đầu chúng treo dưới cửa phủ!", pitch="+3Hz", rate="+6%", lead_in_pause="0.35s", timbre_eq="tyrant_arrogant", emotion="kieu_ngao_dac_thang")
# Line 56: Trác mừng lead-in
add_line(4, "narrator", "Narrator", "Trác mừng mà nói rằng,", pitch="0Hz", rate="-5%", lead_in_pause="0.35s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 57: Đổng Trác
add_line(4, "dialogue", "Dong_Trac", "Ta được Phụng Tiên thì cứ gối cao đầu mà ngủ không lo gì nữa.", pitch="-5Hz", rate="-6%", lead_in_pause="0.42s", timbre_eq="tyrant_arrogant", emotion="dac_y")
# Line 58: Hoa Hùng bước ra lead-in
add_line(4, "narrator", "Narrator", "Trác nói chưa dứt lời thì sau lưng Lã Bố có một người bước ra nói to lên rằng,", pitch="+1Hz", rate="+0%", lead_in_pause="0.35s", timbre_eq="epic_narrator", narrative_mode="epic")
# Line 59: Hoa Hùng
add_line(4, "dialogue", "Hoa_Hung", "Cắt tiết gà. Lọ là phải dùng đến dao mổ trâu! Không phải phiền đến Lã Ôn Hầu, tôi xin ra chém hết đầu chúng nó, dễ như lấy đồ ở trong túi.", pitch="+2Hz", rate="+4%", lead_in_pause="0.32s", timbre_eq="chest_resonance", emotion="kieu_ngao_khinh_thuong")
# Line 60: Trác phong Hoa Hùng
add_line(4, "narrator", "Narrator", "Trác nhìn xem, Người ấy thân cao chín thước, mình hổ lưng lang, đầu báo tay vượn, là người Quan Tây, họ Hoa, tên Hùng. Trác nghe nói thế, thích chí lắm, cho ngay làm kiêu kỵ hiệu úy đem năm vạn quân mã hộ cùng với Lý Túc, Hồ Chẩn. Triệu Xầm đi suốt ngày đêm ra cửa quan nghênh địch. Trong bọn chư hầu, có Pháo Tín là tướng ở Tế Bắc, thấy Tôn Kiên được đi làm tiên phong, sợ Kiên cướp mất công đầu. Bèn mật sai em là Pháo Trung, đem năm nghìn quân mã bộ đi đường tắt, ra thẳng trước cửa quan khiêu chiến.", pitch="+1Hz", rate="+0%", lead_in_pause="0.40s", timbre_eq="epic_narrator", narrative_mode="epic")

# ==================== CHUNK 5 ====================
# Line 61: Hoa Hùng thét lớn lead-in
add_line(5, "narrator", "Narrator", "Hoa Hùng đem năm trăm quân thiết kỵ ra ngoài cửa quan, thét lớn,", pitch="+1Hz", rate="+0%", lead_in_pause="0.35s", timbre_eq="epic_narrator", narrative_mode="epic")
# Line 62: Hoa Hùng
add_line(5, "dialogue", "Hoa_Hung", "Tướng giặc chớ chạy!.", pitch="+4Hz", rate="+8%", lead_in_pause="0.30s", timbre_eq="chest_resonance", emotion="cuong_no")
# Line 63: Tôn Kiên mắng lead-in
add_line(5, "narrator", "Narrator", "Pháo Trung vội lui, bị Hoa Hùng chém chết, tướng tá bị bắt sống rất nhiều. Hoa Hùng sai người đem đầu Pháo Trung về báo tiệp. Trác giao ngay cho Hùng làm đô đốc. Đây nói chuyện Tôn Kiên dẫn bốn tướng đến trước cửa Dĩ Thủy. Bốn tướng ấy là, Một. Trình Phổ, tên chữ là Đức Mưu, người Thổ Ngân, ở Hữu Bắc Bình, Phổ cầm một ngọn xà mâu sắt. Hai. Hoàng Cái, tên chữ là Công Phúc, người ở Linh Lăng, Cái cầm một ngọn roi sắt. Ba. Hàn Đương, tên chữ là Công Nghĩa, người Linh Chi, tỉnh Liêu Tây, Đương cầm một con dao lớn. Bốn. Tổ Mậu, tên chữ là Đại Vinh, người ở Phú Xuân, quận Ngô, Mậu hai tay cầm hai dao. Tôn Kiên mình mặc áo giáp bạc, đầu đội mũ chóp đỏ, cắp dao Cổ Dĩnh, cưỡi ngựa Hoa Tôn. Trỏ tay lên trên cửa quan mà mắng rằng,", pitch="+1Hz", rate="+0%", lead_in_pause="0.40s", timbre_eq="epic_narrator", narrative_mode="epic")
# Line 64: Tôn Kiên
add_line(5, "dialogue", "Ton_Kien", "Thằng tiểu nhân đi phò giặc kia! Sao không mau mau xuống hàng?", pitch="-2Hz", rate="+4%", lead_in_pause="0.32s", timbre_eq="chest_resonance", emotion="cuong_no")
# Line 65: Đánh nhau ở Dĩ Thủy lead-in
add_line(5, "narrator", "Narrator", "Phó tướng của Hoa Hùng là Hồ Chẩn, dẫn năm nghìn quân xuống dưới cửa quan nghênh địch. Tướng Kiên là Trương Phổ vác ngọn mâu, phi ngựa ra thẳng đánh Hồ Chẩn. Đánh nhau được vài hiệp Phổ đâm trúng cổ họng Chẩn, chết ngã từ trên ngựa xuống đất. Kiên bèn thúc quân xông đến trước cửa quan. Trên cửa bắn tên, ném đá xuống như mưa. Kiên phải lui binh về đóng ở Lương Đông, sai người đến chỗ Viên Thiệu báo tiệp và đến chỗ Viên Thuật thúc giục lương thảo. Bấy giờ, có người xui Thuật rằng,", pitch="+1Hz", rate="+0%", lead_in_pause="0.40s", timbre_eq="epic_narrator", narrative_mode="epic")
# Line 66: Mưu sĩ Viên Thuật
add_line(5, "dialogue", "Muu_Si_Vien_Thuat", "Tôn Kiên là một con hổ dữ ở đất Giang Đông. Nếu ta để cho nó phá được Lạc Dương, giết được Đổng Trác, thì khác gì trừ được lang mà lại gặp hổ. Nay đừng phát lương, quân hắn sẽ tan vỡ.", pitch="+1Hz", rate="-4%", lead_in_pause="0.42s", timbre_eq="sharp_cunning", emotion="de_doa_tham_hiem")
# Line 67: Lý Túc bàn lead-in
add_line(5, "narrator", "Narrator", "Thuật nghe, bèn không cấp lương cho Tôn Kiên. Kiên cạn lương, trong quân rối loạn. Quân do thám biết, về cửa quan báo tin. Lý Túc bàn với Hoa Hùng rằng,", pitch="0Hz", rate="-5%", lead_in_pause="0.40s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 68: Lý Túc
add_line(5, "dialogue", "Ly_Tuc", "Đêm hôm nay ta đem một toán quân. Đi lần con đường nhỏ xuống đánh đằng sau trại Tôn Kiên, tướng quân đánh đằng trước, chắc bắt được nó.", pitch="+0Hz", rate="-2%", lead_in_pause="0.40s", timbre_eq="sharp_cunning", emotion="de_doa_tham_hiem")
# Line 69: Tập kích trại Tôn Kiên
add_line(5, "narrator", "Narrator", "Hùng nghe kế ấy, truyền lệnh cho quân sĩ ăn no, để đêm xuống cửa quan đánh giặc. Đêm hôm ấy, gió mát trăng trong. Quân Hùng đến trại Kiên bấy giờ độ nửa đêm, đánh trống hò reo kéo vào. Kiên vội vàng mặc áo cưỡi ngựa đi ra, vừa gặp Hoa Hùng đến. Hai bên đánh nhau được vài hiệp, mặt sau Lý Túc kéo vào sai quân sĩ phóng hỏa. Quân Tôn Kiên rối loạn.", pitch="+1Hz", rate="+0%", lead_in_pause="0.40s", timbre_eq="epic_narrator", narrative_mode="epic")

# ==================== CHUNK 6 ====================
# Line 70: Tổ Mậu bảo Kiên lead-in
add_line(6, "narrator", "Narrator", "Các tướng đánh lộn nhau, duy có Tổ Mậu theo Kiên phá vây chạy. Hoa Hùng từ mặt sau đuổi dồn lên. Kiên cầm cung bắn hai phát tên, Hùng đều tránh được cả, lại giương cung bắn một phát nữa. Kéo quá sức gãy mất cung thước hoa phải vứt bỏ cung tế ngựa chạy. Tổ Mâu bảo Kiên rằng,", pitch="+1Hz", rate="+0%", lead_in_pause="0.38s", timbre_eq="epic_narrator", narrative_mode="epic")
# Line 71: Tổ Mậu
add_line(6, "dialogue", "To_Mau", "Cái mũ chóp đỏ trên đầu của chúa công, bị giặc nó nhận được. Xin cởi mũ đưa cho tôi đội.", pitch="+0Hz", rate="+4%", lead_in_pause="0.32s", timbre_eq="warm_authority", emotion="anh_hung_hao_sang")
# Line 72: Tổ Mậu hy sinh, Viên Thiệu kinh hãi lead-in
add_line(6, "narrator", "Narrator", "Kiên liền cởi mũ đánh đổi cho Mậu, rồi hai người chia đường chạy ra hai ngã. Quân Hoa Hùng cứ đuổi theo người đội mũ chóp đỏ. Kiên chạy sang con đường nhỏ được thoát. Tổ Mậu bị Hoa Hùng đuổi kíp lắm, bèn bỏ mũ ra, treo vào một cái cột nhà cháy dở, rồi trốn vào rừng rậm. Núp một chỗ. Quân Hùng, thấp thoáng dưới bóng trăng, trông thấy cái chóp mũ đỏ ở chỗ nhà cháy cứ vây bọc bốn mặt lại. Không dám đến gần, rồi sau lấy tên bắn mãi mới biết bị lừa. Tổ Mậu ở trong rừng lúc bấy giờ xông ra, hai tay múa đôi dao, chực chém Hoa Hùng, Hùng thét to một tiếng. Đưa một nhát dao, Mậu chết lăn xuống dưới ngựa. Đánh nhau vừa đến tận sáng, Hùng mới kéo quân về. Trình Phổ, Hàn Dương, Hoàng Cái tìm thấy Tôn Kiên, thu nhập quân mã lại rồi đóng trại ở. Tôn Kiên thấy mất Tổ Mậu, thương xót lắm, bèn cấp tốc cho người đi báo Viên Thiệu. Thiệu thất kinh nói,", pitch="+1Hz", rate="+0%", lead_in_pause="0.40s", timbre_eq="epic_narrator", narrative_mode="epic")
# Line 73: Viên Thiệu thốt lên
add_line(6, "dialogue", "Vien_Thieu", "Không ngờ Tôn Văn Đài mà thua Hoa Hùng!", pitch="-1Hz", rate="-6%", lead_in_pause="0.42s", timbre_eq="warm_authority", emotion="bang_hoang_chet_lang")
# Line 74: Thiệu họp chư hầu lead-in
add_line(6, "narrator", "Narrator", "Thiệu họp chư hầu để bàn bạc. Chư hầu đến cả, chỉ có Công Tôn Toản đến sau. Thiệu mời các tướng vào ngồi sắp hàng trong trướng rồi nói rằng,", pitch="0Hz", rate="-5%", lead_in_pause="0.40s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 75: Viên Thiệu
add_line(6, "dialogue", "Vien_Thieu", "Em Pháo Tín không theo mệnh lệnh, tự tiện tiến binh. Mình bị giết, quân sĩ chết nhiều. Đến nay Tôn Văn Đài cũng bị thua, mất hết nhuệ khí, các tướng định thế nào?", pitch="-3Hz", rate="-4%", lead_in_pause="0.45s", timbre_eq="warm_authority", emotion="lo_lang_tram_ngam")
# Line 76: Toản giới thiệu Lưu Bị lead-in
add_line(6, "narrator", "Narrator", "Chư hầu không ai nói gì cả. Thiệu ngẩng mặt lên nhìn chỉ thấy sau lưng Công Tôn Toản có ba người dị thường, đứng cười mát. Thiệu hỏi ai. Toản gọi Lưu Bị ra và nói rằng,", pitch="0Hz", rate="-5%", lead_in_pause="0.40s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 77: Công Tôn Toản
add_line(6, "dialogue", "Cong_Ton_Toan", "Người này là anh em bạn học với tôi thuở nhỏ, hiện đang làm quan lệnh Bình Nguyên. Tên là Lưu Bị.", pitch="-2Hz", rate="+0%", lead_in_pause="0.42s", timbre_eq="warm_authority", emotion="binh_than_tu_nhien")
# Line 78: Tháo hỏi lead-in
add_line(6, "narrator", "Narrator", "Tháo hỏi,", pitch="0Hz", rate="-5%", lead_in_pause="0.35s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 79: Tào Tháo
add_line(6, "dialogue", "Tao_Thao", "Có phải là Lưu Huyền Đức đánh tan giặc Khăn Vàng khi xưa không?", pitch="+1Hz", rate="+0%", lead_in_pause="0.38s", timbre_eq="sharp_cunning", emotion="to_mo_kham_phuc")
# Line 80: Mời Lưu Bị ngồi
add_line(6, "narrator", "Narrator", "Toản nói phải, rồi bảo Lưu Bị ra chào các quan, nhân thể đem công lao và hoàn cảnh xuất thân của Bị ra. Nói chuyện để các tướng nghe. Thiệu thấy nói Lưu Bị là tôn phái nhà Hán bèn sai lấy ghế mời ngồi. Lưu bị khiêm tốn không dám ngồi.", pitch="0Hz", rate="-5%", lead_in_pause="0.40s", timbre_eq="intimate_narrator", narrative_mode="intimate")

# ==================== CHUNK 7 ====================
# Line 81: Thiệu nói lead-in
add_line(7, "narrator", "Narrator", "Thiệu nói,", pitch="0Hz", rate="-5%", lead_in_pause="0.35s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 82: Viên Thiệu
add_line(7, "dialogue", "Vien_Thieu", "Ta kính không phải là kính danh tước nhà ngươi mà là kính người tôn thất nhà vua đấy thôi!", pitch="-3Hz", rate="-2%", lead_in_pause="0.42s", timbre_eq="warm_authority", emotion="hach_dich_kieu_ngao")
# Line 83: Quân do thám báo lead-in
add_line(7, "narrator", "Narrator", "Lưu Bị mới ngồi xuống ghế ở hàng cuối cùng. Quan Vũ, Trương Phi chắp tay đứng hầu đằng sau. Đương khi ấy, có quân do thám lại báo,", pitch="0Hz", rate="-5%", lead_in_pause="0.40s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 84: Quân do thám
add_line(7, "dialogue", "Quan_Do_Tham", "Hoa Hùng dẫn quân thiết kỵ xuống cửa quan. Nó lấy sào cắm cái chóp mũ của Tôn thái thú, đến trước cửa trại, hò hét thách đánh.", pitch="+3Hz", rate="+6%", lead_in_pause="0.32s", timbre_eq="intimate_narrator", emotion="kinh_hai")
# Line 85: Thiệu hỏi lead-in
add_line(7, "narrator", "Narrator", "Thiệu hỏi,", pitch="0Hz", rate="-5%", lead_in_pause="0.35s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 86: Viên Thiệu
add_line(7, "dialogue", "Vien_Thieu", "Ai dám ra trận?", pitch="-1Hz", rate="+2%", lead_in_pause="0.35s", timbre_eq="warm_authority", emotion="sot_ruot")
# Line 87: Du Thiệp thưa lead-in
add_line(7, "narrator", "Narrator", "Sau lưng Viên Thuật, có một tướng lực lưỡng, tên là Du Thiệp bước ra thưa rằng,", pitch="0Hz", rate="-5%", lead_in_pause="0.38s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 88: Du Thiệp
add_line(7, "dialogue", "Du_Thiep", "Tiểu tướng xin ra.", pitch="+1Hz", rate="+2%", lead_in_pause="0.32s", timbre_eq="chest_resonance", emotion="tu_tin")
# Line 89: Quân báo về lead-in
add_line(7, "narrator", "Narrator", "Thiệu mừng sai Thiệp ra. Vừa được một lát, có người về báo,", pitch="0Hz", rate="-5%", lead_in_pause="0.38s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 90: Quân báo
add_line(7, "dialogue", "Quan_Bao", "Thiệp đánh nhau với Hoa Hùng được ba hiệp, bị Hùng chém chết rồi!", pitch="+4Hz", rate="+8%", lead_in_pause="0.30s", timbre_eq="intimate_narrator", emotion="kinh_hoang")
# Line 91: Hàn Phức nói lead-in
add_line(7, "narrator", "Narrator", "Các tướng cả sợ. Thái thú Hàn Phức nói,", pitch="0Hz", rate="-5%", lead_in_pause="0.38s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 92: Hàn Phức
add_line(7, "dialogue", "Han_Phuc", "Tôi có thượng tướng Phan Phụng có thể chém được Hoa Hùng.", pitch="-2Hz", rate="+0%", lead_in_pause="0.40s", timbre_eq="warm_authority", emotion="tu_tin")
# Line 93: Phan Phụng bị chém lead-in
add_line(7, "narrator", "Narrator", "Thiệu bèn sai Phan Phụng ra đánh. Phụng tay cầm một cái búa to, lên ngựa, ra được một lát, lại bị Hoa Hùng chém chết. Các tướng không người nào còn máu mặt. Thiệu nói rằng,", pitch="-1Hz", rate="-5%", lead_in_pause="0.40s", timbre_eq="elegiac_narrator", narrative_mode="elegiac")
# Line 94: Viên Thiệu than
add_line(7, "dialogue", "Vien_Thieu", "Tiếc thay! Danh tướng của ta là Nhan Lương, Văn Sú chưa đến. Giá thử được một trong hai người ấy ở đây thì có sợ gì Hoa Hùng.", pitch="-3Hz", rate="-4%", lead_in_pause="0.45s", timbre_eq="warm_authority", emotion="than_tho_bat_luc")
# Line 95: Quan Vũ xin ra lead-in
add_line(7, "narrator", "Narrator", "Nói chưa dứt lời một người ở dưới thềm, chạy ra, nói to lên rằng,", pitch="+1Hz", rate="+0%", lead_in_pause="0.35s", timbre_eq="epic_narrator", narrative_mode="epic")
# Line 96: Quan Vũ
add_line(7, "dialogue", "Quan_Vu", "Tiểu tướng xin ra chém đầu Hoa Hùng. Đem dân dưới trướng.", pitch="-1Hz", rate="+0%", lead_in_pause="0.32s", timbre_eq="chest_resonance", emotion="anh_hung_hao_sang")
# Line 97: Thiệu hỏi ai Toản thưa lead-in
add_line(7, "narrator", "Narrator", "Mọi người nhìn xem thấy người ấy mình cao chín thước, râu dài hai thước, mắt phượng mày tằm, mặt đỏ như gấc. Tiếng giống chuông kêu. Thiệu hỏi là người nào. Toản thưa,", pitch="+1Hz", rate="+0%", lead_in_pause="0.40s", timbre_eq="epic_narrator", narrative_mode="epic")
# Line 98: Công Tôn Toản
add_line(7, "dialogue", "Cong_Ton_Toan", "Em Huyền Đức tên là Quan Vũ đấy!", pitch="-2Hz", rate="+0%", lead_in_pause="0.38s", timbre_eq="warm_authority", emotion="binh_than_tu_nhien")
# Line 99: Chức gì lead-in
add_line(7, "narrator", "Narrator", "Thiệu lại hỏi hiện làm chức gì? Toản thưa,", pitch="0Hz", rate="-5%", lead_in_pause="0.35s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 100: Công Tôn Toản
add_line(7, "dialogue", "Cong_Ton_Toan", "Vũ theo Huyền Đức làm tay bắn cung.", pitch="-2Hz", rate="-2%", lead_in_pause="0.38s", timbre_eq="warm_authority", emotion="binh_than_tu_nhien")
# Line 101: Viên Thuật thét lead-in
add_line(7, "narrator", "Narrator", "Viên Thuật ở trong trướng thét lên,", pitch="0Hz", rate="-5%", lead_in_pause="0.35s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 102: Viên Thuật
add_line(7, "dialogue", "Vien_Thuat", "Thằng này là thằng nào! Mà dám khinh chư hầu chúng tao không có đại tướng hay sao? Thứ mày là một thằng cung thủ, mà dám nói khoác à? Chúng đâu, đuổi cổ nó ra ngoài kia!", pitch="+4Hz", rate="+8%", lead_in_pause="0.30s", timbre_eq="tyrant_arrogant", emotion="cuong_no")
# Line 103: Tào Tháo ngăn lead-in
add_line(7, "narrator", "Narrator", "Tào Tháo vội ngăn rằng,", pitch="0Hz", rate="-5%", lead_in_pause="0.32s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 104: Tào Tháo
add_line(7, "dialogue", "Tao_Thao", "Công Lộ hãy nguôi cơn giận. Người ấy đã nói mạnh thế, chắc là có dũng lực. Xin hãy thử cho ra, hễ không đánh được, ta sẽ trị tội.", pitch="+1Hz", rate="-2%", lead_in_pause="0.40s", timbre_eq="sharp_cunning", emotion="khuyen_giai_nham_hiem")
# Line 105: Viên Thiệu nói lead-in
add_line(7, "narrator", "Narrator", "Viên Thiệu nói,", pitch="0Hz", rate="-5%", lead_in_pause="0.35s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 106: Viên Thiệu
add_line(7, "dialogue", "Vien_Thieu", "Sai một tay bắn cung ra đánh, giặc nó có cười cho không?", pitch="-3Hz", rate="-2%", lead_in_pause="0.40s", timbre_eq="warm_authority", emotion="do_du_nghi_ngai")
# Line 107: Tào Tháo nói lead-in
add_line(7, "narrator", "Narrator", "Tào Tháo nói,", pitch="0Hz", rate="-5%", lead_in_pause="0.35s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 108: Tào Tháo
add_line(7, "dialogue", "Tao_Thao", "Người ấy diện mạo oai vệ thế kia. Hoa Hùng biết đâu là tay bắn cung.", pitch="+1Hz", rate="+0%", lead_in_pause="0.40s", timbre_eq="sharp_cunning", emotion="kham_phuc_ung_ho")
# Line 109: Quan Công nói lead-in
add_line(7, "narrator", "Narrator", "Quan Công nói,", pitch="0Hz", rate="-5%", lead_in_pause="0.35s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 110: Quan Vũ
add_line(7, "dialogue", "Quan_Vu", "Nếu tôi không đánh được, xin chặt đầu tôi đi!", pitch="-1Hz", rate="+2%", lead_in_pause="0.32s", timbre_eq="chest_resonance", emotion="quyet_doan_dung_manh")
# Line 111: Rót rượu đưa Quan Công lead-in
add_line(7, "narrator", "Narrator", "Tháo sai người rót chén rượu, đưa Quan Công uống trước khi đi. Quan Công nói,", pitch="0Hz", rate="-5%", lead_in_pause="0.38s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 112: Quan Vũ
add_line(7, "dialogue", "Quan_Vu", "Xin hãy để chén rượu đấy, tôi đi rồi về ngay!", pitch="-1Hz", rate="+0%", lead_in_pause="0.35s", timbre_eq="chest_resonance", emotion="hao_sang_tu_tin")
# Line 113: Ra trận
add_line(7, "narrator", "Narrator", "Nói rồi đi ra, vác long đao nhảy lên lưng ngựa.", pitch="+1Hz", rate="+0%", lead_in_pause="0.38s", timbre_eq="epic_narrator", narrative_mode="epic")

# ==================== CHUNK 8 ====================
# Line 114: Chém Hoa Hùng rượu còn nóng
add_line(8, "narrator", "Narrator", "Được một lát chư hầu nghe thấy ngoài cửa quan tiếng trống đánh, tiếng người reo ầm ầm, tựa hồ như trời long đất lở. Núi đổ non nghiêng, ai nấy đều thất kinh đang định sai người ra xem, thì đã thấy tiếng nhạc nhong nhong trở về. Ngựa đã vào tới trung quân. Quan Công cầm đầu Hoa Hùng ném xuống đất, chén rượu của Tào Tháo đưa hãy còn nóng.", pitch="+1Hz", rate="+0%", lead_in_pause="0.40s", timbre_eq="epic_narrator", narrative_mode="epic")
# Line 115: Thơ khen lead-in
add_line(8, "narrator", "Narrator", "Đời sau có thơ khen rằng,", pitch="-1Hz", rate="-6%", lead_in_pause="0.35s", timbre_eq="contemplative_narrator", narrative_mode="contemplative")
# Line 116: . ......
add_line(8, "narrator", "Narrator", ". ......", pitch="-2Hz", rate="-12%", lead_in_pause="1.50s", timbre_eq="contemplative_narrator", narrative_mode="contemplative")
# Line 117-120: Bài thơ khen Quan Vũ chém Hoa Hùng
add_line(8, "poem", "Narrator", "Uy Vũ, lừng danh, đệ nhất công,", pitch="-2Hz", rate="-18%", lead_in_pause="0.85s", timbre_eq="poetic_recitation")
add_line(8, "poem", "Narrator", "Nha môn trống trận, nổi thùng thùng,", pitch="-2Hz", rate="-18%", lead_in_pause="0.85s", timbre_eq="poetic_recitation")
add_line(8, "poem", "Narrator", "Chén rượu rót ra, còn nóng hổi,", pitch="-2Hz", rate="-18%", lead_in_pause="0.85s", timbre_eq="poetic_recitation")
add_line(8, "poem", "Narrator", "Vân Trường, đã chém, chết Hoa Hùng.", pitch="-2Hz", rate="-18%", lead_in_pause="0.85s", timbre_eq="poetic_recitation")
# Line 121: . ......
add_line(8, "narrator", "Narrator", ". ......", pitch="-2Hz", rate="-12%", lead_in_pause="1.50s", timbre_eq="contemplative_narrator", narrative_mode="contemplative")
# Line 122: Trương Phi hăng hái lead-in
add_line(8, "narrator", "Narrator", "Tào Tháo mừng lắm. Lúc ấy, Trương Phi ở sau lưng Lưu Bị mới chạy ra nói to lên rằng,", pitch="+1Hz", rate="+0%", lead_in_pause="0.38s", timbre_eq="epic_narrator", narrative_mode="epic")
# Line 123: Trương Phi
add_line(8, "dialogue", "Truong_Phi", "Đại ca đã chém chết được Hoa Hùng. Sao không nhân thể đánh thốc vào cửa quan, bắt sống lấy Đổng Trác, còn đợi đến bao giờ?", pitch="+4Hz", rate="+8%", lead_in_pause="0.30s", timbre_eq="chest_resonance", emotion="phan_khich_hao_sang")
# Line 124: Viên Thuật giận quát lead-in
add_line(8, "narrator", "Narrator", "Viên Thuật giận quát mắng rằng,", pitch="0Hz", rate="-5%", lead_in_pause="0.30s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 125: Viên Thuật
add_line(8, "dialogue", "Vien_Thuat", "Thằng láo! Đại thần của chúng tao đây còn phải khiêm tốn, thứ mày là tiểu tốt của một quan huyện, sao dám hỗn xược ở đây? Đuổi cả chúng nó ra ngoài kia.", pitch="+4Hz", rate="+8%", lead_in_pause="0.30s", timbre_eq="tyrant_arrogant", emotion="cuong_no")
# Line 126: Tháo can lead-in
add_line(8, "narrator", "Narrator", "Tào Tháo nói,", pitch="0Hz", rate="-5%", lead_in_pause="0.35s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 127: Tào Tháo
add_line(8, "dialogue", "Tao_Thao", "Ai có công thì thưởng, cứ gì quý với tiện!", pitch="+1Hz", rate="+0%", lead_in_pause="0.32s", timbre_eq="sharp_cunning", emotion="thang_than_phan_doi")
# Line 128: Viên Thuật nói lead-in
add_line(8, "narrator", "Narrator", "Viên Thuật nói,", pitch="0Hz", rate="-5%", lead_in_pause="0.35s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 129: Viên Thuật
add_line(8, "dialogue", "Vien_Thuat", "Có phải các ông chỉ trọng một người huyện lệnh thì tôi xin cáo thoái.", pitch="+3Hz", rate="+4%", lead_in_pause="0.35s", timbre_eq="tyrant_arrogant", emotion="ghen_tuong_gian_doi")
# Line 130: Tháo nói lead-in
add_line(8, "narrator", "Narrator", "Tháo nói,", pitch="0Hz", rate="-5%", lead_in_pause="0.35s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 131: Tào Tháo
add_line(8, "dialogue", "Tao_Thao", "Sao lại vì một lời nói, mà bỏ việc lớn?", pitch="+0Hz", rate="-2%", lead_in_pause="0.38s", timbre_eq="sharp_cunning", emotion="hoa_giai_khuyen_can")
# Line 132: Lý Nho hiến kế lead-in
add_line(8, "narrator", "Narrator", "Nói thế rồi Tháo bảo Công Tôn Toản hãy mời các ông ấy về trại. Chư hầu tan, người nào về trại người ấy. Tháo mật sai người đem trâu và rượu đưa sang mừng và úy lạo ba anh em Lưu, Quan, Trương. Quân Hoa Hùng thua, chạy về cửa quan báo Lý Túc. Túc vội vàng viết giấy báo Đổng Trác, Trác họp các quan lại bàn, Lý Nho nói,", pitch="0Hz", rate="-5%", lead_in_pause="0.40s", timbre_eq="intimate_narrator", narrative_mode="intimate")
# Line 133: Lý Nho
add_line(8, "dialogue", "Ly_Nho", "Nay ta mất thượng tướng Hoa Hùng. Thế giặc to lắm. Viên Thiệu là minh chủ, có chú là Viên Ngỗi hiện đang làm thái phó, nếu chúng trong ngoài tiếp ứng cho nhau thì nguy lắm. Ta nên trừ trước đi. Xin thừa tướng thân cầm đại quân, chia đường ra đánh thì mới được.", pitch="-2Hz", rate="-5%", lead_in_pause="0.45s", timbre_eq="sharp_cunning", emotion="de_doa_tham_hiem")
# Line 134: Đổng Trác giết Viên Ngỗi, tiến quân Hổ Lao
add_line(8, "narrator", "Narrator", "Trác nghe lời Nho, gọi Lý Thôi, Quách Dĩ, lĩnh năm trăm quân đến vây nhà thái phó Viên Ngỗi, già trẻ đều giết sạch. Rồi đem đầu Ngỗi ra bêu trước cửa quan. Trác khởi hai mươi vạn quân chia làm hai đường, một đường sai Lý Thôi, Quách Dĩ, đem năm vạn quân ra giữ cửa Dĩ Thủy. Không đánh nhau vội, một đường thì Trác đem mười lăm vạn quân cùng với Lý Nho, Lã Bố, Phàn Trù. Trương Tế giữ cửa quan Hổ Lao, Trác sai Lã Bố lĩnh ba mươi vạn quân ra trước quan, đóng một trại lớn. Trác thì đóng đồn trên cửa quan.", pitch="+1Hz", rate="+0%", lead_in_pause="0.40s", timbre_eq="epic_narrator", narrative_mode="epic")

# ==================== CHUNK 9 ====================
# Line 135: Tháo bàn kế chia quân lead-in
add_line(9, "narrator", "Narrator", "Quân lưu tinh dò được tình hình, kíp vào trại Viên Thiệu báo. Thiệu họp các tướng lại bàn. Tháo nói,", pitch="+1Hz", rate="+0%", lead_in_pause="0.40s", timbre_eq="epic_narrator", narrative_mode="epic")
# Line 136: Tào Tháo
add_line(9, "dialogue", "Tao_Thao", "Đổng Trác đóng quân ở Hổ Lao, là cốt chẹn đường chư hầu. Nay nên chia quân ra, một nửa ra đó nghênh địch.", pitch="+1Hz", rate="+0%", lead_in_pause="0.35s", timbre_eq="sharp_cunning", emotion="phan_tich_chien_luoc")
# Line 137: Lã Bố xung trận đại chiến chư hầu lead-in
add_line(9, "narrator", "Narrator", "Thiệu bèn cắt Vương Khuông, Kiều Mạo, Pháo Tín, Viên Dị, Khổng Dung, Trương Dương, Đào Khiêm. Công Tôn Toản cả thảy tám vị chư hầu đến cửa Hổ Lao đón địch. Tào Tháo thì dẫn quân đi lại tiếp ứng. Chư hầu đều khởi binh đến, thái thú Vương Khuông đi trước. Lã Bố đem năm nghìn quân thiết kỵ lại. Vương Khuông đem quân mã, bày thành thế trận, cưỡi ngựa đứng dưới cửa cờ. Trông thấy Lã Bố ra trận mình mặc áo gấm đỏ trăm hoa, ngoài khoác áo giáo thú diện liên hoàn. Dưới thắt dây lưng sư man, lưng đeo một bộ cung tên, tay cầm một ngọn họa kích, cưỡi ngựa xích thố. Khuông ngoảnh lại hỏi ai dám ra đánh? Đằng sau có một tướng vác ngọn giáo, tế ngựa chạy ra, đó là một danh tướng ở Hà Nội, tên là Phương Duyệt. Hai ngựa giao nhau, chưa được năm hiệp, Duyệt bị Lã Bố đánh một ngọn kích ngã xuống ngựa. Bố xông thẳng vào. Quân Vương Khuông thua to, chạy tán loạn ra bốn mặt. Bố xông xáo vào đám quân Khuông, như chạy vào nơi không người. May sao Kiều Mạo, Viên Di đem hai cánh quân vừa đến, cứu được Vương Khuông, quân Bố mới lui. Chư hầu ba xứ mỗi xứ mất ít nhiều người ngựa, lui ba mươi dặm, đóng trại. Quân năm xứ đi sau cũng dần dần kéo cả đến, họp lại bàn nhau, đều cho Lã Bố là anh hùng, không ai địch nổi. Khi đang lo nghĩ thì có quân vào báo rằng Lã Bố đến khiêu chiến. Chư hầu tám xư đều lên ngựa kéo ra cả, chia quân ra làm tám đội ở trên gò cao. Trông ở đằng xa thấy một toán quân mã, cờ bay phất phới, Lã Bố xông đến. Bộ tướng của Trương Dương, thái thú Thượng Đẳng tên là Mục Thuận vác ngọn giáo tế ngựa ra đánh. Bị Bố đâm một ngọn kích chết lăn từ trên ngựa xuống đất. Thấy thế, một bộ tướng của Khổng Dung, tên là Vũ An Quốc, vác một cái dùi sắt, tế ngựa chạy ra, Lã Bố đến. Đánh nhau được mười hiệp, Bố đưa một ngọn kích đánh gãy cánh tay An Quốc. An Quốc vứt dùi sắt chạy. Chư hầu tám xứ cùng đổ ra mới cứu được An Quốc. Lã Bố lui quân trở về, các chư hầu lại về trại bàn với nhau. Tào Tháo nói,", pitch="+1Hz", rate="+0%", lead_in_pause="0.40s", timbre_eq="epic_narrator", narrative_mode="epic")
# Line 138: Tào Tháo
add_line(9, "dialogue", "Tao_Thao", "Lã Bố anh hùng, không địch được. Nay nên họp cả mười tám nước chư hầu để bàn nhau tìm kế gì đánh được nó.", pitch="+0Hz", rate="-2%", lead_in_pause="0.38s", timbre_eq="sharp_cunning", emotion="tram_ngam_lo_lang")

# ==================== CHUNK 10 ====================
# Line 139: Trương Phi xuất trận lead-in
add_line(10, "narrator", "Narrator", "Hễ bắt sống được Lã Bố, thì giết Đổng Trác chẳng khó gì nữa! Trong khi đang bàn bạc, Lã Bố lại kéo quân đến thách đánh. Công Tôn Toản vác ngọn giáo nhảy ra đánh Lã Bố, mới được vài hiệp, Toản thua chạy. Lã Bố thúc ngựa xích thố xấn lại đuổi, ngựa này chạy nhanh như bay. Bố gần đuổi kịp Toản thì ở bên rìa đường, bỗng có một tướng, mắt tròn trợn ngược. Râu hùm vểnh lên vác một ngọn bát xà mâu, tế ngựa đến thét lên rằng,", pitch="+1Hz", rate="+0%", lead_in_pause="0.40s", timbre_eq="epic_narrator", narrative_mode="epic")
# Line 140: Trương Phi thét
add_line(10, "dialogue", "Truong_Phi", "Thằng ở ba họ kia đừng chạy nữa! Có Trương Phi người đất Yên đây!", pitch="+6Hz", rate="+10%", lead_in_pause="0.30s", timbre_eq="chest_resonance", emotion="cuong_no")
# Line 141: Tam anh chiến Lã Bố
add_line(10, "narrator", "Narrator", "Lã Bố thấy thế bỏ Toản, đánh nhau với Trương Phi. Trương Phi hăng hái cố đánh Lã Bố. Hai người đánh nhau được hơn năm mươi hiệp chưa rõ bên nào thua bên nào được. Quan Công đứng ngoài thấy thế cũng múa thanh long đao nặng tám mươi hai cân đến cùng đánh. Ba con ngựa đứng dàn kiểu chữ đinh, đánh nhau được ba mươi hiệp nữa hai người cũng vẫn không hạ được Lã Bố. Lưu Bị bấy giờ cũng cầm đôi gươm tế ngựa chạy vào đánh giúp. Ba người vây tròn lấy Lã Bố đánh chẳng khác gì quân đèn cù. Binh mã tám xứ ngây mặt ra trông. Lã Bố cố sức chống đỡ không nổi, bèn nhắm giữa mặt Lưu Bị phóng vờ một ngọn kích. Lưu Bị tránh được. Lã Bố mở góc của trận, cắp đao ngược kích, phi ngựa chạy về. Ba người thúc ngựa xấn vào, quân mã tám xứ đều reo ầm lên, xô cả ra đánh. Quan Lã Bố chạy về trên cửa Hổ Lao. Ba người theo sau đuổi mãi.", pitch="+1Hz", rate="+0%", lead_in_pause="0.40s", timbre_eq="epic_narrator", narrative_mode="epic")
# Line 142: Dẫn vào bài ca Tam anh chiến Lã Bố
add_line(10, "narrator", "Narrator", "Cổ nhân, có người làm bài ca kể chuyện Lưu Bị, Quan, Trương đánh Lã Bố rằng,", pitch="-1Hz", rate="-6%", lead_in_pause="0.40s", timbre_eq="contemplative_narrator", narrative_mode="contemplative")
# Line 143: . ......
add_line(10, "narrator", "Narrator", ". ......", pitch="-2Hz", rate="-12%", lead_in_pause="1.50s", timbre_eq="contemplative_narrator", narrative_mode="contemplative")

# Lines 144-169: 26 câu thơ bài ca trong Chunk 10
chunk_10_poems = [
    "Vận Hán đến Hoàn Linh suy thế.",
    "Vầng thái dương đã xế về đoài.",
    "Gian thần Đổng Trác ra oai,",
    "Phế vua, Lưu Hiệp rụng rời thất kinh.",
    "Hịch Tào Tháo truyền nhanh các trấn,",
    "Chư hầu cùng nổi giận dấy binh.",
    "Bản Sơ thủ lãnh đồng minh,",
    "Thề nhau giúp Hán yên bình non sông.",
    "Kia Lã Bố anh hùng ai sánh,",
    "Khắp mọi người dũng mãnh nào bằng?",
    "Áo ngoài giáp bạc sáng choang,",
    "Đầu trên nhấp nhoáng mũ vàng ngù bông.",
    "Mặt thú dữ trập trùng bảo đái,",
    "Cánh phượng bay phấp phới cấm bào.",
    "Vó câu gió chạy ào ào,",
    "Kích hoa sáng quắc soi vào nước trong.",
    "Ra cửa ải tranh hùng ai dám?",
    "Các chư hầu thất đảm kinh hồn.",
    "Trương Phi nhảy vọt ra liền,",
    "Xà mâu một ngọn trận tiền gương uy,",
    "Vểnh râu hổ gầm ghì thét mắng.",
    "Xoe mắt tròn lóng lánh lân la.",
    "Đánh nhau mê mải chưa tha,",
    "Vân Trường nóng tiết nhảy ra xông vào.",
    "Nhoáng màu tuyết, ngọn đao sắc nước,",
    "Áo chiến bào quắc thước màu hoa."
]
for p_text in chunk_10_poems:
    add_line(10, "poem", "Narrator", p_text, pitch="-2Hz", rate="-18%", lead_in_pause="0.85s", timbre_eq="poetic_recitation")

# ==================== CHUNK 11 ====================
# Lines 170-183: 14 câu thơ tiếp nối trong Chunk 11
chunk_11_poems = [
    "Quỷ thần thét, tiếng ngựa ra,",
    "Căm căm khí tức, mắt hoa đỏ ngầu.",
    "Huyền Đức cũng giục mau ngựa nhảy.",
    "Múa đôi gươm vùng vẫy ra oai.",
    "Ba người vây bọc vòng ngoài,",
    "Kẻ đâm người đỡ liền tay không rời.",
    "Tiếng quát háo lay trời động đất,",
    "Sát khí bay cao ngất mây xanh,",
    "Ôn Hầu thế núng nhìn quanh.",
    "Quay đầu ngựa chạy về nhau núi nhà,",
    "Cán họa kích đảo đà tếch trước,",
    "Cờ ngũ hành xơ xác bướm bay.",
    "Giật cương chạy rẽ đường mây,",
    "Hổ Lao trại ấy tọt ngay vào thành."
]
for p_text in chunk_11_poems:
    add_line(11, "poem", "Narrator", p_text, pitch="-2Hz", rate="-18%", lead_in_pause="0.85s", timbre_eq="poetic_recitation")

# Line 184: . ...... Coda kết bài thơ lớn
add_line(11, "narrator", "Narrator", ". ......", pitch="-2Hz", rate="-12%", lead_in_pause="1.50s", timbre_eq="contemplative_narrator", narrative_mode="contemplative")
# Line 185: Trương Phi kêu to lead-in
add_line(11, "narrator", "Narrator", "Ba người đuổi Lã Bố đến dưới cửa quan, trông thấy trên cửa quan có tàn lọng che, gió bay phấp phới. Trương Phi kêu to rằng,", pitch="+1Hz", rate="+0%", lead_in_pause="0.38s", timbre_eq="epic_narrator", narrative_mode="epic")
# Line 186: Trương Phi
add_line(11, "dialogue", "Truong_Phi", "Hẳn Đổng Trác ở đây rồi! Đuổi Lã Bố làm gì nữa, không bằng bắt thằng Đổng Trác mới thực là đào cây nhổ đến tận rễ.", pitch="+4Hz", rate="+8%", lead_in_pause="0.30s", timbre_eq="chest_resonance", emotion="phan_khich_hao_sang")
# Line 187: Tế ngựa lên cửa quan lead-in
add_line(11, "narrator", "Narrator", "Vừa nói vừa tế ngựa lên cửa quan để bắt Đổng Trác. Thế mới thực là,", pitch="0Hz", rate="-5%", lead_in_pause="0.38s", timbre_eq="contemplative_narrator", narrative_mode="contemplative")
# Line 188: . ......
add_line(11, "narrator", "Narrator", ". ......", pitch="-2Hz", rate="-12%", lead_in_pause="1.50s", timbre_eq="contemplative_narrator", narrative_mode="contemplative")
# Line 189-190: Câu đối đúc kết cuối hồi
add_line(11, "poem", "Narrator", "Bắt giặc nên tìm tên đầu sỏ,", pitch="-2Hz", rate="-18%", lead_in_pause="0.85s", timbre_eq="poetic_recitation")
add_line(11, "poem", "Narrator", "Kỳ công lại phải đợi người tài.", pitch="-2Hz", rate="-18%", lead_in_pause="0.85s", timbre_eq="poetic_recitation")
# Line 191: . ......
add_line(11, "narrator", "Narrator", ". ......", pitch="-2Hz", rate="-12%", lead_in_pause="1.50s", timbre_eq="contemplative_narrator", narrative_mode="contemplative")
# Line 192: Câu chốt kết hồi
add_line(11, "narrator", "Narrator", "Chưa biết rồi chuyện ra làm sao, xem đến hồi sau mới rõ.", pitch="-2Hz", rate="-12%", lead_in_pause="0.50s", timbre_eq="contemplative_narrator", narrative_mode="contemplative")

# Count statistics
total_lines = len(lines)
dialogue_lines = [l for l in lines if l["type"] == "dialogue"]
narrator_lines = [l for l in lines if l["type"] == "narrator"]
poem_lines = [l for l in lines if l["type"] == "poem"]

# Character dialogue counts
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
for k, v in char_counts.items():
    print(f"  {k}: {v}")

# Save JSON files
with open(THEATRICAL_SCRIPT_PATH, "w", encoding="utf-8") as f:
    json.dump(lines, f, ensure_ascii=False, indent=2)

with open(THEATRICAL_BIBLE_PATH, "w", encoding="utf-8") as f:
    json.dump(theatrical_bible, f, ensure_ascii=False, indent=2)

print(f"Saved: {THEATRICAL_SCRIPT_PATH}")
print(f"Saved: {THEATRICAL_BIBLE_PATH}")
