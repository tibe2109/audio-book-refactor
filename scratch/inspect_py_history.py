import subprocess

def run(cmd):
    res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return res.stdout.strip()

print("=== ALL COMMITS THAT DELETED .py FILES ===")
py_dels = run('git log --diff-filter=D --summary -- "*.py"')
print(py_dels if py_dels else "None")

print("\n=== ALL COMMITS TOUCHING .py FILES ===")
commits_touching_py = run('git log --name-status -- "*.py"').splitlines()
for line in commits_touching_py:
    if line.startswith('commit ') or any(line.startswith(x) for x in ['A\t', 'D\t', 'M\t', 'R']):
        print(line[:100])
