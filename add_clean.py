import sys
import re

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add auto-cleanup to incoming_file_handler
target1 = '''    # Safely handle missing file names
    file_name = getattr(doc, 'file_name', None)
    if not file_name:
        file_name = "Unknown_Movie.mkv"
        
    file_size = doc.file_size'''

replace1 = '''    # Safely handle missing file names
    file_name = getattr(doc, 'file_name', None)
    if not file_name:
        file_name = "Unknown_Movie.mkv"
        
    import re
    # Auto-clean junk tags and usernames from file name
    file_name = re.sub(r'@[a-zA-Z0-9_]+', '', file_name)
    file_name = re.sub(r'(?i)CharmeLeon', '', file_name)
    file_name = re.sub(r'\s+', ' ', file_name).strip()
        
    file_size = doc.file_size'''

content = content.replace(target1, replace1)


# 2. Add /clean_tags command
clean_tags_logic = '''@app.on_message(filters.chat(CONTROL_CHANNEL_ID) & filters.command("clean_tags", prefixes="/"))
async def clean_tags_command(client, message):
    status_msg = await message.reply_text("dY-,? **Bulk Cleaner Started!**\\nScanning entire Database Channel history to remove @ tags and junk...")
    
    DATABASE_CHANNEL_ID = -1003975570574
    updated_count = 0
    db_updated = 0
    import re
    
    try:
        async for msg in client.get_chat_history(DATABASE_CHANNEL_ID):
            if msg.caption:
                new_caption = re.sub(r'@[a-zA-Z0-9_]+', '', msg.caption)
                new_caption = re.sub(r'(?i)CharmeLeon', '', new_caption)
                
                if new_caption != msg.caption:
                    try:
                        await client.edit_message_caption(
                            chat_id=DATABASE_CHANNEL_ID,
                            message_id=msg.id,
                            caption=new_caption,
                            reply_markup=msg.reply_markup
                        )
                        updated_count += 1
                        await asyncio.sleep(2)
                    except Exception as e:
                        pass
                        
        # Clean MongoDB too
        async for doc in movies_col.find({}):
            fname = doc.get("file_name", "")
            new_fname = re.sub(r'@[a-zA-Z0-9_]+', '', fname)
            new_fname = re.sub(r'(?i)CharmeLeon', '', new_fname)
            
            if new_fname != fname:
                await movies_col.update_one({"_id": doc["_id"]}, {"": {"file_name": new_fname}})
                db_updated += 1
                
        await status_msg.edit_text(f"dY"o **Bulk Clean Complete!**\\n\\ndY-,? Removed @ tags from **{updated_count}** messages.\\no. Cleaned **{db_updated}** records in Database.")
    except Exception as e:
        await status_msg.edit_text(f"?O Error: {e}")

'''

# Insert before rename_command
target2 = '@app.on_message(filters.chat(CONTROL_CHANNEL_ID) & filters.command("rename", prefixes="/"))'
content = content.replace(target2, clean_tags_logic + target2)

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")