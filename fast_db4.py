import sys

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1

for i, line in enumerate(lines):
    if "total_movies = len(ai_cleaned_movies)" in line and "queue_file_handler" in "".join(lines[max(0, i-50):i]):
        if start_idx == -1:
            start_idx = i
    if start_idx != -1 and i > start_idx:
        if "added_count += 1" in line:
            end_idx = i
            break

if start_idx != -1 and end_idx != -1:
    new_loop = '''        total_movies = len(ai_cleaned_movies)
        
        # --- FAST IN-MEMORY CHECK ---
        await status_msg.edit_text(f"⚡ **Fast Scanning Database...** Loading index...")
        db_cursor = movies_col.find({}, {"file_name": 1})
        db_files = [doc.get("file_name", "").lower() for doc in await db_cursor.to_list(length=None)]
        
        queue_cursor = queue_col.find({}, {"movie_name": 1})
        queue_items = {doc.get("movie_name", "").lower() for doc in await queue_cursor.to_list(length=None)}
        
        docs_to_insert = []
        for i, movie in enumerate(ai_cleaned_movies, 1):
            if i % 1000 == 0:
                try:
                    await status_msg.edit_text(f"⚡ **Fast Scanning:** {i} / {total_movies} checked...")
                except Exception:
                    pass
                    
            movie_lower = movie.lower()
            if movie_lower in queue_items:
                skipped_count += 1
                continue
                
            words = re.findall(r'[a-zA-Z0-9]+', movie_lower)
            already_in_db = False
            if words:
                for db_file in db_files:
                    if all(word in db_file for word in words):
                        already_in_db = True
                        break
            
            if already_in_db:
                skipped_count += 1
                docs_to_insert.append({"movie_name": movie, "status": "completed"})
                continue
                
            docs_to_insert.append({"movie_name": movie, "status": "pending"})
            added_count += 1
            
        if docs_to_insert:
            await status_msg.edit_text("💾 **Saving to Queue...**")
            chunk_size = 1000
            for i in range(0, len(docs_to_insert), chunk_size):
                await queue_col.insert_many(docs_to_insert[i:i+chunk_size])\n'''
    
    lines[start_idx:end_idx+1] = [new_loop]
    
    with open('cinescraper.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("Replaced!")
else:
    print("Not found")