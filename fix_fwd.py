import sys

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Remove the already_in_db block in forward_worker
# We want to keep the forward logic but without the if already_in_db check

new_content = re.sub(
    r'# Prevent duplicate forwards.*?if already_in_db:.*?else:\s+# 1\. Forward directly',
    '# 1. Forward directly',
    content,
    flags=re.DOTALL
)

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("done")