import os
import glob
import re

DIR = "/mnt/d/Solution/Audio-Book-Refactor/Kich-ban-clipchamp/Nghe-thuat-quyen-ru/Chuong-14-Giai-on-2-nh-lc-hng--to-thch-th-v-kh-hiu/"

def separate_title(line):
    if not line.strip():
        return line
    
    # Check if line already has `. ......` at the end
    has_pause = line.endswith('. ......')
    
    # Pattern 1: All CAPS title
    m1 = re.match(r'^([A-ZĐÁÀẢÃẠÂẤẦẨẪẬĂẮẰẲẴẶÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴ\s]{4,60})\s+([A-ZĐÁÀẢÃẠÂẤẦẨẪẬĂẮẰẲẴẶÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴ][a-zà-ỹ]+.*)', line)
    if m1:
        title = m1.group(1).strip()
        rest = m1.group(2).strip()
        return f"{title}. ......\n{rest}"
        
    # Pattern 2: lowercase/mixed title followed by Capitalized word
    m2 = re.match(r'^([A-ZĐÁÀẢÃẠÂẤẦẨẪẬĂẮẰẲẴẶÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴa-zà-ỹ0-9.\s]{5,80}?[a-zà-ỹ])\s+([A-ZĐÁÀẢÃẠÂẤẦẨẪẬĂẮẰẲẴẶÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴ][a-zà-ỹ]+.*)', line)
    
    if m2:
        title = m2.group(1).strip()
        rest = m2.group(2).strip()
        # If title ends with punctuation, maybe don't add dot
        if not title[-1] in ['.', '!', '?', ':', ',']:
            return f"{title}. ......\n{rest}"
        else:
            return f"{title} ......\n{rest}"
            
    return line

def add_breathing_commas(text):
    # Add comma after 'là', 'thì', 'rằng' if not followed by punctuation
    text = re.sub(r'\b(là|thì|rằng)\s+([^,.\?!:\s])', r'\1, \2', text)
    # Add comma before 'nhưng', 'bởi vì', 'cho nên', 'tuy nhiên'
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
        
        # We might have split the line into two lines. Process each for commas
        sep_lines = separated.split('\n')
        processed_lines = []
        for sl in sep_lines:
            processed_lines.append(add_breathing_commas(sl))
            
        new_lines.append('\n'.join(processed_lines))
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))

if __name__ == "__main__":
    files = glob.glob(os.path.join(DIR, "*.txt"))
    for f in files:
        process_file(f)
        print(f"Processed: {os.path.basename(f)}")
