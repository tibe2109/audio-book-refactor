import os
import glob
import subprocess
import re
import sys
import time

def extract_code_block(text):
    match = re.search(r'```(?:.*?)\n(.*?)```', text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()

def process_chunk(chunk_path, prompt_text, log_file):
    with open(log_file, 'r', encoding='utf-8') as f:
        processed = f.read().splitlines()
        
    if chunk_path in processed:
        print(f"Skipping already processed: {chunk_path}")
        return True

    print(f"\nProcessing {chunk_path}...")
    with open(chunk_path, 'r', encoding='utf-8') as f:
        content = f.read()

    full_prompt = f"{prompt_text}\n\nVăn bản cần xử lý:\n{content}"
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            result = subprocess.run(["agy", "--print", full_prompt], capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                refined_text = extract_code_block(result.stdout)
                
                with open(chunk_path, 'w', encoding='utf-8') as f:
                    f.write(refined_text)
                    
                with open(log_file, 'a', encoding='utf-8') as f:
                    f.write(chunk_path + "\n")
                    
                print(f"Successfully processed {chunk_path}")
                return True
            else:
                print(f"Error on attempt {attempt+1}: {result.stderr}")
        except Exception as e:
            print(f"Exception on attempt {attempt+1}: {str(e)}")
            
        time.sleep(5)
    
    print(f"Failed to process {chunk_path} after {max_retries} attempts.")
    return False

def main():
    base_dir = "/mnt/d/Solution/Audio-Book-Refactor/Kich-ban-clipchamp/Quy-luat-ve-ban-chat-con-nguoi"
    prompt_file = "/mnt/d/Solution/Audio-Book-Refactor/Promt-chuan-danh-cho-AI-tao-kich-ban-tts-clipchamp"
    log_file = "/mnt/d/Solution/Audio-Book-Refactor/process_log.txt"
    
    if not os.path.exists(log_file):
        open(log_file, 'w').close()
    
    with open(prompt_file, 'r', encoding='utf-8') as f:
        prompt_text = f.read()
        
    subdirs = sorted([d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))])
    
    for d in subdirs:
        if "01-Th" in d:
            continue
            
        chapter_dir = os.path.join(base_dir, d)
        chunk_files = sorted(glob.glob(os.path.join(chapter_dir, "final_script_part_*.txt")), key=lambda x: int(re.search(r'_part_(\d+)', x).group(1)))
        
        print(f"--- Starting Chapter {d} ({len(chunk_files)} chunks) ---")
        for chunk_file in chunk_files:
            process_chunk(chunk_file, prompt_text, log_file)

if __name__ == "__main__":
    main()
