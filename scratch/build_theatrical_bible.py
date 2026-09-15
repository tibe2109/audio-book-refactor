#!/usr/bin/env python3
import os
import re
import json
import glob
from collections import defaultdict, Counter

# ------------------------------------------------------------------------------
# 1. Canonical Rules & Historical Lifecycle
# ------------------------------------------------------------------------------

# Known Major Figures Arc Rules
# Defined as list of (max_chap, age_stage, age_desc)
LIFECYCLE_RULES = {
    # Lưu Bị (161 - 223): Hồi 1-85
    'Luu_Bi': [
        (30, 'thanh_xuan', '24-40 tuổi: Kết nghĩa Đào Viên, lưu lạc khởi nghiệp'),
        (75, 'trung_nien', '41-58 tuổi: Tam Cố Thảo Lư, Kinh Châu, xưng Hán Trung Vương'),
        (120, 'lao_hoa', '59-63 tuổi: Xưng đế, phạt Ngô, tạ thế tại Bạch Đế Thành')
    ],
    # Tào Tháo (155 - 220): Hồi 1-78
    'Tao_Thao': [
        (25, 'thanh_xuan', '30-45 tuổi: Hành thích Đổng Trác, lập nghiệp Trung Nguyên'),
        (65, 'trung_nien', '46-60 tuổi: Quan Độ, Xích Bích, xưng Ngụy Vương'),
        (120, 'lao_hoa', '61-66 tuổi: Hoa Đà chữa bệnh đau đầu, tạ thế Lạc Dương')
    ],
    # Gia Cát Lượng (181 - 234): Hồi 37-104
    'Gia_Cat_Luong': [
        (55, 'thanh_xuan', '27-35 tuổi: Xuất sơn Thảo Lư,舌chiến quần nho, Xích Bích'),
        (95, 'trung_nien', '36-50 tuổi: Định Ba Thục, Bình Nam Man, Thất cầm Mạnh Hoạch'),
        (120, 'lao_hoa', '51-54 tuổi: Xuất Kỳ Sơn, cúc cung tận tụy, Ngũ Trượng Nguyên')
    ],
    # Quan Vũ (160 - 219): Hồi 1-77
    'Quan_Vu': [
        (30, 'thanh_xuan', '25-40 tuổi: Trảm Nhan Lương, qua 5 ải chém 6 tướng'),
        (70, 'trung_nien', '41-55 tuổi: Trấn thủ Kinh Châu, Đơn đao phó hội'),
        (120, 'lao_hoa', '56-60 tuổi: Râu bạc, Uy chấn Hoa Hạ, tạ thế Mạch Thành')
    ],
    # Trương Phi (165 - 221): Hồi 1-81
    'Truong_Phi': [
        (30, 'thanh_xuan', '20-35 tuổi: Hét vang Cầu Trường Bản, chiến Lữ Bố'),
        (70, 'trung_nien', '36-50 tuổi: Nghĩa thả Nghiêm Nhan, đại phá Trương Cáp'),
        (120, 'lao_hoa', '51-55 tuổi: Râu tóc bạc, nôn nóng báo thù anh')
    ],
    # Triệu Vân (168 - 229): Hồi 7-97
    'Trieu_Van': [
        (15, 'nien_thieu', '16-20 tuổi: Thiếu niên cứu Công Tôn Toản'),
        (55, 'thanh_xuan', '21-40 tuổi: Đơn kỵ cứu chúa Đương Dương Trường Bản'),
        (90, 'trung_nien', '41-55 tuổi: Cướp ấu chúa trên sông, Hán Thủy lập công'),
        (120, 'lao_hoa', '56-62 tuổi: Lão tướng 70 tuổi trảm ngũ tướng Kỳ Sơn')
    ],
    # Tôn Quyền (182 - 252): Hồi 7-108
    'Ton_Quyen': [
        (20, 'nien_thieu', '9-18 tuổi: Thiếu niên Giang Đông theo cha và anh'),
        (60, 'thanh_xuan', '19-35 tuổi: Kế vị Tôn Sách, đại chiến Xích Bích'),
        (85, 'trung_nien', '36-50 tuổi: Lấy Kinh Châu, xưng vương, xưng hoàng đế'),
        (120, 'lao_hoa', '51-70 tuổi: Già yếu mỏi mệt, lập phế thái tử')
    ],
    # Tôn Sách (175 - 200): Hồi 7-29
    'Ton_Sach': [
        (10, 'nien_thieu', '15-18 tuổi: Tiểu tướng theo Tôn Kiên phá Đổng Trác'),
        (120, 'thanh_xuan', '19-26 tuổi: Tiểu Bá Vương tung hoành Giang Đông')
    ],
    # Chu Du (175 - 210): Hồi 15-57
    'Chu_Du': [
        (35, 'thanh_xuan', '20-30 tuổi: Trai trẻ tuấn tú, kết nghĩa Tôn Sách'),
        (120, 'trung_nien', '31-36 tuổi: Đại đô đốc Xích Bích, tráng chí chưa thành')
    ],
    # Lữ Bố (? - 198): Hồi 3-19
    'La_Bo': [
        (120, 'thanh_xuan', 'Chiến tướng vô song, kiêu hùng thanh xuân ngông cuồng')
    ],
    # Tư Mã Ý (179 - 251): Hồi 39-108
    'Tu_Ma_Y': [
        (55, 'thanh_xuan', '28-35 tuổi: Mới ra làm quan thời Tào Tháo'),
        (95, 'trung_nien', '36-55 tuổi: Đô đốc cự Gia Cát Lượng ở Vị Thủy'),
        (120, 'lao_hoa', '56-72 tuổi: Giả ngây giả dại, chính biến Cao Bình Lăng')
    ],
    # Lưu Thiện / A Đẩu (207 - 271): Hồi 41-119
    'Luu_Thien': [
        (43, 'au_tho', '0-2 tuổi: Ấu thơ trong tã lót ở Trường Bản'),
        (75, 'nien_thieu', '3-16 tuổi: Thiếu niên ở Thành Đô'),
        (90, 'thanh_xuan', '17-30 tuổi: Kế vị Lưu Bị làm Hán Đế'),
        (115, 'trung_nien', '31-50 tuổi: Hưởng lạc Thành Đô, sủng ái Hoàng Hạo'),
        (120, 'lao_hoa', '51-64 tuổi: An Lạc Công ở Lạc Dương')
    ],
    # Hán Hiến Đế (Lưu Hiệp 181 - 234): Hồi 2-80
    'Tran_Luu_Vuong': [
        (120, 'au_tho', '9 tuổi: Trần Lưu Vương đối đáp Đổng Trác')
    ],
    'Han_Hien_De': [
        (5, 'au_tho', '9-14 tuổi: Ấu đế bị Đổng Trác thao túng'),
        (20, 'nien_thieu', '15-19 tuổi: Thiếu niên thiên tử chạy loạn'),
        (65, 'thanh_xuan', '20-35 tuổi: Máu viết chiếu dải lưng áo'),
        (120, 'trung_nien', '36-40 tuổi: Nhường ngôi cho Tào Phi')
    ],
    'Vua': [
        (5, 'au_tho', 'Ấu chúa thời Hán mạt'),
        (25, 'nien_thieu', 'Thiếu đế bị áp chế'),
        (75, 'thanh_xuan', 'Hoàng đế thanh xuân'),
        (120, 'trung_nien', 'Vương quyền trung niên')
    ],
    # Điêu Thuyền: Hồi 8-9
    'Dieu_Thuyen': [
        (120, 'nien_thieu', '16 tuổi: Thiếu nữ tuyệt sắc, liên hoàn kế')
    ],
    # Khương Duy (202 - 264): Hồi 92-119
    'Khuong_Duy': [
        (95, 'nien_thieu', '20-25 tuổi: Thiếu niên hàng Khổng Minh tại Thiên Thủy'),
        (105, 'thanh_xuan', '26-40 tuổi: Tiếp quản quân cơ'),
        (115, 'trung_nien', '41-55 tuổi: Cửu phạt Trung Nguyên'),
        (120, 'lao_hoa', '56-62 tuổi: Một tấc gan trung, tuẫn tiết')
    ],
    # Lục Tốn (183 - 245): Hồi 83-108
    'Luc_Ton': [
        (85, 'nien_thieu', 'Thư sinh áo trắng trẻ tuổi đốt trại Di Lăng'),
        (105, 'thanh_xuan', 'Thừa tướng Đông Ngô'),
        (120, 'trung_nien', 'Nguyên lão Đông Ngô')
    ],
    # Tào Thực (192 - 232): Hồi 33-79
    'Tao_Thuc': [
        (45, 'nien_thieu', 'Thần đồng thi phú thiếu niên'),
        (75, 'thanh_xuan', 'Thi tài thanh xuân, Thất bộ thi'),
        (120, 'trung_nien', 'Cuối đời u sầu')
    ],
    # Quan Hưng & Trương Bào: Hồi 81-94
    'Quan_Hung': [
        (85, 'nien_thieu', 'Tiểu tướng thiếu niên kế chí cha báo thù'),
        (120, 'thanh_xuan', 'Dũng tướng thanh xuân xuất Kỳ Sơn')
    ],
    'Truong_Bao_Shu': [
        (85, 'nien_thieu', 'Tiểu tướng thiếu niên xuất trận'),
        (120, 'thanh_xuan', 'Dũng tướng thanh xuân')
    ],
    'Truong_Bao': [
        (85, 'nien_thieu', 'Tiểu tướng thiếu niên'),
        (120, 'thanh_xuan', 'Dũng tướng thanh xuân')
    ],
    # Lão tướng cố định
    'Hoang_Trung': [(120, 'lao_hoa', 'Lão tướng dũng mãnh, trảm Hạ Hầu Uyên')],
    'Nghiem_Nhan': [(120, 'lao_hoa', 'Lão tướng Ba Thục, chỉ có đầu rơi chứ không hàng')],
    'Lu_Thuc': [(120, 'lao_hoa', 'Học giả, đại thần nguyên lão triều đình')],
    'Kieu_Huyen': [(120, 'lao_hoa', 'Thái úy già, tri kỷ Tào Tháo')],
    'Vuong_Doan': [(120, 'lao_hoa', 'Tư đồ đầu bạc, mưu trừ Đổng Trác')],
    'Tu_Ma_Huy': [(120, 'lao_hoa', 'Thủy Kính tiên sinh, cao nhân ẩn dật')],
    'Kieu_Quoc_Lao': [(120, 'lao_hoa', 'Bô lão danh gia Giang Đông')],
    'Dong_Thai_Hau': [(120, 'lao_hoa', 'Thái hậu cao niên triều Hán')],
    'Ngo_Quoc_Thai': [(120, 'lao_hoa', 'Quốc thái phu nhân Giang Đông')],
    'Dinh_Phung': [
        (100, 'thanh_xuan', 'Chiến tướng trẻ'),
        (110, 'trung_nien', 'Đại đô đốc'),
        (120, 'lao_hoa', 'Lão tướng tuyết dạ trảm địch')
    ],
}

