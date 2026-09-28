import pymongo
import os
import re
from collections import Counter
from dotenv import load_dotenv

load_dotenv()
client = pymongo.MongoClient(os.environ.get('MONGO_URI'))
movies_col = client['telegram_bot']['movies']

tags = Counter()
empty_files = 0

for doc in movies_col.find({}):
    fname = doc.get("file_name", "")
    if fname:
        words = re.findall(r'@[a-zA-Z0-9_]+', fname)
        for w in words:
            tags[w] += 1
        if fname.strip() == ".mkv" or fname.strip() == ".mp4":
            empty_files += 1

with open("tags_report.txt", "w", encoding="utf-8") as f:
    f.write(f"Empty files (just .mkv): {empty_files}\n\n")
    f.write("Top 100 @tags found in database:\n")
    for tag, count in tags.most_common(100):
        f.write(f"{tag} ({count} files)\n")