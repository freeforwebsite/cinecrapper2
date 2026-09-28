import sys

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    content = f.read()

target1 = '''            # Wait 3 seconds to ensure Telegram and the Target Bot process the Send All request before we click Next!
            await asyncio.sleep(3)'''
            
replacement1 = '''            await asyncio.sleep(0.3)'''

target2 = '''                current_page += 1
                await asyncio.sleep(3)'''
                
replacement2 = '''                current_page += 1
                await asyncio.sleep(0.3)'''

content = content.replace(target1, replacement1)
content = content.replace(target2, replacement2)

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")