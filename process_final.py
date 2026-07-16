import os
import glob
import re

DIR = "/mnt/d/Solution/Audio-Book-Refactor/Kich-ban-clipchamp/Nghe-thuat-quyen-ru/Chuong-13-Giai-on-1-Phn-tch--khi-gi-s-quan-tm-v-mong-mun/"

def separate_title(line):
    if not line.strip():
        return line
        
    # Pattern 1: All CAPS title
    m1 = re.match(r'^([A-ZĐÁÀẢÃẠÂẤẦẨẪẬĂẮẰẲẴẶÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴ\s]{4,60})\s+([A-ZĐÁÀẢÃẠÂẤẦẨẪẬĂẮẰẲẴẶÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴ][a-zà-ỹ]+.*)', line)
    if m1:
        return f"{m1.group(1).strip()}.\n{m1.group(2)}"
        
    # Pattern 2: Lowercase title -> uppercase transition
    m2 = re.match(r'^([A-ZĐÁÀẢÃẠÂẤẦẨẪẬĂẮẰẲẴẶÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴa-zà-ỹ0-9.\s]{4,50}?[a-zà-ỹ])\s+([A-ZĐÁÀẢÃẠÂẤẦẨẪẬĂẮẰẲẴẶÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴ][a-zà-ỹ]+.*)', line)
    
    if m2:
        title = m2.group(1).strip()
        rest = m2.group(2).strip()
        
        if ',' in title or '-' in title or '–' in title or ':' in title:
            return line
            
        if not title[-1] in ['.', '!', '?', ':']:
            return f"{title}.\n{rest}"
        else:
            return f"{title}\n{rest}"
            
    return line

def add_breathing_commas(text):
    text = re.sub(r'\b(là|thì|rằng)\s+([^,.\?!:\s])', r'\1, \2', text)
    text = re.sub(r'([^,.\?!:\s])\s+(nhưng|bởi vì|cho nên|tuy nhiên)\b', r'\1, \2', text)
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
            
        separated = separate_title(line)
        
        parts = separated.split('\n')
        processed_parts = [add_breathing_commas(p) for p in parts]
        
        new_lines.append('\n'.join(processed_parts))
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))

if __name__ == "__main__":
    files = glob.glob(os.path.join(DIR, "*.txt"))
    for f in files:
        process_file(f)
        print(f"Processed: {os.path.basename(f)}")
