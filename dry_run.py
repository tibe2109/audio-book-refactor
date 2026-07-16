import os
import glob
import re

DIR = "/mnt/d/Solution/Audio-Book-Refactor/Kich-ban-clipchamp/Nghe-thuat-quyen-ru/Chuong-13-Giai-on-1-Phn-tch--khi-gi-s-quan-tm-v-mong-mun/"

def separate_title(line):
    if not line.strip():
        return None
        
    m1 = re.match(r'^([A-ZĐÁÀẢÃẠÂẤẦẨẪẬĂẮẰẲẴẶÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴ\s]{4,40})\s+([A-ZĐÁÀẢÃẠÂẤẦẨẪẬĂẮẰẲẴẶÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴ][a-zà-ỹ]+.*)', line)
    if m1:
        return f"{m1.group(1).strip()}.\n{m1.group(2)}"
        
    m2 = re.match(r'^([A-ZĐÁÀẢÃẠÂẤẦẨẪẬĂẮẰẲẴẶÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴa-zà-ỹ0-9.\s]{5,40}?[a-zà-ỹ])\s+([A-ZĐÁÀẢÃẠÂẤẦẨẪẬĂẮẰẲẴẶÉÈẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴ][a-zà-ỹ]+.*)', line)
    
    if m2:
        title = m2.group(1).strip()
        rest = m2.group(2).strip()
        
        # Heuristic: Title usually doesn't contain commas
        if ',' in title:
            return None
            
        if not title[-1] in ['.', '!', '?', ':', ',']:
            return f"{title}.\n{rest}"
        else:
            if title[-1] == ',':
                return f"{title}\n{rest}"
            return f"{title}\n{rest}"
            
    return None

def main():
    files = glob.glob(os.path.join(DIR, "*.txt"))
    for f in files:
        with open(f, 'r', encoding='utf-8') as file:
            lines = file.read().split('\n')
        for line in lines:
            res = separate_title(line)
            if res:
                print(f"[{os.path.basename(f)}]")
                print(f"ORIGINAL: {line[:80]}...")
                print(f"SPLIT   : {res.split(chr(10))[0]} || {res.split(chr(10))[1][:40]}...")
                print("-" * 50)

if __name__ == "__main__":
    main()
