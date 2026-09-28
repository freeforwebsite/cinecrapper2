import sys

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    code = f.read()

target = '''    total_movies = len(ai_cleaned_movies)
    for i, movie in enumerate(ai_cleaned_movies, 1):
        if i % 100 == 0:
            try:
                await status_msg.edit_text(f"\U0001f50d **Scanning Database:** {i} / {total_movies} movies checked...")
            except Exception:
                pass
                
        # Check if already in queue
        existing_queue = await queue_col.find_one({"movie_name": movie})
        if existing_queue:
            skipped_count += 1
            continue
            
        # Check if already in main database using strict regex
        words = re.findall(r'[a-zA-Z0-9]+', movie)
        conditions = [{"file_name": {"": word, "": "i"}} for word in words]
        already_in_db = False
        if conditions:
            already_in_db = await movies_col.find_one({"": conditions})
            
        if already_in_db:
            skipped_count += 1
            # Mark it as completed directly in queue history so it doesn't get processed again
            await queue_col.insert_one({"movie_name": movie, "status": "completed"})
            continue
            
        # Add to pending queue!
        await queue_col.insert_one({"movie_name": movie, "status": "pending"})
        added_count += 1'''

new_loop = '''    total_movies = len(ai_cleaned_movies)
    
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
            await queue_col.insert_many(docs_to_insert[i:i+chunk_size])'''

code = code.replace(target, new_loop)

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.write(code)