import sys

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    code = f.read()

debug_cmd = '''
@app.on_message(filters.command("ping", prefixes="/"))
async def ping_command(client, message):
    await message.reply_text("🏓 **PONG!** The bot is alive and receiving messages!\\nYour Chat ID is: " + str(message.chat.id) + "")
'''
if "ping_command" not in code:
    code = code.replace('async def host_command', debug_cmd + '\nasync def host_command')

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.write(code)