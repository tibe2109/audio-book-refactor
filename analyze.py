import os
import re

dir_path = "/mnt/d/Solution/Audio-Book-Refactor/Kich-ban-clipchamp/Nghe-thuat-quyen-ru/Chuong-7-Ngi-n-b-m-dng/"
for filename in sorted(os.listdir(dir_path)):
    if filename.endswith(".txt"):
        filepath = os.path.join(dir_path, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print(f"\n--- {filename} ---")
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            words = line.split()
            print(f"Line {i+1}: {' '.join(words[:15])}...")
