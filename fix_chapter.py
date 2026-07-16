import os
import glob
import re
import argparse
from num2words import num2words

def fix_content(content):
    # 1. Loại bỏ ký tự cấm: "", (), :, —, -
    content = re.sub(r'["\(\)::—\-]', ' ', content)
    
    # 2. Xử lý số thành chữ (num2words tiếng Việt)
    def replace_num(match):
        num_str = match.group()
        try:
            # handle simple integer
            num = int(num_str)
            return num2words(num, lang='vi')
        except:
            return num_str

    content = re.sub(r'\d+', replace_num, content)
    
    # 3. Sửa dấu 3 chấm sai quy tắc thành chuẩn
    # Tạm thời thay `. ......` bằng một token đặc biệt, sau đó biến mọi `...` thành dấu phẩy (hoặc xoá), rồi trả lại `. ......`
    content = content.replace('. ......', '###DOTDOTDOT###')
    content = content.replace('...', ',')
    content = content.replace('###DOTDOTDOT###', '. ......')
    
    # Dọn dẹp khoảng trắng thừa
    content = re.sub(r'\s+', ' ', content).strip()
    return content

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--chapter_dir", required=True)
    args = parser.parse_args()
    
    chapter_dir = args.chapter_dir
    if not os.path.exists(chapter_dir):
        print(f"Lỗi: Không tìm thấy {chapter_dir}")
        exit(1)
        
    txt_files = glob.glob(os.path.join(chapter_dir, "*.txt"))
    for txt_file in txt_files:
        with open(txt_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            
        fixed_content = fix_content(content)
        
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
            
    print(f"Đã fix xong toàn bộ kịch bản trong: {chapter_dir}")

if __name__ == "__main__":
    main()
