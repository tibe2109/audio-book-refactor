import os
import re
import glob
from num2words import num2words

RAW_DIR = '/mnt/d/Solution/Audio-Book-Refactor/Docs/nghethuat_raw_chapters'
OUT_DIR = '/mnt/d/Solution/Audio-Book-Refactor/Kich-ban-clipchamp/Nghe-thuat-quyen-ru'

def replace_numbers(match):
    num_str = match.group()
    try:
        return num2words(int(num_str), lang='vi')
    except:
        return num_str

def apply_golden_rules(text):
    text = text.replace('"', '').replace('“', '').replace('”', '').replace("'", "")
    text = re.sub(r'[\(\)\-—:;]', ',', text)
    text = re.sub(r'\.{2,}', '', text) 
    text = re.sub(r'\b\d+\b', replace_numbers, text)
    
    names = {
        'Robert Greene': 'Rô bớt Gờ rin', 'Robert': 'Rô bớt', 'Greene': 'Gờ rin', 
        'Cleopatra': 'Cơ lê ô pát tra', 'Julius Caesar': 'Giu li ớt Xê da',
        'Ovid': 'Ô vít', 'Casanova': 'Ca xa nô va', 'Denis Diderot': 'Đê nít Đi đờ rốt',
        'Bathsheba': 'Bát si ba', 'Helen': 'Hê len', 'Hsi Shi': 'Tây Thi',
        'David': 'Đa vít', 'Paris': 'Pa rít', 'Mark Anthony': 'Mác An tô ni',
        'John F. Kenedy': 'Giôn Ép Ken nơ đi', 'Brian Tracy': 'Brai ân Tờ rây xi',
        'Napoleon': 'Na pô lê ông', 'Don Juan': 'Đôn Gioăng',
        'Victor': 'Vích to', 'Pareto': 'Pa rê tô'
    }
    for eng, vi in names.items():
        text = re.sub(r'\b' + eng + r'\b', vi, text, flags=re.IGNORECASE)

    text = re.sub(r',+', ',', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    if not text:
        return ""

    if not re.search(r'[.?!]$', text):
        text += '.'
        
    text += ' ......'
    return text

def process_fallback():
    raw_files = glob.glob(os.path.join(RAW_DIR, "*.txt"))
    for file_path in raw_files:
        basename = os.path.basename(file_path).replace('.txt', '')
        chapter_dir = os.path.join(OUT_DIR, basename)
        os.makedirs(chapter_dir, exist_ok=True)
        
        # Check if the subagent failed to write all files by checking if there's more than 5 files
        # Some subagents created Kich-ban-1 to Kich-ban-3 and stopped.
        # If there are fewer than 5 files but the raw text is > 20KB, it's incomplete.
        existing = glob.glob(os.path.join(chapter_dir, "Kich-ban-*.txt"))
        raw_size = os.path.getsize(file_path)
        
        if len(existing) < 4 and raw_size > 20000:
            print(f"Fallback processing for incomplete chapter: {basename}")
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            paragraphs = content.split('\n\n')
            chunk_size = 20
            chunks = [paragraphs[i:i+chunk_size] for i in range(0, len(paragraphs), chunk_size)]
            
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

if __name__ == "__main__":
    process_fallback()
