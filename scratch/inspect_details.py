import subprocess
import os

def run(cmd):
    res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return res.stdout.strip()

print("=== COMMITS INFO ===")
for i in range(14):
    cmd = f'git log -1 --skip={i} --format="%h | %ad | %s"'
    info = run(cmd)
    print(f"{i}: {info}")

print("\n=== HISTORY OF core/ ===")
core_commits = run('git log --oneline -- core/').splitlines()
print("Commits touching core/:")
for c in core_commits:
    print("  ", c)

print("\n=== FILES IN core/ AT HEAD ===")
core_head = run('git ls-tree -r --name-only HEAD core/').splitlines()
print(f"Total files in core/ at HEAD: {len(core_head)}")
for f in core_head:
    print("  ", f)

print("\n=== CURRENT FILES IN core/ ON DISK ===")
disk_core = [os.path.join('core', f) for f in os.listdir('core')]
for f in disk_core:
    print("  ", f)

print("\n=== ANY DELETED FILES IN core/ EVER? ===")
all_core_dels = run('git log --diff-filter=D --summary -- core/')
print("Deleted in core/ history:\n", all_core_dels if all_core_dels else "None")
