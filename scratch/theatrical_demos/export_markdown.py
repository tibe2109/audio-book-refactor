import json

with open("/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/scratch/theatrical_demos/theatrical_demos_11_to_20.json", "r", encoding="utf-8") as f:
    demos = json.load(f)

md_lines = []
md_lines.append("# 🎭 TỔNG HỢP 10 BẢN DEMO KỊCH BẢN THOẠI KỊCH NGHỆ ĐA THANH (DEMO 11 ĐẾN DEMO 20)")
md_lines.append("## Chuyên Môn: Hiện Thực Phê Phán, Văn Học Xã Hội Lầm Than & Noir Mystery")
md_lines.append("> **Đạo Diễn Kịch Nghệ Chuyên Môn 2:** Phân vai Đa thanh, Điêu khắc Formant ATSE & Ma trận Chuyển giao Âm học Thích ứng [0.35s - 1.20s]")
md_lines.append("")
md_lines.append("---")
md_lines.append("")

for idx, d in enumerate(demos, start=11):
    md_lines.append(f"### 🎬 {d['demo_id']}: {d['title']}")
    md_lines.append(f"- **Thể loại:** {d['genre']}")
    md_lines.append(f"- **Cảm hứng văn học:** {d['source_inspiration']}")
    md_lines.append(f"- **Ý đồ kịch nghệ & Đạo diễn âm thanh:** {d['dramaturgical_rationale']}")
    md_lines.append("")
    md_lines.append("#### 👥 Hồ Sơ Nhân Vật & Thiết Lập Formant:")
    md_lines.append("| Nhân Vật | Độ Tuổi | Khí Chất | Cảm Xúc Chính | Base Pitch | Timbre EQ | Giọng Nền |")
    md_lines.append("| :--- | :--- | :--- | :--- | :---: | :--- | :--- |")
    for spk_id, p in d["characters_profile"].items():
        md_lines.append(f"| {p['name']} | `{p['age_stage']}` | `{p['temperament']}` | `{p.get('social_class', '')}` | `{p['base_pitch']}` | `{p['timbre_eq']}` | `{p['baseline_voice']}` |")
    md_lines.append("")
    md_lines.append("#### 📜 Kịch Bản JSON Chuẩn Hóa:")
    md_lines.append("```json")
    md_lines.append(json.dumps(d["script"], ensure_ascii=False, indent=2))
    md_lines.append("```")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")

with open("/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/scratch/theatrical_demos/theatrical_demos_11_to_20.md", "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))

print("Exported Markdown successfully!")
