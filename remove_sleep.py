import sys

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = '''            # Wait for files from this page to stream
            await asyncio.sleep(15)'''

replacement = '''            # Blast through pages! No need to wait for files to stream because incoming_file_handler catches them instantly in the background!
            await asyncio.sleep(1)'''

content = content.replace(target, replacement)

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")