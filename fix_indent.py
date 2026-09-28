import sys

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = '''            if not active_msg or getattr(active_msg, 'empty', False) or not active_msg.reply_markup:
                print(f"⏱️ Message auto-deleted by Moon Bot after 5 mins! Stopping gracefully.")
            finished_all_pages = True
            break'''
            
replacement = '''            if not active_msg or getattr(active_msg, 'empty', False) or not active_msg.reply_markup:
                print(f"⏱️ Message auto-deleted by Moon Bot after 5 mins! Stopping gracefully.")
                finished_all_pages = True
                break'''

content = content.replace(target, replacement)

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")