import sys
import re

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix V1 MAX_PAGES limit
target1 = '''            if current_page >= 5:
                print(f"Reached MAX_PAGES (5). Stopping to prevent DB spam.")
                finished_all_pages = True
                break'''
                
content = content.replace(target1, '')

# Fix V1 Message Auto-Deleted restart behavior
target2 = '''            active_msg = await client.get_messages(TARGET_BOT, menu_msg_id)
            if not active_msg or getattr(active_msg, 'empty', False) or not active_msg.reply_markup:
                print(f"⚠️ Message auto-deleted after 5 mins! Restarting search to continue from page {current_page}...")
                break # Break inner loop, restart outer search loop'''
                
replacement2 = '''            active_msg = await client.get_messages(TARGET_BOT, menu_msg_id)
            if not active_msg or getattr(active_msg, 'empty', False) or not active_msg.reply_markup:
                print(f"⚠️ Message auto-deleted by Moon Bot after 5 mins! Stopping gracefully.")
                finished_all_pages = True
                break'''
                
content = content.replace(target2, replacement2)

# Fix V2 MAX_PAGES limit
target3 = '''    while True:
        if current_page >= 5:
            print(f"Reached MAX_PAGES (5). Stopping to prevent DB spam.")
            break
        from pyrogram import enums'''
        
replacement3 = '''    while True:
        from pyrogram import enums'''
        
content = content.replace(target3, replacement3)

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")