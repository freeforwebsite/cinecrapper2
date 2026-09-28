import sys

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = '''                current_page += 1
                await asyncio.sleep(1.5)'''
                
replacement = '''                current_page += 1
                await asyncio.sleep(0.3)'''
                
content = content.replace(target, replacement)

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")