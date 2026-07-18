"""
Script debug: xem nội dung từng trang đầu để xác định cấu trúc PDF
"""
import pdfplumber
import sys

PDF_PATH = r"D:\Solution\Audio-Book-Refactor\Docs\Eat That Frog! 21 Great Ways to Stop Procrastinating and Get More Done in Less Time ( PDFDrive ).pdf"

with pdfplumber.open(PDF_PATH) as pdf:
    total = len(pdf.pages)
    print(f"Total pages: {total}")
    
    # In 5 dòng đầu của mỗi trang từ 10-30 để xác định cấu trúc
    for i in range(9, 35):
        page = pdf.pages[i]
        text = page.extract_text() or ""
        lines = [l.strip() for l in text.split('\n') if l.strip()][:4]
        print(f"\n--- Trang {i+1} ---")
        for l in lines:
            print(f"  {l[:100]}")
