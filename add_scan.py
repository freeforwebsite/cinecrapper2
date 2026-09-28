import sys

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    content = f.read()

injection = '''
@app.on_message(filters.chat(CONTROL_CHANNEL_ID) & filters.command("scan_tags", prefixes="/"))
async def scan_tags_command(client, message):
    msg = await message.reply_text("🔍 Scanning database for garbage @tags... This might take a minute.")
    try:
        from collections import Counter
        import re
        tags = Counter()
        async for doc in movies_col.find({}):
            fname = doc.get("file_name", "")
            if fname:
                words = re.findall(r'@[a-zA-Z0-9_]+', fname)
                for w in words:
                    tags[w] += 1
                    
        report = "Top @tags found in database:\\n\\n"
        for tag, count in tags.most_common(500):
            report += f"{tag} ({count} files)\\n"
            
        with open("tags_report.txt", "w", encoding="utf-8") as f:
            f.write(report)
            
        await message.reply_document("tags_report.txt", caption="✅ Scan complete! Here is the list of all tags.")
        await msg.delete()
    except Exception as e:
        await msg.edit_text(f"❌ Error: {e}")
'''

content = content.replace('app.start()', injection + '\\napp.start()')

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")