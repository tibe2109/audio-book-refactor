import os
import re

dir_path = "/mnt/d/Solution/Audio-Book-Refactor/Kich-ban-clipchamp/Nghe-thuat-quyen-ru/Chuong-18-Dn-chng-cho-khng-gian-v-thi-gian-quyn-r"

def add_breathing_commas(text):
    # Split text into sentences based on punctuation (but preserving it)
    sentences = re.split(r'([.!?]+)', text)
    result = []
    
    conjunctions = ['và', 'nhưng', 'để', 'mà', 'thì', 'bởi', 'nên', 'rằng', 'khiến', 'vì']
    
    for i in range(0, len(sentences)-1, 2):
        s = sentences[i]
        p = sentences[i+1]
        
        # Split by existing commas
        parts = s.split(',')
        new_parts = []
        for part in parts:
            words = part.split()
            if len(words) > 12:
                # Try to find a conjunction to insert a comma before
                for conj in conjunctions:
                    if conj in words[4:-4]: # avoid putting comma too close to ends
                        idx = words.index(conj)
                        # Add comma to the word before conjunction
                        words[idx-1] += ','
                        break
            new_parts.append(' '.join(words))
        
        # Join back parts with comma
        new_s = ', '.join(new_parts)
        # Clean up any double commas or spaces before commas
        new_s = re.sub(r'\s+,', ',', new_s)
        new_s = re.sub(r',+', ',', new_s)
        
        result.append(new_s + p)
        
    if len(sentences) % 2 != 0:
        result.append(sentences[-1])
        
    return ''.join(result)

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix joined titles
    # "DẪN CHỨNG CHO KHÔNG GIAN VÀ THỜI GIAN QUYẾN RŨ một."
    content = content.replace("DẪN CHỨNG CHO KHÔNG GIAN VÀ THỜI GIAN QUYẾN RŨ một.", "DẪN CHỨNG CHO KHÔNG GIAN VÀ THỜI GIAN QUYẾN RŨ. ......\n\nmột.")

    # Fix Kich-ban-2 broken title
    content = content.replace("PHỤ LỤC B, CÁM DỖ NHẸ NHÀNG – LÀM. ......\n\nTHẾ NÀO BÁN BẤT CỨ CÁI GÌ CHO. ......\n\nCÔNG CHÚNG. ......", "PHỤ LỤC B, CÁM DỖ NHẸ NHÀNG, LÀM THẾ NÀO BÁN BẤT CỨ CÁI GÌ CHO CÔNG CHÚNG. ......")

    # Some broken sentences split by newlines (like Những tayus)
    content = content.replace("Những tayus. ......\n\ndường như lướt trên sàn nhà", "Những tayus dường như lướt trên sàn nhà")
    content = content.replace("những chiếc gối bạc chứa nay khí. ......\n\nhêli trôi bồng bềnh", "những chiếc gối bạc chứa nay khí hêli trôi bồng bềnh")
    content = content.replace("Ca xa nô va còn đem đến những yếu tố sân khấu. ......\n\ntuyệt vời.", "Ca xa nô va còn đem đến những yếu tố sân khấu tuyệt vời.")
    content = content.replace("loại bỏ đi bất kỳ hình. ......\n\nthức chống đối nào.", "loại bỏ đi bất kỳ hình thức chống đối nào.")

    # 2. Add breathing commas
    paragraphs = content.split('\n')
    new_paragraphs = []
    for p in paragraphs:
        if p.strip():
            # Temporarily remove '. ......' to avoid messing up sentences
            suffix = ''
            if p.endswith('. ......'):
                p = p[:-8]
                suffix = '. ......'
            
            p = add_breathing_commas(p)
            
            p = p + suffix
        new_paragraphs.append(p)
        
    new_content = '\n'.join(new_paragraphs)
    
    # 3. Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Processed {filepath}")

for filename in os.listdir(dir_path):
    if filename.endswith(".txt"):
        process_file(os.path.join(dir_path, filename))