# 10 Temperaments classification dictionary
TEMPERAMENT_REGISTRY = {
    # 1. anh_hung_hao_sang (Anh hùng hào sảng)
    'Quan_Vu': 'anh_hung_hao_sang',
    'Truong_Phi': 'anh_hung_hao_sang',
    'Trieu_Van': 'anh_hung_hao_sang',
    'Hoang_Trung': 'anh_hung_hao_sang',
    'Ton_Sach': 'anh_hung_hao_sang',
    'Ton_Kien': 'anh_hung_hao_sang',
    'Chu_Du': 'anh_hung_hao_sang',
    'Ma_Sieu': 'anh_hung_hao_sang',
    'Cam_Ninh': 'anh_hung_hao_sang',
    'Hua_Chu': 'anh_hung_hao_sang',
    'Dien_Vi': 'anh_hung_hao_sang',
    'Bang_Duc': 'anh_hung_hao_sang',
    'Truong_Lieu': 'anh_hung_hao_sang',
    'Tu_Hoang': 'anh_hung_hao_sang',
    'Thai_Su_Tu': 'anh_hung_hao_sang',
    'Hoang_Cai': 'anh_hung_hao_sang',
    'Nhan_Luong': 'anh_hung_hao_sang',
    'Van_Xu': 'anh_hung_hao_sang',
    'Chu_Thai': 'anh_hung_hao_sang',
    'Trinh_Pho': 'anh_hung_hao_sang',
    'Han_Duong': 'anh_hung_hao_sang',
    'Quan_Binh': 'anh_hung_hao_sang',
    'Quan_Hung': 'anh_hung_hao_sang',
    'Truong_Bao_Shu': 'anh_hung_hao_sang',
    'Dinh_Phung': 'anh_hung_hao_sang',
    'Ton_Phu_Nhan': 'anh_hung_hao_sang',

    # 2. tram_uat_dan_vat (Trầm uất dằn vặt)
    'Tu_Thu': 'tram_uat_dan_vat',
    'Dien_Phong': 'tram_uat_dan_vat',
    'Tran_Cung': 'tram_uat_dan_vat',
    'Luu_Bieu': 'tram_uat_dan_vat',
    'Dong_Thua': 'tram_uat_dan_vat',
    'Vuong_Doan': 'tram_uat_dan_vat',

    # 3. giao_hoat_nham_hiem (Giảo hoạt nham hiểm)
    'Tao_Thao': 'giao_hoat_nham_hiem',
    'Tu_Ma_Y': 'giao_hoat_nham_hiem',
    'Tu_Ma_Su': 'giao_hoat_nham_hiem',
    'Tu_Ma_Chieu': 'giao_hoat_nham_hiem',
    'Gia_Hu': 'giao_hoat_nham_hiem',
    'Quach_Gia': 'giao_hoat_nham_hiem',
    'Ly_Nho': 'giao_hoat_nham_hiem',
    'Chung_Hoi': 'giao_hoat_nham_hiem',
    'Tao_Phi': 'giao_hoat_nham_hiem',

    # 4. hach_dich_bao_nguoc (Hách dịch bạo ngược)
    'Dong_Trac': 'hach_dich_bao_nguoc',
    'La_Bo': 'hach_dich_bao_nguoc',
    'Ha_Hau_Don': 'hach_dich_bao_nguoc',
    'Nguy_Dien': 'hach_dich_bao_nguoc',
    'Vien_Thieu': 'hach_dich_bao_nguoc',
    'Vien_Thuat': 'hach_dich_bao_nguoc',
    'Truong_Giac': 'hach_dich_bao_nguoc',
    'Truong_Bao': 'hach_dich_bao_nguoc',
    'Truong_Luong': 'hach_dich_bao_nguoc',
    'Ha_Tien': 'hach_dich_bao_nguoc',
    'Ly_Thoi': 'hach_dich_bao_nguoc',
    'Quach_Di': 'hach_dich_bao_nguoc',
    'Manh_Hoach': 'hach_dich_bao_nguoc',
    'Chuc_Dung_Phu_Nhan': 'hach_dich_bao_nguoc',
    'Ha_Hoang_Hau': 'hach_dich_bao_nguoc',
    'Dong_Thai_Hau': 'hach_dich_bao_nguoc',
    'Vien_Doc_Buu_Thet': 'hach_dich_bao_nguoc',

    # 5. xun_xoe_don_hen (Xun xoe đớn hèn)
    'Truong_Nhuong': 'xun_xoe_don_hen',
    'Doan_Khue': 'xun_xoe_don_hen',
    'Tao_Tiet': 'xun_xoe_don_hen',
    'Luu_Chuong': 'xun_xoe_don_hen',
    'Luu_Thien': 'xun_xoe_don_hen',

    # 6. trong_sang_thanh_thien (Trong sáng thánh thiện)
    'Luu_Bi': 'trong_sang_thanh_thien',
    'Lo_Tuc': 'trong_sang_thanh_thien',
    'Hoa_Da': 'trong_sang_thanh_thien',
    'My_Truc': 'trong_sang_thanh_thien',
    'Ton_Can': 'trong_sang_thanh_thien',
    'Luu_Nguyen_Khoi': 'trong_sang_thanh_thien',
    'Cam_Phu_Nhan': 'trong_sang_thanh_thien',
    'Bien_Phu_Nhan': 'trong_sang_thanh_thien',

    # 7. bi_kich_uat_nghen (Bi kịch uất nghẹn)
    'Tran_Luu_Vuong': 'bi_kich_uat_nghen',
    'Han_Hien_De': 'bi_kich_uat_nghen',
    'My_Phu_Nhan': 'bi_kich_uat_nghen',

    # 8. lang_man_bay_bong (Lãng mạn bay bổng)
    'Tao_Thuc': 'lang_man_bay_bong',
    'Dieu_Thuyen': 'lang_man_bay_bong',
    'Tieu_Kieu': 'lang_man_bay_bong',
    'Dai_Kieu': 'lang_man_bay_bong',

    # 9. khac_kho_lanh_lung (Khắc khổ lạnh lùng)
    'Gia_Cat_Luong': 'khac_kho_lanh_lung',
    'Lu_Thuc': 'khac_kho_lanh_lung',
    'Phap_Chinh': 'khac_kho_lanh_lung',
    'Tuan_Uc': 'khac_kho_lanh_lung',
    'Trinh_Duc': 'khac_kho_lanh_lung',
    'Dang_Ngai': 'khac_kho_lanh_lung',
    'Truong_Chieu': 'khac_kho_lanh_lung',
    'Luc_Ton': 'khac_kho_lanh_lung',
    'Ngo_Quoc_Thai': 'khac_kho_lanh_lung',

    # 10. teu_tao_hom_hinh (Tếu táo hóm hỉnh)
    'Gian_Ung': 'teu_tao_hom_hinh',
    'Bang_Thong': 'teu_tao_hom_hinh',
    'Duong_Tu': 'teu_tao_hom_hinh',
    'Truong_The_Binh': 'teu_tao_hom_hinh',
    'To_Song': 'teu_tao_hom_hinh',
}

