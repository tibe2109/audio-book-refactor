#!/usr/bin/env python3
# ==============================================================================
# Step 08A: Chief Theatrical Voice & Casting Director
# Skill: arf_08a_theatrical_voice_director
# ==============================================================================
import os
import re
import json
import glob
import argparse
import datetime

# ------------------------------------------------------------------------------
# Canonical Character Registry for Classical Historical Epic (Tam Quốc Diễn Nghĩa)
# ------------------------------------------------------------------------------
KNOWN_CHARACTERS = {
    # Thục Hán (Shu)
    'huyền đức': ('Luu_Bi', 'Lưu Bị', 'male', 'trong_sang_thanh_thien'),
    'lưu bị': ('Luu_Bi', 'Lưu Bị', 'male', 'trong_sang_thanh_thien'),
    'lưu huyền đức': ('Luu_Bi', 'Lưu Bị', 'male', 'trong_sang_thanh_thien'),
    'tiên chủ': ('Luu_Bi', 'Lưu Bị', 'male', 'trong_sang_thanh_thien'),
    'bị': ('Luu_Bi', 'Lưu Bị', 'male', 'trong_sang_thanh_thien'),
    
    'quan vũ': ('Quan_Vu', 'Quan Vũ', 'male', 'khac_kho_lanh_lung'),
    'vân trường': ('Quan_Vu', 'Quan Vũ', 'male', 'khac_kho_lanh_lung'),
    'quan công': ('Quan_Vu', 'Quan Vũ', 'male', 'khac_kho_lanh_lung'),
    'quan tướng quân': ('Quan_Vu', 'Quan Vũ', 'male', 'khac_kho_lanh_lung'),
    
    'trương phi': ('Truong_Phi', 'Trương Phi', 'male', 'anh_hung_hao_sang'),
    'dực đức': ('Truong_Phi', 'Trương Phi', 'male', 'anh_hung_hao_sang'),
    'phi': ('Truong_Phi', 'Trương Phi', 'male', 'anh_hung_hao_sang'),
    
    'gia cát lượng': ('Gia_Cat_Luong', 'Gia Cát Lượng', 'male', 'khac_kho_lanh_lung'),
    'khổng minh': ('Gia_Cat_Luong', 'Gia Cát Lượng', 'male', 'khac_kho_lanh_lung'),
    'ngọa long': ('Gia_Cat_Luong', 'Gia Cát Lượng', 'male', 'khac_kho_lanh_lung'),
    'quân sư': ('Gia_Cat_Luong', 'Gia Cát Lượng', 'male', 'khac_kho_lanh_lung'),
    'lượng': ('Gia_Cat_Luong', 'Gia Cát Lượng', 'male', 'khac_kho_lanh_lung'),
    
    'triệu vân': ('Trieu_Van', 'Triệu Vân', 'male', 'anh_hung_hao_sang'),
    'tử long': ('Trieu_Van', 'Triệu Vân', 'male', 'anh_hung_hao_sang'),
    'vân': ('Trieu_Van', 'Triệu Vân', 'male', 'anh_hung_hao_sang'),
    
    'hoàng trung': ('Hoang_Trung', 'Hoàng Trung', 'male', 'anh_hung_hao_sang'),
    'mã siêu': ('Ma_Sieu', 'Mã Siêu', 'male', 'anh_hung_hao_sang'),
    'khương duy': ('Khuong_Duy', 'Khương Duy', 'male', 'anh_hung_hao_sang'),
    'ngụy diên': ('Nguy_Dien', 'Ngụy Diên', 'male', 'hach_dich_bao_nguoc'),
    'bàng thống': ('Bang_Thong', 'Bàng Thống', 'male', 'teu_tao_hom_hinh'),
    'pháp chính': ('Phap_Chinh', 'Pháp Chính', 'male', 'khac_kho_lanh_lung'),
    'từ thứ': ('Tu_Thu', 'Từ Thứ', 'male', 'tram_uat_dan_vat'),
    'lưu thiền': ('Luu_Thien', 'Lưu Thiền', 'male', 'xun_xoe_don_hen'),
    'hậu chủ': ('Luu_Thien', 'Lưu Thiền', 'male', 'xun_xoe_don_hen'),
    'my trúc': ('My_Truc', 'My Trúc', 'male', 'trong_sang_thanh_thien'),
    'tôn càn': ('Ton_Can', 'Tôn Càn', 'male', 'trong_sang_thanh_thien'),
    'giản ung': ('Gian_Ung', 'Giản Ung', 'male', 'teu_tao_hom_hinh'),
    'nghiêm nhan': ('Nghiem_Nhan', 'Nghiêm Nhan', 'male', 'anh_hung_hao_sang'),
    'mã tắc': ('Ma_Tac', 'Mã Tắc', 'male', 'tram_uat_dan_vat'),
    'mã lăng': ('Ma_Lang', 'Mã Lăng', 'male', 'trong_sang_thanh_thien'),
    'quan bình': ('Quan_Binh', 'Quan Bình', 'male', 'anh_hung_hao_sang'),
    'quan hưng': ('Quan_Hung', 'Quan Hưng', 'male', 'anh_hung_hao_sang'),
    'trương bào': ('Truong_Bao_Shu', 'Trương Bào', 'male', 'anh_hung_hao_sang'),

    # Tào Ngụy (Wei)
    'tào tháo': ('Tao_Thao', 'Tào Tháo', 'male', 'giao_hoat_nham_hiem'),
    'mạnh đức': ('Tao_Thao', 'Tào Tháo', 'male', 'giao_hoat_nham_hiem'),
    'tháo': ('Tao_Thao', 'Tào Tháo', 'male', 'giao_hoat_nham_hiem'),
    'tào phi': ('Tao_Phi', 'Tào Phi', 'male', 'giao_hoat_nham_hiem'),
    'tào duệ': ('Tao_Due', 'Tào Duệ', 'male', 'khac_kho_lanh_lung'),
    'tào thực': ('Tao_Thuc', 'Tào Thực', 'male', 'lang_man_bay_bong'),
    'tào nhân': ('Tao_Nhan', 'Tào Nhân', 'male', 'anh_hung_hao_sang'),
    'tào hồng': ('Tao_Hong', 'Tào Hồng', 'male', 'anh_hung_hao_sang'),
    
    'tư mã ý': ('Tu_Ma_Y', 'Tư Mã Ý', 'male', 'giao_hoat_nham_hiem'),
    'trọng đạt': ('Tu_Ma_Y', 'Tư Mã Ý', 'male', 'giao_hoat_nham_hiem'),
    'tư mã sư': ('Tu_Ma_Su', 'Tư Mã Sư', 'male', 'giao_hoat_nham_hiem'),
    'tư mã chiêu': ('Tu_Ma_Chieu', 'Tư Mã Chiêu', 'male', 'giao_hoat_nham_hiem'),
    'tuân úc': ('Tuan_Uc', 'Tuân Úc', 'male', 'khac_kho_lanh_lung'),
    'quách gia': ('Quach_Gia', 'Quách Gia', 'male', 'giao_hoat_nham_hiem'),
    'giả hủ': ('Gia_Hu', 'Giả Hủ', 'male', 'giao_hoat_nham_hiem'),
    'trình dục': ('Trinh_Duc', 'Trình Dục', 'male', 'khac_kho_lanh_lung'),
    'dương tu': ('Duong_Tu', 'Dương Tu', 'male', 'teu_tao_hom_hinh'),
    'trương liêu': ('Truong_Lieu', 'Trương Liêu', 'male', 'anh_hung_hao_sang'),
    'trương cáp': ('Truong_Cap', 'Trương Cáp', 'male', 'anh_hung_hao_sang'),
    'hạ hầu đôn': ('Ha_Hau_Don', 'Hạ Hầu Đôn', 'male', 'hach_dich_bao_nguoc'),
    'hạ hầu uyên': ('Ha_Hau_Uyen', 'Hạ Hầu Uyên', 'male', 'anh_hung_hao_sang'),
    'hứa chử': ('Hua_Chu', 'Hứa Chử', 'male', 'anh_hung_hao_sang'),
    'điển vi': ('Dien_Vi', 'Điển Vi', 'male', 'anh_hung_hao_sang'),
    'bàng đức': ('Bang_Duc', 'Bàng Đức', 'male', 'anh_hung_hao_sang'),
    'đặng ngải': ('Dang_Ngai', 'Đặng Ngải', 'male', 'khac_kho_lanh_lung'),
    'chung hội': ('Chung_Hoi', 'Chung Hội', 'male', 'giao_hoat_nham_hiem'),

    # Đông Ngô (Wu)
    'tôn kiên': ('Ton_Kien', 'Tôn Kiên', 'male', 'anh_hung_hao_sang'),
    'văn đài': ('Ton_Kien', 'Tôn Kiên', 'male', 'anh_hung_hao_sang'),
    'kiên': ('Ton_Kien', 'Tôn Kiên', 'male', 'anh_hung_hao_sang'),
    'tôn sách': ('Ton_Sach', 'Tôn Sách', 'male', 'anh_hung_hao_sang'),
    'bá phù': ('Ton_Sach', 'Tôn Sách', 'male', 'anh_hung_hao_sang'),
    'sách': ('Ton_Sach', 'Tôn Sách', 'male', 'anh_hung_hao_sang'),
    'tôn quyền': ('Ton_Quyen', 'Tôn Quyền', 'male', 'anh_hung_hao_sang'),
    'trọng mưu': ('Ton_Quyen', 'Tôn Quyền', 'male', 'anh_hung_hao_sang'),
    'quyền': ('Ton_Quyen', 'Tôn Quyền', 'male', 'anh_hung_hao_sang'),
    'ngô chúa': ('Ton_Quyen', 'Tôn Quyền', 'male', 'anh_hung_hao_sang'),
    
    'chu du': ('Chu_Du', 'Chu Du', 'male', 'tram_uat_dan_vat'),
    'công cẩn': ('Chu_Du', 'Chu Du', 'male', 'tram_uat_dan_vat'),
    'du': ('Chu_Du', 'Chu Du', 'male', 'tram_uat_dan_vat'),
    'lỗ túc': ('Lo_Tuc', 'Lỗ Túc', 'male', 'trong_sang_thanh_thien'),
    'tử kính': ('Lo_Tuc', 'Lỗ Túc', 'male', 'trong_sang_thanh_thien'),
    'lữ mông': ('Lu_Mong', 'Lữ Mông', 'male', 'anh_hung_hao_sang'),
    'lục tốn': ('Luc_Ton', 'Lục Tốn', 'male', 'khac_kho_lanh_lung'),
    'hoàng cái': ('Hoang_Cai', 'Hoàng Cái', 'male', 'anh_hung_hao_sang'),
    'cam ninh': ('Cam_Ninh', 'Cam Ninh', 'male', 'hach_dich_bao_nguoc'),
    'trương chiêu': ('Truong_Chieu', 'Trương Chiêu', 'male', 'khac_kho_lanh_lung'),
    'thái sử từ': ('Thai_Su_Tu', 'Thái Sử Từ', 'male', 'anh_hung_hao_sang'),
    'chu thái': ('Chu_Thai', 'Chu Thái', 'male', 'anh_hung_hao_sang'),
    'trình phổ': ('Trinh_Pho', 'Trình Phổ', 'male', 'anh_hung_hao_sang'),
    'hàn đương': ('Han_Duong', 'Hàn Đương', 'male', 'anh_hung_hao_sang'),

    # Quần Hùng & Thời Đầu
    'đổng trác': ('Dong_Trac', 'Đổng Trác', 'male', 'hach_dich_bao_nguoc'),
    'trọng dĩnh': ('Dong_Trac', 'Đổng Trác', 'male', 'hach_dich_bao_nguoc'),
    'trác': ('Dong_Trac', 'Đổng Trác', 'male', 'hach_dich_bao_nguoc'),
    'thái sư': ('Dong_Trac', 'Đổng Trác', 'male', 'hach_dich_bao_nguoc'),
    
    'lã bố': ('La_Bo', 'Lã Bố', 'male', 'hach_dich_bao_nguoc'),
    'phụng tiên': ('La_Bo', 'Lã Bố', 'male', 'hach_dich_bao_nguoc'),
    'bố': ('La_Bo', 'Lã Bố', 'male', 'hach_dich_bao_nguoc'),
    
    'viên thiệu': ('Vien_Thieu', 'Viên Thiệu', 'male', 'hach_dich_bao_nguoc'),
    'bổn sơ': ('Vien_Thieu', 'Viên Thiệu', 'male', 'hach_dich_bao_nguoc'),
    'thiệu': ('Vien_Thieu', 'Viên Thiệu', 'male', 'hach_dich_bao_nguoc'),
    'viên thuật': ('Vien_Thuat', 'Viên Thuật', 'male', 'hach_dich_bao_nguoc'),
    'thuật': ('Vien_Thuat', 'Viên Thuật', 'male', 'hach_dich_bao_nguoc'),
    'nhan lương': ('Nhan_Luong', 'Nhan Lương', 'male', 'anh_hung_hao_sang'),
    'văn xú': ('Van_Xu', 'Văn Xú', 'male', 'anh_hung_hao_sang'),
    
    'trương giác': ('Truong_Giac', 'Trương Giác', 'male', 'hach_dich_bao_nguoc'),
    'giác': ('Truong_Giac', 'Trương Giác', 'male', 'hach_dich_bao_nguoc'),
    'trương bảo': ('Truong_Bao', 'Trương Bảo', 'male', 'hach_dich_bao_nguoc'),
    'trương lương': ('Truong_Luong', 'Trương Lương', 'male', 'hach_dich_bao_nguoc'),
    'lư thực': ('Lu_Thuc', 'Lư Thực', 'male', 'khac_kho_lanh_lung'),
    'thực': ('Lu_Thuc', 'Lư Thực', 'male', 'khac_kho_lanh_lung'),
    'chu tuấn': ('Chu_Tuan', 'Chu Tuấn', 'male', 'anh_hung_hao_sang'),
    'tuấn': ('Chu_Tuan', 'Chu Tuấn', 'male', 'anh_hung_hao_sang'),
    'hoàng phủ tung': ('Hoang_Phu_Tung', 'Hoàng Phủ Tung', 'male', 'anh_hung_hao_sang'),
    'tung': ('Hoang_Phu_Tung', 'Hoàng Phủ Tung', 'male', 'anh_hung_hao_sang'),
    'lưu yên': ('Luu_Yen', 'Lưu Yên', 'male', 'anh_hung_hao_sang'),
    'yên': ('Luu_Yen', 'Lưu Yên', 'male', 'anh_hung_hao_sang'),
    'lưu tĩnh': ('Luu_Tinh', 'Lưu Tĩnh', 'male', 'anh_hung_hao_sang'),
    'tĩnh': ('Luu_Tinh', 'Lưu Tĩnh', 'male', 'anh_hung_hao_sang'),
    'lưu nguyên khởi': ('Luu_Nguyen_Khoi', 'Lưu Nguyên Khởi', 'male', 'trong_sang_thanh_thien'),
    'nguyên khởi': ('Luu_Nguyen_Khoi', 'Lưu Nguyên Khởi', 'male', 'trong_sang_thanh_thien'),
    'cung cảnh': ('Cung_Canh', 'Cung Cảnh', 'male', 'anh_hung_hao_sang'),
    'hứa thiệu': ('Hua_Thieu', 'Hứa Thiệu', 'male', 'khac_kho_lanh_lung'),
    'kiều huyền': ('Kieu_Huyen', 'Kiều Huyền', 'male', 'khac_kho_lanh_lung'),
    'trương thế bình': ('Truong_The_Binh', 'Trương Thế Bình', 'male', 'teu_tao_hom_hinh'),
    'tô song': ('To_Song', 'Tô Song', 'male', 'teu_tao_hom_hinh'),
    'hà tiến': ('Ha_Tien', 'Hà Tiến', 'male', 'hach_dich_bao_nguoc'),
    'đinh nguyên': ('Dinh_Nguyen', 'Đinh Nguyên', 'male', 'khac_kho_lanh_lung'),
    'vương doãn': ('Vuong_Doan', 'Vương Doãn', 'male', 'tram_uat_dan_vat'),
    'trần cung': ('Tran_Cung', 'Trần Cung', 'male', 'khac_kho_lanh_lung'),
    'lý nho': ('Ly_Nho', 'Lý Nho', 'male', 'giao_hoat_nham_hiem'),
    'lý thôi': ('Ly_Thoi', 'Lý Thôi', 'male', 'hach_dich_bao_nguoc'),
    'quách dĩ': ('Quach_Di', 'Quách Dĩ', 'male', 'hach_dich_bao_nguoc'),
    'hoa đà': ('Hoa_Da', 'Hoa Đà', 'male', 'trong_sang_thanh_thien'),
    'khổng dung': ('Khong_Dung', 'Khổng Dung', 'male', 'trong_sang_thanh_thien'),
    'mã đằng': ('Ma_Dang', 'Mã Đằng', 'male', 'anh_hung_hao_sang'),
    'hàn toại': ('Han_Toai', 'Hàn Toại', 'male', 'anh_hung_hao_sang'),
    'lưu biểu': ('Luu_Bieu', 'Lưu Biểu', 'male', 'tram_uat_dan_vat'),
    'lưu chương': ('Luu_Chuong', 'Lưu Chương', 'male', 'xun_xoe_don_hen'),
    'trương lỗ': ('Truong_Lo', 'Trương Lỗ', 'male', 'hach_dich_bao_nguoc'),
    'mạnh hoạch': ('Manh_Hoach', 'Mạnh Hoạch', 'male', 'hach_dich_bao_nguoc'),

    # Hoạn quan & Cận thần
    'trương nhượng': ('Truong_Nhuong', 'Trương Nhượng', 'male', 'xun_xoe_don_hen'),
    'đoạn khuê': ('Doan_Khue', 'Đoạn Khuê', 'male', 'xun_xoe_don_hen'),
    'tào tiết': ('Tao_Tiet', 'Tào Tiết', 'male', 'xun_xoe_don_hen'),

    # Nhân Vật Nữ (Female)
    'điêu thuyền': ('Dieu_Thuyen', 'Điêu Thuyền', 'female', 'trong_sang_thanh_thien'),
    'chúc dung phu nhân': ('Chuc_Dung_Phu_Nhan', 'Chúc Dung Phu Nhân', 'female', 'hach_dich_bao_nguoc'),
    'tôn phu nhân': ('Ton_Phu_Nhan', 'Tôn Phu Nhân', 'female', 'anh_hung_hao_sang'),
    'cam phu nhân': ('Cam_Phu_Nhan', 'Cam Phu Nhân', 'female', 'trong_sang_thanh_thien'),
    'my phu nhân': ('My_Phu_Nhan', 'My Phu Nhân', 'female', 'bi_kich_uat_nghen'),
    'thái hậu': ('Dong_Thai_Hau', 'Đổng Thái Hậu', 'female', 'hach_dich_bao_nguoc'),
    'đổng thái hậu': ('Dong_Thai_Hau', 'Đổng Thái Hậu', 'female', 'hach_dich_bao_nguoc'),
    'hà hoàng hậu': ('Ha_Hoang_Hau', 'Hà Hoàng Hậu', 'female', 'hach_dich_bao_nguoc'),
    'hoàng hậu': ('Ha_Hoang_Hau', 'Hà Hoàng Hậu', 'female', 'hach_dich_bao_nguoc'),
    'biện phu nhân': ('Bien_Phu_Nhan', 'Biện Phu Nhân', 'female', 'trong_sang_thanh_thien'),
    'ngô quốc thái': ('Ngo_Quoc_Thai', 'Ngô Quốc Thái', 'female', 'khac_kho_lanh_lung'),
    'tiểu kiều': ('Tieu_Kieu', 'Tiểu Kiều', 'female', 'lang_man_bay_bong'),
    'đại kiều': ('Dai_Kieu', 'Đại Kiều', 'female', 'lang_man_bay_bong'),
}

