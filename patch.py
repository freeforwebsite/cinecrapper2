import re

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    code = f.read()

def replace_logic(match):
    target = match.group(1)
    
    return f'''                        import urllib.parse
                        import time
                        import re
                        
                        bot_url = os.environ.get("SEARCH_BOT_URL", "https://t.me/Cinevault")
                        
                        found_qualities = set()
                        found_audios = set()
                        movie_year = ""
                        
                        async for m in app.get_chat_history({target}, limit=30):
                            if time.time() - m.date.timestamp() > 300:
                                continue
                            doc = m.document or m.video
                            if doc:
                                file_name = getattr(doc, 'file_name', '')
                                if file_name:
                                    fname_lower = file_name.lower()
                                    if "1080" in fname_lower: found_qualities.add("1080p")
                                    elif "720" in fname_lower: found_qualities.add("720p")
                                    elif "480" in fname_lower: found_qualities.add("480p")
                                    elif "2160" in fname_lower or "4k" in fname_lower: found_qualities.add("2160p")
                                    elif "webrip" in fname_lower: found_qualities.add("WEBRip")
                                    elif "bluray" in fname_lower or "bdrip" in fname_lower: found_qualities.add("BluRay")
                                    
                                    if "tamil" in fname_lower: found_audios.add("Tamil")
                                    if "telugu" in fname_lower: found_audios.add("Telugu")
                                    if "hindi" in fname_lower: found_audios.add("Hindi")
                                    if "malayalam" in fname_lower: found_audios.add("Malayalam")
                                    if "kannada" in fname_lower: found_audios.add("Kannada")
                                    if "english" in fname_lower: found_audios.add("English")
                                    if "multi" in fname_lower: found_audios.add("Multi")
                                    
                                    if not movie_year:
                                        ymatch = re.search(r'\\b(19\\d{{2}}|20\\d{{2}})\\b', file_name)
                                        if ymatch:
                                            movie_year = ymatch.group(1)

                        q_str = ", ".join(sorted(found_qualities)) if found_qualities else "Unknown"
                        a_str = ", ".join(sorted(found_audios)) if found_audios else "Unknown"
                        
                        display_movie = movie
                        if movie_year and str(movie_year) not in display_movie:
                            display_movie = f"{{movie}} {{movie_year}}"
                            
                        # Format as a hyperlink to make it blue in Telegram (markdown style)
                        title_str = f"[{{display_movie}}]({{bot_url}})"
                        
                        text = f"#New_File_Added \\u2705 #Cinevault\\n\\n#Movie\\n\\n\\U0001f3ac Title: **{{title_str}}**\\n\\n\\U0001f3a5 Quality: **{{q_str}}**\\n\\n\\U0001f50a Audio: **{{a_str}}**"
                        
                        reply_markup = InlineKeyboardMarkup([
                            [InlineKeyboardButton("\\u27a1\\ufe0f Get Files \\u2b05\\ufe0f", url=bot_url)]
                        ])
                        await app.send_message(int(update_channel), text, reply_markup=reply_markup, disable_web_page_preview=True)'''

pattern = r'                        import urllib\.parse\s+import time\s+bot_url = os\.environ\.get\("SEARCH_BOT_URL", "https://t\.me/Cinevault"\)\s+found_qualities = set\(\)\s+found_audios = set\(\)\s+async for m in app\.get_chat_history\((TARGET_BOT(?:_V2)?), limit=30\):.*?await app\.send_message\(int\(update_channel\), text, reply_markup=reply_markup\)'

new_code = re.sub(pattern, replace_logic, code, flags=re.DOTALL)

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.write(new_code)