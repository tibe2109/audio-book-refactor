import os
import re

dir_path = '/mnt/d/Solution/Audio-Book-Refactor/Kich-ban-clipchamp/Nghe-thuat-quyen-ru/Chuong-10-Ngi-sao/'

titles = [
    (r'^NGÔI SAO (?=Cuộc sống)', r'NGÔI SAO. ......\n'),
    (r'^Thần tượng ngôi sao (?=Vào một ngày)', r'Thần tượng ngôi sao. ......\n'),
    (r'^Ngôi sao huyền thoại (?=Vào ngày)', r'Ngôi sao huyền thoại. ......\n'),
    (r'^Đặc điểm nổi bật (?=Sự cám dỗ)', r'Đặc điểm nổi bật. ......\n'),
    (r'^Biểu tượng (?=Thần tượng)', r'Biểu tượng. ......\n'),
    (r'^Điểm yếu (?=Những ngôi sao)', r'Điểm yếu. ......\n'),
]

# Words that need a comma before them to create breathing rhythm
# Using \w ensures that we only match when preceded by a word character (no existing punctuation)
comma_words = [
    "nhưng", "bởi vì", "vì vậy", "do đó", "cho nên", 
    "tuy nhiên", "mặc dù", "hay", "hoặc", "nên"
]

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1 & 3: Tách tiêu đề dính liền, thêm `. ......` và xuống dòng (Không xóa `. ......` có sẵn vì không đụng đến chúng)
    for pattern, replacement in titles:
        content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

    # 2: Chèn dấu phẩy tạo nhịp thở
    for word in comma_words:
        if word == "nên":
            # Exclude "trở nên" and "cho nên"
            pattern = r'(?<!\btrở)(?<!\bcho)(?<=\w)\s+(nên)\b'
            content = re.sub(pattern, r', \1', content, flags=re.IGNORECASE)
        elif word == "hay":
            # Exclude "hay là" wait, "hay là" is fine to have comma before "hay".
            # Exclude "hay không" (e.g. có ... hay không)
            pattern = r'(?<=\w)\s+(hay)\b(?!\s+không\b)'
            content = re.sub(pattern, r', \1', content, flags=re.IGNORECASE)
        else:
            pattern = r'(?<=\w)\s+(' + word + r')\b'
            content = re.sub(pattern, r', \1', content, flags=re.IGNORECASE)

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for filename in os.listdir(dir_path):
    if filename.endswith('.txt'):
        process_file(os.path.join(dir_path, filename))

print("Processing complete.")
