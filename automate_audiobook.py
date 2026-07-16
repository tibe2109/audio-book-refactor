import os
import re
import time
from PyPDF2 import PdfReader
from deep_translator import GoogleTranslator

# Đường dẫn file
pdf_path = 'Docs/Eat That Frog! 21 Great Ways to Stop Procrastinating and Get More Done in Less Time ( PDFDrive ).pdf'
out_dir = 'Kich-ban-clipchamp/Eat-that-frog'

os.makedirs(out_dir, exist_ok=True)

def apply_tts_format(text):
    if not text: return ""
    lines = text.split('\n')
    formatted_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Xóa các khoảng trắng thừa
        line = re.sub(r'\s+', ' ', line)
        
        # Các quy tắc ngắt ngắn
        line = re.sub(r'[,;\-\(\):]', ' ... ', line)
        
        # Dấu chấm câu
        line = line.replace('.', ' ...... ')
        
        # Ngắt đoạn
        line += ' ..........'
        formatted_lines.append(line)
        
    return '\n\n'.join(formatted_lines)

def translate_chunk(text):
    if not text.strip(): return ""
    try:
        # Giới hạn của GoogleTranslator là 5000 ký tự, nếu dài hơn cần chia nhỏ
        chunks = [text[i:i+4000] for i in range(0, len(text), 4000)]
        translated_text = ""
        for chunk in chunks:
            translated = GoogleTranslator(source='en', target='vi').translate(chunk)
            translated_text += translated + " "
            time.sleep(1) # Tránh bị rate limit
        return translated_text
    except Exception as e:
        print(f"Lỗi dịch thuật: {e}")
        return text

def process_book():
    print("Đang đọc PDF...")
    reader = PdfReader(pdf_path)
    
    # Gom toàn bộ chữ từ PDF
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() + "\n"

    # Xóa các số trang và header linh tinh nếu có (VD: --- Page X ---)
    full_text = re.sub(r'Eat\s+That\s+Frog!', '', full_text, flags=re.IGNORECASE)
    
    print("Đã đọc xong, đang phân tách chương...")
    
    # Phân chia theo chương. Ta có:
    # Preface
    # Introduction: Eat That Frog
    # 1 Set the Table
    # 2 Plan Every Day in Advance
    # ...
    # Để đơn giản và chính xác, ta sẽ dùng Regex tìm các tiêu đề chương
    
    chapters = []
    
    # Một cách tiếp cận đơn giản hơn là chia văn bản thành các block lớn (ví dụ 10 trang / phần) 
    # nếu không thể regex chính xác mục lục. Nhưng ta sẽ cố gắng split bằng regex:
    # Mục lục thường có dạng "1 Set the Table" đầu dòng
    # Để tránh cắt vỡ, ta sẽ chia làm các đoạn khoảng 10,000 ký tự, hoặc chia theo trang
    # Ở đây tôi sẽ chia làm 22 phần (tương ứng 21 chương + phần đầu) bằng cách duyệt qua văn bản.
    
    # Để đảm bảo script chạy mượt, ta chia theo chunks 15000 ký tự (khoảng 5-7 trang)
    chunk_size = 15000
    sections = [full_text[i:i+chunk_size] for i in range(0, len(full_text), chunk_size)]
    
    print(f"Tổng cộng {len(sections)} phần cần xử lý.")
    
    for i, section in enumerate(sections):
        print(f"Đang xử lý phần {i+1}/{len(sections)}...")
        
        # Dịch
        translated = translate_chunk(section)
        
        # Format TTS
        tts_ready = apply_tts_format(translated)
        
        # Lưu file
        file_name = f"Phan_{i+1:02d}.txt"
        file_path = os.path.join(out_dir, file_name)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(tts_ready)
            
        print(f"Đã lưu {file_name}")

if __name__ == '__main__':
    process_book()
    print("HOÀN THÀNH TOÀN BỘ!")
