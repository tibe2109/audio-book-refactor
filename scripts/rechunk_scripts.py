import os
import glob

def rechunk_directory(directory, max_chars=2800):
    txt_files = glob.glob(os.path.join(directory, "Kich-ban-*.txt"))
    if not txt_files:
        return
        
    # Sort files numerically
    try:
        txt_files.sort(key=lambda f: int(''.join(filter(str.isdigit, os.path.basename(f)))))
    except:
        txt_files.sort()
    
    all_paragraphs = []
    for f in txt_files:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read().strip()
            # Split by \n\n but keep the . ...... attached to the paragraph
            paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
            all_paragraphs.extend(paragraphs)
            
    # Delete old files
    for f in txt_files:
        os.remove(f)
        
    file_num = 1
    current_chunk = []
    current_length = 0
    
    for para in all_paragraphs:
        para_len = len(para)
        # If adding this paragraph exceeds max_chars, write current chunk and start a new one
        if current_length + para_len > max_chars and current_chunk:
            out_path = os.path.join(directory, f"Kich-ban-{file_num}.txt")
            with open(out_path, 'w', encoding='utf-8') as out_file:
                out_file.write("\n\n".join(current_chunk))
            file_num += 1
            current_chunk = [para]
            current_length = para_len
        else:
            current_chunk.append(para)
            current_length += para_len + 2 # +2 for \n\n
            
    # Write the last chunk
    if current_chunk:
        out_path = os.path.join(directory, f"Kich-ban-{file_num}.txt")
        with open(out_path, 'w', encoding='utf-8') as out_file:
            out_file.write("\n\n".join(current_chunk))

def main():
    base_dir = "/mnt/d/Solution/Audio-Book-Refactor/Kich-ban-clipchamp/Nghe-thuat-quyen-ru"
    # Find all subdirectories
    subdirs = [os.path.join(base_dir, d) for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    
    for ch_dir in subdirs:
        rechunk_directory(ch_dir)
        print(f"Rechunked {os.path.basename(ch_dir)}")

if __name__ == "__main__":
    main()
