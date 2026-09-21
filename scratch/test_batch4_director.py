import os, sys, glob, re, json

TITLES = [
    'Thái úy ', 'Thượng thư ', 'Thị trung ', 'Thị Trung ', 'Trưởng sử ',
    'Tham quân ', 'Tham quan ', 'Thái phó ', 'Tư đồ ', 'Tây tào duyện ',
    'Hoàng môn thị lang ', 'Hữu tướng quân ', 'Long Nhương tướng quân ',
    'Đô đốc ', 'Đại tư mã ', 'Đại tướng quân ', 'Phụ quốc tướng quân ',
    'Thái thú ', 'Thái thường khanh là ', 'Quang lộc đại phu là ',
    'Lão tướng là ', 'Hộ vệ là ', 'Thuật sĩ là ', 'Con là '
]

POSTURE_ACTIONS = [
    'đứng dậy', 'ngồi xuống', 'quỳ xuống', 'sụp lạy', 'bước ra', 'bước vào', 'tiến lên', 'lùi lại',
    'ngoảnh lại', 'quay lại', 'ngẩng đầu', 'cúi đầu', 'chắp tay', 'vung tay', 'rút gươm', 'tuốt gươm',
    'chỉ tay', 'chống kiếm', 'chống gươm', 'khoanh tay', 'vỗ bàn', 'đập bàn', 'nhìn quanh', 'ngó trước ngó sau',
    'nín thở', 'thở dài', 'lắc đầu', 'gật đầu', 'vuốt râu', 'vẫy tay', 'trỏ gươm quát', 'trỏ gươm', 'vùng đứng dậy',
    'ngẩng mặt lên', 'ra ban', 'chưa kịp', 'ra ngựa', 'vào chầu', 'lạy tạ', 'lạy', 'mời vào', 'cũng khóc mà',
    'trông thấy', 'thầm khóc vang lên', 'khóc vang lên', 'thầm khóc', 'cầm giáo trỏ'
]

EMOTION_MODIFIERS_EXTRA = [
    'cả giận', 'nổi giận', 'giận dữ', 'mừng rỡ', 'hớn hở', 'kinh hãi', 'hoảng sợ', 'ngạc nhiên',
    'bàng hoàng', 'ngậm ngùi', 'buồn rầu', 'xót xa', 'thống thiết', 'nghi ngờ', 'thầm nghĩ',
    'mừng lắm', 'mừng', 'khóc', 'thất kinh'
]

ADVERBS_EXTRA = [
    'lại', 'bèn', 'liền', 'vội', 'chợt', 'thong thả', 'từ từ', 'nghiêm giọng', 'lớn tiếng',
    'gằn giọng', 'hạ giọng', 'thì thào', 'thong dong', 'bực tức', 'cười', 'cũng', 'mới'
]

FALSE_SPEAKERS = {
    'lại', 'đây', 'thì họ', 'trong hịch', 'trong thư', 'trong sớ', 'có thơ', 'có bài từ',
    'người sau có thơ', 'đời sau có thơ', 'sau này có thơ', 'cả nhà kinh hoàng',
    'mấy sào dặm lá', 'thư', 'cha nàng thường', 'họ'
}

def clean_speaker_and_posture_v2(sp_raw, mod_raw=""):
    clean_sp = sp_raw.strip()
    extracted_posture = []
    combined_mod = (mod_raw or "").strip()

    # Strip prefixes/titles first
    for t in TITLES:
        if clean_sp.lower().startswith(t.lower()):
            clean_sp = clean_sp[len(t):].strip()
            break

    changed = True
    while changed:
        changed = False
        lower_sp = clean_sp.lower()
        for act in sorted(POSTURE_ACTIONS, key=len, reverse=True):
            if lower_sp.endswith(" " + act):
                posture_part = clean_sp[len(clean_sp) - len(act):].strip()
                clean_sp = clean_sp[:-len(act)].strip()
                extracted_posture.insert(0, posture_part)
                changed = True
                break
        if changed:
            continue
        for adv in sorted(ADVERBS_EXTRA + EMOTION_MODIFIERS_EXTRA, key=len, reverse=True):
            if lower_sp.endswith(" " + adv):
                adv_part = clean_sp[len(clean_sp) - len(adv):].strip()
                clean_sp = clean_sp[:-len(adv)].strip()
                combined_mod = (adv_part + " " + combined_mod).strip()
                changed = True
                break

    posture_action = " ".join(extracted_posture)
    return clean_sp, posture_action, combined_mod

