import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('cinescraper.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'async def process_movie(client, movie):' in line:
        print(f"process_movie starts at {i+1}")