import sys

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "Quality : {quality}" in line:
        lines.insert(i, "    👉 🗓 Year : {year}\n")
        break

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Done")