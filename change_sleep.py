import re

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    code = f.read()

code = re.sub(r'await asyncio\.sleep\(60\)', 'await asyncio.sleep(30)', code)
code = re.sub(r'Sleeping for 60 seconds', 'Sleeping for 30 seconds', code)

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.write(code)