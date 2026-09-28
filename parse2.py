with open('all_tags.md', 'r', encoding='utf-8') as f:
    content = f.read()
    
# Content has literal '\n'
lines = content.split('\\n')

with open('clean_tags_list.txt', 'w', encoding='utf-8') as out:
    for line in lines:
        if line.startswith('| @'):
            tag = line.split('|')[1].strip()
            out.write(tag + '\n')