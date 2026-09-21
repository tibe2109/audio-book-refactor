import subprocess

for cmd in [
    ["./tools/ffmpeg/ffmpeg", "-y", "-loop", "1", "-framerate", "25", "-i", "/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/Final-Tam-Quoc-Dien-Nghia/backgrounds/Background-1_1080p.png", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", "10", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-r", "25", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "scratch/test_anull.mp4"],
    ["./tools/ffmpeg/ffmpeg", "-y", "-loop", "1", "-framerate", "25", "-i", "/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/Final-Tam-Quoc-Dien-Nghia/backgrounds/Background-1_1080p.png", "-i", "/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/Final-Tam-Quoc-Dien-Nghia/Final_Audio_01-Hoi-01_Part1.mp3", "-t", "10", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-r", "25", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "scratch/test_audio10.mp4"]
]:
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

for f in ["scratch/test_anull.mp4", "scratch/test_audio10.mp4"]:
    print("Testing:", f)
    res = subprocess.run(["./tools/ffmpeg/ffmpeg", "-v", "error", "-i", f, "-f", "null", "-"], stderr=subprocess.PIPE, text=True)
    if res.stderr:
        print("  Error:", res.stderr[:200])
    else:
        print("  Clean!")
