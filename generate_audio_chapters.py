import os
import subprocess
import glob
import time

# Cấu hình
VOICE = "vi-VN-NamMinhNeural"
RATE = "-20%"
BASE_DIR = "/mnt/d/Solution/Audio-Book-Refactor/Kich-ban-clipchamp/Eat-that-frog"
EDGE_TTS_BIN = "/mnt/d/Solution/Audio-Book-Refactor/venv/bin/edge-tts"

# Định nghĩa các nhóm chương (mỗi nhóm 3 chương, ngoại trừ nhóm cuối)
groups = [
    ["Chuong-6", "Chuong-7", "Chuong-8"],
    ["Chuong-9", "Chuong-10", "Chuong-11"],
    ["Chuong-12", "Chuong-13", "Chuong-14"],
    ["Chuong-15", "Chuong-16", "Chuong-17"],
    ["Chuong-18", "Chuong-19", "Chuong-20"],
    ["Chuong-21"]
]

def get_num(filepath):
    basename = os.path.basename(filepath)
    num_str = basename.replace("Kich-ban-", "").replace(".txt", "")
    try:
        return int(num_str)
    except ValueError:
        return 999

for group in groups:
    group_name = "-".join([c.replace("Chuong-", "") for c in group])
    final_full_mp3 = os.path.join(BASE_DIR, f"Chuong-{group_name}-Full.mp3")
    
    if os.path.exists(final_full_mp3):
        print(f"Đã tồn tại {final_full_mp3}, bỏ qua group này.")
        continue
    
    group_mp3_files = []
    
    for chapter in group:
        chapter_dir = os.path.join(BASE_DIR, chapter)
        if not os.path.isdir(chapter_dir):
            print(f"Không tìm thấy thư mục {chapter_dir}")
            continue
        
        txt_files = glob.glob(os.path.join(chapter_dir, "Kich-ban-*.txt"))
        txt_files.sort(key=get_num)
        
        chapter_mp3s = []
        for txt_file in txt_files:
            # Skip empty files or files containing just spaces/newlines
            with open(txt_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            if not content:
                print(f"File {txt_file} trống, bỏ qua.")
                continue

            basename = os.path.basename(txt_file)
            mp3_name = basename.replace(".txt", "-audio.mp3")
            mp3_path = os.path.join(chapter_dir, mp3_name)
            
            # Skip generation if file already exists
            if not os.path.exists(mp3_path):
                print(f"Đang tạo âm thanh cho: {txt_file} -> {mp3_path}")
                cmd = [
                    EDGE_TTS_BIN,
                    "--voice", VOICE,
                    "--rate", RATE,
                    "--file", txt_file,
                    "--write-media", mp3_path
                ]
                
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        subprocess.run(cmd, check=True)
                        break
                    except subprocess.CalledProcessError:
                        if attempt < max_retries - 1:
                            print(f"Lỗi khi gọi edge-tts. Thử lại lần {attempt+1}...")
                            time.sleep(5)
                        else:
                            print("Lỗi tạo âm thanh quá nhiều lần. Bỏ qua file này.")
                time.sleep(2)  # Nghỉ 2 giây trước file tiếp theo
            else:
                print(f"Đã có sẵn {mp3_path}, sử dụng lại.")
                
            if os.path.exists(mp3_path):
                chapter_mp3s.append(mp3_path)
                group_mp3_files.append(mp3_path)
            
        # Tùy chọn nối theo từng chương
        chapter_full_mp3 = os.path.join(BASE_DIR, f"{chapter}-Full.mp3")
        if not os.path.exists(chapter_full_mp3) and chapter_mp3s:
            print(f"Đang ghép các file của {chapter} thành {chapter_full_mp3}")
            with open(chapter_full_mp3, 'wb') as outfile:
                for mp3_path in chapter_mp3s:
                    with open(mp3_path, 'rb') as infile:
                        outfile.write(infile.read())
                        
    # Nối theo group
    if group_mp3_files:
        print(f"Đang ghép các file của group {group_name} thành {final_full_mp3}")
        with open(final_full_mp3, 'wb') as outfile:
            for mp3_path in group_mp3_files:
                with open(mp3_path, 'rb') as infile:
                    outfile.write(infile.read())

print("\n=> HOÀN THÀNH TẤT CẢ CÁC CHƯƠNG CÒN LẠI!")
