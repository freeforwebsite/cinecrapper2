import sys

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = '''            # Blast through pages! No need to wait for files to stream because incoming_file_handler catches them instantly in the background!
            await asyncio.sleep(1)'''
            
replacement = '''            # Wait 3 seconds to ensure Telegram and the Target Bot process the Send All request before we click Next!
            await asyncio.sleep(3)'''

content = content.replace(target, replacement)

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")