import re

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    code = f.read()

pattern = r'(already_in_db = await movies_col\.find_one\(\{"\": conditions\}\)\s+if already_in_db):\s+(await queue_col\.update_one\(\{"_id": task\["_id"\]\}\, \{"\": \{"status": "completed"\}\}\))'
code = re.sub(pattern, r'\1 and not task.get("force", False):\n                \2', code)

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.write(code)