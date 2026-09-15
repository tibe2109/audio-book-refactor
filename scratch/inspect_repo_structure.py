import subprocess
import os

def run(cmd):
    res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return res.stdout.strip()

print("=== 1. COMPARE universal-audiobook-pipeline IN HEAD VS ROOT ===")
uap_files = run('git ls-tree -r --name-only HEAD universal-audiobook-pipeline/').splitlines()
print(f"Total files in universal-audiobook-pipeline at HEAD: {len(uap_files)}")

for u_path in uap_files:
    rel_path = u_path[len("universal-audiobook-pipeline/"):]
    # Check possible root locations
    root_exists = os.path.exists(rel_path)
    agent_skill = os.path.exists(os.path.join(".agent", rel_path))
    agy_skill = os.path.exists(os.path.join(".agy", rel_path))
    status = "EXISTS at root" if root_exists else ("EXISTS in .agent" if agent_skill else ("EXISTS in .agy" if agy_skill else "MISSING"))
    print(f"  {rel_path} -> {status}")