# ------------------------------------------------------------------------------
# 2. Acoustic Base Scales (Section 1.2)
# ------------------------------------------------------------------------------
AGE_BASE_PITCH = {
    'au_tho': 9,       # Range: +8Hz to +12Hz
    'nien_thieu': 5,   # Range: +4Hz to +7Hz
    'thanh_xuan': 1,   # Range: 0Hz to +3Hz
    'trung_nien': -4,  # Range: -3Hz to -5Hz
    'lao_hoa': -7      # Range: -6Hz to -8Hz
}

AGE_BASE_RATE = {
    'au_tho': 10,
    'nien_thieu': 6,
    'thanh_xuan': 2,
    'trung_nien': -6,
    'lao_hoa': -16
}

TEMPERAMENT_DELTAS = {
    'anh_hung_hao_sang': {'pitch': 0, 'rate': 0},
    'tram_uat_dan_vat': {'pitch': -2, 'rate': -4},
    'giao_hoat_nham_hiem': {'pitch': -1, 'rate': -2},
    'hach_dich_bao_nguoc': {'pitch': 2, 'rate': 4},
    'xun_xoe_don_hen': {'pitch': 3, 'rate': 4},
    'trong_sang_thanh_thien': {'pitch': 1, 'rate': 2},
    'bi_kich_uat_nghen': {'pitch': -1, 'rate': -4},
    'lang_man_bay_bong': {'pitch': 2, 'rate': -2},
    'khac_kho_lanh_lung': {'pitch': -1, 'rate': -4},
    'teu_tao_hom_hinh': {'pitch': 2, 'rate': 3},
}

