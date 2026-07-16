import os
import subprocess
import glob

# Đường dẫn file nhạc nền
BGM_FILE = "/mnt/d/Solution/Audio-Book-Refactor/nhac-nen.mp3"
BASE_DIR = "/mnt/d/Solution/Audio-Book-Refactor/Kich-ban-clipchamp/Eat-that-frog"

# Chúng ta sẽ tìm tất cả các file có tên chứa "Full.mp3" (không có -BGM) để mix nhạc nền.
full_files = glob.glob(os.path.join(BASE_DIR, "Chuong-*-Full.mp3"))

# Vì file nhạc nền của bạn dài, mình sẽ cắt lấy các đoạn khác nhau.
# Bắt đầu từ giây 0, file tiếp theo sẽ lấy từ phút thứ 5, file sau nữa lấy từ phút thứ 10...
start_offset = 0

print(f"Tìm thấy {len(full_files)} file cần mix nhạc nền.")

for audio_file in full_files:
    if "-BGM" in audio_file:
        continue # Bỏ qua nếu đã mix
    
    out_file = audio_file.replace(".mp3", "-BGM.mp3")
    if os.path.exists(out_file):
        print(f"Đã tồn tại {out_file}, bỏ qua.")
        start_offset += 300  # Vẫn tịnh tiến 5 phút
        continue
    
    print(f"\nĐang trộn nhạc nền cho: {os.path.basename(audio_file)}")
    print(f"Sử dụng đoạn nhạc nền bắt đầu từ giây thứ: {start_offset}")
    
    # Lệnh ffmpeg
    # -i audio_file : luồng 0 (giọng đọc)
    # -ss start_offset -i BGM_FILE : luồng 1 (nhạc nền, trích xuất từ vị trí start_offset)
    # [1:a]volume=0.15[bg] : giảm âm lượng nhạc nền xuống 15% để không lấn át giọng đọc
    # [0:a][bg]amix=inputs=2:duration=first:dropout_transition=2[out] : trộn 2 luồng, lấy thời lượng bằng file đọc
    cmd = [
        "ffmpeg", "-y",
        "-i", audio_file,
        "-ss", str(start_offset),
        "-i", BGM_FILE,
        "-filter_complex", "[1:a]volume=0.15[bg];[0:a][bg]amix=inputs=2:duration=first:dropout_transition=2[out]",
        "-map", "[out]",
        out_file
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"✅ Thành công tạo: {os.path.basename(out_file)}")
        # Cộng thêm 300 giây (5 phút) cho đoạn nhạc của file tiếp theo
        start_offset += 300 
    except FileNotFoundError:
        print("❌ KHÔNG TÌM THẤY FFMPEG. Vui lòng cài đặt ffmpeg bằng lệnh: sudo apt install ffmpeg")
        break
    except Exception as e:
        print(f"❌ Lỗi khi trộn nhạc cho {audio_file}: {e}")

print("\n=> HOÀN TẤT QUÁ TRÌNH LỒNG NHẠC NỀN!")
