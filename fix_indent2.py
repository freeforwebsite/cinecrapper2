import sys

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "for bot in target_bots:" in line:
        # indent the next 20 lines by 4 spaces
        for j in range(i+2, i+21):
            if "q_str = " in lines[j]: break
            lines[j] = "    " + lines[j]

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Done")