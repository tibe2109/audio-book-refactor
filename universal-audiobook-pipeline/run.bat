@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion
title Universal Audiobook Runner v2.0

:: Kiểm tra và kích hoạt môi trường ảo
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo [!] Chưa phát hiện môi trường ảo venv. Đang tự động chạy setup.bat...
    call setup.bat
    if exist "venv\Scripts\activate.bat" (
        call venv\Scripts\activate.bat
    ) else (
        echo [!] Lỗi: Không thể khởi tạo venv.
        pause
        exit /b 1
    )
)

:menu
cls
echo ================================================================================
echo      HỆ THỐNG SẢN XUẤT SÁCH NÓI TỰ ĐỘNG VẠN NĂNG (UNIVERSAL AUDIOBOOK v2.0)
echo ================================================================================
echo.
echo   [1] Xử lý tự động 1 chương cụ thể (Kiểm toán QC -^> Thu âm Song thanh -^> Hòa âm BGM)
echo   [2] Xử lý tự động TOÀN BỘ các chương chưa hoàn thành
echo   [3] Kiểm toán chất lượng kịch bản (Thẩm định 7 Cổng Hard Quality Gates)
echo   [4] Khởi tạo dự án sách mới từ file PDF (Bước 01: Extract Structure)
echo   [5] Kiểm tra hoặc Cài đặt lại môi trường hệ thống (Setup/Repair)
echo   [0] Thoát
echo.
echo ================================================================================
set /p choice="Nhập lựa chọn của bạn (1/2/3/4/5/0): "

if "%choice%"=="1" (
    echo.
    set /p bdir="Nhập thư mục sách (mặc định: input_books): "
    if "!bdir!"=="" set bdir=input_books
    set /p chap="Nhập tên thư mục chương cần xử lý (ví dụ: 01-chapter-1): "
    if not "!chap!"=="" (
        echo.
        echo [*] Đang kích hoạt dây chuyền tự động cho chương: !chap! ...
        python core\antigravity_audiobook_pipeline.py --book_dir "!bdir!" --chapter "!chap!"
    )
    echo.
    pause
    goto menu
)

if "%choice%"=="2" (
    echo.
    set /p bdir="Nhập thư mục sách (mặc định: input_books): "
    if "!bdir!"=="" set bdir=input_books
    echo [*] Đang khởi chạy tự động cho tất cả các chương chưa hoàn thành...
    python core\antigravity_audiobook_pipeline.py --book_dir "!bdir!" --all
    echo.
    pause
    goto menu
)

if "%choice%"=="3" (
    echo.
    set /p bdir="Nhập thư mục sách (mặc định: input_books): "
    if "!bdir!"=="" set bdir=input_books
    set /p chap="Nhập tên thư mục chương cần kiểm toán QC: "
    if not "!chap!"=="" (
        python -c "import os, sys; sys.path.insert(0, 'core'); from universal_audiobook_workflow import UniversalAudiobookWorkflow; wf = UniversalAudiobookWorkflow('!bdir!', '!chap!'); res = wf.audit_quality_gates(); print('\n=== KẾT QUẢ KIỂM TOÁN QC ==='); print('Đạt chuẩn:', res.get('passed')); print('Chi tiết:', res)"
    )
    echo.
    pause
    goto menu
)

if "%choice%"=="4" (
    echo.
    set /p pdf="Nhập đường dẫn file PDF sách gốc: "
    set /p slug="Nhập mã định danh sách (ví dụ: Dac-Nhan-Tam): "
    if not "!pdf!"=="" (
        echo [*] Đang bóc tách cấu trúc sách PDF...
        python .agy\skills\arf_01_pdf_structure_extractor\scripts\extract_structure.py --pdf_path "!pdf!" --output_dir "input_books" --book_slug "!slug!"
    )
    echo.
    pause
    goto menu
)

if "%choice%"=="5" (
    call setup.bat
    goto menu
)

if "%choice%"=="0" exit /b 0

goto menu
