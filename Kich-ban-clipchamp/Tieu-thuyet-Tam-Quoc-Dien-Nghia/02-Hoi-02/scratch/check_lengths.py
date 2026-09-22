# -*- coding: utf-8 -*-
import os
import re

CHAPTER_DIR = "/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/02-Hoi-02"
KICH_BAN_DIR = os.path.join(CHAPTER_DIR, "kich-ban")

def clean_for_compare(text):
    # normalize spaces, dots, newlines
    text = re.sub(r'\s+', ' ', text).strip()
    return text

for i in range(1, 14):
    p = os.path.join(KICH_BAN_DIR, f"Kich-ban-{i}.txt")
    with open(p, "r", encoding="utf-8") as f:
        content = f.read().strip()
    print(f"Chunk {i}: length={len(content)} chars, words={len(content.split())}")
