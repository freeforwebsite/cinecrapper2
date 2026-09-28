with open('all_tags.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    
with open('clean_tags_list.txt', 'w', encoding='utf-8') as out:
    for line in lines:
        if line.startswith('| @'):
            tag = line.split('|')[1].strip()
            out.write(tag + '\\n')