def vn_to_ascii_id(text):
    """Converts Vietnamese string into clean ASCII identifier (e.g. 'Tào Tháo' -> 'Tao_Thao')."""
    accents = {
        'à': 'a', 'á': 'a', 'ả': 'a', 'ã': 'a', 'ạ': 'a',
        'ă': 'a', 'ằ': 'a', 'ắ': 'a', 'ẳ': 'a', 'ẵ': 'a', 'ặ': 'a',
        'â': 'a', 'ầ': 'a', 'ấ': 'a', 'ẩ': 'a', 'ẫ': 'a', 'ậ': 'a',
        'đ': 'd',
        'è': 'e', 'é': 'e', 'ẻ': 'e', 'ẽ': 'e', 'ẹ': 'e',
        'ê': 'e', 'ề': 'e', 'ế': 'e', 'ể': 'e', 'ễ': 'e', 'ệ': 'e',
        'ì': 'i', 'í': 'i', 'ỉ': 'i', 'ĩ': 'i', 'ị': 'i',
        'ò': 'o', 'ó': 'o', 'ỏ': 'o', 'õ': 'o', 'ọ': 'o',
        'ô': 'o', 'ồ': 'o', 'ố': 'o', 'ổ': 'o', 'ỗ': 'o', 'ộ': 'o',
        'ơ': 'o', 'ờ': 'o', 'ớ': 'o', 'ở': 'o', 'ỡ': 'o', 'ợ': 'o',
        'ù': 'u', 'ú': 'u', 'ủ': 'u', 'ũ': 'u', 'ụ': 'u',
        'ư': 'u', 'ừ': 'u', 'ứ': 'u', 'ử': 'u', 'ữ': 'u', 'ự': 'u',
        'ỳ': 'y', 'ý': 'y', 'ỷ': 'y', 'ỹ': 'y', 'ỵ': 'y'
    }
    s = text.lower()
    res = []
    for ch in s:
        res.append(accents.get(ch, ch))
    s_clean = "".join(res)
    return re.sub(r'[^a-zA-Z0-9]+', '_', s_clean.title()).strip('_')

