import sys

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = lines[:877] + ["\n"] + lines[991:]

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)