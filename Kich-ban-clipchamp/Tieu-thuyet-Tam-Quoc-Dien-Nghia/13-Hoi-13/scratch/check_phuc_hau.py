import json

with open("/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia/13-Hoi-13/theatrical_script.json", "r", encoding="utf-8") as f:
    script = json.load(f)

for item in script:
    if item.get("type") == "dialogue":
        print(f"[{item.get('speaker')}]: {item.get('text')}")
