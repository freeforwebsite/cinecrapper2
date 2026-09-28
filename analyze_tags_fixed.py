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

print("Top 30 @tags in your database:")
for tag, count in tags.most_common(30):
    print(f"- {tag} ({count} files)")