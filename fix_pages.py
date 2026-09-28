import sys

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# process_movie_v2 fix
content = re.sub(
    r'while True:\n\s+from pyrogram import enums',
    'while True:\n        if current_page >= 5:\n            print(f"Reached MAX_PAGES (5). Stopping to prevent DB spam.")\n            break\n        from pyrogram import enums',
    content
)

# process_movie fix
content = re.sub(
    r'finished_all_pages = False\n\s+while True:\n\s+active_msg = await client.get_messages\(TARGET_BOT, menu_msg_id\)',
    'finished_all_pages = False\n        while True:\n            if current_page >= 5:\n                print(f"Reached MAX_PAGES (5). Stopping to prevent DB spam.")\n                finished_all_pages = True\n                break\n            active_msg = await client.get_messages(TARGET_BOT, menu_msg_id)',
    content
)

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("done")