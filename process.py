import os
import glob
import re

DIR = "/mnt/d/Solution/Audio-Book-Refactor/Kich-ban-clipchamp/Nghe-thuat-quyen-ru/Chuong-14-Giai-on-2-nh-lc-hng--to-thch-th-v-kh-hiu/"

def separate_title(line):
    if not line.strip():
        return line
    
    # Ignore if line starts with space or already has punctuation at the very beginning (like bullet points)
    # Actually just look at the first 70 characters
    
    # Pattern 1: All CAPS title
    # MONG MUỐN Nạn nhân...
    m1 = re.match(r'^([A-ZĐÁÀẢÃẠÂẤẦẨẪẬĂẮẰẲẴẶÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴ\s]{4,40})\s+([A-ZĐÁÀẢÃẠÂẤẦẨẪẬĂẮẰẲẴẶÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴ][a-zà-ỹ]+.*)', line)
    if m1:
        return f"{m1.group(1).strip()}.\n{m1.group(2)}"
        
    # Pattern 2: lowercase/mixed title followed by Capitalized word
    # một. Chọn nạn nhân phù hợp Tất cả...
    # Bí quyết quyến rũ Suốt cuộc đời...
    # We look for a string of words (length 5 to 60) that ends in a lowercase letter, space, then a Capital letter
    m2 = re.match(r'^([A-ZĐÁÀẢÃẠÂẤẦẨẪẬĂẮẰẲẴẶÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴa-zà-ỹ0-9.\s]{5,60}?[a-zà-ỹ])\s+([A-ZĐÁÀẢÃẠÂẤẦẨẪẬĂẮẰẲẴẶÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴ][a-zà-ỹ]+.*)', line)
    
    if m2:
        title = m2.group(1).strip()
        rest = m2.group(2).strip()
        # Check if the title already ends with punctuation
        if not title[-1] in ['.', '!', '?', ':', ',']:
            return f"{title}.\n{rest}"
        else:
            # If it already ends with a punctuation (e.g. comma), just add newline
            if title[-1] == ',':
                return f"{title}\n{rest}"
            return f"{title}\n{rest}"
            
    return line

def add_breathing_commas(text):
    # Add comma after 'là', 'thì', 'rằng' if not followed by punctuation
    text = re.sub(r'\b(là|thì|rằng)\s+([^,.\?!:\s])', r'\1, \2', text)
    # Add comma before 'nhưng', 'bởi vì', 'cho nên'
    text = re.sub(r'([^,.\?!:\s])\s+(nhưng|bởi vì|cho nên)\b', r'\1, \2', text)
    return text

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        if not line.strip():
            new_lines.append(line)
            continue
            
        # 1. Separate title
        separated = separate_title(line)
        
        # 2. Add commas
        processed = add_breathing_commas(separated)
        
        new_lines.append(processed)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))

if __name__ == "__main__":
    files = glob.glob(os.path.join(DIR, "*.txt"))
    for f in files:
        process_file(f)
        print(f"Processed: {os.path.basename(f)}")
