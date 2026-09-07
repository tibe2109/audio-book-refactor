#!/usr/bin/env bash
# ==============================================================================
# Universal Audiobook Pipeline - Linux & macOS Auto-Setup Wizard (v2.0)
# ==============================================================================
set -e

# Màu sắc hiển thị
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}================================================================================${NC}"
echo -e "${BLUE}   HỆ THỐNG SẢN XUẤT SÁCH NÓI VẠN NĂNG - UNIVERSAL AUDIOBOOK PIPELINE v2.0     ${NC}"
echo -e "${BLUE}   CÀI ĐẶT TỰ ĐỘNG CHO LINUX & macOS (ONE-CLICK SETUP WIZARD)                   ${NC}"
echo -e "${BLUE}================================================================================${NC}"
echo ""

# 1. Kiểm tra Python
echo -e "${YELLOW}[*] BƯỚC 1/4: Đang kiểm tra môi trường Python 3...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[!] LỖI: Không tìm thấy python3 trên hệ thống!${NC}"
    echo -e "[*] Vui lòng cài đặt Python 3.10+ (Ví dụ: sudo apt install python3 python3-venv python3-pip)"
    exit 1
fi

PY_VER=$(python3 --version)
echo -e "${GREEN}[✓] Đã phát hiện: $PY_VER${NC}"

# 2. Khởi tạo virtual environment
echo ""
echo -e "${YELLOW}[*] BƯỚC 2/4: Đang kiểm tra / khởi tạo môi trường ảo Python (venv)...${NC}"
if [ ! -f "venv/bin/activate" ]; then
    echo "    -> Đang tạo môi trường ảo mới (venv)..."
    python3 -m venv venv
    echo -e "${GREEN}[✓] Khởi tạo thành công thư mục venv.${NC}"
else
    echo -e "${GREEN}[✓] Môi trường ảo venv đã sẵn sàng.${NC}"
fi

# 3. Kích hoạt venv và cài đặt dependencies
echo ""
echo -e "${YELLOW}[*] BƯỚC 3/4: Đang kích hoạt venv và cài đặt thư viện cần thiết...${NC}"
source venv/bin/activate
pip install --upgrade pip --quiet
echo "    -> Đang cài đặt thư viện từ requirements.txt..."
pip install -r requirements.txt
echo -e "${GREEN}[✓] Toàn bộ thư viện xử lý âm thanh AI đã được cài đặt thành công!${NC}"

# 4. Kiểm tra FFmpeg
echo ""
echo -e "${YELLOW}[*] BƯỚC 4/4: Đang kiểm tra công cụ chuyển đổi âm thanh FFmpeg...${NC}"
if command -v ffmpeg &> /dev/null; then
    echo -e "${GREEN}[✓] Đã phát hiện FFmpeg trong hệ thống PATH!${NC}"
else
    echo -e "${YELLOW}[!] Chưa có FFmpeg hệ thống.${NC}"
    echo "    -> Thư viện 'imageio-ffmpeg' (Python fallback) đã sẵn sàng hoạt động tự động."
    echo "    -> (Khuyến nghị) Bạn có thể cài thêm FFmpeg native để đạt tốc độ tối đa:"
    echo "       • Ubuntu/Debian: sudo apt update && sudo apt install -y ffmpeg"
    echo "       • Arch Linux:    sudo pacman -S ffmpeg"
    echo "       • macOS:         brew install ffmpeg"
fi

# Cấp quyền thực thi cho các file shell
chmod +x run.sh 2>/dev/null || true
chmod +x setup.sh 2>/dev/null || true

echo ""
echo -e "${GREEN}================================================================================${NC}"
echo -e "${GREEN}   🎉 CÀI ĐẶT HOÀN TẤT 100%! HỆ THỐNG ĐÃ SẴN SÀNG VẬN HÀNH TRÊN LINUX / macOS. ${NC}"
echo -e "${GREEN}================================================================================${NC}"
echo ""
echo -e "  Bạn có thể khởi động hệ thống bằng lệnh:"
echo -e "    ${BLUE}./run.sh${NC} (để mở menu giao diện điều khiển)"
echo -e "    Hoặc ra lệnh cho AI trong Antigravity, Claude Code, Cursor, Codex..."
echo ""
