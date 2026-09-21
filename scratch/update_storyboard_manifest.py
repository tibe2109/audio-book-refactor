import os
import json
import glob
import re

BASE_DIR = "/media/hoanganh/disk1_vol1/Solution/audio-book-refactor/Kich-ban-clipchamp/Tam-Quoc-Dien-Nghia"
MANIFEST_PATH = os.path.join(BASE_DIR, ".storyboard_manifest.json")

CHAPTERS = ["02-Hoi-02", "03-Hoi-03", "04-Hoi-04", "05-Hoi-05"]

def audit_chapter(chap_name):
    chap_dir = os.path.join(BASE_DIR, chap_name)
    sb_dir = os.path.join(chap_dir, "storyboard_video")
    kb_dir = os.path.join(chap_dir, "kich-ban")
    dur_file = os.path.join(chap_dir, ".chunks_duration.json")
    
    with open(dur_file, "r", encoding="utf-8") as f:
        durations = json.load(f)
        
    total_scripts = len(glob.glob(os.path.join(kb_dir, "Kich-ban-*.txt")))
    sb_files = sorted(glob.glob(os.path.join(sb_dir, "Kich-ban-*.md")), key=lambda x: int(os.path.basename(x).replace("Kich-ban-","").replace(".md","")))
    
    report = {
        "chapter": chap_name,
        "total_scripts": total_scripts,
        "storyboards_found": len(sb_files),
        "files": [],
        "all_valid": True,
        "errors": []
    }
    
    for i in range(1, total_scripts + 1):
        sb_file = os.path.join(sb_dir, f"Kich-ban-{i}.md")
        txt_file = os.path.join(kb_dir, f"Kich-ban-{i}.txt")
        file_name = f"Kich-ban-{i}.md"
        
        if not os.path.exists(sb_file):
            report["all_valid"] = False
            report["errors"].append(f"Missing {file_name}")
            continue
            
        with open(sb_file, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Check 2 tables / sections
        has_part1 = ("PHẦN 1" in content or "BẢNG PHÂN CẢNH" in content) and "|" in content
        has_part2 = ("PHẦN 2" in content or "MÔ TẢ CHI TIẾT" in content)
        if not (has_part1 and has_part2):
            report["all_valid"] = False
            report["errors"].append(f"{file_name}: Missing Part 1 or Part 2")
            
        # Check aspect ratio
        if "16:9" not in content:
            report["all_valid"] = False
            report["errors"].append(f"{file_name}: Missing 16:9 aspect ratio")
            
        # Check text coverage
        if os.path.exists(txt_file):
            with open(txt_file, "r", encoding="utf-8") as f:
                raw_text = f.read()
            raw_words = set(re.findall(r"\b\w{3,}\b", raw_text.lower()))
            sb_words = set(re.findall(r"\b\w{3,}\b", content.lower()))
            coverage = 1.0 - (len(raw_words - sb_words) / max(1, len(raw_words)))
            if coverage < 0.70:
                report["all_valid"] = False
                report["errors"].append(f"{file_name}: Low word coverage {coverage:.1%}")
                
        report["files"].append({
            "name": file_name,
            "size": len(content),
            "valid": True
        })
        
    return report

def update_manifest():
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)
        
    updated = False
    summary_results = []
    
    for chap in CHAPTERS:
        rep = audit_chapter(chap)
        summary_results.append(rep)
        if rep["storyboards_found"] == rep["total_scripts"] and rep["all_valid"]:
            manifest["chapters"][chap]["storyboards_completed"] = [f["name"] for f in rep["files"]]
            manifest["chapters"][chap]["storyboards_pending"] = []
            manifest["chapters"][chap]["status"] = "completed"
            updated = True
        else:
            completed = [f["name"] for f in rep["files"]]
            pending = [f"Kich-ban-{i}.md" for i in range(1, rep["total_scripts"] + 1) if f"Kich-ban-{i}.md" not in completed]
            manifest["chapters"][chap]["storyboards_completed"] = completed
            manifest["chapters"][chap]["storyboards_pending"] = pending
            manifest["chapters"][chap]["status"] = "in_progress" if completed else "pending"
            
    # Recalculate totals
    total_completed = 0
    total_pending = 0
    for c_key, c_val in manifest["chapters"].items():
        total_completed += len(c_val.get("storyboards_completed", []))
        total_pending += len(c_val.get("storyboards_pending", []))
        
    manifest["total_storyboards_completed"] = total_completed
    manifest["total_storyboards_pending"] = total_pending
    
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        
    print("Manifest updated successfully.")
    for rep in summary_results:
        print(f"[{rep['chapter']}] Found: {rep['storyboards_found']}/{rep['total_scripts']}, Valid: {rep['all_valid']}")
        if rep['errors']:
            print(f"   Errors: {rep['errors'][:3]}")

if __name__ == "__main__":
    update_manifest()
