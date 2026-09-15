import subprocess

def run(cmd):
    res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return res.stdout.strip()

missing = [
    ".audiobook_root",
    "AI_ONBOARDING.md",
    "HUONG_DAN_SU_DUNG.md",
    "docs/HUONG_DAN_THUYET_MINH_NOI_DUNG_TRUC_QUAN_AUDIOBOOK.md",
    "run.bat",
    "run.sh",
    "setup.bat",
    "setup.sh"
]

for m in missing:
    git_path = f"universal-audiobook-pipeline/{m}"
    content = run(f"git show HEAD:{git_path}")
    print(f"=== {m} (Length: {len(content)} chars) ===")
    print("\n".join(content.splitlines()[:20]))
    print("-" * 50)
