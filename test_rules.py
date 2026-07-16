import os
import re
from num2words import num2words

def replace_numbers(match):
    num_str = match.group()
    try:
        return num2words(int(num_str), lang='vi')
    except:
        return num_str

def apply_golden_rules(text):
    text = text.replace('"', '').replace('“', '').replace('”', '').replace("'", "")
    text = re.sub(r'[\(\)\-—:;]', ',', text)
    text = re.sub(r'\.{2,}', '', text) 
    text = re.sub(r'\b\d+\b', replace_numbers, text)
    
    names = {
        'Robert Greene': 'Rô bớt Gờ rin', 'Robert': 'Rô bớt', 'Greene': 'Gờ rin', 
        'Cleopatra': 'Cơ lê ô pát tra', 'Julius Caesar': 'Giu li ớt Xê da',
        'Ovid': 'Ô vít', 'Casanova': 'Ca xa nô va', 'Denis Diderot': 'Đê nít Đi đờ rốt',
        'Bathsheba': 'Bát si ba', 'Helen': 'Hê len', 'Hsi Shi': 'Tây Thi',
        'David': 'Đa vít', 'Paris': 'Pa rít', 'Mark Anthony': 'Mác An tô ni',
        'John F. Kenedy': 'Giôn Ép Ken nơ đi', 'Brian Tracy': 'Brai ân Tờ rây xi',
        'Napoleon': 'Na pô lê ông', 'Don Juan': 'Đôn Gioăng',
        'Victor': 'Vích to', 'Pareto': 'Pa rê tô'
    }
    for eng, vi in names.items():
        text = re.sub(r'\b' + eng + r'\b', vi, text, flags=re.IGNORECASE)

    text = re.sub(r',+', ',', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    if not text:
        return ""

    if not re.search(r'[.?!]$', text):
        text += '.'
        
    text += ' ......'
    return text

with open('/mnt/d/Solution/Audio-Book-Refactor/Docs/nghethuat_raw_chapters/Chuong-1-LI-NI-U.txt', 'r', encoding='utf-8') as f:
    content = f.read()

paragraphs = content.split('\n\n')
print("ORIGINAL TITLE:")
print(paragraphs[0])
print("\nPROCESSED TITLE:")
print(apply_golden_rules(paragraphs[0]))

print("\nORIGINAL PARA 1:")
print(paragraphs[1])
print("\nPROCESSED PARA 1:")
print(apply_golden_rules(paragraphs[1]))
