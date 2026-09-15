import subprocess

def run(cmd):
    res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return res.stdout.strip()

print("=== 1. DELETED IN 2c859b3 ===")
files_2c859b3 = run('git show --name-status 2c859b3').splitlines()
deleted_2c859b3 = [line for line in files_2c859b3 if line.startswith('D\t')]
print(f"Total deleted in 2c859b3: {len(deleted_2c859b3)}")
# Sample categories
cats = {}
for line in deleted_2c859b3:
    path = line.split('\t')[1]
    top = path.split('/')[0] if '/' in path else 'ROOT'
    cats[top] = cats.get(top, 0) + 1
print("Categories deleted in 2c859b3:", cats)

print("\n=== 2. DELETED IN 11862ec ===")
files_11862ec = run('git show --name-status 11862ec').splitlines()
deleted_11862ec = [line for line in files_11862ec if line.startswith('D\t')]
print(f"Total deleted in 11862ec: {len(deleted_11862ec)}")
cats_11 = {}
for line in deleted_11862ec:
    path = line.split('\t')[1]
    top = path.split('/')[0] if '/' in path else 'ROOT'
    cats_11[top] = cats_11.get(top, 0) + 1
print("Categories deleted in 11862ec:", cats_11)
for line in deleted_11862ec:
    print("  ", line)

print("\n=== 3. ALL COMMITS WITH DELETIONS ===")
commits_raw = run('git log --format="%H|%h|%s"')
for line in commits_raw.splitlines():
    h, short_h, msg = line.split('|')
    show = run(f'git show --name-status {h}').splitlines()
    dels = [l for l in show if l.startswith('D\t')]
    if dels:
        print(f"[{short_h}] {msg}: {len(dels)} files deleted")
