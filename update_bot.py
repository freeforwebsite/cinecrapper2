import sys

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = 'TARGET_BOT = os.environ.get("TARGET_BOT", "@Moonknightxbot")'
replacement = 'TARGET_BOT = os.environ.get("TARGET_BOT", "@Movie_Provider_Infinity_Bot")'

content = content.replace(target, replacement)

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")