with open('cinescraper.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find all lines with task.get and print line numbers
for i, line in enumerate(lines, 1):
    if 'task.get' in line:
        print(f"Line {i}: {line.rstrip()}")