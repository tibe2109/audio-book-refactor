import subprocess
import json

def run(cmd):
    res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return res.stdout.strip()

commits_raw = run('git log --format="%H|%h|%ad|%an|%s" --date=short')
commits = [line.split('|') for line in commits_raw.splitlines() if line]

print(f"Total commits: {len(commits)}")
for c in commits:
    full_h, short_h, date, author, msg = c
    files = run(f'git show --name-status --oneline {full_h}').splitlines()[1:]
    added = sum(1 for f in files if f.startswith('A\t'))
    deleted = sum(1 for f in files if f.startswith('D\t'))
    modified = sum(1 for f in files if f.startswith('M\t'))
    renamed = sum(1 for f in files if f.startswith('R'))
    print(f"[{short_h}] {date} by {author}: {msg} (A:{added}, D:{deleted}, M:{modified}, R:{renamed})")