TEMPERAMENT_NAMES_VI = {
    'anh_hung_hao_sang': 'Anh hùng hào sảng',
    'tram_uat_dan_vat': 'Trầm uất dằn vặt',
    'giao_hoat_nham_hiem': 'Giảo hoạt nham hiểm',
    'hach_dich_bao_nguoc': 'Hách dịch bạo ngược',
    'xun_xoe_don_hen': 'Xun xoe đớn hèn',
    'trong_sang_thanh_thien': 'Trong sáng thánh thiện',
    'bi_kich_uat_nghen': 'Bi kịch uất nghẹn',
    'lang_man_bay_bong': 'Lãng mạn bay bổng',
    'khac_kho_lanh_lung': 'Khắc khổ lạnh lùng',
    'teu_tao_hom_hinh': 'Tếu táo hóm hỉnh'
}

AGE_NAMES_VI = {
    'au_tho': 'Ấu thơ (0-13 tuổi)',
    'nien_thieu': 'Niên thiếu / Vỡ giọng (14-18 tuổi)',
    'thanh_xuan': 'Thanh xuân (19-35 tuổi)',
    'trung_nien': 'Trung niên (36-55 tuổi)',
    'lao_hoa': 'Lão hóa (>55 tuổi)'
}

ATSE_DESCRIPTIONS = {
    'chest_resonance': {
        'name': 'Vang rền lồng ngực (Chest Resonance)',
        'target_characters': 'Hảo hán xung trận, dũng tướng mãnh liệt',
        'dsp': 'Boost 180Hz (+4dB), Boost 2kHz (+2dB)',
        'acoustic_effect': 'Vang rền lồng ngực, đanh thép như lệnh sấm truyền'
    },
    'warm_authority': {
        'name': 'Uy quyền trầm ấm (Warm Authority)',
        'target_characters': 'Bậc minh chủ, quân sư, nho tướng, đại phu',
        'dsp': 'Boost 300Hz (+2.5dB), Dip 3.5kHz (-2dB)',
        'acoustic_effect': 'Trầm ấm, đĩnh đạc, tròn vành rõ chữ của bậc danh gia'
    },
    'sharp_cunning': {
        'name': 'The lạnh giảo hoạt (Sharp Cunning)',
        'target_characters': 'Gian hùng, mưu sĩ thâm hiểm, nịnh thần',
        'dsp': 'Low-cut <200Hz, Boost 3kHz (+3.5dB)',
        'acoustic_effect': 'The lạnh, gằn mép, hiểm hóc, giảo hoạt sắc bén'
    },
    'aged_gravel': {
        'name': 'Khàn đục sương gió (Aged Gravel)',
        'target_characters': 'Trưởng lão, lão tướng, nhân vật cao niên',
        'dsp': 'Boost 450Hz (+3dB), Roll-off >5kHz (-3dB)',
        'acoustic_effect': 'Khàn đục, cũ kỹ, trải đời của kiếp người sương gió'
    },
    'youth_bright': {
        'name': 'Sáng mảnh trong trẻo (Youth Bright)',
        'target_characters': 'Ấu chúa, thiếu niên, thiếu nữ thanh tân',
        'dsp': 'Low-cut 250Hz, Boost 4kHz (+3dB)',
        'acoustic_effect': 'Sáng mảnh, thanh thoát, ngây thơ trong trẻo'
    }
}

