"""
Bước 3 (Fixed): Đọc PDF và phân tách thành các chương thô.
- Bỏ qua trang TOC (trang 12-13)
- Tìm tiêu đề chương thực sự trong nội dung (từ trang 14 trở đi)
- Lưu raw_original.txt theo từng chương
"""
import os
import re
import pdfplumber

PDF_PATH = r"D:\Solution\Audio-Book-Refactor\Docs\Eat That Frog! 21 Great Ways to Stop Procrastinating and Get More Done in Less Time ( PDFDrive ).pdf"
OUTPUT_BASE = r"D:\Solution\Audio-Book-Refactor\Kich-ban-clipchamp\Eat-that-frog"

# TOC kết thúc ở trang 13, nội dung thật bắt đầu từ trang 14 (index 13)
TOC_END_PAGE = 13  # 1-indexed, trang cuối TOC

# Cấu trúc chương - (folder, pattern để nhận dạng đầu trang)
# Pattern là chuỗi đầu tiên xuất hiện trên trang bắt đầu chương
CHAPTERS = [
    ("00-Preface",      r"^Preface$"),
    ("01-Intro",        r"^Introduction:\s*Eat That Frog"),
    ("02-Chuong-01",    r"^1\s+Set the Table"),
    ("03-Chuong-02",    r"^2\s+Plan Every Day in Advance"),
    ("04-Chuong-03",    r"^3\s+Apply the 80/20 Rule to Everything"),
    ("05-Chuong-04",    r"^4\s+Consider the Consequences"),
    ("06-Chuong-05",    r"^5\s+Practice Creative Procrastination"),
    ("07-Chuong-06",    r"^6\s+Use the ABCDE Method Continually"),
    ("08-Chuong-07",    r"^7\s+Focus on Key Result Areas"),
    ("09-Chuong-08",    r"^8\s+Apply the Law of Three"),
    ("10-Chuong-09",    r"^9\s+Prepare Thoroughly Before You Begin"),
    ("11-Chuong-10",    r"^10\s+Take It One Oil Barrel at a Time"),
    ("12-Chuong-11",    r"^11\s+Upgrade Your Key Skills"),
    ("13-Chuong-12",    r"^12\s+Identify Your Key Constraints"),
    ("14-Chuong-13",    r"^13\s+Put the Pressure on Yourself"),
    ("15-Chuong-14",    r"^14\s+Motivate Yourself into Action"),
    ("16-Chuong-15",    r"^15\s+Technology Is a Terrible Master"),
    ("17-Chuong-16",    r"^16\s+Technology Is a Wonderful Servant"),
    ("18-Chuong-17",    r"^17\s+Focus Your Attention"),
    ("19-Chuong-18",    r"^18\s+Slice and Dice the Task"),
    ("20-Chuong-19",    r"^19\s+Create Large Chunks of Time"),
    ("21-Chuong-20",    r"^20\s+Develop a Sense of Urgency"),
    ("22-Chuong-21",    r"^21\s+Single Handle Every Task"),
    ("23-Conclusion",   r"^Conclusion:"),
]

def extract_pages(pdf_path):
    """Đọc toàn bộ trang PDF, trả về list [(page_num_1indexed, text)]."""
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            pages.append((i + 1, text))
    return pages

def find_chapter_starts(pages, chapters, toc_end):
    """
    Tìm trang đầu của mỗi chương trong nội dung thật (sau TOC).
    Kiểm tra xem dòng đầu tiên của trang có khớp với pattern chương không.
    """
    chapter_starts = {}  # folder -> page_num
    
    for page_num, text in pages:
        if page_num <= toc_end:
            continue  # Bỏ qua trang TOC
        
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        if not lines:
            continue
        
        first_line = lines[0]
        
        for folder, pattern in chapters:
            if folder in chapter_starts:
                continue  # Đã tìm thấy rồi
            if re.match(pattern, first_line, re.IGNORECASE):
                chapter_starts[folder] = page_num
                print(f"  ✓ Tìm thấy [{folder}] tại trang {page_num}: '{first_line[:60]}'")
                break
    
    return chapter_starts

def save_chapter(folder_name, text, output_base):
    """Lưu raw text vào thư mục chương."""
    chapter_dir = os.path.join(output_base, folder_name)
    os.makedirs(chapter_dir, exist_ok=True)
    raw_path = os.path.join(chapter_dir, "raw_original.txt")
    with open(raw_path, 'w', encoding='utf-8') as f:
        f.write(text.strip())
    size = len(text.strip())
    print(f"     => Đã lưu: {raw_path} ({size:,} ký tự)")
    return size

def main():
    print("=" * 60)
    print("BƯỚC 3 (Fixed): Đọc PDF và Phân tách Chương")
    print("=" * 60)

    os.makedirs(OUTPUT_BASE, exist_ok=True)

    print(f"\n📖 Đang đọc PDF...")
    pages = extract_pages(PDF_PATH)
    print(f"   Tổng số trang: {len(pages)}")
    print(f"   Bỏ qua {TOC_END_PAGE} trang đầu (bìa + TOC)")

    print("\n🔍 Tìm ranh giới các chương (từ trang 14 trở đi)...")
    chapter_starts = find_chapter_starts(pages, CHAPTERS, TOC_END_PAGE)

    # Sắp xếp theo thứ tự trang
    sorted_chapters = []
    for folder, pattern in CHAPTERS:
        if folder in chapter_starts:
            sorted_chapters.append((folder, chapter_starts[folder]))

    sorted_chapters.sort(key=lambda x: x[1])

    print(f"\n📂 Tìm thấy {len(sorted_chapters)}/{len(CHAPTERS)} chương.")

    # Thống kê không tìm thấy
    not_found = [f for f, p in CHAPTERS if f not in chapter_starts]
    if not_found:
        print(f"⚠️  Không tìm thấy: {not_found}")

    print("\n📝 Trích xuất nội dung từng chương...")
    page_text = {p: t for p, t in pages}
    
    total_chars = 0
    for i, (folder, start_page) in enumerate(sorted_chapters):
        if i + 1 < len(sorted_chapters):
            end_page = sorted_chapters[i + 1][1] - 1
        else:
            end_page = len(pages)

        chapter_text = ""
        for pnum in range(start_page, end_page + 1):
            chapter_text += page_text.get(pnum, "") + "\n"

        print(f"\n  [{folder}] (Trang {start_page}→{end_page})")
        size = save_chapter(folder, chapter_text, OUTPUT_BASE)
        total_chars += size

    print(f"\n{'='*60}")
    print(f"✅ HOÀN THÀNH BƯỚC 3!")
    print(f"   Tổng: {len(sorted_chapters)} chương | {total_chars:,} ký tự")
    print(f"   Output: {OUTPUT_BASE}")

if __name__ == "__main__":
    main()