# ------------------------------------------------------------------------------
# Acoustic Parameters Tables (SKILL.md Section 1.2) - Enhanced Deep Contrast
# ------------------------------------------------------------------------------
AGE_ACOUSTIC = {
    'au_tho': {'pitch': 10, 'rate': 10},
    'nien_thieu': {'pitch': 6, 'rate': 6},
    'thanh_xuan': {'pitch': 1, 'rate': 2},
    'trung_nien': {'pitch': -4, 'rate': -8},
    'lao_hoa': {'pitch': -8, 'rate': -18},
}

TEMPERAMENT_DELTAS = {
    'anh_hung_hao_sang': {'pitch': -2, 'rate': 0},
    'tram_uat_dan_vat': {'pitch': -3, 'rate': -6},
    'giao_hoat_nham_hiem': {'pitch': 1, 'rate': -4},
    'hach_dich_bao_nguoc': {'pitch': 3, 'rate': 6},
    'xun_xoe_don_hen': {'pitch': 6, 'rate': 8},
    'trong_sang_thanh_thien': {'pitch': 3, 'rate': 2},
    'bi_kich_uat_nghen': {'pitch': -4, 'rate': -8},
    'lang_man_bay_bong': {'pitch': 1, 'rate': -3},
    'khac_kho_lanh_lung': {'pitch': -3, 'rate': -6},
    'teu_tao_hom_hinh': {'pitch': 3, 'rate': 4},
}

