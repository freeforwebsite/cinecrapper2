import re

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update queue_worker to respect "force" flag
pattern1 = r'(if already_in_db:)'
replacement1 = r'if already_in_db and not task.get("force", False):'
code = re.sub(pattern1, replacement1, code)

# 2. Add /force command
force_cmd = '''
@app.on_message(filters.chat(CONTROL_CHANNEL_ID) & filters.command("force", prefixes="/"))
async def force_command(client, message):
    try:
        movie = message.text.split(" ", 1)[1].strip()
        if not movie:
            raise ValueError()
        await queue_col.insert_one({"movie_name": movie, "status": "pending", "force": True, "is_urgent": True})
        await message.reply_text(f"""✅ **Forced:** {movie}\nIt has been urgently queued and will completely bypass the database check!""")
    except Exception:
        await message.reply_text("⚠️ Usage: /force Movie Name 2024")
'''

pattern2 = r'(@app\.on_message\(filters\.chat\(CONTROL_CHANNEL_ID\) & filters\.command\("status", prefixes="/"\)\))'
code = re.sub(pattern2, force_cmd + r'\n\1', code)

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.write(code)