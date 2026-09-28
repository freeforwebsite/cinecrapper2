import re

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    code = f.read()

log_setup = '''
import logging
from logging.handlers import RotatingFileHandler

# Set up logging to a file
logger = logging.getLogger("cinescraper")
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler("scraper.log", maxBytes=1024*1024, backupCount=1)
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Overwrite built-in print to also log to file
import builtins
_original_print = builtins.print
def custom_print(*args, **kwargs):
    _original_print(*args, **kwargs)
    message = " ".join(str(a) for a in args)
    logger.info(message)
builtins.print = custom_print

@app.on_message(filters.chat(CONTROL_CHANNEL_ID) & filters.command("logs", prefixes="/"))
async def logs_command(client, message):
    try:
        with open("scraper.log", "r", encoding="utf-8") as f:
            lines = f.readlines()
        last_lines = "".join(lines[-30:])
        if not last_lines:
            last_lines = "No logs yet."
        await message.reply_text(f"""📝 **Recent Logs:**\n\n`\n{last_lines}\n`""")
    except Exception as e:
        await message.reply_text(f"Error reading logs: {e}")
'''

# Find a good place to inject this, right after app = Client(...) block
pattern = r'(app = Client\(\s*"cinescraper",\s*api_id=API_ID,\s*api_hash=API_HASH,\s*session_string=SESSION_STRING\s*\))'
new_code = re.sub(pattern, r'\1\n' + log_setup, code)

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.write(new_code)