EMOTION_DELTAS = {
    'cuong_no': {'pitch': 6, 'rate': 8},
    'dau_don_trang_troi': {'pitch': -5, 'rate': -10},
    'de_doa_tham_hiem': {'pitch': -5, 'rate': -6},
    'ninh_bo_van_xin': {'pitch': 6, 'rate': 6},
    'hoi_hop_thi_thao': {'pitch': -1, 'rate': -6},
    'doc_thoai_dan_vat': {'pitch': -3, 'rate': -5},
    'ghen_tuong_cay_dang': {'pitch': 2, 'rate': 0},
    'nguong_ngung_tinh_dau': {'pitch': 3, 'rate': -2},
    'bang_hoang_chet_lang': {'pitch': 0, 'rate': -10},
    'hoan_ca_dac_thang': {'pitch': 4, 'rate': 5},
    'mia_mai_cham_biem': {'pitch': 2, 'rate': -3},
    'met_moi_buong_xuoi': {'pitch': -5, 'rate': -8},
    'binh_than_tu_nhien': {'pitch': 0, 'rate': 0},
}

# Dialogue Cue Verbs & Regex
VERB_PATTERN = r'nói|bảo|hỏi|thưa|đáp|quát|than|mắng|hô|kêu|can|khen|thề|cười|nghĩ|thầm nghĩ|bàn|tâu|truyền|dặn|hét|nhủ|ngâm|vịnh'

DIALOGUE_CUE_REGEX = re.compile(
    r'(?P<lead>(?:^|[.!?\n]\s*)(?P<speaker>[A-ZÀ-Ỹ][a-zà-ỹ]+(?:\s+[A-ZÀ-Ỹa-zà-ỹ]+){0,3})\s+(?P<modifier>cả giận\s+|liền\s+|vội\s+|bèn\s+|lại\s+|mừng rỡ\s+|kinh hãi\s+|ngạc nhiên\s+|thầm\s+)?(?P<verb>' + VERB_PATTERN + r')(?:\s+lớn|\s+rằng|\s+mà\s+rằng)?\s*,\s*)(?P<quote>[A-ZÀ-Ỹ][^.!?\n]+(?:[.!?]+|\n|$))',
    re.UNICODE
)

# Poetry Lead-in Pattern
POEM_INTRO_RE = re.compile(
    r'(?P<intro>(?:Có bài từ rằng|Có bài phú rằng|Có thơ rằng|Có thơ khen rằng|Có thơ than rằng|Đó chính là|'
    r'Người sau có thơ rằng|Người sau có thơ khen rằng|Người sau có thơ than rằng|'
    r'Đời sau có thơ rằng|Đời sau có thơ khen rằng|Đời sau có thơ than rằng|'
    r'Sau này có thơ rằng|Sau này có thơ khen rằng|Sau này có thơ than rằng|'
    r'Bèn ngâm rằng|Ngâm rằng)\s*[,:]?\s*)$',
    re.IGNORECASE | re.UNICODE
)

# Contextual Scene Lexicons for Narrator (Section 1.6)
EPIC_KEYWORDS = [
    'chém', 'giết', 'đánh', 'xông vào', 'xông pha', 'xung phong', 'đại chiến', 'giáp chiến',
    'hai ngựa', 'đao', 'giáo', 'kích', 'trống trận', 'reo hò', 'dậy đất', 'tung hoành',
    'rượt đuổi', 'thừa thắng', 'đại phá', 'vung đao', 'phóng ngựa', 'một nhát', 'chém đứt',
    'rơi đầu', 'chém chết', 'đuổi theo', 'hỗn chiến', 'giao chiến', 'vây khốn', 'phá vây', 'ngã nhào'
]

ELEGIAC_KEYWORDS = [
    'chết thảm', 'tử trận', 'khóc than', 'than khóc', 'rơi lệ', 'gạt lệ', 'khóc lóc',
    'đau xót', 'thảm bại', 'máu chảy thành sông', 'ngậm ngùi', 'xót xa', 'bi ai', 'thống thiết',
    'trăn trối', 'thương tiếc', 'đau lòng', 'tự sát', 'oan uổng', 'tuyệt mệnh', 'thảm khốc'
]

SUSPENSE_KEYWORDS = [
    'mai phục', 'phục kích', 'nín thở', 'trong đêm', 'đêm tối', 'rình rập', 'dò xét',
    'thích khách', 'mưu kế bí mật', 'lẻn vào', 'âm thầm', 'cẩn mật', 'chờ đợi thời cơ',
    'bất thần', 'đánh úp', 'phóng hỏa', 'kín đáo', 'mật báo'
]

CONTEMPLATIVE_KEYWORDS = [
    'hồi thứ', 'hồi sau sẽ rõ', 'sự thể thế nào', 'chưa biết tính mạng', 'thế lớn trong thiên hạ',
    'tan lâu rồi lại họp', 'nhà chu suy yếu', 'hưng suy', 'được mất', 'muôn thuở', 'nghìn thu',
    'bài từ rằng', 'thơ khen rằng', 'thơ than rằng', 'đó chính là'
]

def classify_narrator_mode(text, p_idx=0, total_p=1, chunk_idx=1, total_chunks=1):
    low = text.lower()
    if text.strip() == '. ......':
        return 'contemplative'
    if any(k in low for k in CONTEMPLATIVE_KEYWORDS):
        return 'contemplative'
    if chunk_idx == 1 and p_idx == 0:
        return 'contemplative'
    if chunk_idx == total_chunks and p_idx >= total_p - 1:
        return 'contemplative'
    if any(k in low for k in ELEGIAC_KEYWORDS):
        return 'elegiac'
    if any(k in low for k in SUSPENSE_KEYWORDS):
        return 'suspense'
    if any(k in low for k in EPIC_KEYWORDS):
        return 'epic'
    return 'intimate'

def get_narrator_acoustic(narrator_mode, is_lead_in=False, is_poem_intro=False, is_pause=False):
    voice = "vi-VN-NamMinhNeural"
    if is_pause:
        return voice, "-2Hz", "-12%", "1.50s", "contemplative_narrator"
    if is_poem_intro:
        return voice, "-2Hz", "-12%", "0.85s", "contemplative_narrator"

    if narrator_mode == 'epic':
        pitch = "+1Hz"
        rate = "+0%"
        lead_in = "0.35s" if is_lead_in else "0.30s"
        timbre_eq = "epic_narrator"
    elif narrator_mode == 'elegiac':
        pitch = "-3Hz"
        rate = "-10%"
        lead_in = "0.60s" if is_lead_in else "0.65s"
        timbre_eq = "elegiac_narrator"
    elif narrator_mode == 'suspense':
        pitch = "+1Hz"
        rate = "-8%"
        lead_in = "0.45s" if is_lead_in else "0.40s"
        timbre_eq = "suspense_narrator"
    elif narrator_mode == 'contemplative':
        pitch = "-2Hz"
        rate = "-12%"
        lead_in = "0.70s"
        timbre_eq = "contemplative_narrator"
    else:
        pitch = "+0Hz"
        rate = "-5%"
        lead_in = "0.38s" if is_lead_in else "0.35s"
        timbre_eq = "intimate_narrator"

    return voice, pitch, rate, lead_in, timbre_eq

