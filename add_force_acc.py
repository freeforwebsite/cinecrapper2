import sys
import re

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = '''    if account_doc:
        ACTIVE_ACCOUNT = account_doc.get("account", "1")
    else:
        ACTIVE_ACCOUNT = "1"'''
        
replacement = '''    if os.environ.get("FORCE_ACCOUNT"):
        ACTIVE_ACCOUNT = os.environ.get("FORCE_ACCOUNT")
        print(f"⚠️ [DUAL-ACCOUNT ENGINE] FORCE_ACCOUNT is set! Forcing Account {ACTIVE_ACCOUNT}!")
    elif account_doc:
        ACTIVE_ACCOUNT = account_doc.get("account", "1")
    else:
        ACTIVE_ACCOUNT = "1"'''

content = content.replace(target, replacement)

# Also disable rotation_worker if FORCE_ACCOUNT is used!
rot_target = '''app.loop.create_task(rotation_worker())'''
rot_replace = '''if not os.environ.get("FORCE_ACCOUNT"):
    app.loop.create_task(rotation_worker())
else:
    print("⚠️ [DUAL-ACCOUNT ENGINE] Rotation disabled because FORCE_ACCOUNT is active.")'''

content = content.replace(rot_target, rot_replace)

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")