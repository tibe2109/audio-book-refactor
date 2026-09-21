import json, re

with open('Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/03-Hoi-03/.chunks_duration.json') as f:
    durations = json.load(f)

chunks = {}
for i in range(1, 11):
    with open(f'Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/03-Hoi-03/kich-ban/Kich-ban-{i}.txt', 'r', encoding='utf-8') as f:
        chunks[i] = f.read()

# Let's define sentence boundaries for each chunk
def get_sentences(text):
    # Regex to find sentences while keeping everything
    # We can split at sentence boundaries (. | ! | ? followed by space or newline)
    pattern = re.compile(r'(.+?(?:[.!?]\s+|\.\s+\.\.\.\.\.\.\n+|\n+|$))', re.DOTALL)
    pieces = pattern.findall(text)
    assert "".join(pieces) == text
    return pieces

plan = {}

# CHUNK 1 (153.36s, target 7 shots, ~21.9s/shot, ~329 chars/shot)
# Total chars = 2303
s1 = get_sentences(chunks[1])
# Let's inspect cumulative chars of s1
# We want 7 shots.
def group_pieces(pieces, cut_indices, total_dur):
    shots = []
    prev = 0
    for idx in cut_indices:
        shots.append("".join(pieces[prev:idx]))
        prev = idx
    shots.append("".join(pieces[prev:]))
    
    total_chars = sum(len(s) for s in shots)
    durs = [round(len(s)/total_chars * total_dur, 2) for s in shots]
    diff = round(total_dur - sum(durs), 2)
    durs[-1] = round(durs[-1] + diff, 2)
    return shots, durs

