import sys

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "for bot in target_bots:" in line:
        start_idx = i + 21
        for j in range(start_idx, start_idx + 10):
            if "q_str = " in lines[j]: break
            lines[j] = "    " + lines[j]
        break

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Done")