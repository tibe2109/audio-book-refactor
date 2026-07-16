import os
import glob
import re

def process_title(line):
    # Detect if title is glued to the first sentence.
    # Title consists of multiple all-uppercase words.
    words = line.split()
    title_words = []
    rest_words = []
    
    for i, word in enumerate(words):
        has_lower = any(c.islower() for c in word)
        has_upper = any(c.isupper() for c in word)
        
        if has_lower:
            rest_words = words[i:]
            break
        else:
            title_words.append(word)
            
    # To be a valid title glued to a sentence, we need at least one title word,
    # and at least one rest word.
    if title_words and rest_words:
        # Also ensure at least one title word actually has uppercase letters (not just punctuation/numbers)
        if any(any(c.isupper() for c in w) for w in title_words):
            title_str = " ".join(title_words)
            rest_str = " ".join(rest_words)
            return f"{title_str}. ......\n{rest_str}"
            
    return line

def add_commas_to_long_sentences(paragraph):
    # 1. Temporarily replace ". ......" so it doesn't get affected by sentence splitting.
    paragraph = paragraph.replace('. ......', '###DOTDOTDOT###')
    
    # 2. Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', paragraph)
    new_sentences = []
    
    for s in sentences:
        words = s.split()
        # count words. if > 15 and no comma, insert a comma.
        if len(words) > 15 and ',' not in s:
            for keyword in ['rằng', 'là', 'để', 'mà', 'thì', 'và', 'hoặc']:
                if keyword in words[5:-5]:
                    idx = words.index(keyword)
                    # Insert comma to the word
                    words[idx] = words[idx] + ','
                    break
            else:
                mid = len(words) // 2
                words[mid] = words[mid] + ','
            new_sentences.append(' '.join(words))
        else:
            new_sentences.append(s)
            
    res = ' '.join(new_sentences)
    
    # 3. Restore ". ......"
    res = res.replace('###DOTDOTDOT###', '. ......')
    
    # 4. Clean up any weird comma artifacts just in case
    res = res.replace(', .', '.')
    res = res.replace(',,', ',')
    
    return res

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    paragraphs = content.split('\n')
    new_paragraphs = []
    
    for i, p in enumerate(paragraphs):
        p = p.strip()
        if not p:
            new_paragraphs.append("")
            continue
            
        p = process_title(p)
        
        # Now p might be two lines if a title was split.
        sub_paragraphs = p.split('\n')
        processed_subs = []
        for sub_p in sub_paragraphs:
            sub_p = sub_p.strip()
            if sub_p:
                sub_p = add_commas_to_long_sentences(sub_p)
            processed_subs.append(sub_p)
            
        new_paragraphs.append('\n'.join(processed_subs))
        
    final_content = '\n'.join(new_paragraphs)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(final_content)

def main():
    target_dir = "/mnt/d/Solution/Audio-Book-Refactor/Kich-ban-clipchamp/Nghe-thuat-quyen-ru/Chuong-8-Ngi-n-b-duyn-dng"
    files = glob.glob(os.path.join(target_dir, "*.txt"))
    for f in files:
        print(f"Processing {f}...")
        process_file(f)
    print("Done!")

if __name__ == "__main__":
    main()
