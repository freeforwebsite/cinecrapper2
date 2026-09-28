import re

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    code = f.read()

pattern = r'(await status_msg\.edit_text\(f"✅ \*\*AI Analysis Complete!\*\*\\nNow high-speed cross-referencing \{len\(ai_cleaned_movies\)\} movies against your database\.\.\."\)\s+added_count = 0\s+skipped_count = 0\s+docs_to_insert = \[\]\s+total_movies = len\(ai_cleaned_movies\)\s+for i, movie in enumerate\(ai_cleaned_movies, 1\):\s+if i % 100 == 0:\s+try:\s+await status_msg\.edit_text\(f"🔍 \*\*Scanning Database:\*\* \{i\} / \{total_movies\} movies checked\.\.\."\)\s+except Exception:\s+pass\s+# Check queue\s+existing_queue = await queue_col\.find_one\(\{"movie_name": movie\}\)\s+if existing_queue:\s+skipped_count \+= 1\s+continue\s+# Check DB\s+words = re\.findall\(r\'\[a-zA-Z0-9\]\+\', movie\)\s+conditions = \[\{"file_name": \{"\": word, "\": "i"\}\} for word in words\]\s+already_in_db = False\s+if conditions:\s+already_in_db = await movies_col\.find_one\(\{"\": conditions\}\)\s+if already_in_db:\s+skipped_count \+= 1\s+docs_to_insert\.append\(\{"movie_name": movie, "status": "completed"\}\)\s+continue\s+docs_to_insert\.append\(\{"movie_name": movie, "status": "pending"\}\)\s+added_count \+= 1\s+if docs_to_insert:\s+await queue_col\.insert_many\(docs_to_insert\))'

replacement = '''await status_msg.edit_text(f"✅ **AI Analysis Complete!**\\nNow high-speed cross-referencing {len(ai_cleaned_movies)} movies against your database...")
        
        # Load all DB files into memory for fast check
        db_files_cursor = movies_col.find({}, {"file_name": 1})
        db_files = [doc.get("file_name", "").lower() for doc in await db_files_cursor.to_list(length=None)]
        
        # Load all queue items into memory for fast check
        queue_cursor = queue_col.find({}, {"movie_name": 1})
        queue_movies = {doc.get("movie_name", "").lower() for doc in await queue_cursor.to_list(length=None)}
        
        added_count = 0
        skipped_count = 0
        docs_to_insert = []
        
        total_movies = len(ai_cleaned_movies)
        for i, movie in enumerate(ai_cleaned_movies, 1):
            if i % 100 == 0:
                try:
                    await status_msg.edit_text(f"🔍 **Scanning Database:** {i} / {total_movies} movies checked...")
                except Exception:
                    pass
            
            movie_lower = movie.lower()
            if movie_lower in queue_movies:
                skipped_count += 1
                continue
                
            words = [w for w in re.findall(r'[a-zA-Z0-9]+', movie_lower)]
            
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
            await queue_col.insert_many(docs_to_insert)'''

new_code = re.sub(pattern, replacement, code, flags=re.DOTALL)

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.write(new_code)