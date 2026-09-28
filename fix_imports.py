import re

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Remove the internal imports from the patched sections
pattern = r'(from pyrogram\.types import InlineKeyboardMarkup, InlineKeyboardButton\s+)import urllib\.parse\s+import time\s+import re'
replacement = r'\1'

new_code = re.sub(pattern, replacement, code)

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.write(new_code)