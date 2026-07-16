import os
import re

dir_path = "/mnt/d/Solution/Audio-Book-Refactor/Kich-ban-clipchamp/Nghe-thuat-quyen-ru/Chuong-11-Ngi-khng-quyn-r/"

titles = [
    "NGƯỜI KHÔNG QUYẾN RŨ",
    "Đặc điểm nổi bật",
    "Người cá tính loài thú ,Brutes, –",
    "Người cá tính bóp nghẹt ,suffocator, –",
    "Người hay răn dạy ,Moralizer, –",
    "Người hà tiện, keo cú ,Tightwad, –",
    "Người tiếp tân vênh váo ,Bumbler, –",
    "Người ba hoa chích chòe –",
    "Người hay phản ứng –",
    "Người trưởng giả –",
    "Trường hợp điển hình một.",
    "một.",
    "hai.",
    "ba.",
    "bốn.",
    "năm.",
    "Biểu tượng Con cua.",
    "Điểm yếu"
]

def process_titles(text):
    for title in titles:
        escaped_title = re.escape(title)
        pattern = r'^(' + escaped_title + r')\s+(?!\.\s*\.\.\.\.\.\.)(.)'
        
        def replacer(match):
            t = match.group(1)
            # if title already ends with '.', just append ' ......'
            if t.endswith('.') or t.endswith('–'):
                return t + " ......\n" + match.group(2)
            else:
                return t + ". ......\n" + match.group(2)
            
        lines = text.split('\n')
        new_lines = []
        for line in lines:
            if re.match(pattern, line):
                line = re.sub(pattern, replacer, line)
            new_lines.append(line)
        text = '\n'.join(new_lines)
    return text

def insert_commas(text):
    lines = text.split('\n')
    new_lines = []
    conjunctions = ['và', 'mà', 'thì', 'là', 'nhưng', 'để', 'bởi vì', 'cho nên', 'nên', 'hoặc', 'vì thế']
    
    for line in lines:
        if not line.strip() or line.strip() == '. ......':
            new_lines.append(line)
            continue
            
        words = line.split(' ')
        out_words = []
        current_chunk_length = 0
        for i, word in enumerate(words):
            out_words.append(word)
            current_chunk_length += 1
            
            # If current word has punctuation, reset counter
            if any(p in word for p in ['.', ',', '?', '!', ':', ';', '–', '-']):
                current_chunk_length = 0
            else:
                # if we have a decent chunk and the next word is a conjunction
                if current_chunk_length >= 6 and i + 1 < len(words):
                    next_word = words[i+1].lower()
                    if next_word in conjunctions:
                        out_words[-1] = out_words[-1] + ","
                        current_chunk_length = 0
        
        new_lines.append(" ".join(out_words))
    return '\n'.join(new_lines)

for i in range(1, 4):
    filename = f"Kich-ban-{i}.txt"
    filepath = os.path.join(dir_path, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = process_titles(content)
    content = insert_commas(content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Processing complete.")
