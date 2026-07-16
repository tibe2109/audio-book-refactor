import os
import re

directory = "/mnt/d/Solution/Audio-Book-Refactor/Kich-ban-clipchamp/Nghe-thuat-quyen-ru/Chuong-16-Giai-on-4-Ngh-thut-chinh-phc-v-duy-tr-tnh-cm/"

def process_text(text):
    # 1. Tách tiêu đề dính liền
    # Pattern: a common title like "Bí quyết quyến rũ", "Sức quyến rũ", "Giải thích", or "hai mươi mốt. Cho họ cơ hội thua..." 
    # followed by an uppercase word that starts the paragraph.
    # We look for a lowercase character (or number/dot/comma), space, then an uppercase character.
    # But only specific cases to avoid splitting normal sentences that have uppercase names like "với Baudelaire".
    
    # Specific known title prefixes:
    titles_re = re.compile(r'^(Bí quyết quyến rũ|Sức quyến rũ|Biểu tượng|Điểm yếu|Giải thích|(?:một|hai|ba|bốn|năm|sáu|bảy|tám|chín|mười|hai mươi[\w\s]*)\.\s+.*?)\s+([A-ZĐ][a-zà-ỹ])', re.MULTILINE)
    text = titles_re.sub(r'\1\n\n\2', text)
    
    # "GIAI ĐOẠN bốn, NGHỆ THUẬT CHINH PHỤC VÀ DUY TRÌ TÌNH. ......\n\nCẢM Trước tiên..." -> "GIAI ĐOẠN bốn, NGHỆ THUẬT CHINH PHỤC VÀ DUY TRÌ TÌNH CẢM\n\nTrước tiên..."
    text = text.replace("TÌNH. ......\n\nCẢM Trước tiên", "TÌNH CẢM\n\nTrước tiên")
    
    # 2. Chèn dấu phẩy tạo nhịp thở
    # Insert comma before some conjunctions in long segments.
    # We'll use a simple heuristic: if a sentence has more than 15 words without a comma, 
    # insert a comma before "và", "nhưng", "để", "thì", "mà", "rằng".
    conjunctions = ["và", "nhưng", "để", "thì", "mà", "rằng", "bởi vì", "vì thế", "do đó"]
    
    def add_commas(match):
        sentence = match.group(0)
        # Split into segments by existing punctuation
        segments = re.split(r'([,.;:!?])', sentence)
        new_segments = []
        for i in range(0, len(segments), 2):
            seg = segments[i]
            words = seg.split()
            if len(words) > 12:
                # Find the best conjunction to split at roughly the middle
                best_idx = -1
                for j in range(5, len(words) - 5):
                    if words[j].lower() in conjunctions:
                        best_idx = j
                        break
                if best_idx != -1:
                    words[best_idx] = ", " + words[best_idx]
                    seg = " ".join(words)
            new_segments.append(seg)
            if i + 1 < len(segments):
                new_segments.append(segments[i+1])
        return "".join(new_segments)

    # Process each sentence
    text = re.sub(r'[^.!?]+[.!?]', add_commas, text)
    
    return text

for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = process_text(content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"Processed {filename}")
