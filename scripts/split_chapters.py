import os
import re

text_path = '/mnt/d/Solution/Audio-Book-Refactor/scratch_pdf_nghethuat.txt'
out_dir = '/mnt/d/Solution/Audio-Book-Refactor/Docs/nghethuat_chunks'
os.makedirs(out_dir, exist_ok=True)

with open(text_path, 'r', encoding='utf-8') as f:
    text = f.read()

# The book is huge. We can split it into chunks of roughly 50000 characters.
chunk_size = 50000
chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

for i, chunk in enumerate(chunks):
    chunk_path = os.path.join(out_dir, f'chunk_{i+1:03d}.txt')
    with open(chunk_path, 'w', encoding='utf-8') as f:
        f.write(chunk)
print(f"Split into {len(chunks)} chunks.")
