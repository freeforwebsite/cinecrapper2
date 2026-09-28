import sys

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    code = f.read()

target = '''        if conditions:
            already_in_db = await movies_col.find_one({"$and": conditions})
            
        if already_in_db:
            await queue_col.update_one({"_id": task["_id"]}, {"$set": {"status": "completed"}})'''

replacement = '''        if conditions:
            already_in_db = await movies_col.find_one({"$and": conditions})
            
        if already_in_db and not task.get("force", False):
            await queue_col.update_one({"_id": task["_id"]}, {"$set": {"status": "completed"}})'''

code = code.replace(target, replacement)

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.write(code)