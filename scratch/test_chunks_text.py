import json, re

for c in range(1, 11):
    fn = f'Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/03-Hoi-03/kich-ban/Kich-ban-{c}.txt'
    with open(fn, 'r', encoding='utf-8') as f:
        text = f.read()
    print(f"\n==================== CHUNK {c} ====================")
    # Split by newlines and sentence ends
    # Let's inspect raw text
    print(text)
