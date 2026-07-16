import fitz
import os
import re
from num2words import num2words

pdf_path = '/mnt/d/Solution/Audio-Book-Refactor/Docs/Nghe-thuat-quyen-ru.pdf'
out_dir = '/mnt/d/Solution/Audio-Book-Refactor/Kich-ban-clipchamp/Nghe-thuat-quyen-ru'

def replace_numbers(match):
    num_str = match.group()
    try:
        return num2words(int(num_str), lang='vi')
    except:
        return num_str

def apply_golden_rules(text):
    text = text.replace('"', '').replace('“', '').replace('”', '').replace("'", "")
    text = re.sub(r'[\(\)\-—:]', ',', text)
    text = re.sub(r'\.{2,}', '', text) 
    text = re.sub(r'\b\d+\b', replace_numbers, text)
    
    names = {
        'Robert Greene': 'Rô bớt Gờ rin', 'Robert': 'Rô bớt', 'Greene': 'Gờ rin', 
        'Cleopatra': 'Cơ lê ô pát tra', 'Julius Caesar': 'Giu li ớt Xê da',
        'Ovid': 'Ô vít', 'Casanova': 'Ca xa nô va', 'Denis Diderot': 'Đê nít Đi đờ rốt',
        'Bathsheba': 'Bát si ba', 'Helen': 'Hê len', 'Hsi Shi': 'Tây Thi',
        'David': 'Đa vít', 'Paris': 'Pa rít', 'Mark Anthony': 'Mác An tô ni',
        'John F. Kenedy': 'Giôn Ép Ken nơ đi', 'Brian Tracy': 'Brai ân Tờ rây xi'
    }
    for eng, vi in names.items():
        text = re.sub(r'\b' + eng + r'\b', vi, text, flags=re.IGNORECASE)

    # Clean up commas and spaces
    text = re.sub(r',+', ',', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    if not text:
        return ""

    if not re.search(r'[.?!]$', text):
        text += '.'
        
    text += ' ......'
    return text

def extract_book():
    # Remove old dir
    os.system(f"rm -rf '{out_dir}'")
    os.makedirs(out_dir, exist_ok=True)
    
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
                        
        chunk_size = 30
        chunks = [paragraphs[i:i+chunk_size] for i in range(0, len(paragraphs), chunk_size)]
        
        dir_name = f"Chuong-{chapter_num}-{ch['title']}"
        chapter_dir = os.path.join(out_dir, dir_name)
        os.makedirs(chapter_dir, exist_ok=True)
        
        file_num = 1
        for chunk in chunks:
            tts_blocks = []
            for para in chunk:
                processed_para = apply_golden_rules(para)
                if processed_para:
                    tts_blocks.append(processed_para)
            
            if tts_blocks:
                out_path = os.path.join(chapter_dir, f'Kich-ban-{file_num}.txt')
                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write('\n\n'.join(tts_blocks))
                file_num += 1
                
        print(f"Generated {file_num-1} scripts for {dir_name}")
        chapter_num += 1

if __name__ == "__main__":
    extract_book()
