import re

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Fix the global task.get bug
code = code.replace('if already_in_db and not task.get("force", False):', 'if already_in_db:')
# Restore it ONLY in queue_worker where task is defined!
pattern = r'(already_in_db = await movies_col\.find_one\(\{"\": conditions\}\)\s+if already_in_db):\s+(await queue_col\.update_one\(\{"_id": task\["_id"\]\}\, \{"\": \{"status": "completed"\}\}\)\s+continue)'
code = re.sub(pattern, r'\1 and not task.get("force", False):\n                \2', code)

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.write(code)