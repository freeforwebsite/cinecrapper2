import sys

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('\\napp.start()', '\napp.start()')

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")