def resolve_character_age_stage(cid, chap_idx, name=""):
    low_name = name.lower()
    # Check manual lifecycle rules first
    if cid in LIFECYCLE_RULES:
        for max_chap, stage, desc in LIFECYCLE_RULES[cid]:
            if chap_idx <= max_chap:
                return stage
        return LIFECYCLE_RULES[cid][-1][1]
    
    # Specific keywords
    if any(k in low_name for k in ('thơ', 'ấu', 'hài đồng', 'đồng tử', 'tiểu nhi', 'trẻ con', 'trần lưu vương')):
        return 'au_tho'
    if any(k in low_name for k in ('thiếu niên', 'tiểu tướng', 'tiểu đồng', 'thị nữ', 'thư sinh')):
        return 'nien_thieu'
    if any(k in low_name for k in ('lão', 'ông', 'bà', 'thái hậu', 'quốc thái', 'trưởng lão', 'bô lão')):
        return 'lao_hoa'
    
    # Historical epoch heuristic
    if chap_idx <= 25:
        return 'thanh_xuan'
    elif chap_idx <= 75:
        return 'trung_nien'
    else:
        return 'lao_hoa'

def resolve_character_temperament(cid, name=""):
    if cid in TEMPERAMENT_REGISTRY:
        return TEMPERAMENT_REGISTRY[cid]
    
    low_name = name.lower()
    if any(k in low_name for k in ('thơ', 'ngâm', 'thiền', 'nàng', 'mỹ', 'kiều')):
        return 'lang_man_bay_bong'
    if any(k in low_name for k in ('thét', 'quát', 'giận', 'hách', 'bạo', 'hung', 'trác', 'bố')):
        return 'hach_dich_bao_nguoc'
    if any(k in low_name for k in ('cười', 'hài', 'ung', 'tu', 'bàng')):
        return 'teu_tao_hom_hinh'
    if any(k in low_name for k in ('than', 'khóc', 'nghẹn', 'oan', 'uất')):
        return 'bi_kich_uat_nghen'
    if any(k in low_name for k in ('thầm', 'mưu', 'kế', 'gian', 'nham', 'hiểm')):
        return 'giao_hoat_nham_hiem'
    if any(k in low_name for k in ('nịnh', 'quỳ', 'van', 'lạy', 'đớn hèn')):
        return 'xun_xoe_don_hen'
    if any(k in low_name for k in ('nhân', 'hiền', 'đức', 'từ', 'thánh')):
        return 'trong_sang_thanh_thien'
    if any(k in low_name for k in ('lạnh', 'khắc', 'nghiêm', 'chính', 'nghị')):
        return 'khac_kho_lanh_lung'
    if any(k in low_name for k in ('uất', 'sầu', 'trầm', 'lo')):
        return 'tram_uat_dan_vat'
    
    return 'anh_hung_hao_sang'

