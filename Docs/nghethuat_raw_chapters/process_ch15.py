import os
import re

NAME_MAP = {
    "Oedipus": "Ơ đi pút",
    "Natalie": "Na ta li",
    "Barney": "Ba ni",
    "Marion": "Ma ri on",
    "de l'Orme": "đờ Lôm",
    "Cardinal": "Các đi nan",
    "Richelieu": "Ri sơ li ơ",
    "Grammont": "Gờ ram mông",
    "Brissac": "Bờ rít sác",
    "Guinevere": "Ghi nê vơ",
    "Arthur": "A thưa",
    "Lancelot": "Lan xơ lót",
    "Meleagant": "Mê lê a găng",
    "Tullia": "Tun li a",
    "d'Aragona": "đa ra gô na",
    "Tasso": "Tát sô",
    "Ferrara": "Phe ra ra",
    "Ovid": "Ô vít",
    "Peter": "Pi tơ",
    "Green": "Gờ rin",
    "Andreas": "An đờ rê át",
    "Capellanus": "Ca pen la nứt",
    "Walsh": "Oan",
    "Saint-Preuil": "Sanh Prơi",
    "Maisonfort": "Mây dông pho",
    "Bagnolet": "Ba nhô lê",
    "Count": "Cao",
    "Bussy-Rabutin": "Bút si Ra bu tin",
    "Gaules": "Gôn",
    "Nina": "Ni na",
    "Epton": "Ép tơn",
    "Achilles": "A sin",
    "Briseis": "Bờ ri xê ít",
    "Argive": "A ghi vơ",
    "Hector": "Héc to",
    "Andromache": "An đờ rô mác",
    "Agamemnon": "A ga mem non",
    "Cassandra": "Cát san đờ ra",
    "Freud": "Phờ rớt",
    "Sigmund": "Xích mần"
}

def convert_number_to_vietnamese(match):
    num_str = match.group(0)
    # For simple numbers, just let Clipchamp read them, but for short ranges like 5-10:
    return num_str # Clipchamp AI is actually very good at reading standard numbers in Vietnamese (like 16 -> mười sáu). We'll leave digits alone but fix ranges.

def process_text(text):
    # Fix ranges like 5-10
    text = re.sub(r'(\d+)\s*-\s*(\d+)', r'\1 đến \2', text)
    # Fix % 
    text = re.sub(r'%', ' phần trăm', text)
    
    # Remove quotes, hyphens, dashes, parentheses, colons
    text = re.sub(r'["“”‘’]', '', text)
    text = re.sub(r'[—–]', ',', text)
    text = re.sub(r'-', ' ', text)
    text = re.sub(r'[\(\)]', ',', text)
    text = re.sub(r':', ',', text)
    
    # Replace multiple dots with comma, avoiding the end of paragraph marker later
    text = re.sub(r'\.{2,}', ',', text)
    
    # Phonetic translation
    for eng, vie in NAME_MAP.items():
        text = re.sub(r'\b' + re.escape(eng) + r'\b', vie, text, flags=re.IGNORECASE)
        
    return text

input_path = '/mnt/d/Solution/Audio-Book-Refactor/Docs/nghethuat_raw_chapters/Chuong-15-Giai-on-3-Vch-ng--gy-n-tng-mnh-bng-nhng-bin-php-c-bit.txt'
output_dir = '/mnt/d/Solution/Audio-Book-Refactor/Kich-ban-clipchamp/Nghe-thuat-quyen-ru/Chuong-15/'
os.makedirs(output_dir, exist_ok=True)

with open(input_path, 'r', encoding='utf-8') as f:
    raw_lines = f.readlines()

sentences = []
for line in raw_lines:
    line = line.strip()
    if not line:
        continue
    
    processed = process_text(line)
    
    # Split paragraph into sentences by . ? !
    # Using regex to split but keep the delimiter
    parts = re.split(r'([.?!])', processed)
    
    para_sentences = []
    current_sentence = ""
    for i in range(0, len(parts)-1, 2):
        s = (parts[i] + parts[i+1]).strip()
        # cleanup spaces around commas
        s = re.sub(r'\s+,', ',', s)
        s = re.sub(r',\s+', ', ', s)
        if s:
            para_sentences.append(s)
            
    # if there is leftover text without punctuation
    if len(parts) % 2 != 0 and parts[-1].strip():
        s = parts[-1].strip()
        s = re.sub(r'\s+,', ',', s)
        s = re.sub(r',\s+', ', ', s)
        if s:
            para_sentences.append(s + '.')
            
    if not para_sentences:
        continue
        
    # Append paragraph pause to the last sentence
    para_sentences[-1] += '\n. ......\n'
    
    sentences.extend(para_sentences)

# Split into chunks of 15-20 sentences (let's use 18)
chunk_size = 18
chunks = [sentences[i:i + chunk_size] for i in range(0, len(sentences), chunk_size)]

for idx, chunk in enumerate(chunks):
    chunk_text = ' '.join(chunk)
    # Format as code block isn't necessary for the text files themselves, just raw text.
    out_file = os.path.join(output_dir, f'Kich-ban-{idx+1}.txt')
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(chunk_text)

print("Processing complete!")
