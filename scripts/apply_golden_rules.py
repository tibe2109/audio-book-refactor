import os
import re
from num2words import num2words

input_file = '/mnt/d/Solution/Audio-Book-Refactor/scratch_pdf_nghethuat.txt'
out_dir = '/mnt/d/Solution/Audio-Book-Refactor/Kich-ban-clipchamp/Nghe-thuat-quyen-ru'
os.makedirs(out_dir, exist_ok=True)

def replace_numbers(match):
    num_str = match.group()
    try:
        # num2words supports vietnamese
        return num2words(int(num_str), lang='vi')
    except:
        return num_str

def apply_golden_rules(text):
    # 1. Remove quotes
    text = text.replace('"', '').replace('“', '').replace('”', '').replace("'", "")
    # 2. Replace colons, parentheses, dashes with comma for breathing
    text = re.sub(r'[\(\)\-:]', ',', text)
    # 3. Replace ... with space inside sentences
    text = text.replace('...', ' ')
    
    # 4. Replace numbers with words
    text = re.sub(r'\b\d+\b', replace_numbers, text)
    
    # 5. Phonetic names (basic mapping)
    names = {
        'Robert': 'Rô bớt',
        'Greene': 'Gờ rin',
        'Cleopatra': 'Cơ lê ô pát tra',
        'Julius Caesar': 'Giu li ớt Xê da',
        'Ovid': 'Ô vít',
        'Casanova': 'Ca xa nô va'
    }
    for eng, vi in names.items():
        text = re.sub(r'\b' + eng + r'\b', vi, text, flags=re.IGNORECASE)
    
    # Process paragraphs
    lines = text.split('\n')
    processed_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Merge multiple commas
        line = re.sub(r',+', ',', line)
        line = re.sub(r'\s+', ' ', line)
        
        # Add 6 dots at the end for long pause
        line = line + ' ......'
        processed_lines.append(line)
        
    return '\n\n'.join(processed_lines)

def main():
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Split the whole text into chunks of roughly 4000 characters for TTS (Clipchamp likes small chunks)
    # Clipchamp limit is 10 mins usually, ~1500-2000 words
    # We will split into chunks of 30 paragraphs
    paragraphs = text.split('\n')
    # group by 30
    chunk_size = 40
    chunks = [paragraphs[i:i + chunk_size] for i in range(0, len(paragraphs), chunk_size)]
    
    part_num = 1
    for chunk in chunks:
        chunk_text = '\n'.join(chunk).strip()
        if not chunk_text:
            continue
        
        tts_text = apply_golden_rules(chunk_text)
        
        out_path = os.path.join(out_dir, f'Kich-ban-{part_num}.txt')
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(tts_text)
        part_num += 1
        
    print(f"Processed into {part_num - 1} scripts in {out_dir}")

if __name__ == "__main__":
    main()
