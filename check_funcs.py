import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('cinescraper.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(510, 1380):
    if 'async def' in lines[i]:
        print(f"{i+1}: {lines[i].rstrip()}")