print('clean_speaker_and_posture_v2 defined.')

VERB_PATTERN = r'nói|bảo|hỏi|thưa|đáp|quát|than|mắng|hô|kêu|can|khen|thề|cười|nghĩ|thầm nghĩ|bàn|tâu|truyền|dặn|hét|nhủ|ngâm|vịnh'

DIALOGUE_CUE_REGEX = re.compile(
    r'(?P<lead>(?:^|[.!?\n]\s*)(?P<speaker>[A-ZÀ-Ỹ][a-zà-ỹ]+(?:\s+[A-ZÀ-Ỹa-zà-ỹ]+){0,4})\s+(?P<modifier>cả giận\s+|liền\s+|vội\s+|bèn\s+|lại\s+|mừng rỡ\s+|kinh hãi\s+|ngạc nhiên\s+|thầm\s+)?(?P<verb>' + VERB_PATTERN + r')(?:\s+lớn|\s+rằng|\s+mà\s+rằng)?\s*,\s*)(?P<quote>[A-ZÀ-Ỹ][^.!?\n]+(?:[.!?]+|\n|$))',
    re.UNICODE
)

KNOWN_CHARS_V2 = {
    # Thục Hán (Shu)
    'gia cát lượng': ('Gia_Cat_Luong', 'Gia Cát Lượng', 'male', 'khac_kho_lanh_lung'),
    'khổng minh': ('Gia_Cat_Luong', 'Gia Cát Lượng', 'male', 'khac_kho_lanh_lung'),
    'lượng': ('Gia_Cat_Luong', 'Gia Cát Lượng', 'male', 'khac_kho_lanh_lung'),
    'khương duy': ('Khuong_Duy', 'Khương Duy', 'male', 'anh_hung_hao_sang'),
    'bá ước': ('Khuong_Duy', 'Khương Duy', 'male', 'anh_hung_hao_sang'),
    'duy': ('Khuong_Duy', 'Khương Duy', 'male', 'anh_hung_hao_sang'),
    'ngụy diên': ('Nguy_Dien', 'Ngụy Diên', 'male', 'hach_dich_bao_nguoc'),
    'diên': ('Nguy_Dien', 'Ngụy Diên', 'male', 'hach_dich_bao_nguoc'),
    'triệu vân': ('Trieu_Van', 'Triệu Vân', 'male', 'anh_hung_hao_sang'),
    'tử long': ('Trieu_Van', 'Triệu Vân', 'male', 'anh_hung_hao_sang'),
    'quan hưng': ('Quan_Hung', 'Quan Hưng', 'male', 'anh_hung_hao_sang'),
    'hưng': ('Quan_Hung', 'Quan Hưng', 'male', 'anh_hung_hao_sang'),
    'trương bào': ('Truong_Bao_Shu', 'Trương Bào', 'male', 'anh_hung_hao_sang'),
    'bào': ('Truong_Bao_Shu', 'Trương Bào', 'male', 'anh_hung_hao_sang'),
    'vương bình': ('Vuong_Binh', 'Vương Bình', 'male', 'anh_hung_hao_sang'),
    'bình': ('Vuong_Binh', 'Vương Bình', 'male', 'anh_hung_hao_sang'),
    'mã tốc': ('Ma_Toc', 'Mã Tốc', 'male', 'tram_uat_dan_vat'),
    'tốc': ('Ma_Toc', 'Mã Tốc', 'male', 'tram_uat_dan_vat'),
    'mã đại': ('Ma_Dai', 'Mã Đại', 'male', 'anh_hung_hao_sang'),
    'lưu thiền': ('Luu_Thien', 'Lưu Thiền', 'male', 'xun_xoe_don_hen'),
    'hậu chủ': ('Luu_Thien', 'Lưu Thiền', 'male', 'xun_xoe_don_hen'),
    'thiền': ('Luu_Thien', 'Lưu Thiền', 'male', 'xun_xoe_don_hen'),
    'phí vĩ': ('Phi_Vi', 'Phí Vĩ', 'male', 'trong_sang_thanh_thien'),
    'vĩ': ('Phi_Vi', 'Phí Vĩ', 'male', 'trong_sang_thanh_thien'),
    'dương nghi': ('Duong_Nghi', 'Dương Nghi', 'male', 'tram_uat_dan_vat'),
    'nghi': ('Duong_Nghi', 'Dương Nghi', 'male', 'tram_uat_dan_vat'),
    'tưởng uyển': ('Tuong_Uyen', 'Tưởng Uyển', 'male', 'trong_sang_thanh_thien'),
    'trương dực': ('Truong_Duc', 'Trương Dực', 'male', 'anh_hung_hao_sang'),
    'dực': ('Truong_Duc', 'Trương Dực', 'male', 'anh_hung_hao_sang'),
    'liêu hóa': ('Lieu_Hoa', 'Liêu Hóa', 'male', 'anh_hung_hao_sang'),
    'hóa': ('Lieu_Hoa', 'Liêu Hóa', 'male', 'anh_hung_hao_sang'),
    'hoa': ('Lieu_Hoa', 'Liêu Hóa', 'male', 'anh_hung_hao_sang'),
    'đặng chi': ('Dang_Chi', 'Đặng Chi', 'male', 'trong_sang_thanh_thien'),
    'chi': ('Dang_Chi', 'Đặng Chi', 'male', 'trong_sang_thanh_thien'),
    'trần thức': ('Tran_Thuc', 'Trần Thức', 'male', 'anh_hung_hao_sang'),
    'thức': ('Tran_Thuc', 'Trần Thức', 'male', 'anh_hung_hao_sang'),
    'phó thiêm': ('Pho_Thiem', 'Phó Thiêm', 'male', 'anh_hung_hao_sang'),
    'thiêm': ('Pho_Thiem', 'Phó Thiêm', 'male', 'anh_hung_hao_sang'),
    'tưởng thư': ('Tuong_Thu', 'Tưởng Thư', 'male', 'xun_xoe_don_hen'),
    'thư': ('Tuong_Thu', 'Tưởng Thư', 'male', 'xun_xoe_don_hen'),
    'gia cát chiêm': ('Gia_Cat_Chiem', 'Gia Cát Chiêm', 'male', 'trong_sang_thanh_thien'),
    'chiêm': ('Gia_Cat_Chiem', 'Gia Cát Chiêm', 'male', 'trong_sang_thanh_thien'),
    'đổng quyết': ('Dong_Quyet', 'Đổng Quyết', 'male', 'trong_sang_thanh_thien'),
    'quyết': ('Dong_Quyet', 'Đổng Quyết', 'male', 'trong_sang_thanh_thien'),
    'lưu thầm': ('Luu_Tham', 'Lưu Thầm', 'male', 'bi_kich_uat_nghen'),
    'thầm': ('Luu_Tham', 'Lưu Thầm', 'male', 'bi_kich_uat_nghen'),
    'thôi phu nhân': ('Thoi_Phu_Nhan', 'Thôi Phu Nhân', 'female', 'bi_kich_uat_nghen'),
    'khước chính': ('Khuoc_Chinh', 'Khước Chính', 'male', 'trong_sang_thanh_thien'),
    'chính': ('Khuoc_Chinh', 'Khước Chính', 'male', 'trong_sang_thanh_thien'),
    'tiêu chu': ('Tieu_Chu', 'Tiêu Chu', 'male', 'khac_kho_lanh_lung'),
    'phàn kiến': ('Phan_Kien', 'Phàn Kiến', 'male', 'trong_sang_thanh_thien'),
    'cẩu an': ('Cau_An', 'Cẩu An', 'male', 'xun_xoe_don_hen'),
    'đổng doãn': ('Dong_Doan', 'Đổng Doãn', 'male', 'trong_sang_thanh_thien'),

    # Tào Ngụy & Tây Tấn (Wei & Jin)
    'tư mã ý': ('Tu_Ma_Y', 'Tư Mã Ý', 'male', 'giao_hoat_nham_hiem'),
    'trọng đạt': ('Tu_Ma_Y', 'Tư Mã Ý', 'male', 'giao_hoat_nham_hiem'),
    'đạt': ('Tu_Ma_Y', 'Tư Mã Ý', 'male', 'giao_hoat_nham_hiem'),
    'tư mã sư': ('Tu_Ma_Su', 'Tư Mã Sư', 'male', 'giao_hoat_nham_hiem'),
    'sư': ('Tu_Ma_Su', 'Tư Mã Sư', 'male', 'giao_hoat_nham_hiem'),
    'tư mã chiêu': ('Tu_Ma_Chieu', 'Tư Mã Chiêu', 'male', 'giao_hoat_nham_hiem'),
    'chiêu': ('Tu_Ma_Chieu', 'Tư Mã Chiêu', 'male', 'giao_hoat_nham_hiem'),
    'tư mã viêm': ('Tu_Ma_Viem', 'Tư Mã Viêm', 'male', 'anh_hung_hao_sang'),
    'viêm': ('Tu_Ma_Viem', 'Tư Mã Viêm', 'male', 'anh_hung_hao_sang'),
    'tấn chủ': ('Tu_Ma_Viem', 'Tư Mã Viêm', 'male', 'anh_hung_hao_sang'),
    'tư mã vọng': ('Tu_Ma_Vong', 'Tư Mã Vọng', 'male', 'anh_hung_hao_sang'),
    'vọng': ('Tu_Ma_Vong', 'Tư Mã Vọng', 'male', 'anh_hung_hao_sang'),
    'tào chân': ('Tao_Chan', 'Tào Chân', 'male', 'hach_dich_bao_nguoc'),
    'tử đan': ('Tao_Chan', 'Tào Chân', 'male', 'hach_dich_bao_nguoc'),
    'chân': ('Tao_Chan', 'Tào Chân', 'male', 'hach_dich_bao_nguoc'),
    'tào duệ': ('Tao_Due', 'Tào Duệ', 'male', 'khac_kho_lanh_lung'),
    'duệ': ('Tao_Due', 'Tào Duệ', 'male', 'khac_kho_lanh_lung'),
    'ngụy chủ': ('Tao_Due', 'Tào Duệ', 'male', 'khac_kho_lanh_lung'),
    'tào sảng': ('Tao_Sang', 'Tào Sảng', 'male', 'hach_dich_bao_nguoc'),
    'sảng': ('Tao_Sang', 'Tào Sảng', 'male', 'hach_dich_bao_nguoc'),
    'tào hy': ('Tao_Hy', 'Tào Hy', 'male', 'xun_xoe_don_hen'),
    'hy': ('Tao_Hy', 'Tào Hy', 'male', 'xun_xoe_don_hen'),
    'tào phương': ('Tao_Phuong', 'Tào Phương', 'male', 'xun_xoe_don_hen'),
    'phương': ('Tao_Phuong', 'Tào Phương', 'male', 'xun_xoe_don_hen'),
    'tào mao': ('Tao_Mao', 'Tào Mao', 'male', 'anh_hung_hao_sang'),
    'mao': ('Tao_Mao', 'Tào Mao', 'male', 'anh_hung_hao_sang'),
    'tào hoán': ('Tao_Hoan', 'Tào Hoán', 'male', 'xun_xoe_don_hen'),
    'hoán': ('Tao_Hoan', 'Tào Hoán', 'male', 'xun_xoe_don_hen'),
    'hạ hầu mậu': ('Ha_Hau_Mau', 'Hạ Hầu Mậu', 'male', 'hach_dich_bao_nguoc'),
    'mậu': ('Ha_Hau_Mau', 'Hạ Hầu Mậu', 'male', 'hach_dich_bao_nguoc'),
    'hạ hầu bá': ('Ha_Hau_Ba', 'Hạ Hầu Bá', 'male', 'anh_hung_hao_sang'),
    'bá': ('Ha_Hau_Ba', 'Hạ Hầu Bá', 'male', 'anh_hung_hao_sang'),
    'trương cáp': ('Truong_Cap', 'Trương Cáp', 'male', 'anh_hung_hao_sang'),
    'cáp': ('Truong_Cap', 'Trương Cáp', 'male', 'anh_hung_hao_sang'),
    'quách hoài': ('Quach_Hoai', 'Quách Hoài', 'male', 'giao_hoat_nham_hiem'),
    'hoài': ('Quach_Hoai', 'Quách Hoài', 'male', 'giao_hoat_nham_hiem'),
    'đặng ngải': ('Dang_Ngai', 'Đặng Ngải', 'male', 'khac_kho_lanh_lung'),
    'ngải': ('Dang_Ngai', 'Đặng Ngải', 'male', 'khac_kho_lanh_lung'),
    'đặng trung': ('Dang_Trung', 'Đặng Trung', 'male', 'anh_hung_hao_sang'),
    'trung': ('Dang_Trung', 'Đặng Trung', 'male', 'anh_hung_hao_sang'),
    'chung hội': ('Chung_Hoi', 'Chung Hội', 'male', 'giao_hoat_nham_hiem'),
    'hội': ('Chung_Hoi', 'Chung Hội', 'male', 'giao_hoat_nham_hiem'),
    'vương lãng': ('Vuong_Lang', 'Vương Lãng', 'male', 'khac_kho_lanh_lung'),
    'lãng': ('Vuong_Lang', 'Vương Lãng', 'male', 'khac_kho_lanh_lung'),
    'hoa hâm': ('Hoa_Ham', 'Hoa Hâm', 'male', 'xun_xoe_don_hen'),
    'hâm': ('Hoa_Ham', 'Hoa Hâm', 'male', 'xun_xoe_don_hen'),
    'vương túc': ('Vuong_Tuc', 'Vương Túc', 'male', 'khac_kho_lanh_lung'),
    'vương thúc': ('Vuong_Tuc', 'Vương Túc', 'male', 'khac_kho_lanh_lung'),
    'túc': ('Vuong_Tuc', 'Vương Túc', 'male', 'khac_kho_lanh_lung'),
    'phó hỗ': ('Pho_Ha', 'Phó Hà', 'male', 'khac_kho_lanh_lung'),
    'phó hô': ('Pho_Ha', 'Phó Hà', 'male', 'khac_kho_lanh_lung'),
    'phó hà': ('Pho_Ha', 'Phó Hà', 'male', 'khac_kho_lanh_lung'),
    'chung do': ('Chung_Do', 'Chung Do', 'male', 'khac_kho_lanh_lung'),
    'vương quán': ('Vuong_Quan', 'Vương Quán', 'male', 'anh_hung_hao_sang'),
    'mẹ vương quán': ('Me_Vuong_Quan', 'Mẹ Vương Quán', 'female', 'anh_hung_hao_sang'),
    'bà mẹ': ('Me_Vuong_Quan', 'Mẹ Vương Quán', 'female', 'anh_hung_hao_sang'),
    'vệ quán': ('Ve_Quan', 'Vệ Quán', 'male', 'giao_hoat_nham_hiem'),
    'quán': ('Ve_Quan', 'Vệ Quán', 'male', 'giao_hoat_nham_hiem'),
    'kỳ kiến': ('Ky_Kien', 'Kỳ Kiến', 'male', 'anh_hung_hao_sang'),
    'kiến': ('Ky_Kien', 'Kỳ Kiến', 'male', 'anh_hung_hao_sang'),
    'hoạn phạm': ('Hoan_Pham', 'Hoạn Phạm', 'male', 'khac_kho_lanh_lung'),
    'phạm': ('Hoan_Pham', 'Hoạn Phạm', 'male', 'khac_kho_lanh_lung'),
    'tân tệ': ('Tan_Te', 'Tân Tệ', 'male', 'trong_sang_thanh_thien'),
    'tệ': ('Tan_Te', 'Tân Tệ', 'male', 'trong_sang_thanh_thien'),
    'lý thắng': ('Ly_Thang', 'Lý Thắng', 'male', 'xun_xoe_don_hen'),
    'thắng': ('Ly_Thang', 'Lý Thắng', 'male', 'xun_xoe_don_hen'),
    'văn khâm': ('Van_Kham', 'Văn Khâm', 'male', 'anh_hung_hao_sang'),
    'khâm': ('Van_Kham', 'Văn Khâm', 'male', 'anh_hung_hao_sang'),
    'quán khâu kiệm': ('Quan_Kuu_Kiem', 'Quán Khâu Kiệm', 'male', 'anh_hung_hao_sang'),
    'kiệm': ('Quan_Kuu_Kiem', 'Quán Khâu Kiệm', 'male', 'anh_hung_hao_sang'),
    'trần thái': ('Tran_Thai', 'Trần Thái', 'male', 'anh_hung_hao_sang'),
    'thái': ('Tran_Thai', 'Trần Thái', 'male', 'anh_hung_hao_sang'),
    'giả sung': ('Gia_Sung', 'Giả Sung', 'male', 'giao_hoat_nham_hiem'),
    'sung': ('Gia_Sung', 'Giả Sung', 'male', 'giao_hoat_nham_hiem'),
    'gia cát đản': ('Gia_Cat_Dan', 'Gia Cát Đản', 'male', 'anh_hung_hao_sang'),
    'đản': ('Gia_Cat_Dan', 'Gia Cát Đản', 'male', 'anh_hung_hao_sang'),
    'thiệu đễ': ('Thieu_De', 'Thiệu Đễ', 'male', 'khac_kho_lanh_lung'),
    'đễ': ('Thieu_De', 'Thiệu Đễ', 'male', 'khac_kho_lanh_lung'),
    'thiệu hoãn': ('Thieu_Hoan', 'Thiệu Hoãn', 'male', 'anh_hung_hao_sang'),
    'hoãn': ('Thieu_Hoan', 'Thiệu Hoãn', 'male', 'anh_hung_hao_sang'),
    'gia cát tự': ('Gia_Cat_Tu', 'Gia Cát Tự', 'male', 'khac_kho_lanh_lung'),
    'tự': ('Gia_Cat_Tu', 'Gia Cát Tự', 'male', 'khac_kho_lanh_lung'),
    'đỗ dự': ('Do_Du', 'Đỗ Dự', 'male', 'anh_hung_hao_sang'),
    'vương hồn': ('Vuong_Hon', 'Vương Hồn', 'male', 'anh_hung_hao_sang'),
    'trương hoa': ('Truong_Hoa', 'Trương Hoa', 'male', 'trong_sang_thanh_thien'),
    'thượng quảng': ('Thuong_Quang', 'Thượng Quảng', 'male', 'teu_tao_hom_hinh'),
    'quảng': ('Thuong_Quang', 'Thượng Quảng', 'male', 'teu_tao_hom_hinh'),
    'quản lộ': ('Quan_Lo', 'Quản Lộ', 'male', 'trong_sang_thanh_thien'),
    'lộ': ('Quan_Lo', 'Quản Lộ', 'male', 'trong_sang_thanh_thien'),
    'ty diễn': ('Ty_Dien', 'Ty Diễn', 'male', 'anh_hung_hao_sang'),
    'trịnh văn': ('Trinh_Van', 'Trịnh Văn', 'male', 'giao_hoat_nham_hiem'),
    'thôi lăng': ('Thoi_Lang', 'Thôi Lăng', 'male', 'anh_hung_hao_sang'),
    'lăng': ('Thoi_Lang', 'Thôi Lăng', 'male', 'anh_hung_hao_sang'),
    'mã tuân': ('Ma_Tuan', 'Mã Tuân', 'male', 'khac_kho_lanh_lung'),
    'tuân': ('Ma_Tuan', 'Mã Tuân', 'male', 'khac_kho_lanh_lung'),
    'phí diệu': ('Phi_Dieu', 'Phí Diệu', 'male', 'anh_hung_hao_sang'),
    'diệu': ('Phi_Dieu', 'Phí Diệu', 'male', 'anh_hung_hao_sang'),
    'cận tường': ('Can_Tuong', 'Cận Tường', 'male', 'trong_sang_thanh_thien'),
    'tường': ('Can_Tuong', 'Cận Tường', 'male', 'trong_sang_thanh_thien'),
    'tôn lễ': ('Ton_Le', 'Tôn Lễ', 'male', 'anh_hung_hao_sang'),
    'lễ': ('Ton_Le', 'Tôn Lễ', 'male', 'anh_hung_hao_sang'),
    'lưu hoa': ('Luu_Hoa', 'Lưu Hoa', 'male', 'trong_sang_thanh_thien'),
    'giả quỳ': ('Gia_Quy', 'Giả Quỳ', 'male', 'khac_kho_lanh_lung'),
    'quỳ': ('Gia_Quy', 'Giả Quỳ', 'male', 'khac_kho_lanh_lung'),
    'dương hựu': ('Duong_Huu', 'Dương Hựu', 'male', 'trong_sang_thanh_thien'),

    # Đông Ngô (Wu)
    'tôn quyền': ('Ton_Quyen', 'Tôn Quyền', 'male', 'anh_hung_hao_sang'),
    'quyền': ('Ton_Quyen', 'Tôn Quyền', 'male', 'anh_hung_hao_sang'),
    'lục tốn': ('Luc_Ton', 'Lục Tốn', 'male', 'khac_kho_lanh_lung'),
    'tốn': ('Luc_Ton', 'Lục Tốn', 'male', 'khac_kho_lanh_lung'),
    'lục kháng': ('Luc_Khang', 'Lục Khang', 'male', 'anh_hung_hao_sang'),
    'kháng': ('Luc_Khang', 'Lục Khang', 'male', 'anh_hung_hao_sang'),
    'tôn hưu': ('Ton_Huu', 'Tôn Hưu', 'male', 'anh_hung_hao_sang'),
    'hưu': ('Ton_Huu', 'Tôn Hưu', 'male', 'anh_hung_hao_sang'),
    'tôn hạo': ('Ton_Hao', 'Tôn Hạo', 'male', 'hach_dich_bao_nguoc'),
    'hạo': ('Ton_Hao', 'Tôn Hạo', 'male', 'hach_dich_bao_nguoc'),
    'tôn lâm': ('Ton_Lam', 'Tôn Lâm', 'male', 'hach_dich_bao_nguoc'),
    'lâm': ('Ton_Lam', 'Tôn Lâm', 'male', 'hach_dich_bao_nguoc'),
    'đinh phụng': ('Dinh_Phung', 'Đinh Phụng', 'male', 'anh_hung_hao_sang'),
    'phụng': ('Dinh_Phung', 'Đinh Phụng', 'male', 'anh_hung_hao_sang'),
    'toàn kỷ': ('Toan_Ky', 'Toàn Kỷ', 'male', 'anh_hung_hao_sang'),
    'kỷ': ('Toan_Ky', 'Toàn Kỷ', 'male', 'anh_hung_hao_sang'),
    'chu phường': ('Chu_Phuong', 'Chu Phường', 'male', 'anh_hung_hao_sang'),
    'phường': ('Chu_Phuong', 'Chu Phường', 'male', 'anh_hung_hao_sang'),
    'gia cát cẩn': ('Gia_Cat_Can', 'Gia Cát Cẩn', 'male', 'trong_sang_thanh_thien'),
    'cẩn': ('Gia_Cat_Can', 'Gia Cát Cẩn', 'male', 'trong_sang_thanh_thien'),
    'gia cát khác': ('Gia_Cat_Khac', 'Gia Cát Khác', 'male', 'hach_dich_bao_nguoc'),
    'khác': ('Gia_Cat_Khac', 'Gia Cát Khác', 'male', 'hach_dich_bao_nguoc'),
    'đằng dận': ('Dang_Dan', 'Đằng Dận', 'male', 'trong_sang_thanh_thien'),
    'dận': ('Dang_Dan', 'Đằng Dận', 'male', 'trong_sang_thanh_thien'),
    'trương để': ('Truong_De', 'Trương Để', 'male', 'anh_hung_hao_sang'),
    'để': ('Truong_De', 'Trương Để', 'male', 'anh_hung_hao_sang'),
    'sầm hôn': ('Sam_Hon', 'Sầm Hôn', 'male', 'xun_xoe_don_hen'),
    'hôn': ('Sam_Hon', 'Sầm Hôn', 'male', 'xun_xoe_don_hen'),
    'gia cát nghiễn': ('Gia_Cat_Nghien', 'Gia Cát Nghiễn', 'male', 'anh_hung_hao_sang'),
    'nghiễn': ('Gia_Cat_Nghien', 'Gia Cát Nghiễn', 'male', 'anh_hung_hao_sang'),
    'tôn dự': ('Ton_Du', 'Tôn Dự', 'male', 'trong_sang_thanh_thien'),

    # Triều thần & Quân sĩ chung
    'các quan': ('Cac_Quan', 'Các Quan', 'male', 'anh_hung_hao_sang'),
    'quần thần': ('Cac_Quan', 'Các Quan', 'male', 'anh_hung_hao_sang'),
    'đại thần': ('Cac_Quan', 'Các Quan', 'male', 'anh_hung_hao_sang'),
    'ba người': ('Cac_Quan', 'Các Quan', 'male', 'anh_hung_hao_sang'),
    'hai người': ('Cac_Quan', 'Các Quan', 'male', 'anh_hung_hao_sang'),
    'cận thần': ('Can_Than', 'Cận Thần', 'male', 'xun_xoe_don_hen'),
    'sứ giả': ('Su_Gia', 'Sứ Giả', 'male', 'anh_hung_hao_sang'),
    'người hầu': ('Nguoi_Hau', 'Người Hầu', 'male', 'xun_xoe_don_hen'),
    'lính canh': ('Linh_Canh', 'Lính Canh', 'male', 'anh_hung_hao_sang'),
    'quân sĩ': ('Quan_Si', 'Quân Sĩ', 'male', 'anh_hung_hao_sang'),
    'tướng sĩ': ('Tuong_Si', 'Tướng Sĩ', 'male', 'anh_hung_hao_sang'),
}

