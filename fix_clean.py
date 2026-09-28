import sys
import re

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('await status_msg.edit_text(f"dY"o **Bulk Clean Complete!**\\\\n\\\\ndY-,? Removed @ tags from **{updated_count}** messages.\\\\no. Cleaned **{db_updated}** records in Database.")', 'await status_msg.edit_text(f"✅ **Bulk Clean Complete!**\\n\\n🧹 Removed tags from **{updated_count}** messages.\\n💾 Cleaned **{db_updated}** records in Database.")')

# Also wait, I might have messed up the string literal. Let's use regex to fix it.
content = re.sub(r'await status_msg\.edit_text\(f"dY"o.*', 'await status_msg.edit_text(f"✅ **Bulk Clean Complete!**\\\\n\\\\n🧹 Removed tags from **{updated_count}** messages.\\\\n💾 Cleaned **{db_updated}** records in Database.")', content)

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed syntax")