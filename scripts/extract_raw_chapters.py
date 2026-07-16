import fitz
import os
import re

pdf_path = '/mnt/d/Solution/Audio-Book-Refactor/Docs/Nghe-thuat-quyen-ru.pdf'
out_dir = '/mnt/d/Solution/Audio-Book-Refactor/Docs/nghethuat_raw_chapters'
os.makedirs(out_dir, exist_ok=True)

def extract_book():
    doc = fitz.open(pdf_path)
    toc = doc.get_toc()
    
    chapters = []
    for item in toc:
        level, title, page = item
        if 'LỜI NÓI ĐẦU' in title or level == 2:
            clean_title = re.sub(r'[^a-zA-Z0-9\s_]', '', title).strip().replace(' ', '-')
            chapters.append({
                'title': clean_title,
                'start_page': page - 1, 
                'end_page': doc.page_count - 1
            })
            
    for i in range(len(chapters) - 1):
        chapters[i]['end_page'] = chapters[i+1]['start_page'] - 1
        
    chapter_num = 1
    for ch in chapters:
        if ch['start_page'] > ch['end_page']:
            ch['end_page'] = ch['start_page']
            
        paragraphs = []
        for p in range(ch['start_page'], ch['end_page'] + 1):
            if p < doc.page_count:
                blocks = doc[p].get_text("blocks")
                for b in blocks:
                    block_text = b[4].replace('\n', ' ').strip()
                    if block_text:
                        paragraphs.append(block_text)
                        
        raw_text = '\n\n'.join(paragraphs)
        if raw_text.strip():
            dir_name = f"Chuong-{chapter_num}-{ch['title']}"
            out_path = os.path.join(out_dir, f"{dir_name}.txt")
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(raw_text)
        
        chapter_num += 1

if __name__ == "__main__":
    extract_book()