CANONICAL_REMAP_V2 = {
    'Bieu': 'Luu_Bieu',
    'Doan': 'Dong_Doan',
    'Doan_Lai': 'Dong_Doan',
    'Doan_Dung_Day': 'Dong_Doan',
    'Mot_Nguoi': 'Nguoi_Hau',
    'Nguoi_Ay': 'Nguoi_Hau',
    'Nguoi_Kia': 'Nguoi_Hau',
    'Ten_Ay': 'Nguoi_Hau',
    'Quan_Canh': 'Linh_Canh',
    'Quan_Canh_Cua': 'Linh_Canh',
    'Linh_Canh_Cua': 'Linh_Canh',
    'Quan_Giu_Kho': 'Linh_Canh',
    'Quan_Huong_Dao': 'Linh_Canh',
    'Quan_Thuc': 'Quan_Si',
    'Quan_Man': 'Quan_Si',
    'Quan': 'Quan_Si',
    'Cac_Tuong': 'Tuong_Si',
    'Thai_Thu': 'Cac_Quan',
    'Ba_Nguoi_Cung': 'Cac_Quan',
    'Cac_Quan_Cung': 'Cac_Quan',
    'Dai_Than_Lai': 'Cac_Quan',
    'May_Sao_Dam_La': 'Tao_Chan',
}

