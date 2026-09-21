import json, re

with open('Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/03-Hoi-03/.chunks_duration.json') as f:
    durations = json.load(f)

# Let's inspect Chunk 1 to 10 texts and test proposed splits
for c in range(1, 11):
    fn = f'Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/03-Hoi-03/kich-ban/Kich-ban-{c}.txt'
    with open(fn, 'r', encoding='utf-8') as f:
        text = f.read()
    total_dur = durations[f'chunk_{c}.mp3']
    print(f"=== Chunk {c}: Total Duration = {total_dur}s, Total Chars = {len(text)} ===")
