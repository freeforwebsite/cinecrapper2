import pymongo
import os
import re
from collections import Counter
from dotenv import load_dotenv

load_dotenv()
client = pymongo.MongoClient(os.environ.get('MONGO_URI'))
movies_col = client['telegram_bot']['movies']

tags = Counter()

ignore = {'the', 'a', 'an', 'of', 'and', 'in', 'hindi', 'tamil', 'telugu', 'malayalam', 'kannada', 'english', 'webrip', 'dvdrip', 'brrip', 'hdrip', 'bluray', '1080p', '720p', '480p', '360p', '2160p', '4k', 'x264', 'x265', 'hevc', '10bit', 'aac', 'ddp5', 'esub', 'msub', 'ss', 'web', 'dl', 'dual', 'audio', 'multi'}

for doc in movies_col.find({}):
    fname = doc.get("file_name", "")
    if fname:
        words = re.findall(r'[a-zA-Z0-9@_]+', fname)
        for w in words:
            wl = w.lower()
            if not wl.isnumeric() and len(wl) > 3 and wl not in ignore:
                tags[w] += 1

print("Top 30 suspicious tags in your database:")
for tag, count in tags.most_common(30):
    print(f"- {tag} ({count} files)")