def resolve_character_timbre_eq(cid, gender, age_stage, temperament, emotion):
    if gender == 'female' or age_stage in ('au_tho', 'nien_thieu'):
        return 'youth_bright'
    if age_stage == 'lao_hoa':
        return 'aged_gravel'
    if temperament == 'xun_xoe_don_hen' or emotion == 'ninh_bo_van_xin':
        return 'servile_flatterer'
    if temperament == 'hach_dich_bao_nguoc':
        return 'tyrant_arrogant'
    if emotion in ('dau_don_trang_troi', 'bi_kich_uat_nghen'):
        return 'tragic_grief'
    if cid in ('Truong_Phi', 'Hua_Chu', 'Dien_Vi', 'Cam_Ninh', 'Bang_Duc', 'Nhan_Luong', 'Van_Xu') or (temperament == 'anh_hung_hao_sang' and emotion in ('cuong_no', 'hoan_ca_dac_thang')):
        return 'chest_resonance'
    if cid in ('Tao_Thao', 'Tu_Ma_Y', 'Tu_Ma_Su', 'Tu_Ma_Chieu', 'Chung_Hoi', 'Dong_Trac', 'Vien_Thuat', 'Ly_Nho', 'Truong_Nhuong', 'Doan_Khue') or temperament in ('giao_hoat_nham_hiem',):
        return 'sharp_cunning'
    if cid in ('Luu_Bi', 'Quan_Vu', 'Gia_Cat_Luong', 'Trieu_Van', 'Ton_Quyen', 'Lo_Tuc', 'Tu_Thu', 'Khuong_Duy', 'Ma_Sieu', 'Tuan_Uc') or temperament in ('trong_sang_thanh_thien', 'khac_kho_lanh_lung'):
        return 'warm_authority'
    return 'warm_authority' if temperament == 'anh_hung_hao_sang' else 'sharp_cunning'

def compute_contextual_handoff(prev_type, curr_type, curr_speaker, prev_speaker, verb, modifier, emotion):
    """
    Computes adaptive, intelligent theatrical handoff pause (lead_in_pause):
    - Instant / Interruption (0.30s - 0.35s): Heated argument, shouting, sudden intervention with safety cushion.
    - Urgent lead-in (0.35s - 0.40s): Sudden command / cry after narrator action.
    - Natural dialogue turn (0.42s - 0.50s): Standard conversational turn between characters.
    - Deliberate / Pensive / Solemn (0.60s - 0.85s): Thoughtful reply, sigh, royal court ceremony.
    - Dramatic silence / Shock (0.85s - 1.20s): Following shock, dying breath, or philosophical revelation.
    - Dialogue resonance (0.50s - 0.60s): After character finishes speaking before narrator continues.
    """
    mod = (modifier or "").lower()
    vb = (verb or "").lower()

    if prev_type == "narrator" and curr_type == "dialogue":
        if any(w in mod for w in ("cả giận", "kinh hãi", "vội")) or vb in ("quát", "thét", "hét", "hô"):
            return "0.35s"  # Sudden, urgent entry
        if any(w in mod for w in ("thở dài", "ngậm ngùi", "buông xuôi")) or vb in ("than", "khóc", "nghĩ", "thầm nghĩ"):
            return "0.65s"  # Pensive sigh before speech
        return "0.42s"  # Natural lead-in

    elif prev_type == "dialogue" and curr_type == "dialogue":
        if prev_speaker != curr_speaker:
            if emotion in ("cuong_no", "de_doa_tham_hiem") or vb in ("quát", "mắng", "cãi"):
                return "0.30s"  # Instant cutoff / interruption with safety cushion!
            if emotion in ("hoi_hop_thi_thao", "doc_thoai_dan_vat", "met_moi_buong_xuoi", "dau_don_trang_troi"):
                return "0.75s"  # Heavy emotional breath
            return "0.45s"  # Natural character turn
        else:
            return "0.32s"  # Same character pause between sentences

    elif prev_type == "dialogue" and curr_type == "narrator":
        return "0.55s"  # Resonance pause for character's words to sink in

    return "0.35s"

def resolve_character_identity(speaker_str, quote_str, chap_num):
    clean_sp = speaker_str.strip().lower()

    if clean_sp in ('người ấy', 'người kia', 'một người'):
        if 'trương phi' in quote_str.lower() or 'dực đức' in quote_str.lower():
            clean_sp = 'trương phi'
        elif 'quan vũ' in quote_str.lower() or 'vân trường' in quote_str.lower() or 'trương sinh' in quote_str.lower():
            clean_sp = 'quan vũ'
        elif 'lưu bị' in quote_str.lower() or 'huyền đức' in quote_str.lower():
            clean_sp = 'lưu bị'
        elif 'tào tháo' in quote_str.lower():
            clean_sp = 'tào tháo'

    cid = 'Unknown'
    cname = speaker_str.strip()
    gender = 'male'
    temp = 'anh_hung_hao_sang'

    if clean_sp in KNOWN_CHARACTERS:
        cid, cname, gender, temp = KNOWN_CHARACTERS[clean_sp]
    else:
        matched = None
        for k in sorted(KNOWN_CHARACTERS.keys(), key=lambda x: -len(x)):
            if k in clean_sp:
                matched = KNOWN_CHARACTERS[k]
                break
        if matched:
            cid, cname, gender, temp = matched
        else:
            cid = vn_to_ascii_id(speaker_str)
            cname = speaker_str.strip().title()
            if any(w in clean_sp for w in ('bà', 'mẹ', 'nàng', 'phu nhân', 'thái hậu', 'hoàng hậu', 'cơ', 'nữ', 'thị')):
                gender = 'female'
            else:
                gender = 'male'
            temp = 'anh_hung_hao_sang'

    if cid in ('Hoang_Trung', 'Nghiem_Nhan', 'Kieu_Huyen', 'Vuong_Doan', 'Lu_Thuc', 'Dinh_Nguyen'):
        age_stage = 'lao_hoa'
    elif cid in ('Gia_Cat_Luong', 'Tu_Ma_Y'):
        if chap_num <= 55:
            age_stage = 'thanh_xuan'
        elif chap_num <= 90:
            age_stage = 'trung_nien'
        else:
            age_stage = 'lao_hoa'
    elif cid in ('Luu_Thien', 'Tao_Phi', 'Tao_Thuc', 'Ton_Sach', 'Ton_Quyen', 'Chu_Du'):
        if chap_num <= 40:
            age_stage = 'thanh_xuan'
        elif chap_num <= 80:
            age_stage = 'trung_nien'
        else:
            age_stage = 'lao_hoa'
    else:
        if chap_num <= 25:
            age_stage = 'thanh_xuan'
        elif chap_num <= 75:
            age_stage = 'trung_nien'
        else:
            age_stage = 'lao_hoa'

    return cid, cname, gender, age_stage, temp

