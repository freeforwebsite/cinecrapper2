import sys

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    content = f.read()

rename_logic = '''@app.on_message(filters.chat(CONTROL_CHANNEL_ID) & filters.command("rename", prefixes="/"))
async def rename_command(client, message):
    try:
        args = message.text.split(" ", 1)[1].strip()
        if "|" not in args:
            raise ValueError()
            
        old_word, new_word = [x.strip() for x in args.split("|", 1)]
        if not old_word or not new_word:
            raise ValueError()
            
        status_msg = await message.reply_text(f"🔍 **Searching Database Channel for:** {old_word}...")
        
        DATABASE_CHANNEL_ID = -1003975570574
        
        updated_count = 0
        async for msg in client.search_messages(chat_id=DATABASE_CHANNEL_ID, query=old_word):
            if msg.caption:
                import re
                new_caption = re.sub(re.escape(old_word), new_word, msg.caption, flags=re.IGNORECASE)
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
                        print(f"Error editing message {msg.id}: {e}")
                        
        db_updated = 0
        import re
        regex = re.compile(re.escape(old_word), re.IGNORECASE)
        async for doc in movies_col.find({"file_name": regex}):
            new_file_name = regex.sub(new_word, doc["file_name"])
            await movies_col.update_one({"_id": doc["_id"]}, {"": {"file_name": new_file_name}})
            db_updated += 1
            
        await status_msg.edit_text(f"✅ **Rename Complete!**\\n✏️ Edited **{updated_count}** messages in the Database Channel.\\n💾 Updated **{db_updated}** records in MongoDB.\\n\\n({old_word} ➡️ {new_word})")
        
    except Exception:
        await message.reply_text("⚠️ Usage: /rename old_name | new_name\\nExample: /rename Modha | Mudhal Rathiri")

'''

# Insert right before unified_file_handler
target = '@app.on_message(filters.chat(CONTROL_CHANNEL_ID) & (filters.document | filters.command(["queue", "forcequeue"], prefixes="/")))'
content = content.replace(target, rename_logic + target)

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Added rename command!")