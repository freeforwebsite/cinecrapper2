import sys

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Fix task.get bug in queue_worker
target1 = '''        if conditions:
            already_in_db = await movies_col.find_one({"$and": conditions})
            
        if already_in_db:
            await queue_col.update_one({"_id": task["_id"]}, {"$set": {"status": "completed"}})'''

replacement1 = '''        if conditions:
            already_in_db = await movies_col.find_one({"$and": conditions})
            
        if already_in_db and not task.get("force", False):
            await queue_col.update_one({"_id": task["_id"]}, {"$set": {"status": "completed"}})'''

code = code.replace(target1, replacement1)

# 2. Add /host command
host_cmd = '''
@app.on_message(filters.chat(CONTROL_CHANNEL_ID) & filters.command("host", prefixes="/"))
async def host_command(client, message):
    import socket
    hostname = socket.gethostname()
    host_env = "Render" if "RENDER" in os.environ else "Back4App/Other"
    
    await message.reply_text(f"🌐 **Current Host Environment:** {host_env}\\n🖥️ **Server ID:** {hostname}\\n👤 **Active Telegram Account:** {ACTIVE_ACCOUNT}")
'''
code = code.replace('@app.on_message(filters.chat(CONTROL_CHANNEL_ID) & filters.command("force", prefixes="/"))', host_cmd + '\n@app.on_message(filters.chat(CONTROL_CHANNEL_ID) & filters.command("force", prefixes="/"))')

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.write(code)