def detect_emotion(modifier_str, verb_str, quote_str):
    mod = (modifier_str or '').lower()
    vb = (verb_str or '').lower()
    qt = quote_str.lower()

    if 'giận' in mod or vb in ('quát', 'mắng', 'hét') or 'láo quá' in qt or 'ngươi dám' in qt or 'giết' in qt:
        return 'cuong_no'
    if 'mừng' in mod or vb == 'cười' or 'tốt lắm' in qt or 'hả dạ' in qt or 'thắng rồi' in qt:
        return 'hoan_ca_dac_thang'
    if vb in ('than', 'khóc') or 'khóc' in mod or 'ngậm ngùi' in mod or 'ôi' in qt or 'tiếc thay' in qt:
        return 'dau_don_trang_troi'
    if 'kinh' in mod or 'sợ' in mod or 'bàng hoàng' in mod:
        return 'bang_hoang_chet_lang'
    if 'đe dọa' in mod or 'gằn' in mod:
        return 'de_doa_tham_hiem'
    if 'van' in mod or 'lạy' in mod:
        return 'ninh_bo_van_xin'
    if 'thì thào' in mod or 'rỉ tai' in mod or 'thầm' in mod:
        return 'hoi_hop_thi_thao'
    if 'thở dài' in mod or 'buông xuôi' in mod:
        return 'met_moi_buong_xuoi'
    return 'binh_than_tu_nhien'

def compute_acoustic_tone(age_stage, temperament, emotion, gender):
    base_age = AGE_ACOUSTIC.get(age_stage, AGE_ACOUSTIC['thanh_xuan'])
    d_temp = TEMPERAMENT_DELTAS.get(temperament, TEMPERAMENT_DELTAS['anh_hung_hao_sang'])
    d_emo = EMOTION_DELTAS.get(emotion, EMOTION_DELTAS['binh_than_tu_nhien'])

    p_val = base_age['pitch'] + d_temp['pitch'] + d_emo['pitch']
    r_val = base_age['rate'] + d_temp['rate'] + d_emo['rate']

    p_val = max(-10, min(12, p_val))
    r_val = max(-25, min(20, r_val))

    p_str = f"+{p_val}Hz" if p_val > 0 else (f"{p_val}Hz" if p_val < 0 else "+0Hz")
    r_str = f"+{r_val}%" if r_val > 0 else (f"{r_val}%" if r_val < 0 else "+0%")
    voice = "vi-VN-HoaiMyNeural" if gender == "female" else "vi-VN-NamMinhNeural"

    return voice, p_str, r_str

