import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('cinescraper.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'if success:' in line:
        start = max(0, i-2)
        end = min(len(lines), i+80)
        print("-------")
        for j in range(start, end):
            print(f"{j+1}: {lines[j].rstrip()}")