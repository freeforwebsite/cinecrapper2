import re

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace i % 15 == 0 and i % 25 == 0 with i % 100 == 0 to prevent Telegram FloodWait limits
code = re.sub(r'if i % 15 == 0:', 'if i % 100 == 0:', code)
code = re.sub(r'if i % 25 == 0:', 'if i % 100 == 0:', code)

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.write(code)