def direct_chapter_theatrical_script(chap_dir, chap_idx=1, chap_title=""):
    kb_dir = os.path.join(chap_dir, "kich-ban")
    if not os.path.isdir(kb_dir):
        return None

    kb_files = sorted(
        glob.glob(os.path.join(kb_dir, "Kich-ban-*.txt")),
        key=lambda x: int(re.search(r'Kich-ban-(\d+)\.txt', x).group(1)) if re.search(r'Kich-ban-(\d+)\.txt', x) else 0
    )

    if not kb_files:
        return None

    total_chunks = len(kb_files)
    theatrical_lines = []
    character_bible = {
        "Narrator": {
            "name": "Người dẫn chuyện",
            "gender": "male",
            "voice": "vi-VN-NamMinhNeural",
            "base_pitch": "+0Hz",
            "base_rate": "-5%",
            "narrative_modes": set(),
            "dialogue_count": 0
        }
    }

    line_id = 1
    total_dialogues = 0
    total_narrators = 0
    total_poems = 0

    for chunk_idx, f_path in enumerate(kb_files, 1):
        with open(f_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Isolate . ...... into its own standalone blocks
        clean_content = re.sub(r'(\. \.\.\.\.\.\.)', r'\n\n\1\n\n', content)
        raw_paragraphs = [p.strip() for p in clean_content.split("\n\n") if p.strip()]
        total_p = len(raw_paragraphs)

        expecting_poem = False

        for p_idx, p in enumerate(raw_paragraphs):
            # 1. Standalone Dramatic Pause
            if p == ". ......":
                v, pt, rt, lp, teq = get_narrator_acoustic('contemplative', is_pause=True)
                theatrical_lines.append({
                    "line_id": line_id,
                    "chunk_id": chunk_idx,
                    "type": "narrator",
                    "speaker": "Narrator",
                    "narrative_mode": "contemplative",
                    "text": ". ......",
                    "voice": v,
                    "pitch": pt,
                    "rate": rt,
                    "lead_in_pause": lp,
                    "timbre_eq": teq
                })
                character_bible["Narrator"]["narrative_modes"].add("contemplative")
                line_id += 1
                total_narrators += 1
                continue

            # 2. Check for Poetry Lead-in Pattern at paragraph end
            m_intro = POEM_INTRO_RE.search(p)
            if m_intro:
                before_intro = p[:m_intro.start()].strip()
                intro_text = m_intro.group('intro').strip()

                # If there was prose/dialogue before the intro in this paragraph
                if before_intro:
                    m_d = list(DIALOGUE_CUE_REGEX.finditer(before_intro))
                    if not m_d:
                        m_mode = classify_narrator_mode(before_intro, p_idx, total_p, chunk_idx, total_chunks)
                        v, pt, rt, lp, teq = get_narrator_acoustic(m_mode)
                        theatrical_lines.append({
                            "line_id": line_id,
                            "chunk_id": chunk_idx,
                            "type": "narrator",
                            "speaker": "Narrator",
                            "narrative_mode": m_mode,
                            "text": before_intro,
                            "voice": v,
                            "pitch": pt,
                            "rate": rt,
                            "lead_in_pause": lp,
                            "timbre_eq": teq
                        })
                        character_bible["Narrator"]["narrative_modes"].add(m_mode)
                        line_id += 1
                        total_narrators += 1
                    else:
                        # Parse dialogue inside before_intro
                        last_pos = 0
                        for m_sub in m_d:
                            b_lead = before_intro[last_pos:m_sub.start()].strip()
                            l_txt = m_sub.group("lead").strip()
                            q_txt = m_sub.group("quote").strip()
                            sp_raw = m_sub.group("speaker").strip()
                            mod_s = m_sub.group("modifier") or ""
                            vb_s = m_sub.group("verb")

                            n_lead = (b_lead + " " + l_txt).strip() if b_lead else l_txt
                            if n_lead:
                                v, pt, rt, lp, teq = get_narrator_acoustic("intimate", is_lead_in=True)
                                theatrical_lines.append({
                                    "line_id": line_id,
                                    "chunk_id": chunk_idx,
                                    "type": "narrator",
                                    "speaker": "Narrator",
                                    "narrative_mode": "intimate",
                                    "text": n_lead,
                                    "voice": v,
                                    "pitch": pt,
                                    "rate": rt,
                                    "lead_in_pause": lp,
                                    "timbre_eq": teq
                                })
                                character_bible["Narrator"]["narrative_modes"].add("intimate")
                                line_id += 1
                                total_narrators += 1

                            cid, cname, gender, age_stage, temp = resolve_character_identity(sp_raw, q_txt, chap_idx)
                            emotion = detect_emotion(mod_s, vb_s, q_txt)
                            voice, pitch, rate = compute_acoustic_tone(age_stage, temp, emotion, gender)
                            char_timbre = resolve_character_timbre_eq(cid, gender, age_stage, temp, emotion)

                            prev_type = theatrical_lines[-1]["type"] if theatrical_lines else "narrator"
                            prev_sp = theatrical_lines[-1]["speaker"] if theatrical_lines else "Narrator"
                            d_lead_in = compute_contextual_handoff(prev_type, "dialogue", cid, prev_sp, vb_s, mod_s, emotion)

                            theatrical_lines.append({
                                "line_id": line_id,
                                "chunk_id": chunk_idx,
                                "type": "dialogue",
                                "speaker": cid,
                                "character_name": cname,
                                "text": q_txt,
                                "age_stage": age_stage,
                                "temperament": temp,
                                "emotion": emotion,
                                "voice": voice,
                                "pitch": pitch,
                                "rate": rate,
                                "lead_in_pause": d_lead_in,
                                "timbre_eq": char_timbre
                            })
                            line_id += 1
                            total_dialogues += 1
                            last_pos = m_sub.end()

                            if cid not in character_bible:
                                character_bible[cid] = {
                                    "name": cname,
                                    "gender": gender,
                                    "voice": voice,
                                    "age_stage": age_stage,
                                    "temperament": temp,
                                    "timbre_eq": char_timbre,
                                    "sample_emotions": [emotion],
                                    "dialogue_count": 1
                                }
                            else:
                                character_bible[cid]["dialogue_count"] += 1
                                if emotion not in character_bible[cid]["sample_emotions"]:
                                    character_bible[cid]["sample_emotions"].append(emotion)

                        tail = before_intro[last_pos:].strip()
                        if tail:
                            v, pt, rt, lp, teq = get_narrator_acoustic("intimate")
                            theatrical_lines.append({
                                "line_id": line_id,
                                "chunk_id": chunk_idx,
                                "type": "narrator",
                                "speaker": "Narrator",
                                "narrative_mode": "intimate",
                                "text": tail,
                                "voice": v,
                                "pitch": pt,
                                "rate": rt,
                                "lead_in_pause": "0.35s",
                                "timbre_eq": teq
                            })
                            character_bible["Narrator"]["narrative_modes"].add("intimate")
                            line_id += 1
                            total_narrators += 1

                # Now append the poem intro line
                v, pt, rt, lp, teq = get_narrator_acoustic('contemplative', is_poem_intro=True)
                theatrical_lines.append({
                    "line_id": line_id,
                    "chunk_id": chunk_idx,
                    "type": "narrator",
                    "speaker": "Narrator",
                    "narrative_mode": "contemplative",
                    "text": intro_text,
                    "voice": v,
                    "pitch": pt,
                    "rate": rt,
                    "lead_in_pause": lp,
                    "timbre_eq": teq
                })
                character_bible["Narrator"]["narrative_modes"].add("contemplative")
                line_id += 1
                total_narrators += 1

                expecting_poem = True
                continue

            # 3. Dedicated Poem Verse Extraction (Rule 4 Poetic Engine)
            if expecting_poem:
                sublines = [l.strip() for l in p.splitlines() if l.strip()]
                for verse_line in sublines:
                    # Ensure terminal punctuation on verse
                    if not verse_line.endswith(('.', '!', '?', ',', ';', ':')):
                        verse_line += ','

                    theatrical_lines.append({
                        "line_id": line_id,
                        "chunk_id": chunk_idx,
                        "type": "poem",
                        "speaker": "Narrator",
                        "text": verse_line,
                        "voice": "vi-VN-NamMinhNeural",
                        "pitch": "-2Hz",
                        "rate": "-18%",
                        "lead_in_pause": "0.85s",
                        "timbre_eq": "poetic_recitation"
                    })
                    line_id += 1
                    total_poems += 1

                expecting_poem = False
                continue

            # 4. Standard Dialogue / Narrative Flow
            macro_mode = classify_narrator_mode(p, p_idx, total_p, chunk_idx, total_chunks)

            matches = list(DIALOGUE_CUE_REGEX.finditer(p))
            if not matches:
                v, pt, rt, lp, teq = get_narrator_acoustic(macro_mode)
                theatrical_lines.append({
                    "line_id": line_id,
                    "chunk_id": chunk_idx,
                    "type": "narrator",
                    "speaker": "Narrator",
                    "narrative_mode": macro_mode,
                    "text": p,
                    "voice": v,
                    "pitch": pt,
                    "rate": rt,
                    "lead_in_pause": lp,
                    "timbre_eq": teq
                })
                character_bible["Narrator"]["narrative_modes"].add(macro_mode)
                line_id += 1
                total_narrators += 1
            else:
                last_pos = 0
                for m_idx, m in enumerate(matches):
                    before_lead = p[last_pos:m.start()].strip()
                    lead_text = m.group("lead").strip()
                    quote_text = m.group("quote").strip()
                    speaker_raw = m.group("speaker").strip()
                    modifier = m.group("modifier") or ""
                    verb = m.group("verb")

                    narrator_chunk = (before_lead + " " + lead_text).strip() if before_lead else lead_text
                    if narrator_chunk:
                        v, pt, rt, lp, teq = get_narrator_acoustic(macro_mode, is_lead_in=True)
                        theatrical_lines.append({
                            "line_id": line_id,
                            "chunk_id": chunk_idx,
                            "type": "narrator",
                            "speaker": "Narrator",
                            "narrative_mode": macro_mode,
                            "text": narrator_chunk,
                            "voice": v,
                            "pitch": pt,
                            "rate": rt,
                            "lead_in_pause": lp,
                            "timbre_eq": teq
                        })
                        character_bible["Narrator"]["narrative_modes"].add(macro_mode)
                        line_id += 1
                        total_narrators += 1

                    cid, cname, gender, age_stage, temp = resolve_character_identity(speaker_raw, quote_text, chap_idx)
                    emotion = detect_emotion(modifier, verb, quote_text)
                    voice, pitch, rate = compute_acoustic_tone(age_stage, temp, emotion, gender)
                    char_timbre_eq = resolve_character_timbre_eq(cid, gender, age_stage, temp, emotion)

                    prev_type = theatrical_lines[-1]["type"] if theatrical_lines else "narrator"
                    prev_sp = theatrical_lines[-1]["speaker"] if theatrical_lines else "Narrator"
                    d_lead_in = compute_contextual_handoff(prev_type, "dialogue", cid, prev_sp, verb, modifier, emotion)

                    theatrical_lines.append({
                        "line_id": line_id,
                        "chunk_id": chunk_idx,
                        "type": "dialogue",
                        "speaker": cid,
                        "character_name": cname,
                        "text": quote_text,
                        "age_stage": age_stage,
                        "temperament": temp,
                        "emotion": emotion,
                        "voice": voice,
                        "pitch": pitch,
                        "rate": rate,
                        "lead_in_pause": d_lead_in,
                        "timbre_eq": char_timbre_eq
                    })
                    line_id += 1
                    total_dialogues += 1
                    last_pos = m.end()

                    if cid not in character_bible:
                        character_bible[cid] = {
                            "name": cname,
                            "gender": gender,
                            "voice": voice,
                            "age_stage": age_stage,
                            "temperament": temp,
                            "timbre_eq": char_timbre_eq,
                            "sample_emotions": [emotion],
                            "dialogue_count": 1
                        }
                    else:
                        character_bible[cid]["dialogue_count"] += 1
                        if emotion not in character_bible[cid]["sample_emotions"]:
                            character_bible[cid]["sample_emotions"].append(emotion)

                rest_p = p[last_pos:].strip()
                if rest_p:
                    v, pt, rt, lp, teq = get_narrator_acoustic(macro_mode)
                    lead_in_res = "0.55s" if (theatrical_lines and theatrical_lines[-1]["text"].endswith(("!", "?"))) else "0.45s"
                    theatrical_lines.append({
                        "line_id": line_id,
                        "chunk_id": chunk_idx,
                        "type": "narrator",
                        "speaker": "Narrator",
                        "narrative_mode": macro_mode,
                        "text": rest_p,
                        "voice": v,
                        "pitch": pt,
                        "rate": rt,
                        "lead_in_pause": lead_in_res,
                        "timbre_eq": teq
                    })
                    character_bible["Narrator"]["narrative_modes"].add(macro_mode)
                    line_id += 1
                    total_narrators += 1

    character_bible["Narrator"]["dialogue_count"] = total_narrators
    character_bible["Narrator"]["narrative_modes"] = sorted(list(character_bible["Narrator"]["narrative_modes"]))

    theatrical_script_path = os.path.join(chap_dir, "theatrical_script.json")
    with open(theatrical_script_path, "w", encoding="utf-8") as f:
        json.dump(theatrical_lines, f, indent=2, ensure_ascii=False)

    bible_meta = {
        "chapter_folder": os.path.basename(chap_dir),
        "chapter_index": chap_idx,
        "chapter_title": chap_title,
        "genre": "classical_epic_literature",
        "total_theatrical_lines": len(theatrical_lines),
        "narrator_lines": total_narrators,
        "poem_lines": total_poems,
        "dialogue_lines": total_dialogues,
        "characters_cast_count": len(character_bible) - 1,
        "characters": character_bible,
        "directed_at": datetime.datetime.now().isoformat()
    }
    bible_path = os.path.join(chap_dir, ".theatrical_bible.json")
    with open(bible_path, "w", encoding="utf-8") as f:
        json.dump(bible_meta, f, indent=2, ensure_ascii=False)

    return {
        "theatrical_script_file": theatrical_script_path,
        "theatrical_bible_file": bible_path,
        "total_lines": len(theatrical_lines),
        "narrator_lines": total_narrators,
        "poem_lines": total_poems,
        "dialogue_lines": total_dialogues,
        "characters_count": len(character_bible) - 1
    }

def direct_book_theatrical_scripts(book_dir, chapter_filter=None, from_chap=None, to_chap=None):
    manifest_path = os.path.join(book_dir, ".session_manifest.json")
    manifest = {}
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

    chapters = manifest.get("chapters", [])
    if not chapters:
        subdirs = sorted([d for d in os.listdir(book_dir) if os.path.isdir(os.path.join(book_dir, d)) and not d.startswith('.')])
        chapters = [{"index": idx, "folder": d, "title": d} for idx, d in enumerate(subdirs)]
        manifest["chapters"] = chapters

    print(f"[*] Starting Step 08A Theatrical Voice & Casting Direction in {book_dir}...")
    processed_count = 0
    total_dialogues_book = 0
    total_poems_book = 0
    total_lines_book = 0
    unique_characters_book = set()
    report_rows = []

    for i, chap in enumerate(chapters, 1):
        chap_num = chap.get("index", i - 1) + 1
        folder_name = chap["folder"]

        if chapter_filter and folder_name != chapter_filter and str(chap_num) != str(chapter_filter):
            continue
        if from_chap and chap_num < from_chap:
            continue
        if to_chap and chap_num > to_chap:
            continue

        chap_dir = os.path.join(book_dir, folder_name)
        if not os.path.exists(chap_dir):
            continue

        res = direct_chapter_theatrical_script(chap_dir, chap_num, chap.get("title", folder_name))
        if not res:
            print(f"    [!] {folder_name}: No script chunks found in kich-ban/.")
            continue

        processed_count += 1
        total_dialogues_book += res["dialogue_lines"]
        total_poems_book += res["poem_lines"]
        total_lines_book += res["total_lines"]

        with open(res["theatrical_bible_file"], "r", encoding="utf-8") as bf:
            b_data = json.load(bf)
            for c_id in b_data.get("characters", {}):
                if c_id != "Narrator":
                    unique_characters_book.add(c_id)

        chap["step_8a_status"] = "completed"
        chap["theatrical_script_file"] = os.path.relpath(res["theatrical_script_file"], book_dir)
        chap["theatrical_bible_file"] = os.path.relpath(res["theatrical_bible_file"], book_dir)
        chap["total_theatrical_lines"] = res["total_lines"]
        chap["total_poem_lines"] = res["poem_lines"]
        chap["total_dialogue_lines"] = res["dialogue_lines"]
        chap["total_characters_cast"] = res["characters_count"]

        report_rows.append(
            f"| {chap_num:03d} | [`{folder_name}`](file://{res['theatrical_script_file']}) | {res['total_lines']} | {res['narrator_lines']} | {res['dialogue_lines']} | {res['poem_lines']} | {res['characters_count']} | ✅ COMPLETED |"
        )
        print(f"    -> [✓] {folder_name}: {res['total_lines']} lines ({res['dialogue_lines']} dialogues | {res['poem_lines']} poems | {res['characters_count']} characters cast)")

    manifest["pipeline_stage"] = "08a_theatrical_directed"
    manifest["step_8a_status"] = "completed"
    manifest["theatrical_characters_total"] = len(unique_characters_book)
    manifest["theatrical_dialogues_total"] = total_dialogues_book
    manifest["theatrical_poems_total"] = total_poems_book
    manifest["updated_at"] = datetime.datetime.now().isoformat()

    tmp_path = manifest_path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    os.replace(tmp_path, manifest_path)

    master_report_path = os.path.join(book_dir, "Master_Theatrical_Report.md")
    master_lines = [
        f"# BÁO CÁO ĐẠO DIỄN KỊCH NGHỆ & PHÂN VAI (MASTER THEATRICAL REPORT)",
        f"## Tác phẩm: {manifest.get('book_title', os.path.basename(book_dir))}",
        f"**Tổng số Hồi đã đạo diễn:** {processed_count}/{len(chapters)}",
        f"**Tổng số câu kịch bản phân vai:** {total_lines_book:,} lines",
        f"**Tổng số câu thoại nhân vật (Dialogue):** {total_dialogues_book:,} lines",
        f"**Tổng số câu ngâm thơ (Poem):** {total_poems_book:,} lines",
        f"**Tổng số nhân vật được tạo hồ sơ giọng đọc:** {len(unique_characters_book)} nhân vật",
        f"**Thời điểm hoàn thành:** `{datetime.datetime.now().isoformat()}`\n",
        "| Hồi | Thư Mục | Tổng Số Câu | Lời Dẫn | Lời Thoại | Ngâm Thơ | Số Nhân Vật | Trạng Thái Bước 08A |",
        "| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |"
    ]
    master_lines.extend(report_rows)
    master_lines.append("\n---\n*Kịch bản phân vai và hồ sơ âm học xuất bản tự động bởi Chief Theatrical Voice & Casting Director (Step 08A)*")

    with open(master_report_path, "w", encoding="utf-8") as mf:
        mf.write("\n".join(master_lines))

    print(f"\n======================================================================")
    print(f"[✓] STEP 08A COMPLETE: Directed {processed_count} chapters | {total_dialogues_book:,} dialogues | {total_poems_book:,} poems | {len(unique_characters_book)} characters")
    print(f"[*] Master Report: {master_report_path}")
    print(f"[*] Session manifest updated: {manifest_path}")
    print(f"======================================================================")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Step 08A: Chief Theatrical Voice & Casting Director")
    parser.add_argument("--book_dir", default="Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia", help="Book directory path")
    parser.add_argument("--chapter", default=None, help="Specific chapter folder or index")
    parser.add_argument("--from_chap", type=int, default=None, help="Start chapter index")
    parser.add_argument("--to_chap", type=int, default=None, help="End chapter index")
    args = parser.parse_args()

    direct_book_theatrical_scripts(args.book_dir, args.chapter, args.from_chap, args.to_chap)
