import sys

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('\\n\\n@app.on_message', '\n\n@app.on_message')

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed")