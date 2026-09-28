with open('cinescraper.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines[1050:1080]):
    print(f"{1050+i}: {line.encode('ascii', 'ignore').decode('ascii').rstrip()}")