def resolve_character_timbre(cid, gender, age_stage, temperament):
    if gender == 'female' or age_stage in ('au_tho', 'nien_thieu'):
        return 'youth_bright'
    if age_stage == 'lao_hoa':
        return 'aged_gravel'
    if temperament == 'anh_hung_hao_sang':
        if cid in ('Truong_Phi', 'Hua_Chu', 'Dien_Vi', 'Cam_Ninh', 'Bang_Duc', 'Nhan_Luong', 'Van_Xu', 'Ha_Hau_Don'):
            return 'chest_resonance'
        return 'warm_authority'
    if temperament in ('giao_hoat_nham_hiem', 'xun_xoe_don_hen'):
        return 'sharp_cunning'
    if temperament in ('trong_sang_thanh_thien', 'khac_kho_lanh_lung', 'tram_uat_dan_vat'):
        return 'warm_authority'
    if temperament == 'hach_dich_bao_nguoc':
        return 'chest_resonance'
    return 'warm_authority'

def calculate_base_acoustic(age_stage, temperament):
    b_pitch = AGE_BASE_PITCH.get(age_stage, 1)
    b_rate = AGE_BASE_RATE.get(age_stage, 2)
    d_temp = TEMPERAMENT_DELTAS.get(temperament, {'pitch': 0, 'rate': 0})
    
    final_pitch = b_pitch + d_temp['pitch']
    final_rate = b_rate + d_temp['rate']
    
    # Clamp strictly within [-8Hz, +12Hz]
    final_pitch = max(-8, min(12, final_pitch))
    final_rate = max(-20, min(15, final_rate))
    
    p_str = f"+{final_pitch}Hz" if final_pitch > 0 else (f"{final_pitch}Hz" if final_pitch < 0 else "+0Hz")
    r_str = f"+{final_rate}%" if final_rate > 0 else (f"{final_rate}%" if final_rate < 0 else "+0%")
    return p_str, r_str, final_pitch, final_rate

print("Module loaded successfully.")
