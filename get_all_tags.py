import pymongo
import re
from collections import Counter

client = pymongo.MongoClient('mongodb+srv://dharani2006lakshmi_db_user:Byi5WDiKV6H53Xe1@cluster0.p93dbly.mongodb.net')
movies_col = client['telegram_bot']['movies']

tags = Counter()

for doc in movies_col.find({}):
    fname = doc.get("file_name", "")
    if fname:
        words = re.findall(r'@[a-zA-Z0-9_]+', fname)
        for w in words:
            tags[w] += 1

report = "Here are all the @tags found in your database:\\n\\n"
report += "| Tag | Number of Files |\\n"
report += "|---|---|\\n"
for tag, count in tags.most_common():
    report += f"| {tag} | {count} |\\n"

with open('all_tags.md', 'w', encoding='utf-8') as f:
    f.write(report)