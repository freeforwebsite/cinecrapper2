import sys
import re

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    content = f.read()

unified_handler = '''@app.on_message(filters.chat(CONTROL_CHANNEL_ID) & (filters.document | filters.command(["queue", "forcequeue"], prefixes="/")))
async def unified_file_handler(client, message):
    \"\"\"Unified handler for PDF/TXT uploads. Normal queue or force queue.\"\"\"
    is_force = False
    doc_message = message
    
    if message.text:
        text = message.text.lower()
        if not message.reply_to_message or not getattr(message.reply_to_message, 'document', None):
            await message.reply_text("⚠️ Please reply to a PDF or TXT file!")
            return
        doc_message = message.reply_to_message
        if text.startswith("/forcequeue"):
            is_force = True
    else:
        caption = (message.caption or "").strip().lower()
        if caption.startswith("/forcequeue"):
            is_force = True
            
    file_name = doc_message.document.file_name.lower()
    if not (file_name.endswith(".txt") or file_name.endswith(".pdf")):
        return
        
    status_msg = await message.reply_text("⚡ **Processing File...** Downloading...")
    file_path = await doc_message.download()
    
    try:
        import re
        movies = []
        if file_name.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            movies = [re.sub(r'^\\d+\\.\\s*', '', m.strip()) for m in lines if m.strip()]
        elif file_name.endswith(".pdf"):
            import pypdf
            await status_msg.edit_text("⚡ Parsing PDF file...")
            with open(file_path, "rb") as fh:
                reader = pypdf.PdfReader(fh)
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        lines = text.split("\\n")
                        page_movies = [re.sub(r'^\\d+\\.\\s*', '', m.strip()) for m in lines if m.strip()]
                        movies.extend(page_movies)
        
        import os
        os.remove(file_path)
        
        movies = list(dict.fromkeys(movies))
        movies = [m for m in movies if len(m) > 2]
        
        if not movies:
            await status_msg.edit_text("❌ No movies found in the file.")
            return

        total = len(movies)
        
        if is_force:
            await status_msg.edit_text(f"⚡ **FORCE QUEUE ACTIVE!**\\nInjecting {total} movies with pure speed...")
            chunk_size = 1000
            inserted = 0
            for i in range(0, total, chunk_size):
                chunk = movies[i:i+chunk_size]
                docs = [{"movie_name": m, "status": "pending", "force": True} for m in chunk]
                await queue_col.insert_many(docs)
                inserted += len(chunk)
            
            await status_msg.edit_text(f"✅ **Force Queue Complete!**\\n🚀 {inserted} movies queued!")
            return
            
        else:
            await status_msg.edit_text(f"🔍 **Normal Queue Active!**\\nFast-scanning {total} movies...")
            db_cursor = movies_col.find({}, {"file_name": 1})
            db_files = [doc.get("file_name", "").lower() for doc in await db_cursor.to_list(length=None)]
            
            queue_cursor = queue_col.find({}, {"movie_name": 1})
            queue_items = {doc.get("movie_name", "").lower() for doc in await queue_cursor.to_list(length=None)}
            
            added_count = 0
            skipped_count = 0
            docs_to_insert = []
            
            for i, movie in enumerate(movies, 1):
                if i % 1000 == 0:
                    try:
                        await status_msg.edit_text(f"⚡ **Fast Scanning:** {i} / {total} checked...")
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
                    continue
                    
                docs_to_insert.append({"movie_name": movie, "status": "pending"})
                added_count += 1
                
            if docs_to_insert:
                await queue_col.insert_many(docs_to_insert)
                
            await status_msg.edit_text(f"✅ **Queue Complete!**\\nAdded: {added_count}\\nSkipped: {skipped_count}")

    except Exception as e:
        await status_msg.edit_text(f"❌ Error: {e}")'''

# Remove old forcequeue_file_handler
content = re.sub(r'@app\.on_message\(filters\.chat\(CONTROL_CHANNEL_ID\) & \(filters\.document \| filters\.command\("forcequeue", prefixes="/"\)\)\)\nasync def forcequeue_file_handler\(client, message\):.*?(?=@app\.on_message)', unified_handler + '\\n\\n', content, flags=re.DOTALL)

# Remove old queue_file_handler
content = re.sub(r'@app\.on_message\(filters\.chat\(CONTROL_CHANNEL_ID\) & filters\.document\(\)\)\nasync def queue_file_handler\(client, message\):.*?(?=@app\.on_message)', '', content, flags=re.DOTALL)

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Rewrite complete!")