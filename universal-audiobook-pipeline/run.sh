#!/usr/bin/env bash
# ==============================================================================
# Universal Audiobook Runner v2.0 - Linux & macOS Interactive CLI
# ==============================================================================
set -e

# Kích hoạt venv
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "[!] Chưa phát hiện môi trường ảo venv. Đang tự động chạy setup.sh..."
    bash setup.sh
    source venv/bin/activate
fi

# Màu sắc
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

while true; do
    clear || true
    echo -e "${CYAN}================================================================================${NC}"
    echo -e "${CYAN}      HỆ THỐNG SẢN XUẤT SÁCH NÓI TỰ ĐỘNG VẠN NĂNG (UNIVERSAL AUDIOBOOK v2.0)    ${NC}"
    echo -e "${CYAN}================================================================================${NC}"
    echo ""
    echo "  [1] Xử lý tự động 1 chương cụ thể (Kiểm toán QC -> Thu âm Song thanh -> Hòa âm BGM)"
    echo "  [2] Xử lý tự động TOÀN BỘ các chương chưa hoàn thành"
    echo "  [3] Kiểm toán chất lượng kịch bản (Thẩm định 7 Cổng Hard Quality Gates)"
    echo "  [4] Khởi tạo dự án sách mới từ file PDF (Bước 01: Extract Structure)"
    echo "  [5] Kiểm tra hoặc Cài đặt lại môi trường hệ thống (Setup/Repair)"
    echo "  [0] Thoát"
    echo ""
    echo -e "${CYAN}================================================================================${NC}"
    read -p "Nhập lựa chọn của bạn (1/2/3/4/5/0): " choice

    case $choice in
        1)
            echo ""
            read -p "Nhập thư mục sách (mặc định: input_books): " bdir
            bdir=${bdir:-input_books}
            read -p "Nhập tên thư mục chương cần xử lý (ví dụ: 01-chapter-1): " chap
            if [ -n "$chap" ]; then
                echo -e "${YELLOW}[*] Đang kích hoạt dây chuyền tự động cho chương: $chap ...${NC}"
                python3 core/antigravity_audiobook_pipeline.py --book_dir "$bdir" --chapter "$chap"
            fi
            read -p "Bấm phím Enter để tiếp tục..." dummy
            ;;
        2)
            echo ""
            read -p "Nhập thư mục sách (mặc định: input_books): " bdir
            bdir=${bdir:-input_books}
            echo -e "${YELLOW}[*] Đang khởi chạy tự động cho tất cả các chương chưa hoàn thành...${NC}"
            python3 core/antigravity_audiobook_pipeline.py --book_dir "$bdir" --all
            read -p "Bấm phím Enter để tiếp tục..." dummy
            ;;
        3)
            echo ""
            read -p "Nhập thư mục sách (mặc định: input_books): " bdir
            bdir=${bdir:-input_books}
            read -p "Nhập tên thư mục chương cần kiểm toán QC: " chap
            if [ -n "$chap" ]; then
                python3 -c "import os, sys; sys.path.insert(0, 'core'); from universal_audiobook_workflow import UniversalAudiobookWorkflow; wf = UniversalAudiobookWorkflow('$bdir', '$chap'); res = wf.audit_quality_gates(); print('\n=== KẾT QUẢ KIỂM TOÁN QC ==='); print('Đạt chuẩn:', res.get('passed')); print('Chi tiết:', res)"
            fi
            read -p "Bấm phím Enter để tiếp tục..." dummy
            ;;
        4)
            echo ""
            read -p "Nhập đường dẫn file PDF sách gốc: " pdf
            read -p "Nhập mã định danh sách (ví dụ: Dac-Nhan-Tam): " slug
            if [ -n "$pdf" ]; then
                echo -e "${YELLOW}[*] Đang bóc tách cấu trúc sách PDF...${NC}"
                python3 .agy/skills/arf_01_pdf_structure_extractor/scripts/extract_structure.py --pdf_path "$pdf" --output_dir "input_books" --book_slug "$slug"
            fi
            read -p "Bấm phím Enter để tiếp tục..." dummy
            ;;
        5)
            bash setup.sh
            ;;
        0)
            echo "Tạm biệt!"
            exit 0
            ;;
        *)
            echo -e "${RED}[!] Lựa chọn không hợp lệ.${NC}"
            sleep 1
            ;;
    esac
done
