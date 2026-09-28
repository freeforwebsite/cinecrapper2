import sys

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = '''            # 1. Forward directly to Database Channel to guarantee backup
            await client.copy_message(
                    chat_id=DATABASE_CHANNEL_ID,
                    from_chat_id=from_chat_id,
                    message_id=msg_id,
                    caption=caption
                )'''

replacement = '''            # 1. Forward directly to Database Channel to guarantee backup
            from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
            btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔥 Join CineSearch 🔥", url="https://t.me/+bTXW_3aYxlw3YWU1")]])
            
            await client.copy_message(
                    chat_id=DATABASE_CHANNEL_ID,
                    from_chat_id=from_chat_id,
                    message_id=msg_id,
                    caption=caption,
                    reply_markup=btn
                )'''

content = content.replace(target, replacement)

# Do the same for the Control Room copy
target2 = '''            # 2. Forward to Control Room (chat_id) for visual feedback
            if chat_id != DATABASE_CHANNEL_ID:
                await client.copy_message(
                        chat_id=chat_id,
                        from_chat_id=from_chat_id,
                        message_id=msg_id,
                        caption=caption
                    )'''
                    
replacement2 = '''            # 2. Forward to Control Room (chat_id) for visual feedback
            if chat_id != DATABASE_CHANNEL_ID:
                await client.copy_message(
                        chat_id=chat_id,
                        from_chat_id=from_chat_id,
                        message_id=msg_id,
                        caption=caption,
                        reply_markup=btn
                    )'''
                    
content = content.replace(target2, replacement2)

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")