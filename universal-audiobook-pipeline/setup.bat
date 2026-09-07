@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion
title Universal Audiobook Pipeline - Windows Installer

echo ================================================================================
echo    HỆ THỐNG SẢN XUẤT SÁCH NÓI VẠN NĂNG - UNIVERSAL AUDIOBOOK PIPELINE v2.0
echo    CÀI ĐẶT TỰ ĐỘNG 1-CLICK (WINDOWS SETUP WIZARD)
echo ================================================================================
echo.

:: 1. Kiểm tra Python
echo [*] BƯỚC 1/4: Đang kiểm tra môi trường Python...
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo.
    echo [!] LỖI: Máy tính của bạn chưa cài đặt Python hoặc chưa bật PATH!
    echo [*] Vui lòng tải và cài đặt Python 3.10 trở lên tại: https://www.python.org/downloads/
    echo [*] LƯU Ý QUAN TRỌNG: Khi cài, nhớ TÍCH CHỌN ô "Add Python to PATH"!
    echo.
    pause
    exit /b 1
)

for /f "tokens=2 delims= " %%i in ('python --version 2^>^&1') do set PY_VER=%%i
echo [✓] Đã phát hiện Python phiên bản: !PY_VER!

:: 2. Khởi tạo môi trường ảo (Virtual Environment)
echo.
echo [*] BƯỚC 2/4: Đang kiểm tra / khởi tạo môi trường ảo Python (venv)...
if not exist "venv\Scripts\activate.bat" (
    echo     -> Đang tạo môi trường ảo mới (venv)...
    python -m venv venv
    if %ERRORLEVEL% neq 0 (
        echo [!] Lỗi khi tạo venv. Vui lòng kiểm tra quyền ghi trên ổ đĩa.
        pause
        exit /b 1
    )
    echo [✓] Khởi tạo thành công thư mục venv.
) else (
    echo [✓] Môi trường ảo venv đã sẵn sàng.
)

:: 3. Kích hoạt venv và cài đặt dependencies
echo.
echo [*] BƯỚC 3/4: Đang kích hoạt venv và cài đặt các thư viện cần thiết...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip --quiet
echo     -> Đang cài đặt thư viện từ requirements.txt...
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo [!] Cảnh báo: Có gói thư viện cài đặt chưa hoàn tất. Đang thử lại...
    pip install edge-tts mutagen pypdf pdfplumber imageio-ffmpeg requests tqdm
)
echo [✓] Toàn bộ thư viện xử lý âm thanh AI đã được cài đặt thành công!

:: 4. Kiểm tra FFmpeg
echo.
echo [*] BƯỚC 4/4: Đang kiểm tra công cụ chuyển đổi âm thanh FFmpeg...
where ffmpeg >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo [✓] Đã phát hiện FFmpeg trong hệ thống PATH của máy tính.
) else (
    if exist "tools\ffmpeg\ffmpeg.exe" (
        echo [✓] Đã phát hiện FFmpeg cục bộ tại: tools\ffmpeg\ffmpeg.exe
    ) else (
        echo [!] Máy tính chưa có FFmpeg. Đang tự động tải bản FFmpeg Portable...
        python tools\download_ffmpeg.py
    )
)

echo.
echo ================================================================================
echo    🎉 CÀI ĐẶT HOÀN TẤT 100%! HỆ THỐNG ĐÃ SẴN SÀNG VẬN HÀNH.
echo ================================================================================
echo.
echo  Bạn có thể bắt đầu sản xuất sách nói ngay bằng cách:
echo    1. Nhấp đúp chuột vào file: run.bat (để mở menu chọn nhanh)
echo    2. Hoặc ra lệnh trực tiếp cho AI trong Antigravity IDE / Claude / ChatGPT / Cursor
echo.
pause
