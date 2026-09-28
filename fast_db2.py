import re

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    code = f.read()

pattern = r'(\s+)total_movies = len\(ai_cleaned_movies\)\s+for i, movie in enumerate\(ai_cleaned_movies, 1\):.*?added_count \+= 1'

new_loop = '''\g<1>total_movies = len(ai_cleaned_movies)
\g<1>
\g<1># --- FAST IN-MEMORY CHECK ---
\g<1>await status_msg.edit_text(f"⚡ **Fast Scanning Database...** Loading index...")
\g<1>db_cursor = movies_col.find({}, {"file_name": 1})
\g<1>db_files = [doc.get("file_name", "").lower() for doc in await db_cursor.to_list(length=None)]
\g<1>
\g<1>queue_cursor = queue_col.find({}, {"movie_name": 1})
\g<1>queue_items = {doc.get("movie_name", "").lower() for doc in await queue_cursor.to_list(length=None)}
\g<1>
\g<1>docs_to_insert = []
\g<1>for i, movie in enumerate(ai_cleaned_movies, 1):
\g<1>    if i % 1000 == 0:
\g<1>        try:
\g<1>            await status_msg.edit_text(f"⚡ **Fast Scanning:** {i} / {total_movies} checked...")
\g<1>        except Exception:
\g<1>            pass
\g<1>            
\g<1>    movie_lower = movie.lower()
\g<1>    if movie_lower in queue_items:
\g<1>        skipped_count += 1
\g<1>        continue
\g<1>        
\g<1>    words = re.findall(r'[a-zA-Z0-9]+', movie_lower)
\g<1>    already_in_db = False
\g<1>    if words:
\g<1>        for db_file in db_files:
\g<1>            if all(word in db_file for word in words):
\g<1>                already_in_db = True
\g<1>                break
\g<1>    
\g<1>    if already_in_db:
\g<1>        skipped_count += 1
\g<1>        docs_to_insert.append({"movie_name": movie, "status": "completed"})
\g<1>        continue
\g<1>        
\g<1>    docs_to_insert.append({"movie_name": movie, "status": "pending"})
\g<1>    added_count += 1
\g<1>    
\g<1>if docs_to_insert:
\g<1>    await status_msg.edit_text("💾 **Saving to Queue...**")
\g<1>    chunk_size = 1000
\g<1>    for i in range(0, len(docs_to_insert), chunk_size):
\g<1>        await queue_col.insert_many(docs_to_insert[i:i+chunk_size])'''

code = re.sub(pattern, new_loop, code, flags=re.DOTALL, count=1)

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.write(code)