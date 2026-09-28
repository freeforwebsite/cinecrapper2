import sys
import re

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the auto-cleaner
target = '''    # Auto-clean junk tags and usernames from file name
    file_name = re.sub(r'@[a-zA-Z0-9_]+', '', file_name)
    file_name = re.sub(r'(?i)CharmeLeon', '', file_name)
    file_name = re.sub(r'\\s+', ' ', file_name).strip()'''

replacement = '''    # Auto-clean junk tags and usernames from file name
    file_name = re.sub(r'@[a-zA-Z0-9_]+', '', file_name)
    file_name = re.sub(r'(?i)CharmeLeon', '', file_name)
    
    # Strip encoder groups after the last hyphen (e.g. " - mkvCine.mkv")
    if ' - ' in file_name:
        parts = file_name.rsplit(' - ', 1)
        ext = ''
        if '.' in parts[1]:
            ext = '.' + parts[1].rsplit('.', 1)[-1]
        file_name = parts[0] + ext
        
    file_name = re.sub(r'\\s+', ' ', file_name).strip()'''

content = content.replace(target, replacement)

# 2. Update the bulk cleaner for existing messages
target2 = '''            if msg.caption:
                new_caption = re.sub(r'@[a-zA-Z0-9_]+', '', msg.caption)
                new_caption = re.sub(r'(?i)CharmeLeon', '', new_caption)
                
                if new_caption != msg.caption:'''

replacement2 = '''            if msg.caption:
                new_caption = re.sub(r'@[a-zA-Z0-9_]+', '', msg.caption)
                new_caption = re.sub(r'(?i)CharmeLeon', '', new_caption)
                
                # Also clean Name: field in caption if it has a hyphen encoder
                lines = new_caption.split('\\n')
                for i, line in enumerate(lines):
                    if line.startswith('📁 Name:') or line.startswith('Name:'):
                        if ' - ' in line:
                            parts = line.rsplit(' - ', 1)
                            ext = ''
                            if '.' in parts[1]:
                                ext = '.' + parts[1].rsplit('.', 1)[-1]
                            lines[i] = parts[0] + ext
                new_caption = '\\n'.join(lines)
                
                if new_caption != msg.caption:'''

content = content.replace(target2, replacement2)

# 3. Update the bulk cleaner for Mongo DB
target3 = '''            new_fname = re.sub(r'@[a-zA-Z0-9_]+', '', fname)
            new_fname = re.sub(r'(?i)CharmeLeon', '', new_fname)
            
            if new_fname != fname:'''

replacement3 = '''            new_fname = re.sub(r'@[a-zA-Z0-9_]+', '', fname)
            new_fname = re.sub(r'(?i)CharmeLeon', '', new_fname)
            
            if ' - ' in new_fname:
                parts = new_fname.rsplit(' - ', 1)
                ext = ''
                if '.' in parts[1]:
                    ext = '.' + parts[1].rsplit('.', 1)[-1]
                new_fname = parts[0] + ext
            
            if new_fname != fname:'''

content = content.replace(target3, replacement3)

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")