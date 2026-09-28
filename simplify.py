import sys
import re

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    content = f.read()

unified_handler = '''@app.on_message(filters.chat(CONTROL_CHANNEL_ID) & (filters.document | filters.command(["queue", "forcequeue"], prefixes="/")))
async def unified_file_handler(client, message):
    \"\"\"Unified handler for PDF/TXT uploads. ALWAYS queues everything with force: True.\"\"\"
    doc_message = message
    
    if message.text:
        if not message.reply_to_message or not getattr(message.reply_to_message, 'document', None):
            await message.reply_text("⚠️ Please reply to a PDF or TXT file!")
            return
        doc_message = message.reply_to_message
            
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
        
        await status_msg.edit_text(f"⚡ **POWER MODE ACTIVE!**\\nInjecting {total} movies into queue without scanning database...")
        
        chunk_size = 1000
        inserted = 0
        for i in range(0, total, chunk_size):
            chunk = movies[i:i+chunk_size]
            docs = [{"movie_name": m, "status": "pending", "force": True} for m in chunk]
            await queue_col.insert_many(docs)
            inserted += len(chunk)
        
        await status_msg.edit_text(f"✅ **Queue Complete!**\\n🚀 {inserted} movies queued instantly.\\nThey will be scraped even if they exist in the database.")

    except Exception as e:
        await status_msg.edit_text(f"❌ Error: {e}")'''

# Use replace instead of regex for simplicity
start_idx = content.find('@app.on_message(filters.chat(CONTROL_CHANNEL_ID) & (filters.document | filters.command(["queue", "forcequeue"], prefixes="/")))')
end_idx = content.find('@app.on_message(filters.chat(CONTROL_CHANNEL_ID) & filters.command("status", prefixes="/"))')

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + unified_handler + '\\n\\n' + content[end_idx:]
    with open('cinescraper.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Replaced!")
else:
    print("Could not find boundaries")