base_dir = '/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia'
total_dialogues = 0
all_chars_detected = {}

for chap_num in range(91, 121):
    folder = f'{chap_num}-Hoi-{chap_num}'
    chap_dir = os.path.join(base_dir, folder)
    kb_files = sorted(glob.glob(os.path.join(chap_dir, 'kich-ban', 'Kich-ban-*.txt')))
    chap_chars = set()
    for f in kb_files:
        with open(f, 'r', encoding='utf-8') as fp:
            txt = fp.read()
        for p in txt.split('\n\n'):
            p = p.strip()
            if not p: continue
            for m in DIALOGUE_CUE_REGEX.finditer(p):
                sp_raw = m.group('speaker').strip()
                mod = m.group('modifier') or ''
                verb = m.group('verb')
                lead = m.group('lead')
                quote = m.group('quote')
                
                clean_sp, act, extra_mod = clean_speaker_and_posture_v2(sp_raw, mod)
                low_sp = clean_sp.lower().strip()
                
                # Check false speaker
                if low_sp in FALSE_SPEAKERS:
                    continue
                if any(low_sp.startswith(bad) for bad in ['lại nói', 'đây nói', 'thì họ', 'trong hịch', 'trong thư', 'trong sớ', 'có thơ', 'người sau có thơ']):
                    continue
                
                # Context overrides
                cid = None
                cname = clean_sp.title()
                gender = 'male'
                
                if low_sp in ('văn',) and chap_num == 92:
                    cid, cname, gender, _ = KNOWN_CHARS_V2['triệu vân']
                elif low_sp in ('văn',) and chap_num == 102:
                    cid, cname, gender, _ = KNOWN_CHARS_V2['trịnh văn']
                elif low_sp in ('dự',) and chap_num == 120:
                    cid, cname, gender, _ = KNOWN_CHARS_V2['đỗ dự']
                elif low_sp in ('dự',) and chap_num == 105:
                    cid, cname, gender, _ = KNOWN_CHARS_V2['tôn dự']
                elif low_sp in ('quán',) and chap_num == 114:
                    cid, cname, gender, _ = KNOWN_CHARS_V2['vương quán']
                elif low_sp in ('quán',) and chap_num == 119:
                    cid, cname, gender, _ = KNOWN_CHARS_V2['vệ quán']
                elif low_sp in ('đại',) and chap_num in (94, 104, 105):
                    cid, cname, gender, _ = KNOWN_CHARS_V2['mã đại']
                elif low_sp in ('tuân',) and chap_num == 93:
                    cid, cname, gender, _ = KNOWN_CHARS_V2['mã tuân']
                elif low_sp in KNOWN_CHARS_V2:
                    cid, cname, gender, _ = KNOWN_CHARS_V2[low_sp]
                else:
                    # Match substrings
                    for k in sorted(KNOWN_CHARS_V2.keys(), key=lambda x: -len(x)):
                        if k == low_sp or (len(k) >= 4 and k in low_sp):
                            cid, cname, gender, _ = KNOWN_CHARS_V2[k]
                            break
                    if not cid:
                        raw_id = re.sub(r'[^a-zA-Z0-9]+', '_', clean_sp.title()).strip('_')
                        cid = CANONICAL_REMAP_V2.get(raw_id, raw_id)
                
                if cid:
                    total_dialogues += 1
                    chap_chars.add(cid)
                    all_chars_detected[cid] = all_chars_detected.get(cid, 0) + 1

print(f'Test completed. Total dialogues in 91-120: {total_dialogues}')
print(f'Total unique character IDs: {len(all_chars_detected)}')
suspicious = [c for c in all_chars_detected.keys() if '_' not in c or any(bad in c for bad in ['_Lai', '_Mung', '_Cuoi', '_Khoc', '_Thay', '_Ban', '_Kip'])]
print(f'Remaining suspicious characters: {len(suspicious)} -> {suspicious}')
