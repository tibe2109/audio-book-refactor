import os
import glob

chap_dir = "/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/17-Hoi-17"
kich_ban_dir = os.path.join(chap_dir, "kich-ban")
files = sorted(glob.glob(os.path.join(kich_ban_dir, "Kich-ban-*.txt")))

for fpath in files:
    print(f"=== {os.path.basename(fpath)} ===")
    with open(fpath, "r", encoding="utf-8") as f:
        text = f.read()
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    for p_idx, p in enumerate(paragraphs):
        print(f"  [P{p_idx+1}] len={len(p)}: {p[:100]}...")
