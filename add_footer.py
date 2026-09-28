import sys

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "Subtitle : {subtitle}" in line:
        lines[i] = line.replace('"""', '\n\n@Cinesearch\nhttps://t.me/+bTXW_3aYxlw3YWU1"""')
        break

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Done")