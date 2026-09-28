import sys
import re

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(
    r"print\(f\".*?Message auto-deleted after 5 mins! Restarting search to continue from page \{current_page\}\.\.\.\"\)\s*break # Break inner loop, restart outer search loop",
    "print(f\"⏱️ Message auto-deleted by Moon Bot after 5 mins! Stopping gracefully.\")\n            finished_all_pages = True\n            break",
    content
)

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")