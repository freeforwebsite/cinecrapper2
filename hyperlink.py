import sys

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update caption text to use Markdown hyperlink
target = '''@Cinesearch
https://t.me/+bTXW_3aYxlw3YWU1"""'''

replacement = '''[@Cinesearch](https://t.me/+bTXW_3aYxlw3YWU1)"""'''

content = content.replace(target, replacement)

# 2. Add parse_mode to copy_message
content = content.replace('caption=caption,', 'caption=caption, parse_mode=enums.ParseMode.MARKDOWN,')

# 3. Remove the inline button since they said "no"
# Wait, they might still like the button? "no if i clik the @cinesearch it want to redirect like the link hidden in the word"
# I'll just remove the button to exactly match their request so I don't annoy them.
target2 = '''            from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
            btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔥 Join CineSearch 🔥", url="https://t.me/+bTXW_3aYxlw3YWU1")]])
            
            await client.copy_message(
                    chat_id=DATABASE_CHANNEL_ID,
                    from_chat_id=from_chat_id,
                    message_id=msg_id,
                    caption=caption,
                    parse_mode=enums.ParseMode.MARKDOWN,
                    reply_markup=btn
                )'''
                
replacement2 = '''            from pyrogram.enums import ParseMode
            await client.copy_message(
                    chat_id=DATABASE_CHANNEL_ID,
                    from_chat_id=from_chat_id,
                    message_id=msg_id,
                    caption=caption,
                    parse_mode=ParseMode.MARKDOWN
                )'''

content = content.replace(target2, replacement2)

# Do the same for the second one
target3 = '''                await client.copy_message(
                        chat_id=chat_id,
                        from_chat_id=from_chat_id,
                        message_id=msg_id,
                        caption=caption,
                        parse_mode=enums.ParseMode.MARKDOWN,
                        reply_markup=btn
                    )'''
                    
replacement3 = '''                await client.copy_message(
                        chat_id=chat_id,
                        from_chat_id=from_chat_id,
                        message_id=msg_id,
                        caption=caption,
                        parse_mode=ParseMode.MARKDOWN
                    )'''
                    
content = content.replace(target3, replacement3)

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")