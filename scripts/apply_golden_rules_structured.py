import os
import re
from num2words import num2words

input_file = '/mnt/d/Solution/Audio-Book-Refactor/scratch_pdf_nghethuat.txt'
base_out_dir = '/mnt/d/Solution/Audio-Book-Refactor/Kich-ban-clipchamp/Nghe-thuat-quyen-ru'

def replace_numbers(match):
    num_str = match.group()
    try:
        return num2words(int(num_str), lang='vi')
    except:
        return num_str

def apply_golden_rules(text):
    text = text.replace('"', '').replace('“', '').replace('”', '').replace("'", "")
    text = re.sub(r'[\(\)\-:]', ',', text)
    text = text.replace('...', ' ')
    text = re.sub(r'\b\d+\b', replace_numbers, text)
    names = {
        'Robert': 'Rô bớt', 'Greene': 'Gờ rin', 'Cleopatra': 'Cơ lê ô pát tra',
        'Julius Caesar': 'Giu li ớt Xê da', 'Ovid': 'Ô vít', 'Casanova': 'Ca xa nô va'
    }
    for eng, vi in names.items():
        text = re.sub(r'\b' + eng + r'\b', vi, text, flags=re.IGNORECASE)
    
    lines = text.split('\n')
    processed_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        line = re.sub(r',+', ',', line)
        line = re.sub(r'\s+', ' ', line)
        line = line + ' ......'
        processed_lines.append(line)
        
    return '\n\n'.join(processed_lines)

def main():
    if not os.path.exists(input_file):
        print("Missing input text!")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    paragraphs = text.split('\n')
    
    # Structure: 100 paragraphs per file, 5 files per chapter (500 paragraphs per chapter)
    chapter_num = 1
    file_num = 1
    
    for i in range(0, len(paragraphs), 100):
        chunk = paragraphs[i:i+100]
        chunk_text = '\n'.join(chunk).strip()
        if not chunk_text:
            continue
            
        tts_text = apply_golden_rules(chunk_text)
        
        chapter_dir = os.path.join(base_out_dir, f'Chuong-{chapter_num}')
        os.makedirs(chapter_dir, exist_ok=True)
        
        out_path = os.path.join(chapter_dir, f'Kich-ban-{file_num}.txt')
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(tts_text)
        
        file_num += 1
        if file_num > 5:
            chapter_num += 1
            file_num = 1

    print("Hoàn tất tạo kịch bản theo cấu trúc thư mục!")

if __name__ == "__main__":
    main()
