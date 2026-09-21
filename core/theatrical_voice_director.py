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
    'lưu hoàng thúc': ('Luu_Bi', 'Lưu Bị', 'male', 'trong_sang_thanh_thien'),
    'hoàng thúc': ('Luu_Bi', 'Lưu Bị', 'male', 'trong_sang_thanh_thien'),
    'bị': ('Luu_Bi', 'Lưu Bị', 'male', 'trong_sang_thanh_thien'),
    
    'quan vũ': ('Quan_Vu', 'Quan Vũ', 'male', 'khac_kho_lanh_lung'),
    'vân trường': ('Quan_Vu', 'Quan Vũ', 'male', 'khac_kho_lanh_lung'),
    'quan công': ('Quan_Vu', 'Quan Vũ', 'male', 'khac_kho_lanh_lung'),
    'quan tướng quân': ('Quan_Vu', 'Quan Vũ', 'male', 'khac_kho_lanh_lung'),
    'vũ': ('Quan_Vu', 'Quan Vũ', 'male', 'khac_kho_lanh_lung'),
    'quan': ('Quan_Vu', 'Quan Vũ', 'male', 'khac_kho_lanh_lung'),
    
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
    'trung': ('Hoang_Trung', 'Hoàng Trung', 'male', 'anh_hung_hao_sang'),
    'mã siêu': ('Ma_Sieu', 'Mã Siêu', 'male', 'anh_hung_hao_sang'),
    'siêu': ('Ma_Sieu', 'Mã Siêu', 'male', 'anh_hung_hao_sang'),
    'khương duy': ('Khuong_Duy', 'Khương Duy', 'male', 'anh_hung_hao_sang'),
    'ngụy diên': ('Nguy_Dien', 'Ngụy Diên', 'male', 'hach_dich_bao_nguoc'),
    'diên': ('Nguy_Dien', 'Ngụy Diên', 'male', 'hach_dich_bao_nguoc'),
    'trịnh văn': ('Trinh_Van', 'Trịnh Văn', 'male', 'giao_hoat_nham_hiem'),
    'văn': ('Trinh_Van', 'Trịnh Văn', 'male', 'giao_hoat_nham_hiem'),
    'bàng thống': ('Bang_Thong', 'Bàng Thống', 'male', 'teu_tao_hom_hinh'),
    'pháp chính': ('Phap_Chinh', 'Pháp Chính', 'male', 'khac_kho_lanh_lung'),
    'chính': ('Phap_Chinh', 'Pháp Chính', 'male', 'khac_kho_lanh_lung'),
    'từ thứ': ('Tu_Thu', 'Từ Thứ', 'male', 'tram_uat_dan_vat'),
    'lưu thiền': ('Luu_Thien', 'Lưu Thiền', 'male', 'xun_xoe_don_hen'),
    'hậu chủ': ('Luu_Thien', 'Lưu Thiền', 'male', 'xun_xoe_don_hen'),
    'my trúc': ('My_Truc', 'My Trúc', 'male', 'trong_sang_thanh_thien'),
    'my chúc': ('My_Truc', 'My Trúc', 'male', 'trong_sang_thanh_thien'),
    'chúc': ('My_Truc', 'My Trúc', 'male', 'trong_sang_thanh_thien'),
    'my phương': ('My_Phuong', 'My Phương', 'male', 'xun_xoe_don_hen'),
    'phương': ('My_Phuong', 'My Phương', 'male', 'xun_xoe_don_hen'),
    'tôn càn': ('Ton_Can', 'Tôn Càn', 'male', 'trong_sang_thanh_thien'),
    'càn': ('Ton_Can', 'Tôn Càn', 'male', 'trong_sang_thanh_thien'),
    'giản ung': ('Gian_Ung', 'Giản Ung', 'male', 'teu_tao_hom_hinh'),
    'ung': ('Gian_Ung', 'Giản Ung', 'male', 'teu_tao_hom_hinh'),
    'châu thương': ('Chau_Thuong', 'Châu Thương', 'male', 'anh_hung_hao_sang'),
    'quan định': ('Quan_Dinh', 'Quan Định', 'male', 'anh_hung_hao_sang'),
    'định': ('Quan_Dinh', 'Quan Định', 'male', 'anh_hung_hao_sang'),
    'quan bình': ('Quan_Binh', 'Quan Bình', 'male', 'anh_hung_hao_sang'),
    'quan hưng': ('Quan_Hung', 'Quan Hưng', 'male', 'anh_hung_hao_sang'),
    'trương bào': ('Truong_Bao_Shu', 'Trương Bào', 'male', 'anh_hung_hao_sang'),
    'lưu phong': ('Luu_Phong', 'Lưu Phong', 'male', 'anh_hung_hao_sang'),
    'nghiêm nhan': ('Nghiem_Nhan', 'Nghiêm Nhan', 'male', 'anh_hung_hao_sang'),
    'mã tắc': ('Ma_Tac', 'Mã Tắc', 'male', 'tram_uat_dan_vat'),
    'mã lăng': ('Ma_Lang', 'Mã Lăng', 'male', 'trong_sang_thanh_thien'),
    'lưu tịch': ('Luu_Tich', 'Lưu Tịch', 'male', 'anh_hung_hao_sang'),
    'cung đô': ('Cung_Do', 'Cung Đô', 'male', 'anh_hung_hao_sang'),
    'hồ hoa': ('Ho_Hoa', 'Hồ Hoa', 'male', 'trong_sang_thanh_thien'),
    'hồ ban': ('Ho_Ban', 'Hồ Ban', 'male', 'anh_hung_hao_sang'),

    # Tào Ngụy (Wei)
    'tào tháo': ('Tao_Thao', 'Tào Tháo', 'male', 'giao_hoat_nham_hiem'),
    'mạnh đức': ('Tao_Thao', 'Tào Tháo', 'male', 'giao_hoat_nham_hiem'),
    'tháo': ('Tao_Thao', 'Tào Tháo', 'male', 'giao_hoat_nham_hiem'),
    'tào công': ('Tao_Thao', 'Tào Tháo', 'male', 'giao_hoat_nham_hiem'),
    'thừa tướng': ('Tao_Thao', 'Tào Tháo', 'male', 'giao_hoat_nham_hiem'),
    'tào phi': ('Tao_Phi', 'Tào Phi', 'male', 'giao_hoat_nham_hiem'),
    'tào duệ': ('Tao_Due', 'Tào Duệ', 'male', 'khac_kho_lanh_lung'),
    'tào thực': ('Tao_Thuc', 'Tào Thực', 'male', 'lang_man_bay_bong'),
    'tào nhân': ('Tao_Nhan', 'Tào Nhân', 'male', 'anh_hung_hao_sang'),
    'nhân': ('Tao_Nhan', 'Tào Nhân', 'male', 'anh_hung_hao_sang'),
    'tào hồng': ('Tao_Hong', 'Tào Hồng', 'male', 'anh_hung_hao_sang'),
    'hồng': ('Tao_Hong', 'Tào Hồng', 'male', 'anh_hung_hao_sang'),
    'tào tung': ('Tao_Tung', 'Tào Tung', 'male', 'tram_uat_dan_vat'),
    'tào báo': ('Tao_Bao', 'Tào Báo', 'male', 'xun_xoe_don_hen'),
    'hạ hầu đôn': ('Ha_Hau_Don', 'Hạ Hầu Đôn', 'male', 'hach_dich_bao_nguoc'),
    'đôn': ('Ha_Hau_Don', 'Hạ Hầu Đôn', 'male', 'hach_dich_bao_nguoc'),
    'hạ hầu uyên': ('Ha_Hau_Uyen', 'Hạ Hầu Uyên', 'male', 'anh_hung_hao_sang'),
    'uyên': ('Ha_Hau_Uyen', 'Hạ Hầu Uyên', 'male', 'anh_hung_hao_sang'),
    'trương liêu': ('Truong_Lieu', 'Trương Liêu', 'male', 'anh_hung_hao_sang'),
    'liêu': ('Truong_Lieu', 'Trương Liêu', 'male', 'anh_hung_hao_sang'),
    'văn viễn': ('Truong_Lieu', 'Trương Liêu', 'male', 'anh_hung_hao_sang'),
    'hứa chử': ('Hua_Chu', 'Hứa Chử', 'male', 'anh_hung_hao_sang'),
    'chử': ('Hua_Chu', 'Hứa Chử', 'male', 'anh_hung_hao_sang'),
    'điển vi': ('Dien_Vi', 'Điển Vi', 'male', 'anh_hung_hao_sang'),
    'vi': ('Dien_Vi', 'Điển Vi', 'male', 'anh_hung_hao_sang'),
    'lý điển': ('Ly_Dien', 'Lý Điển', 'male', 'anh_hung_hao_sang'),
    'điển': ('Ly_Dien', 'Lý Điển', 'male', 'anh_hung_hao_sang'),
    'nhạc tiến': ('Nhac_Tien', 'Nhạc Tiến', 'male', 'anh_hung_hao_sang'),
    'vu cấm': ('Vu_Cam', 'Vu Cấm', 'male', 'khac_kho_lanh_lung'),
    'từ hoảng': ('Tu_Hoang', 'Từ Hoảng', 'male', 'anh_hung_hao_sang'),
    'tuân úc': ('Tuan_Uc', 'Tuân Úc', 'male', 'khac_kho_lanh_lung'),
    'úc': ('Tuan_Uc', 'Tuân Úc', 'male', 'khac_kho_lanh_lung'),
    'văn nhược': ('Tuan_Uc', 'Tuân Úc', 'male', 'khac_kho_lanh_lung'),
    'tuân du': ('Tuan_Du', 'Tuân Du', 'male', 'khac_kho_lanh_lung'),
    'quách gia': ('Quach_Gia', 'Quách Gia', 'male', 'giao_hoat_nham_hiem'),
    'gia': ('Quach_Gia', 'Quách Gia', 'male', 'giao_hoat_nham_hiem'),
    'phụng hiếu': ('Quach_Gia', 'Quách Gia', 'male', 'giao_hoat_nham_hiem'),
    'giả hủ': ('Gia_Hu', 'Giả Hủ', 'male', 'giao_hoat_nham_hiem'),
    'hủ': ('Gia_Hu', 'Giả Hủ', 'male', 'giao_hoat_nham_hiem'),
    'văn hòa': ('Gia_Hu', 'Giả Hủ', 'male', 'giao_hoat_nham_hiem'),
    'trình dục': ('Trinh_Duc', 'Trình Dục', 'male', 'khac_kho_lanh_lung'),
    'dục': ('Trinh_Duc', 'Trình Dục', 'male', 'khac_kho_lanh_lung'),
    'trọng đức': ('Trinh_Duc', 'Trình Dục', 'male', 'khac_kho_lanh_lung'),
    'mãn sủng': ('Man_Sung', 'Mãn Sủng', 'male', 'khac_kho_lanh_lung'),
    'sủng': ('Man_Sung', 'Mãn Sủng', 'male', 'khac_kho_lanh_lung'),
    'bá ninh': ('Man_Sung', 'Mãn Sủng', 'male', 'khac_kho_lanh_lung'),
    'lưu hoa': ('Luu_Hoa', 'Lưu Hoa', 'male', 'khac_kho_lanh_lung'),
    'mao giới': ('Mao_Gioi', 'Mao Giới', 'male', 'khac_kho_lanh_lung'),
    'lưu đái': ('Luu_Dai', 'Lưu Đái', 'male', 'hach_dich_bao_nguoc'),
    'vương trung': ('Vuong_Trung', 'Vương Trung', 'male', 'hach_dich_bao_nguoc'),
    'dương tu': ('Duong_Tu', 'Dương Tu', 'male', 'teu_tao_hom_hinh'),
    'tư mã ý': ('Tu_Ma_Y', 'Tư Mã Ý', 'male', 'giao_hoat_nham_hiem'),
    'trọng đạt': ('Tu_Ma_Y', 'Tư Mã Ý', 'male', 'giao_hoat_nham_hiem'),
    'tư mã sư': ('Tu_Ma_Su', 'Tư Mã Sư', 'male', 'giao_hoat_nham_hiem'),
    'tư mã chiêu': ('Tu_Ma_Chieu', 'Tư Mã Chiêu', 'male', 'giao_hoat_nham_hiem'),
    'chiêu': ('Tu_Ma_Chieu', 'Tư Mã Chiêu', 'male', 'giao_hoat_nham_hiem'),
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
    'tôn tĩnh': ('Ton_Tinh', 'Tôn Tĩnh', 'male', 'anh_hung_hao_sang'),
    'ngô cảnh': ('Ngo_Canh', 'Ngô Cảnh', 'male', 'anh_hung_hao_sang'),
    'chu du': ('Chu_Du', 'Chu Du', 'male', 'tram_uat_dan_vat'),
    'công cẩn': ('Chu_Du', 'Chu Du', 'male', 'tram_uat_dan_vat'),
    'du': ('Chu_Du', 'Chu Du', 'male', 'tram_uat_dan_vat'),
    'lỗ túc': ('Lo_Tuc', 'Lỗ Túc', 'male', 'trong_sang_thanh_thien'),
    'tử kính': ('Lo_Tuc', 'Lỗ Túc', 'male', 'trong_sang_thanh_thien'),
    'túc': ('Lo_Tuc', 'Lỗ Túc', 'male', 'trong_sang_thanh_thien'),
    'lữ mông': ('Lu_Mong', 'Lữ Mông', 'male', 'anh_hung_hao_sang'),
    'lục tốn': ('Luc_Ton', 'Lục Tốn', 'male', 'khac_kho_lanh_lung'),
    'hoàng cái': ('Hoang_Cai', 'Hoàng Cái', 'male', 'anh_hung_hao_sang'),
    'cam ninh': ('Cam_Ninh', 'Cam Ninh', 'male', 'hach_dich_bao_nguoc'),
    'trương chiêu': ('Truong_Chieu', 'Trương Chiêu', 'male', 'khac_kho_lanh_lung'),
    'thái sử từ': ('Thai_Su_Tu', 'Thái Sử Từ', 'male', 'anh_hung_hao_sang'),
    'từ': ('Thai_Su_Tu', 'Thái Sử Từ', 'male', 'anh_hung_hao_sang'),
    'chu thái': ('Chu_Thai', 'Chu Thái', 'male', 'anh_hung_hao_sang'),
    'trình phổ': ('Trinh_Pho', 'Trình Phổ', 'male', 'anh_hung_hao_sang'),
    'phổ': ('Trinh_Pho', 'Trình Phổ', 'male', 'anh_hung_hao_sang'),
    'hàn đương': ('Han_Duong', 'Hàn Đương', 'male', 'anh_hung_hao_sang'),
    'lã phạm': ('La_Pham', 'Lã Phạm', 'male', 'khac_kho_lanh_lung'),
    'phạm': ('La_Pham', 'Lã Phạm', 'male', 'khac_kho_lanh_lung'),

    # Triều Đình & Nhà Hán (Han Imperial)
    'vua': ('Han_Hien_De', 'Hán Hiến Đế', 'male', 'bi_kich_uat_nghen'),
    'hiến đế': ('Han_Hien_De', 'Hán Hiến Đế', 'male', 'bi_kich_uat_nghen'),
    'hán hiến đế': ('Han_Hien_De', 'Hán Hiến Đế', 'male', 'bi_kich_uat_nghen'),
    'hoàng đế': ('Han_Hien_De', 'Hán Hiến Đế', 'male', 'bi_kich_uat_nghen'),
    'thiên tử': ('Han_Hien_De', 'Hán Hiến Đế', 'male', 'bi_kich_uat_nghen'),
    'vua linh đế': ('Vua_Linh_De', 'Vua Linh Đế', 'male', 'xun_xoe_don_hen'),
    'linh đế': ('Vua_Linh_De', 'Vua Linh Đế', 'male', 'xun_xoe_don_hen'),
    'thiếu đế': ('Thieu_De', 'Thiếu Đế', 'male', 'bi_kich_uat_nghen'),
    'trần lưu vương': ('Tran_Luu_Vuong', 'Trần Lưu Vương', 'male', 'trong_sang_thanh_thien'),
    'hà tiến': ('Ha_Tien', 'Hà Tiến', 'male', 'hach_dich_bao_nguoc'),
    'tiến': ('Ha_Tien', 'Hà Tiến', 'male', 'hach_dich_bao_nguoc'),
    'đổng thừa': ('Dong_Thua', 'Đổng Thừa', 'male', 'tram_uat_dan_vat'),
    'thừa': ('Dong_Thua', 'Đổng Thừa', 'male', 'tram_uat_dan_vat'),
    'quốc cữu': ('Dong_Thua', 'Đổng Thừa', 'male', 'tram_uat_dan_vat'),
    'đổng thêu': ('Dong_Thua', 'Đổng Thừa', 'male', 'tram_uat_dan_vat'),
    'chủng tập': ('Chung_Tap', 'Chủng Tập', 'male', 'anh_hung_hao_sang'),
    'tập': ('Chung_Tap', 'Chủng Tập', 'male', 'anh_hung_hao_sang'),
    'vương tử phục': ('Vuong_Tu_Phuc', 'Vương Tử Phục', 'male', 'tram_uat_dan_vat'),
    'tử phục': ('Vuong_Tu_Phuc', 'Vương Tử Phục', 'male', 'tram_uat_dan_vat'),
    'ngô thạc': ('Ngo_Thac', 'Ngô Thạc', 'male', 'anh_hung_hao_sang'),
    'ngô tử lan': ('Ngo_Tu_Lan', 'Ngô Tử Lan', 'male', 'anh_hung_hao_sang'),
    'mã đằng': ('Ma_Dang', 'Mã Đằng', 'male', 'anh_hung_hao_sang'),
    'cát bình': ('Cat_Binh', 'Cát Bình', 'male', 'khac_kho_lanh_lung'),
    'nễ hành': ('Ne_Hanh', 'Nễ Hành', 'male', 'teu_tao_hom_hinh'),
    'vương doãn': ('Vuong_Doan', 'Vương Doãn', 'male', 'tram_uat_dan_vat'),
    'doãn': ('Vuong_Doan', 'Vương Doãn', 'male', 'tram_uat_dan_vat'),
    'vương tư đồ': ('Vuong_Doan', 'Vương Doãn', 'male', 'tram_uat_dan_vat'),
    'tư đồ': ('Vuong_Doan', 'Vương Doãn', 'male', 'tram_uat_dan_vat'),
    'lư thực': ('Lu_Thuc', 'Lư Thực', 'male', 'khac_kho_lanh_lung'),
    'thực': ('Lu_Thuc', 'Lư Thực', 'male', 'khac_kho_lanh_lung'),
    'chu tuấn': ('Chu_Tuan', 'Chu Tuấn', 'male', 'anh_hung_hao_sang'),
    'tuấn': ('Chu_Tuan', 'Chu Tuấn', 'male', 'anh_hung_hao_sang'),
    'hoàng phủ tung': ('Hoang_Phu_Tung', 'Hoàng Phủ Tung', 'male', 'anh_hung_hao_sang'),
    'tung': ('Hoang_Phu_Tung', 'Hoàng Phủ Tung', 'male', 'anh_hung_hao_sang'),
    'dương bưu': ('Duong_Buu', 'Dương Bưu', 'male', 'tram_uat_dan_vat'),
    'lưu đào': ('Luu_Dao', 'Lưu Đào', 'male', 'khac_kho_lanh_lung'),
    'trần đam': ('Tran_Dam', 'Trần Đam', 'male', 'khac_kho_lanh_lung'),
    'trần lâm': ('Tran_Lam', 'Trần Lâm', 'male', 'khac_kho_lanh_lung'),
    'sái ung': ('Sai_Ung', 'Sái Ung', 'male', 'trong_sang_thanh_thien'),
    'sái mạo': ('Sai_Mao', 'Sái Mạo', 'male', 'giao_hoat_nham_hiem'),
    'khổng dung': ('Khong_Dung', 'Khổng Dung', 'male', 'trong_sang_thanh_thien'),

    # Quần Hùng & Các Tướng Lĩnh
    'đổng trác': ('Dong_Trac', 'Đổng Trác', 'male', 'hach_dich_bao_nguoc'),
    'trác': ('Dong_Trac', 'Đổng Trác', 'male', 'hach_dich_bao_nguoc'),
    'trọng dĩnh': ('Dong_Trac', 'Đổng Trác', 'male', 'hach_dich_bao_nguoc'),
    'thái sư': ('Dong_Trac', 'Đổng Trác', 'male', 'hach_dich_bao_nguoc'),
    'lã bố': ('La_Bo', 'Lã Bố', 'male', 'hach_dich_bao_nguoc'),
    'phụng tiên': ('La_Bo', 'Lã Bố', 'male', 'hach_dich_bao_nguoc'),
    'bố': ('La_Bo', 'Lã Bố', 'male', 'hach_dich_bao_nguoc'),
    'lý nho': ('Ly_Nho', 'Lý Nho', 'male', 'giao_hoat_nham_hiem'),
    'nho': ('Ly_Nho', 'Lý Nho', 'male', 'giao_hoat_nham_hiem'),
    'lý thôi': ('Ly_Thoi', 'Lý Thôi', 'male', 'hach_dich_bao_nguoc'),
    'thôi': ('Ly_Thoi', 'Lý Thôi', 'male', 'hach_dich_bao_nguoc'),
    'quách dĩ': ('Quach_Di', 'Quách Dĩ', 'male', 'hach_dich_bao_nguoc'),
    'dĩ': ('Quach_Di', 'Quách Dĩ', 'male', 'hach_dich_bao_nguoc'),
    'lý túc': ('Ly_Tuc', 'Lý Túc', 'male', 'xun_xoe_don_hen'),
    'trần cung': ('Tran_Cung', 'Trần Cung', 'male', 'khac_kho_lanh_lung'),
    'cung': ('Tran_Cung', 'Trần Cung', 'male', 'khac_kho_lanh_lung'),
    'trần đăng': ('Tran_Dang', 'Trần Đăng', 'male', 'giao_hoat_nham_hiem'),
    'đăng': ('Tran_Dang', 'Trần Đăng', 'male', 'giao_hoat_nham_hiem'),
    'trần khuê': ('Tran_Khue', 'Trần Khuê', 'male', 'giao_hoat_nham_hiem'),
    'khuê': ('Tran_Khue', 'Trần Khuê', 'male', 'giao_hoat_nham_hiem'),
    'đào khiêm': ('Dao_Khiem', 'Đào Khiêm', 'male', 'tram_uat_dan_vat'),
    'khiêm': ('Dao_Khiem', 'Đào Khiêm', 'male', 'tram_uat_dan_vat'),
    'công tôn toản': ('Cong_Ton_Toan', 'Công Tôn Toản', 'male', 'anh_hung_hao_sang'),
    'toản': ('Cong_Ton_Toan', 'Công Tôn Toản', 'male', 'anh_hung_hao_sang'),
    'viên thiệu': ('Vien_Thieu', 'Viên Thiệu', 'male', 'hach_dich_bao_nguoc'),
    'thiệu': ('Vien_Thieu', 'Viên Thiệu', 'male', 'hach_dich_bao_nguoc'),
    'bổn sơ': ('Vien_Thieu', 'Viên Thiệu', 'male', 'hach_dich_bao_nguoc'),
    'viên thuật': ('Vien_Thuat', 'Viên Thuật', 'male', 'hach_dich_bao_nguoc'),
    'thuật': ('Vien_Thuat', 'Viên Thuật', 'male', 'hach_dich_bao_nguoc'),
    'kỷ linh': ('Ky_Linh', 'Kỷ Linh', 'male', 'hach_dich_bao_nguoc'),
    'linh': ('Ky_Linh', 'Kỷ Linh', 'male', 'hach_dich_bao_nguoc'),
    'cao thuận': ('Cao_Thuan', 'Cao Thuận', 'male', 'anh_hung_hao_sang'),
    'thuận': ('Cao_Thuan', 'Cao Thuận', 'male', 'anh_hung_hao_sang'),
    'trương tú': ('Truong_Tu', 'Trương Tú', 'male', 'anh_hung_hao_sang'),
    'tú': ('Truong_Tu', 'Trương Tú', 'male', 'anh_hung_hao_sang'),
    'hàn phức': ('Han_Phuc', 'Hàn Phức', 'male', 'tram_uat_dan_vat'),
    'phức': ('Han_Phuc', 'Hàn Phức', 'male', 'tram_uat_dan_vat'),
    'nhan lương': ('Nhan_Luong', 'Nhan Lương', 'male', 'anh_hung_hao_sang'),
    'lương': ('Nhan_Luong', 'Nhan Lương', 'male', 'anh_hung_hao_sang'),
    'văn xú': ('Van_Xu', 'Văn Xú', 'male', 'anh_hung_hao_sang'),
    'xú': ('Van_Xu', 'Văn Xú', 'male', 'anh_hung_hao_sang'),
    'điền phong': ('Dien_Phong', 'Điền Phong', 'male', 'khac_kho_lanh_lung'),
    'thẩm phối': ('Tham_Phoi', 'Thẩm Phối', 'male', 'khac_kho_lanh_lung'),
    'thẩm': ('Tham_Phoi', 'Thẩm Phối', 'male', 'khac_kho_lanh_lung'),
    'quách đồ': ('Quach_Do', 'Quách Đồ', 'male', 'giao_hoat_nham_hiem'),
    'phùng kỷ': ('Phung_Ky', 'Phùng Kỷ', 'male', 'giao_hoat_nham_hiem'),
    'trương cáp': ('Truong_Cap', 'Trương Cáp', 'male', 'anh_hung_hao_sang'),
    'cáp': ('Truong_Cap', 'Trương Cáp', 'male', 'anh_hung_hao_sang'),
    'hứa du': ('Hua_Du', 'Hứa Du', 'male', 'teu_tao_hom_hinh'),
    'viên hy': ('Vien_Hy', 'Viên Hy', 'male', 'anh_hung_hao_sang'),
    'hy': ('Vien_Hy', 'Viên Hy', 'male', 'anh_hung_hao_sang'),
    'viên đàm': ('Vien_Dam', 'Viên Đàm', 'male', 'anh_hung_hao_sang'),
    'viên thượng': ('Vien_Thuong', 'Viên Thượng', 'male', 'anh_hung_hao_sang'),
    'hầu thành': ('Hau_Thanh', 'Hầu Thành', 'male', 'anh_hung_hao_sang'),
    'tống hiến': ('Tong_Hien', 'Tống Hiến', 'male', 'anh_hung_hao_sang'),
    'ngụy tục': ('Nguy_Tuc', 'Ngụy Tục', 'male', 'anh_hung_hao_sang'),
    'lữ bá xa': ('La_Ba_Sa', 'Lữ Bá Xa', 'male', 'trong_sang_thanh_thien'),
    'lý nhạc': ('Ly_Nhac', 'Lý Nhạc', 'male', 'hach_dich_bao_nguoc'),
    'hàn dũng': ('Han_Dung', 'Hàn Dũng', 'male', 'anh_hung_hao_sang'),
    'hàn dận': ('Han_Dan', 'Hàn Dận', 'male', 'xun_xoe_don_hen'),
    'dương phụng': ('Duong_Phung', 'Dương Phụng', 'male', 'anh_hung_hao_sang'),
    'hàn tiêm': ('Han_Tiem', 'Hàn Tiêm', 'male', 'hach_dich_bao_nguoc'),
    'tống quả': ('Tong_Qua', 'Tống Quả', 'male', 'anh_hung_hao_sang'),
    'lưu biểu': ('Luu_Bieu', 'Lưu Biểu', 'male', 'tram_uat_dan_vat'),
    'biểu': ('Luu_Bieu', 'Lưu Biểu', 'male', 'tram_uat_dan_vat'),
    'cảnh thăng': ('Luu_Bieu', 'Lưu Biểu', 'male', 'tram_uat_dan_vat'),
    'kinh châu mục': ('Luu_Bieu', 'Lưu Biểu', 'male', 'tram_uat_dan_vat'),
    'châu mục': ('Luu_Bieu', 'Lưu Biểu', 'male', 'tram_uat_dan_vat'),
    'khoái lương': ('Khoai_Luong', 'Khoái Lương', 'male', 'khac_kho_lanh_lung'),
    'khoái việt': ('Khoai_Viet', 'Khoái Việt', 'male', 'khac_kho_lanh_lung'),
    'hoàng tổ': ('Hoang_To', 'Hoàng Tổ', 'male', 'anh_hung_hao_sang'),
    'hàn toại': ('Han_Toai', 'Hàn Toại', 'male', 'anh_hung_hao_sang'),
    'trương giác': ('Truong_Giac', 'Trương Giác', 'male', 'hach_dich_bao_nguoc'),
    'giác': ('Truong_Giac', 'Trương Giác', 'male', 'hach_dich_bao_nguoc'),
    'trương bảo': ('Truong_Bao', 'Trương Bảo', 'male', 'hach_dich_bao_nguoc'),
    'trương lương': ('Truong_Luong', 'Trương Lương', 'male', 'hach_dich_bao_nguoc'),
    'hoa đà': ('Hoa_Da', 'Hoa Đà', 'male', 'trong_sang_thanh_thien'),
    'quách thường': ('Quach_Thuong', 'Quách Thường', 'male', 'trong_sang_thanh_thien'),
    'trần chấn': ('Tran_Chan', 'Trần Chấn', 'male', 'khac_kho_lanh_lung'),
    'chấn': ('Tran_Chan', 'Trần Chấn', 'male', 'khac_kho_lanh_lung'),
    'hoa hùng': ('Hoa_Hung', 'Hoa Hùng', 'male', 'hach_dich_bao_nguoc'),
    'du thiệp': ('Du_Thiep', 'Du Thiệp', 'male', 'anh_hung_hao_sang'),
    'phan phụng': ('Phan_Phung', 'Phan Phụng', 'male', 'anh_hung_hao_sang'),
    'mục thuận': ('Muc_Thuan', 'Mục Thuận', 'male', 'anh_hung_hao_sang'),
    'vũ an quốc': ('Vu_An_Quoc', 'Vũ An Quốc', 'male', 'anh_hung_hao_sang'),
    'nam hoa lão tiên': ('Nam_Hoa_Lao_Tien', 'Nam Hoa Lão Tiên', 'male', 'khac_kho_lanh_lung'),
    'vu cát': ('Vu_Cat', 'Vu Cát', 'male', 'khac_kho_lanh_lung'),

    # Nhân Vật Nữ (Female)
    'điêu thuyền': ('Dieu_Thuyen', 'Điêu Thuyền', 'female', 'trong_sang_thanh_thien'),
    'thuyền': ('Dieu_Thuyen', 'Điêu Thuyền', 'female', 'trong_sang_thanh_thien'),
    'đổng quý phi': ('Dong_Quy_Phi', 'Đổng Quý Phi', 'female', 'bi_kich_uat_nghen'),
    'quý phi': ('Dong_Quy_Phi', 'Đổng Quý Phi', 'female', 'bi_kich_uat_nghen'),
    'hà hoàng hậu': ('Ha_Hoang_Hau', 'Hà Hoàng Hậu', 'female', 'hach_dich_bao_nguoc'),
    'hà thái hậu': ('Ha_Hoang_Hau', 'Hà Hoàng Hậu', 'female', 'hach_dich_bao_nguoc'),
    'hoàng hậu': ('Ha_Hoang_Hau', 'Hà Hoàng Hậu', 'female', 'hach_dich_bao_nguoc'),
    'đổng thái hậu': ('Dong_Thai_Hau', 'Đổng Thái Hậu', 'female', 'hach_dich_bao_nguoc'),
    'thái hậu': ('Dong_Thai_Hau', 'Đổng Thái Hậu', 'female', 'hach_dich_bao_nguoc'),
    'cam phu nhân': ('Cam_Phu_Nhan', 'Cam Phu Nhân', 'female', 'trong_sang_thanh_thien'),
    'my phu nhân': ('My_Phu_Nhan', 'My Phu Nhân', 'female', 'bi_kich_uat_nghen'),
    'tôn phu nhân': ('Ton_Phu_Nhan', 'Tôn Phu Nhân', 'female', 'anh_hung_hao_sang'),
    'biện phu nhân': ('Bien_Phu_Nhan', 'Biện Phu Nhân', 'female', 'trong_sang_thanh_thien'),
    'ngô quốc thái': ('Ngo_Quoc_Thai', 'Ngô Quốc Thái', 'female', 'khac_kho_lanh_lung'),
    'châu thị': ('Chau_Thi', 'Châu Thị', 'female', 'lang_man_bay_bong'),
    'nghiêm thị': ('Nghiem_Thi', 'Nghiêm Thị', 'female', 'tram_uat_dan_vat'),
    'hồ thị': ('Nghiem_Thi', 'Nghiêm Thị', 'female', 'tram_uat_dan_vat'),
    'hai phu nhân': ('Hai_Phu_Nhan', 'Hai Phu Nhân', 'female', 'trong_sang_thanh_thien'),
    'phu nhân': ('Phu_Nhan', 'Phu Nhân', 'female', 'trong_sang_thanh_thien'),
    'vợ': ('Phu_Nhan', 'Phu Nhân', 'female', 'trong_sang_thanh_thien'),
    'mẹ': ('Me', 'Mẹ', 'female', 'trong_sang_thanh_thien'),

    # Vai Phụ & Tập Thể (Secondary Characters & Crowds)
    'tướng sĩ': ('Tuong_Si', 'Tướng Sĩ', 'male', 'anh_hung_hao_sang'),
    'các tướng': ('Tuong_Si', 'Tướng Sĩ', 'male', 'anh_hung_hao_sang'),
    'hai tướng': ('Tuong_Si', 'Tướng Sĩ', 'male', 'anh_hung_hao_sang'),
    'ba tướng': ('Tuong_Si', 'Tướng Sĩ', 'male', 'anh_hung_hao_sang'),
    'chư tướng': ('Tuong_Si', 'Tướng Sĩ', 'male', 'anh_hung_hao_sang'),
    'tráng sĩ': ('Tuong_Si', 'Tướng Sĩ', 'male', 'anh_hung_hao_sang'),
    'các quan': ('Cac_Quan', 'Các Quan', 'male', 'khac_kho_lanh_lung'),
    'trăm quan': ('Cac_Quan', 'Các Quan', 'male', 'khac_kho_lanh_lung'),
    'quân sĩ': ('Quan_Si', 'Quân Sĩ', 'male', 'anh_hung_hao_sang'),
    'quân lính': ('Quan_Si', 'Quân Sĩ', 'male', 'anh_hung_hao_sang'),
    'tên lính': ('Quan_Si', 'Quân Sĩ', 'male', 'anh_hung_hao_sang'),
    'quân báo': ('Quan_Si', 'Quân Sĩ', 'male', 'anh_hung_hao_sang'),
    'quân do thám': ('Quan_Si', 'Quân Sĩ', 'male', 'anh_hung_hao_sang'),
    'người khăn vàng': ('Quan_Si', 'Quân Sĩ', 'male', 'anh_hung_hao_sang'),
    'người hầu': ('Nguoi_Hau', 'Người Hầu', 'male', 'xun_xoe_don_hen'),
    'kẻ hầu': ('Nguoi_Hau', 'Người Hầu', 'male', 'xun_xoe_don_hen'),
    'quân hầu': ('Nguoi_Hau', 'Người Hầu', 'male', 'xun_xoe_don_hen'),
    'người hầu gái': ('Nguoi_Hau_Gai', 'Người Hầu Gái', 'female', 'xun_xoe_don_hen'),
    'hầu gái': ('Nguoi_Hau_Gai', 'Người Hầu Gái', 'female', 'xun_xoe_don_hen'),
    'thị nữ': ('Nguoi_Hau_Gai', 'Người Hầu Gái', 'female', 'xun_xoe_don_hen'),
    'tả hữu': ('Nguoi_Hau', 'Người Hầu', 'male', 'xun_xoe_don_hen'),
    'gia nhân': ('Nguoi_Hau', 'Người Hầu', 'male', 'xun_xoe_don_hen'),
    'lính canh': ('Linh_Canh', 'Lính Canh', 'male', 'anh_hung_hao_sang'),
    'lính canh cửa': ('Linh_Canh', 'Lính Canh', 'male', 'anh_hung_hao_sang'),
    'quân canh': ('Linh_Canh', 'Lính Canh', 'male', 'anh_hung_hao_sang'),
    'sứ giả': ('Su_Gia', 'Sứ Giả', 'male', 'khac_kho_lanh_lung'),
    'sứ': ('Su_Gia', 'Sứ Giả', 'male', 'khac_kho_lanh_lung'),
    'thổ dân': ('Tho_Dan', 'Thổ Dân', 'male', 'anh_hung_hao_sang'),
    'ông già': ('Ong_Gia', 'Ông Già', 'male', 'trong_sang_thanh_thien'),
    'một ông già': ('Ong_Gia', 'Ông Già', 'male', 'trong_sang_thanh_thien'),
    'học trò': ('Hoc_Tro', 'Học Trò', 'male', 'trong_sang_thanh_thien'),
    'mưu sĩ': ('Muu_Si', 'Mưu Sĩ', 'male', 'giao_hoat_nham_hiem'),
    'chư hầu': ('Chu_Hau', 'Chư Hầu', 'male', 'anh_hung_hao_sang'),
    'tướng tá': ('Tuong_Si', 'Tướng Tá', 'male', 'anh_hung_hao_sang'),
    'quần thần': ('Quan_Than', 'Quần Thần', 'male', 'xun_xoe_don_hen'),
    'cổ lại': ('Quan_Si', 'Cổ Lại', 'male', 'anh_hung_hao_sang'),

    # Late Three Kingdoms & Historical Monosyllables
    'chiêm': ('Gia_Cat_Chiem', 'Gia Cát Chiêm', 'male', 'trong_sang_thanh_thien'),
    'gia cát chiêm': ('Gia_Cat_Chiem', 'Gia Cát Chiêm', 'male', 'trong_sang_thanh_thien'),
    'thầm': ('Luu_Tham', 'Lưu Thầm', 'male', 'anh_hung_hao_sang'),
    'lưu thầm': ('Luu_Tham', 'Lưu Thầm', 'male', 'anh_hung_hao_sang'),
    'kháng': ('Luc_Khang', 'Lục Kháng', 'male', 'khac_kho_lanh_lung'),
    'lục kháng': ('Luc_Khang', 'Lục Kháng', 'male', 'khac_kho_lanh_lung'),
    'phủ': ('Vuong_Phu', 'Vương Phủ', 'male', 'tram_uat_dan_vat'),
    'vương phủ': ('Vuong_Phu', 'Vương Phủ', 'male', 'tram_uat_dan_vat'),
    'quỳ': ('Gia_Quy', 'Giả Quỳ', 'male', 'khac_kho_lanh_lung'),
    'giả quỳ': ('Gia_Quy', 'Giả Quỳ', 'male', 'khac_kho_lanh_lung'),
    'tùng': ('Truong_Tung', 'Trương Tùng', 'male', 'teu_tao_hom_hinh'),
    'trương tùng': ('Truong_Tung', 'Trương Tùng', 'male', 'teu_tao_hom_hinh'),
    'ninh': ('Cam_Ninh', 'Cam Ninh', 'male', 'anh_hung_hao_sang'),
    'tốn': ('Luc_Ton', 'Lục Tốn', 'male', 'khac_kho_lanh_lung'),
    'bá ngôn': ('Luc_Ton', 'Lục Tốn', 'male', 'khac_kho_lanh_lung'),
    'mông': ('Lu_Mong', 'Lữ Mông', 'male', 'anh_hung_hao_sang'),
    'tử minh': ('Lu_Mong', 'Lữ Mông', 'male', 'anh_hung_hao_sang'),
    'ngải': ('Dang_Ngai', 'Đặng Ngải', 'male', 'giao_hoat_nham_hiem'),
    'sĩ tái': ('Dang_Ngai', 'Đặng Ngải', 'male', 'giao_hoat_nham_hiem'),
    'hội': ('Chung_Hoi', 'Chung Hội', 'male', 'giao_hoat_nham_hiem'),
    'sĩ quý': ('Chung_Hoi', 'Chung Hội', 'male', 'giao_hoat_nham_hiem'),
    'duy': ('Khuong_Duy', 'Khương Duy', 'male', 'anh_hung_hao_sang'),
    'bá ước': ('Khuong_Duy', 'Khương Duy', 'male', 'anh_hung_hao_sang'),
    'viêm': ('Tu_Ma_Viem', 'Tư Mã Viêm', 'male', 'hach_dich_bao_nguoc'),
    'tấn chủ': ('Tu_Ma_Viem', 'Tư Mã Viêm', 'male', 'hach_dich_bao_nguoc'),
    'tư mã viêm': ('Tu_Ma_Viem', 'Tư Mã Viêm', 'male', 'hach_dich_bao_nguoc'),
    'hy': ('Tao_Hy', 'Tào Hy', 'male', 'tram_uat_dan_vat'),
    'tào hy': ('Tao_Hy', 'Tào Hy', 'male', 'tram_uat_dan_vat'),
    'vương khuông': ('Vuong_Khuong', 'Vương Khuông', 'male', 'anh_hung_hao_sang'),
    'vương quán': ('Vuong_Quan', 'Vương Quán', 'male', 'anh_hung_hao_sang'),
    'vương cơ': ('Vuong_Co', 'Vương Cơ', 'male', 'anh_hung_hao_sang'),
    'vương thúc': ('Vuong_Thuc', 'Vương Thúc', 'male', 'khac_kho_lanh_lung'),
    'phó hỗ': ('Pho_Ho', 'Phó Hỗ', 'male', 'khac_kho_lanh_lung'),
    'ngụy bình': ('Nguy_Binh', 'Ngụy Bình', 'male', 'anh_hung_hao_sang'),
    'trịnh văn': ('Trinh_Van', 'Trịnh Văn', 'male', 'giao_hoat_nham_hiem'),
    'đóa tư': ('Doa_Tu', 'Đóa Tư Đại Vương', 'male', 'hach_dich_bao_nguoc'),
    'đóa tư đại vương': ('Doa_Tu', 'Đóa Tư Đại Vương', 'male', 'hach_dich_bao_nguoc'),
    'dương kỳ': ('Duong_Ky', 'Dương Kỳ', 'male', 'trong_sang_thanh_thien'),
    'lã khoáng': ('La_Khoang', 'Lã Khoáng', 'male', 'anh_hung_hao_sang'),
    'tôn hoàn': ('Ton_Hoan', 'Tôn Hoàn', 'male', 'anh_hung_hao_sang'),
    'hoàn': ('Ton_Hoan', 'Tôn Hoàn', 'male', 'anh_hung_hao_sang'),
    'đinh dị': ('Dinh_Di', 'Đinh Dị', 'male', 'tram_uat_dan_vat'),
    'đỗ quỳnh': ('Do_Quynh', 'Đỗ Quỳnh', 'male', 'khac_kho_lanh_lung'),
    'phí y': ('Phi_Y', 'Phí Y', 'male', 'trong_sang_thanh_thien'),
    'tưởng uyển': ('Tuong_Uyen', 'Tưởng Uyển', 'male', 'trong_sang_thanh_thien'),
    'bàng đức': ('Bang_Duc', 'Bàng Đức', 'male', 'anh_hung_hao_sang'),
    'vương thị': ('Vuong_Thi', 'Vương Thị', 'female', 'anh_hung_hao_sang'),
    'từ mẫu': ('Tu_Mau', 'Từ Mẫu', 'female', 'trong_sang_thanh_thien'),
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
    r'Bèn ngâm rằng|Ngâm rằng)\s*[,:]?\s*)',
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
        return voice, "-2Hz", "-12%", "1.20s", "contemplative_narrator"
    if is_poem_intro:
        return voice, "-2Hz", "-12%", "0.55s", "contemplative_narrator"

    if narrator_mode == 'epic':
        pitch = "+1Hz"
        rate = "+0%"
        lead_in = "0.48s" if is_lead_in else "0.45s"
        timbre_eq = "epic_narrator"
    elif narrator_mode == 'elegiac':
        pitch = "-3Hz"
        rate = "-10%"
        lead_in = "0.60s" if is_lead_in else "0.65s"
        timbre_eq = "elegiac_narrator"
    elif narrator_mode == 'suspense':
        pitch = "+1Hz"
        rate = "-8%"
        lead_in = "0.48s" if is_lead_in else "0.45s"
        timbre_eq = "suspense_narrator"
    elif narrator_mode == 'contemplative':
        pitch = "-2Hz"
        rate = "-12%"
        lead_in = "0.70s"
        timbre_eq = "contemplative_narrator"
    else:
        pitch = "+0Hz"
        rate = "-5%"
        lead_in = "0.48s" if is_lead_in else "0.45s"
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
    Strictly bounded within [0.45s - 1.20s] to ensure the previous speaker's breath
    and release tail are 100% completed before the next line starts.
    - Instant / Interruption (0.45s - 0.52s): Heated argument, shouting, sudden intervention with breath safety cushion.
    - Urgent lead-in (0.48s - 0.58s): Sudden command / cry after narrator action.
    - Natural dialogue turn (0.55s - 0.68s): Standard conversational turn between characters.
    - Dialogue resonance (0.65s - 0.80s): After character finishes speaking before narrator continues.
    - Deliberate / Pensive / Solemn (0.75s - 0.95s): Thoughtful reply, sigh.
    - Regal ceremony (0.80s - 1.00s): Royal court ceremony, solemn oath.
    - Dramatic silence / Shock / Coda (1.00s - 1.20s): Following shock, dying breath, philosophical revelation, or poetic silence.
    """
    mod = (modifier or "").lower()
    vb = (verb or "").lower()

    if prev_type == "narrator" and curr_type == "dialogue":
        if any(w in mod for w in ("cả giận", "kinh hãi", "vội")) or vb in ("quát", "thét", "hét", "hô"):
            return "0.48s"  # Sudden, urgent entry with natural breath cushion
        if any(w in mod for w in ("thở dài", "ngậm ngùi", "buông xuôi")) or vb in ("than", "khóc", "nghĩ", "thầm nghĩ"):
            return "0.75s"  # Pensive sigh before speech
        return "0.55s"  # Natural lead-in

    elif prev_type == "dialogue" and curr_type == "dialogue":
        if prev_speaker != curr_speaker:
            if emotion in ("cuong_no", "de_doa_tham_hiem") or vb in ("quát", "mắng", "cãi"):
                return "0.48s"  # Interruption allowing previous speaker's breath to complete
            if emotion in ("hoi_hop_thi_thao", "doc_thoai_dan_vat", "met_moi_buong_xuoi", "dau_don_trang_troi"):
                return "0.85s"  # Heavy emotional breath
            return "0.58s"  # Natural character turn
        else:
            return "0.45s"  # Same character pause between sentences

    elif prev_type == "dialogue" and curr_type == "narrator":
        return "0.65s"  # Resonance pause for character's words to sink in

    return "0.48s"

# ------------------------------------------------------------------------------
# Action & Posture Stripping & Canonical Unification Constants
# ------------------------------------------------------------------------------
POSTURE_ACTIONS = [
    'đứng dậy tạ', 'đứng dậy', 'đứng lên', 'ngồi xuống', 'quỳ xuống', 'sụp lạy', 'rập đầu', 'bước ra', 'bước vào', 'tiến lên', 'lùi lại',
    'ngoảnh lại', 'quay lại', 'ngẩng đầu', 'ngẩng mặt lên', 'ngẩng mặt', 'cúi đầu', 'chắp tay', 'khoanh tay', 'vỗ bàn', 'đập bàn', 'nhìn quanh', 'ngó trước ngó sau',
    'ngó quanh', 'nín thở', 'thở dài', 'lắc đầu', 'gật đầu', 'vuốt râu', 'vẫy tay', 'chống giáo', 'chống kiếm', 'chống đao',
    'vung đao', 'vung gươm', 'vung kiếm', 'vung tay', 'vung roi', 'rút gươm ra', 'rút gươm', 'rút kiếm', 'rút đao', 'tra gươm', 'tra kiếm',
    'trỏ roi lên', 'trỏ sang', 'về đến trận', 'vào chầu', 'ra ngựa', 'dừng ngựa', 'lạy xuống đất', 'sụp xuống lạy', 'lạy', 'quỳ',
    'xuống ngựa', 'lên ngựa', 'chỉ tay', 'bịt miệng', 'che mặt', 'bịt tai', 'trở về', 'trở rồi', 'trở ra mà', 'vào trong trại',
    'vào', 'ngồi'
]

EMOTION_MODIFIERS_EXTRA = [
    'gạt nước mắt', 'chảy nước mắt', 'lau nước mắt', 'nhỏ lệ', 'ứa nước mắt', 'rơi lệ', 'khóc than', 'khóc lóc', 'khóc lạy',
    'khóc vang lên', 'khóc rống lên', 'khóc mà', 'khóc và', 'khóc', 'cười lớn', 'cười nhạt', 'cười nụ', 'cười ha hả', 'cười ầm lên',
    'cười to', 'cười ngất', 'cười', 'mừng rỡ', 'mừng', 'giận dữ', 'nổi giận lên', 'nổi giận', 'cả giận', 'giận lắm',
    'hằm hằm nét mặt', 'hằm hằm mặt', 'tái mặt', 'biến sắc', 'giật mình', 'kinh hãi', 'hoảng sợ', 'ngạc nhiên',
    'bàng hoàng', 'ngậm ngùi', 'buồn rầu', 'xót xa', 'thống thiết', 'nghi ngờ', 'thầm nghĩ', 'thở dài', 'sợ hãi', 'sợ',
    'bĩu môi', 'hớn hở', 'bực tức', 'hăm hở', 'trợn mắt', 'thất kinh', 'kinh sợ', 'trông thấy', 'nghe thấy'
]

ADVERBS_EXTRA = [
    'lại', 'bèn', 'liền', 'vội vàng', 'vội', 'chợt', 'bỗng', 'mới', 'thong thả', 'từ từ', 'nghiêm giọng', 'lớn tiếng',
    'gằn giọng', 'hạ giọng', 'thì thào', 'thong dong', 'giả cách', 'giả vờ', 'ngang nhiên', 'sực nhớ đến', 'thấy vậy mới',
    'thấy vậy', 'đang', 'đã', 'sắp', 'cũng', 'đều', 'vẫn', 'cứ', 'rồi'
]

VERB_ACTIONS = [
    'phán hỏi', 'phán bảo', 'phán', 'truyền bảo', 'truyền lệnh', 'truyền', 'quát hỏi', 'quát mắng', 'quát lên', 'quát',
    'thét', 'hét', 'hô lớn', 'hô', 'gọi', 'can ngăn', 'can', 'dặn dò', 'dặn', 'mắng', 'than khóc', 'than thở', 'than',
    'hỏi', 'đáp', 'tâu', 'bảo', 'nói', 'khen ngợi', 'khen', 'thề', 'bàn định', 'bàn', 'nhủ', 'ngâm', 'vịnh',
    'xin nhận tội', 'nhận tội', 'lạy tạ', 'tạ', 'mời', 'nhìn', 'trông', 'thấy', 'nghe'
]

PREFIX_STRIP = [
    'thái thú ', 'đại tướng ', 'trưởng sử ', 'thứ sử ', 'thừa tướng ', 'thượng thư phó ', 'thượng thư ',
    'giám quân ', 'tham quân ', 'thái úy ', 'đô đốc ', 'tiên phong ', 'trung lang tướng ', 'tướng quân ',
    'lại một người ', 'lại một nười ', 'lại một ', 'em là ',
    'bèn gọi ', 'liền gọi ', 'sai gọi ', 'chợt có ', 'lại có ', 'bỗng có ', 'chợt lại có ',
    'có hai tướng ra ', 'có tướng ra ', 'có người ', 'một người ', 'các tướng ',
    'trong thư lại ', 'thư lại được ', 'vứt xuống đất rồi ', 'rồi thấy ', 'rồi mật ', 'rồi tùng ',
    'rồi gọi mã đại ', 'rồi ', 'bèn ', 'cho nên ', 'vì thế '
]

CANONICAL_CHAR_REMAP = {
    # Pinyin fixes
    'Liu_Biao': 'Luu_Bieu',
    'Jia_Xu': 'Gia_Hu',
    'Zhang_Xiu': 'Truong_Tu',
    'Yuan_Shao': 'Vien_Thieu',

    # Imperial & Titles
    'Hien_De': 'Han_Hien_De',
    'Vua': 'Han_Hien_De',
    'Hoang_De': 'Han_Hien_De',
    'Thien_Tu': 'Han_Hien_De',
    'Vua_Phan': 'Han_Hien_De',
    'Vua_Mung': 'Han_Hien_De',
    'Vua_Du': 'Han_Hien_De',
    'Vua_Gat_Nuoc_Mat': 'Han_Hien_De',
    'Hien_De_Khoc': 'Han_Hien_De',
    'Trong_Chieu': 'Han_Hien_De',
    'Ha_Thai_Hau': 'Ha_Hoang_Hau',
    'Dong_Thieu': 'Dong_Thua',
    'Dong_Thua_Cuoi': 'Dong_Thua',
    'Thua_Che_Mat_Khoc': 'Dong_Thua',
    'Thua_Giat_Minh': 'Dong_Thua',
    'Thua': 'Dong_Thua',
    'Tap': 'Chung_Tap',
    'Tu_Phuc': 'Vuong_Tu_Phuc',

    # Single Syllable / Actions
    'Bieu': 'Luu_Bieu',
    'Bieu_Lai': 'Luu_Bieu',
    'Doan': 'Vuong_Doan',
    'Doan_Lai': 'Vuong_Doan',
    'Doan_Dung_Day': 'Vuong_Doan',
    'Cung': 'Tran_Cung',
    'Cung_Tro_Ra_Ma': 'Tran_Cung',
    'Dang': 'Tran_Dang',
    'Dang_Ham_Ham_Mat': 'Tran_Dang',
    'Tru_Moi_Tran_Dang': 'Tran_Dang',
    'Khue': 'Tran_Khue',
    'Ky_Linh_So': 'Ky_Linh',
    'Linh': 'Ky_Linh',
    'Linh_Lai': 'Ky_Linh',
    'Toan': 'Cong_Ton_Toan',
    'Toan_Lai': 'Cong_Ton_Toan',
    'Toai_Lai': 'Han_Toai',
    'Dao_Khiem_Khoc': 'Dao_Khiem',
    'Khiem_Moi': 'Dao_Khiem',
    'Khiem': 'Dao_Khiem',
    'Don': 'Ha_Hau_Don',
    'Don_Chong_Giao': 'Ha_Hau_Don',
    'Don_Tro_Ve': 'Ha_Hau_Don',
    'Don_Lai': 'Ha_Hau_Don',
    'Uyen': 'Ha_Hau_Uyen',
    'Lieu': 'Truong_Lieu',
    'Lieu_Lai': 'Truong_Lieu',
    'Vi': 'Dien_Vi',
    'Dien': 'Ly_Dien',
    'Chu': 'Hua_Chu',
    'Hong': 'Tao_Hong',
    'Nhan': 'Tao_Nhan',
    'Uc': 'Tuan_Uc',
    'Uc_Lai': 'Tuan_Uc',
    'Uc_Suc_Nho_Den': 'Tuan_Uc',
    'Thu_Lai_Duoc': 'Tuan_Uc',
    'Trong_Thu_Lai': 'Tham_Phoi',
    'Duc': 'Trinh_Duc',
    'Gia': 'Quach_Gia',
    'Gia_Lai': 'Quach_Gia',
    'Hu': 'Gia_Hu',
    'Sung': 'Man_Sung',
    'Sung_Lai': 'Man_Sung',
    'Hoa': 'Luu_Hoa',
    'Tuc': 'Lo_Tuc',
    'Du': 'Chu_Du',
    'Pho': 'Trinh_Pho',
    'Chuc': 'My_Truc',
    'My_Chuc': 'My_Truc',
    'Ung': 'Gian_Ung',
    'Ung_Xin_Nhan_Toi': 'Gian_Ung',
    'Can': 'Ton_Can',
    'Dinh': 'Quan_Dinh',
    'Quan': 'Quan_Vu',
    'Ben_Goi_Chau_Thuong': 'Quan_Vu',
    'Quach_Thuong_Khoc': 'Quach_Thuong',
    'Quach_Tuong_Goi': 'Quach_Do',
    'Thuan': 'Cao_Thuan',
    'Thuyen': 'Dieu_Thuyen',
    'Cap': 'Truong_Cap',
    'Phuc': 'Han_Phuc',
    'Luong': 'Nhan_Luong',
    'Xu': 'Van_Xu',
    'Hy': 'Vien_Hy',
    'Tham': 'Tham_Phoi',
    'Truong_Tu_Voi': 'Truong_Tu',
    'Tu_Cung_Cuoi': 'Thai_Su_Tu',
    'Tu': 'Thai_Su_Tu',
    'Tu_Gian_Lam': 'Tu_Gian',
    'Han_Dung_Moi': 'Han_Dung',
    'Ho_Ban_Bung': 'Ho_Ban',
    'Ly_Ung_Moi': 'Lo_Tuc',
    'Tran_Vi_Biu_Moi': 'Tran_Vi',
    'Bo_Gia_Cach_Cuoi': 'La_Bo',
    'Tao_Cong_Cuoi': 'Tao_Thao',
    'Vien_Ngoi': 'Vien_Thieu',
    'Vo_Thay_Vay_Moi': 'Phu_Nhan',
    'Phu_Nhan_Khoc': 'Phu_Nhan',
    'Hai_Phu_Nhan_Lai': 'Hai_Phu_Nhan',
    'Ho_Nghiem_Khoc': 'Nghiem_Thi',
    'Ho_Nghiem': 'Nghiem_Thi',
    'Hau_Thanh_Khoc': 'Hau_Thanh',
    'De_Lai': 'Luu_De',
    'Thoi': 'Ly_Thoi',
    'Thoi_Mung': 'Ly_Thoi',
    'Di': 'Quach_Di',
    'Di_Gian_Lam': 'Quach_Di',
    'Nho': 'Ly_Nho',

    # Crowds & Secondary
    'Mot_Nguoi': 'Nguoi_Hau',
    'Nguoi_Ay': 'Nguoi_Hau',
    'Nguoi_Kia': 'Nguoi_Hau',
    'Quan_Canh': 'Linh_Canh',
    'Quan_Canh_Cua': 'Linh_Canh',
    'Linh_Canh_Cua': 'Linh_Canh',
    'Cac_Tuong_Ngac_Nhien': 'Tuong_Si',
    'Co_Hai_Tuong_Ra': 'Tuong_Si',
    'Moi_Vao_Trong_Trai': 'Tuong_Si',
    'Cung_Vao': 'Tuong_Si',
    'Cac_Tuong': 'Tuong_Si',
    'Moi_Nguoi': 'Quan_Si',
    'Hai_Nguoi_Dong_Thanh': 'Quan_Si',
    'Dong_Thanh_Luu_Quan': 'Luu_Bi',
    'Loi_The_Vuon_Dao': 'Luu_Bi',
    'Chot_Lai_Co_Nguoi': 'Quan_Si',
    'Van_Su': 'Quan_Si',
    'Quan_Bao': 'Quan_Si',
    'Quan_Do_Tham': 'Quan_Si',
    'Ten_Linh': 'Quan_Si',
    'Nguoi_Khan_Vang': 'Quan_Si',
    'Quan_Hau': 'Nguoi_Hau',
    'Quan_Hoang_Mon': 'Nguoi_Hau',
    'Nha_Bep': 'Nguoi_Hau',
    'Ta_Huu': 'Nguoi_Hau',
    'Nguoi_Nha_La_Ba_Sa': 'Nguoi_Hau',
    'Muu_Si_Vien_Thuat': 'Muu_Si',
    'Su': 'Su_Gia',
    'Toi': 'Tran_Cung',

    # Late Three Kingdoms & Posture/Action fixes
    'Bo_Ham_Ho': 'La_Bo',
    'Phu_Tron_Mat': 'Vuong_Doan',
    'Phu': 'Vuong_Doan',
    'Sieu': 'Ma_Sieu',
    'Van': 'Trinh_Van',
    'Du_Cuoi_Ha_Ha': 'Chu_Du',
    'Du_Lay_Xuong_Dat': 'Chu_Du',
    'Du_Noi_Gian_Len': 'Chu_Du',
    'Lai_Thay_Du': 'Chu_Du',
    'Ninh_Rut_Guom_Ra': 'Cam_Ninh',
    'Sieu_Tro_Roi_Len': 'Ma_Sieu',
    'Ngai_Ngang_Mat_Len': 'Dang_Ngai',
    'Vuong_Thi_Quat_Len': 'Vuong_Thi',
    'Tu_Mau_That_Kinh': 'Tu_Mau',
    'Trinh_Van_Lay': 'Trinh_Van',
    'Van_Lay': 'Trinh_Van',
    'Chiem_Cung_Khoc_Ma': 'Gia_Cat_Chiem',
    'Chiem': 'Gia_Cat_Chiem',
    'Vuong_Phu_Khoc_Ma': 'Vuong_Phu',
    'Phu_Khoc_Va': 'Vuong_Phu',
    'Tham_Khoc_Vang_Len': 'Luu_Tham',
    'Tham': 'Luu_Tham',
    'Luc_Khang_Trong_Thay': 'Luc_Khang',
    'Dien_Moi': 'Nguy_Dien',
    'Dien_Cung': 'Nguy_Dien',
    'Hoan_Cung': 'Ton_Hoan',
    'Hoan': 'Ton_Hoan',
    'Luu_Chuong_Cung': 'Luu_Chuong',
    'Tu_Cung': 'Thai_Su_Tu',
    'Dinh_Di_Cung': 'Dinh_Di',
    'Duc_Ve_Den_Tran': 'Bang_Duc',
    'Duong_Ky_Vao_Chau': 'Duong_Ky',
    'Manh_Hoach_Tro_Sang': 'Manh_Hoach',
    'La_Khoang_Ra_Ngua': 'La_Khoang',
    'Roi_Tung': 'Truong_Tung',
    'Tung': 'Truong_Tung',
    'Roi_Goi_Ma_Dai': 'Gia_Cat_Luong',
    'May_Sao_Dam_La': 'Tu_Ma_Y',
    'Ty_Dien_Ra_Ngua': 'Phi_Y',
    'Em_La_Tao_Hy': 'Tao_Hy',
    'Mot_Ong_Gia_Ra': 'Ong_Gia',
    'Nguoi_Co_Lai_Cu': 'Quan_Si',
    'Nguoi_Mac_Ao_Do': 'Nguoi_Hau',
    'Nguoi_Thanh_Nien': 'Nguoi_Hau',
    'Lai_Mot_Nguoi': 'Nguoi_Hau',
    'Lai_Mot_Nuoi': 'Nguoi_Hau',
    'Chu_Hau_Deu': 'Chu_Hau',
    'Tuong_Ta_Deu': 'Tuong_Si',
    'Quan_Than_Deu': 'Quan_Than',
    'Moi_Nguoi_Deu': 'Quan_Si',
    'Moi_Nguoi_Ve_Deu': 'Quan_Si',
    'Doa_Tu_Dai_Vuong': 'Doa_Tu',
    'Duong_Dai_Tuong': 'Duong_Phung',
    'Thai_Thu': 'Thai_Thu',
    'Thuong_Thu_Pho': 'Pho_Ho',
    'Thuong_Thu_Pho_Ho': 'Pho_Ho',
    'Dung_Len': 'Nguoi_Hau',
    'Buoc_Ra': 'Nguoi_Hau',
    'Gia_Quy': 'Gia_Quy',
    'Quy': 'Gia_Quy',
}

def clean_speaker_and_posture(sp_raw, mod_raw=""):
    """
    Strips posture actions, adverbs, verbs, and trailing/leading non-name words from raw speaker string.
    Returns: (cleaned_speaker, posture_action, combined_modifier)
    """
    clean_sp = sp_raw.strip()
    extracted_posture = []
    combined_mod = (mod_raw or "").strip()

    # Prefix strip loop
    changed = True
    while changed:
        changed = False
        lower_sp = clean_sp.lower()
        for pref in sorted(PREFIX_STRIP, key=len, reverse=True):
            if lower_sp.startswith(pref):
                clean_sp = clean_sp[len(pref):].strip()
                changed = True
                break

    all_suffixes = (
        sorted(POSTURE_ACTIONS, key=len, reverse=True) +
        sorted(EMOTION_MODIFIERS_EXTRA, key=len, reverse=True) +
        sorted(ADVERBS_EXTRA, key=len, reverse=True) +
        sorted(VERB_ACTIONS, key=len, reverse=True)
    )

    changed = True
    while changed:
        changed = False
        lower_sp = clean_sp.lower()
        for act in all_suffixes:
            if lower_sp.endswith(" " + act):
                part = clean_sp[len(clean_sp) - len(act):].strip()
                clean_sp = clean_sp[:-len(act)].strip()
                if act in POSTURE_ACTIONS:
                    extracted_posture.insert(0, part)
                else:
                    combined_mod = (part + " " + combined_mod).strip()
                changed = True
                break

    posture_action = " ".join(extracted_posture)
    return clean_sp, posture_action, combined_mod

def resolve_character_identity(speaker_str, quote_str, chap_num, prev_context=""):
    clean_sp, posture_act, extra_mod = clean_speaker_and_posture(speaker_str)
    lower_sp = clean_sp.lower().strip()

    if lower_sp == 'đức':
        if chap_num >= 60:
            return 'Bang_Duc', 'Bàng Đức', 'male', 'lao_hoa', 'anh_hung_hao_sang'
        else:
            return 'Trinh_Duc', 'Trình Dục', 'male', 'lao_hoa', 'khac_kho_lanh_lung'

    # Generic crowd / pronoun resolution
    if lower_sp in ('người ấy', 'người kia', 'một người', 'người', 'nười'):
        lower_q = quote_str.lower()
        lower_prev = prev_context.lower()

        if any(w in lower_prev for w in ('người hầu', 'hỏi tin', 'nhà trong', 'tướng phủ', 'buồng', 'hầu mới', 'hầu cận', 'gia nhân', 'tiểu đồng')):
            lower_sp = 'người hầu'
        elif any(w in lower_prev for w in ('lính', 'quân', 'canh cửa', 'cửa phủ')):
            lower_sp = 'lính canh'
        elif any(k in lower_q for k in ('ta là trương', 'ta họ trương', 'dực đức đây')):
            lower_sp = 'trương phi'
        elif any(k in lower_q for k in ('ta là quan', 'vân trường đây', 'ta họ quan')):
            lower_sp = 'quan vũ'
        elif any(k in lower_q for k in ('ta là lưu', 'huyền đức đây', 'ta họ lưu')):
            lower_sp = 'lưu bị'
        elif any(k in lower_q for k in ('ta là tào', 'mạnh đức đây')):
            lower_sp = 'tào tháo'
        elif any(k in lower_q for k in ('ta là lã', 'phụng tiên đây')):
            lower_sp = 'lã bố'
        else:
            lower_sp = 'người hầu'
    elif lower_sp in ('lại', 'mới', 'bèn', 'rồi', 'chợt', 'đoạn'):
        lower_prev = prev_context.lower()
        if any(w in lower_prev for w in ('khổng minh', 'quân sư', 'lượng')):
            lower_sp = 'gia cát lượng'
        elif any(w in lower_prev for w in ('lưu bị', 'huyền đức', 'hoàng thúc', 'tiên chủ')):
            lower_sp = 'lưu bị'
        elif any(w in lower_prev for w in ('trương phi', 'dực đức', 'phi')):
            lower_sp = 'trương phi'
        elif any(w in lower_prev for w in ('quan vũ', 'vân trường', 'quan công')):
            lower_sp = 'quan vũ'
        elif any(w in lower_prev for w in ('tôn sách', 'bá phù')):
            lower_sp = 'tôn sách'
        elif any(w in lower_prev for w in ('tôn quyền', 'trọng mưu')):
            lower_sp = 'tôn quyền'
        elif any(w in lower_prev for w in ('chu du', 'công cẩn')):
            lower_sp = 'chu du'
        elif any(w in lower_prev for w in ('tào tháo', 'mạnh đức', 'thừa tướng')):
            lower_sp = 'tào tháo'
        elif any(w in lower_prev for w in ('tư mã ý', 'trọng đạt')):
            lower_sp = 'tư mã ý'
        elif any(w in lower_prev for w in ('khương duy', 'bá ước')):
            lower_sp = 'khương duy'
        elif any(w in lower_prev for w in ('hồ ban')):
            lower_sp = 'hồ ban'
        else:
            lower_sp = 'người hầu'

    cid = 'Unknown'
    cname = clean_sp.strip()
    gender = 'male'
    temp = 'anh_hung_hao_sang'

    if lower_sp in KNOWN_CHARACTERS:
        cid, cname, gender, temp = KNOWN_CHARACTERS[lower_sp]
    else:
        matched = None
        for k in sorted(KNOWN_CHARACTERS.keys(), key=lambda x: -len(x)):
            if k == lower_sp or (len(k) >= 3 and k in lower_sp):
                matched = KNOWN_CHARACTERS[k]
                break
        if matched:
            cid, cname, gender, temp = matched
        else:
            raw_id = vn_to_ascii_id(clean_sp)
            if raw_id in CANONICAL_CHAR_REMAP:
                target_id = CANONICAL_CHAR_REMAP[raw_id]
                cid = target_id
                cname = target_id.replace('_', ' ')
                for k, v in KNOWN_CHARACTERS.items():
                    if v[0] == target_id:
                        cid, cname, gender, temp = v
                        break
            else:
                cid = raw_id
                cname = clean_sp.strip().title()
                if any(w in lower_sp for w in ('bà', 'mẹ', 'nàng', 'phu nhân', 'thái hậu', 'hoàng hậu', 'cơ', 'nữ', 'thị', 'gái')):
                    gender = 'female'
                else:
                    gender = 'male'
                temp = 'anh_hung_hao_sang'

    if cid in CANONICAL_CHAR_REMAP:
        target_id = CANONICAL_CHAR_REMAP[cid]
        cid = target_id
        cname = target_id.replace('_', ' ')
        for k, v in KNOWN_CHARACTERS.items():
            if v[0] == target_id:
                cid, cname, gender, temp = v
                break

    # Age stage logic
    if cid in ('Hoang_Trung', 'Nghiem_Nhan', 'Kieu_Huyen', 'Vuong_Doan', 'Lu_Thuc', 'Dinh_Nguyen', 'Dong_Thai_Hau', 'Ong_Gia', 'Nam_Hoa_Lao_Tien', 'Vu_Cat'):
        age_stage = 'lao_hoa'
    elif cid in ('Luu_Bieu', 'Khoai_Luong', 'Hoang_To', 'Dong_Trac', 'Ha_Tien', 'Vien_Thieu', 'Dao_Khiem', 'Cong_Ton_Toan', 'Dong_Thua'):
        age_stage = 'trung_nien'
    elif cid in ('Gia_Cat_Luong', 'Tu_Ma_Y'):
        if chap_num <= 55:
            age_stage = 'thanh_xuan'
        elif chap_num <= 90:
            age_stage = 'trung_nien'
        else:
            age_stage = 'lao_hoa'
    elif cid in ('Luu_Thien', 'Tao_Phi', 'Tao_Thuc', 'Ton_Sach', 'Ton_Quyen', 'Chu_Du', 'Quan_Binh', 'Quan_Hung', 'Truong_Bao_Shu', 'Dieu_Thuyen'):
        if chap_num <= 40:
            age_stage = 'thanh_xuan'
        elif chap_num <= 80:
            age_stage = 'trung_nien'
        else:
            age_stage = 'lao_hoa'
    elif cid in ('Han_Hien_De', 'Thieu_De', 'Tran_Luu_Vuong'):
        if chap_num <= 20:
            age_stage = 'au_tho'
        elif chap_num <= 40:
            age_stage = 'thanh_xuan'
        else:
            age_stage = 'trung_nien'
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

                            clean_sp, posture_act, extra_mod = clean_speaker_and_posture(sp_raw, mod_s)
                            full_mod = (extra_mod + " " + mod_s).strip()

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

                            lower_clean_sp = clean_sp.lower()
                            is_narrator_quote = (
                                (lower_clean_sp in ('lại', 'lai') and vb_s == 'nói')
                                or (lower_clean_sp in ('lại', 'lai') and q_txt.lower().startswith(('đến ', 'tư mã ', 'dương nghi ', 'ngụy diên ', 'chung hội ', 'đặng ngải ', 'hậu chủ ', 'khương duy ', 'ngô chủ ', 'vương tuấn ')))
                                or lower_clean_sp.startswith(('trong thư', 'thư lại', 'thư rằng', 'trong chiếu', 'đời sau có thơ', 'người sau có thơ', 'có thơ rằng', 'đức khổng tử có', 'trong binh pháp có', 'lại nói', 'lại nhắc'))
                                or lower_clean_sp in ('lời thề vườn đào', 'cho nên', 'vì thế', 'mày sao dám la', 'đệ thường nghe', 'rồi thấy', 'người cổ lại cũ', 'vứt xuống đất rồi')
                            )
                            if is_narrator_quote:
                                v, pt, rt, lp, teq = get_narrator_acoustic("intimate")
                                theatrical_lines.append({
                                    "line_id": line_id,
                                    "chunk_id": chunk_idx,
                                    "type": "narrator",
                                    "speaker": "Narrator",
                                    "narrative_mode": "intimate",
                                    "text": q_txt,
                                    "voice": v,
                                    "pitch": pt,
                                    "rate": rt,
                                    "lead_in_pause": "0.55s",
                                    "timbre_eq": teq
                                })
                                character_bible["Narrator"]["narrative_modes"].add("intimate")
                                line_id += 1
                                total_narrators += 1
                                last_pos = m_sub.end()
                                continue

                            prev_ctx = n_lead
                            cid, cname, gender, age_stage, temp = resolve_character_identity(clean_sp, q_txt, chap_idx, prev_context=prev_ctx)
                            emotion = detect_emotion(full_mod, vb_s, q_txt)
                            voice, pitch, rate = compute_acoustic_tone(age_stage, temp, emotion, gender)
                            char_timbre = resolve_character_timbre_eq(cid, gender, age_stage, temp, emotion)

                            prev_type = theatrical_lines[-1]["type"] if theatrical_lines else "narrator"
                            prev_sp = theatrical_lines[-1]["speaker"] if theatrical_lines else "Narrator"
                            d_lead_in = compute_contextual_handoff(prev_type, "dialogue", cid, prev_sp, vb_s, full_mod, emotion)

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
                                "lead_in_pause": "0.48s",
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

                after_intro = p[m_intro.end():].strip()
                if after_intro:
                    sublines = [l.strip() for l in after_intro.splitlines() if l.strip()]
                    for verse_line in sublines:
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
                else:
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

                    clean_sp, posture_act, extra_mod = clean_speaker_and_posture(speaker_raw, modifier)
                    full_mod = (extra_mod + " " + modifier).strip()

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

                    lower_clean_sp = clean_sp.lower()
                    is_narrator_quote = (
                        (lower_clean_sp in ('lại', 'lai', 'thấy', 'rồi thấy') and verb == 'nói')
                        or (lower_clean_sp in ('lại', 'lai') and quote_text.lower().startswith(('đến ', 'tư mã ', 'dương nghi ', 'ngụy diên ', 'chung hội ', 'đặng ngải ', 'hậu chủ ', 'khương duy ', 'ngô chủ ', 'vương tuấn ')))
                        or lower_clean_sp.startswith(('trong thư', 'thư lại', 'thư rằng', 'trong chiếu', 'đời sau có thơ', 'người sau có thơ', 'có thơ rằng', 'đức khổng tử có', 'trong binh pháp có', 'lại nói', 'lại nhắc'))
                        or lower_clean_sp in ('lời thề vườn đào', 'cho nên', 'vì thế', 'mày sao dám la', 'đệ thường nghe', 'rồi thấy', 'người cổ lại cũ', 'vứt xuống đất rồi')
                    )
                    if is_narrator_quote:
                        v, pt, rt, lp, teq = get_narrator_acoustic(macro_mode)
                        theatrical_lines.append({
                            "line_id": line_id,
                            "chunk_id": chunk_idx,
                            "type": "narrator",
                            "speaker": "Narrator",
                            "narrative_mode": macro_mode,
                            "text": quote_text,
                            "voice": v,
                            "pitch": pt,
                            "rate": rt,
                            "lead_in_pause": "0.55s",
                            "timbre_eq": teq
                        })
                        character_bible["Narrator"]["narrative_modes"].add(macro_mode)
                        line_id += 1
                        total_narrators += 1
                        last_pos = m.end()
                        continue

                    prev_ctx = (before_lead + " " + lead_text) if before_lead else lead_text
                    cid, cname, gender, age_stage, temp = resolve_character_identity(clean_sp, quote_text, chap_idx, prev_context=prev_ctx)
                    emotion = detect_emotion(full_mod, verb, quote_text)
                    voice, pitch, rate = compute_acoustic_tone(age_stage, temp, emotion, gender)
                    char_timbre_eq = resolve_character_timbre_eq(cid, gender, age_stage, temp, emotion)

                    prev_type = theatrical_lines[-1]["type"] if theatrical_lines else "narrator"
                    prev_sp = theatrical_lines[-1]["speaker"] if theatrical_lines else "Narrator"
                    d_lead_in = compute_contextual_handoff(prev_type, "dialogue", cid, prev_sp, verb, full_mod, emotion)

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
    book_level_characters = {}
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
            for c_id, c_info in b_data.get("characters", {}).items():
                if c_id != "Narrator":
                    unique_characters_book.add(c_id)
                    if c_id not in book_level_characters:
                        book_level_characters[c_id] = dict(c_info)
                        book_level_characters[c_id]["chapters"] = [folder_name]
                        book_level_characters[c_id]["total_dialogues"] = c_info.get("dialogue_count", 0)
                    else:
                        if folder_name not in book_level_characters[c_id].get("chapters", []):
                            book_level_characters[c_id].setdefault("chapters", []).append(folder_name)
                        book_level_characters[c_id]["total_dialogues"] = book_level_characters[c_id].get("total_dialogues", 0) + c_info.get("dialogue_count", 0)

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

    # Export aggregated Master Theatrical Bible at root of book
    master_bible_path = os.path.join(book_dir, ".theatrical_bible.json")
    with open(master_bible_path, "w", encoding="utf-8") as mbf:
        json.dump({
            "book": os.path.basename(book_dir),
            "updated_at": datetime.datetime.now().isoformat(),
            "characters_count": len(book_level_characters),
            "characters": book_level_characters
        }, mbf, indent=2, ensure_ascii=False)

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
