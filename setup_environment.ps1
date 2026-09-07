<#
.SYNOPSIS
    Script khởi tạo môi trường tự động Universal Audiobook Pipeline trên Windows (PowerShell).
#>
$ErrorActionPreference = "Continue"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "    UNIVERSAL AUDIOBOOK PIPELINE - POWERSHELL SETUP WIZARD (v2.0)" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan

# 1. Kiểm tra Python
Write-Host "`n[*] BƯỚC 1/4: Đang kiểm tra phiên bản Python..." -ForegroundColor Yellow
try {
    $pyVer = python --version 2>&1
    Write-Host "[✓] Phát hiện: $pyVer" -ForegroundColor Green
} catch {
    Write-Host "[!] LỖI: Không tìm thấy Python trong hệ thống. Vui lòng cài đặt Python >= 3.10 từ python.org" -ForegroundColor Red
    pause
    exit 1
}

# 2. Tạo Virtual Environment
$venvPath = Join-Path $PSScriptRoot "venv"
Write-Host "`n[*] BƯỚC 2/4: Đang kiểm tra môi trường ảo venv..." -ForegroundColor Yellow
if (-not (Test-Path (Join-Path $venvPath "Scripts\activate.ps1"))) {
    Write-Host "    -> Đang khởi tạo môi trường ảo Python (venv)..." -ForegroundColor Gray
    python -m venv $venvPath
    Write-Host "[✓] Đã tạo venv tại: $venvPath" -ForegroundColor Green
} else {
    Write-Host "[✓] Môi trường ảo venv đã sẵn sàng." -ForegroundColor Green
}

# 3. Kích hoạt venv và cài đặt gói
$pipExe = Join-Path $venvPath "Scripts\pip.exe"
$pythonExe = Join-Path $venvPath "Scripts\python.exe"

Write-Host "`n[*] BƯỚC 3/4: Đang nâng cấp pip và cài đặt dependencies..." -ForegroundColor Yellow
& $pipExe install --upgrade pip --quiet
& $pipExe install -r (Join-Path $PSScriptRoot "requirements.txt")
Write-Host "[✓] Hoàn tất cài đặt toàn bộ dependencies." -ForegroundColor Green

# 4. Kiểm tra và tải FFmpeg
Write-Host "`n[*] BƯỚC 4/4: Đang kiểm tra công cụ FFmpeg..." -ForegroundColor Yellow
$ffmpegToolPath = Join-Path $PSScriptRoot "tools\ffmpeg\ffmpeg.exe"
$sysFfmpeg = Get-Command "ffmpeg" -ErrorAction SilentlyContinue

if ($sysFfmpeg) {
    Write-Host "[✓] Đã phát hiện FFmpeg trong hệ thống PATH: $($sysFfmpeg.Source)" -ForegroundColor Green
} elseif (Test-Path $ffmpegToolPath) {
    Write-Host "[✓] Đã phát hiện FFmpeg cục bộ: $ffmpegToolPath" -ForegroundColor Green
} elseif (Test-Path (Join-Path $PSScriptRoot "ffmpeg-7.0.2-amd64-static\ffmpeg.exe")) {
    Write-Host "[✓] Đã phát hiện FFmpeg tại thư mục tĩnh ffmpeg-7.0.2-amd64-static" -ForegroundColor Green
} else {
    Write-Host "[!] Đang tự động tải FFmpeg portable..." -ForegroundColor Yellow
    & $pythonExe (Join-Path $PSScriptRoot "tools\download_ffmpeg.py")
}

Write-Host "`n================================================================================" -ForegroundColor Cyan
Write-Host "    🎉 KHỞI TẠO HOÀN TẤT THÀNH CÔNG! HỆ THỐNG ĐÃ SẴN SÀNG." -ForegroundColor Green
Write-Host "    Bạn có thể chạy dự án bằng file: .\run_audiobook.bat" -ForegroundColor White
Write-Host "================================================================================" -ForegroundColor Cyan
