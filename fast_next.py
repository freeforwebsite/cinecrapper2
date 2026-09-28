import sys
import re

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace sleep(4) after clicking Next with sleep(1.5) to speed up pagination
target = '''                current_page += 1
                await asyncio.sleep(4)'''

replacement = '''                current_page += 1
                await asyncio.sleep(1.5)'''
                
content = content.replace(target, replacement)

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")