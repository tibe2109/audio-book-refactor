import os
import subprocess
import glob
import time

VOICE = "vi-VN-NamMinhNeural"
RATE = "-20%"
BASE_DIR = "/mnt/d/Solution/Audio-Book-Refactor/Kich-ban-clipchamp/Nghe-thuat-quyen-ru"
EDGE_TTS_BIN = "/mnt/d/Solution/Audio-Book-Refactor/venv/bin/edge-tts"

def get_num(filepath):
    basename = os.path.basename(filepath)
    num_str = basename.replace("Kich-ban-", "").replace(".txt", "")
    try:
        return int(num_str)
    except ValueError:
        return 999
        
def get_chapter_num(dirpath):
    basename = os.path.basename(dirpath)
    # Ex: Chuong-1, Chuong-19
    match = __import__('re').search(r'Chuong-(\d+)', basename)
    if match:
        return int(match.group(1))
    return 999

def process_audio():
    chapter_dirs = glob.glob(os.path.join(BASE_DIR, "Chuong-*"))
    chapter_dirs.sort(key=get_chapter_num)
    
    processed_any = False

    for chapter_dir in chapter_dirs:
        txt_files = glob.glob(os.path.join(chapter_dir, "Kich-ban-*.txt"))
        txt_files.sort(key=get_num)
        
        for txt_file in txt_files:
            basename = os.path.basename(txt_file)
            mp3_name = basename.replace(".txt", "-audio.mp3")
            mp3_path = os.path.join(chapter_dir, mp3_name)
            
            if not os.path.exists(mp3_path):
                print(f"Đang tạo âm thanh cho: {txt_file} -> {mp3_path}")
                cmd = [
                    EDGE_TTS_BIN,
                    "--voice", VOICE,
                    "--rate", RATE,
                    "--file", txt_file,
                    "--write-media", mp3_path
                ]
                try:
                    subprocess.run(cmd, check=True)
                    processed_any = True
                    time.sleep(1)
                except subprocess.CalledProcessError as e:
                    print(f"Lỗi tạo audio file {txt_file}: {e}")
                    
    return processed_any

def main():
    print("Bắt đầu tiến trình theo dõi và tạo Audio tự động...")
    # Loop for roughly 2 hours waiting for subagents to finish
    for _ in range(120):
        try:
            processed = process_audio()
            if not processed:
                # If no new files, sleep for 60 seconds
                print("Đang đợi thêm kịch bản mới...")
                time.sleep(60)
            else:
                # If it processed files, immediately check again
                pass
        except Exception as e:
            print(f"Lỗi: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
