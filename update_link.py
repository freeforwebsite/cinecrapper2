import sys

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = '''[@Cinesearch](https://t.me/+bTXW_3aYxlw3YWU1)'''
replacement = '''[@wrldcine](https://t.me/+bTXW_3aYxlw3YWU1)'''

content = content.replace(target, replacement)

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")