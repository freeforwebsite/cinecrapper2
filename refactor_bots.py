import re

with open('cinescraper.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Refactor process_movie to take target_bot
content = content.replace("async def process_movie(client, movie):", "async def process_movie(client, movie, target_bot):")
# Now replace TARGET_BOT with target_bot inside process_movie
# I need to be careful not to replace TARGET_BOT globally, just inside process_movie and queue_worker where needed.

# Actually, an easier way is to just define a list of bots!
target_bots = '["@Moonknightxbot", "@Movie_Provider_Infinity_Bot"]'

# Let's write a targeted replacement
# First, change process_movie signature
import ast
# Using regex to replace TARGET_BOT with target_bot inside process_movie function block
# It's easier to just use string replace but limit it to the function body.

def replace_in_func(content, func_name, old, new):
    start_idx = content.find(f"async def {func_name}(")
    if start_idx == -1: return content
    end_idx = content.find("async def ", start_idx + 10)
    if end_idx == -1: end_idx = len(content)
    
    func_body = content[start_idx:end_idx]
    func_body = func_body.replace(old, new)
    return content[:start_idx] + func_body + content[end_idx:]

content = replace_in_func(content, "process_movie", "async def process_movie(client, movie):", "async def process_movie(client, movie, target_bot):")
content = replace_in_func(content, "process_movie", "TARGET_BOT", "target_bot")

# Now update queue_worker
queue_worker_old = '''            movie = task["movie_name"]
            success = await process_movie(app, movie)'''
            
queue_worker_new = '''            movie = task["movie_name"]
            
            target_bots = ["@Moonknightxbot", "@Movie_Provider_Infinity_Bot"]
            tasks = [process_movie(app, movie, bot) for bot in target_bots]
            results = await asyncio.gather(*tasks)
            success = any(results)'''

content = content.replace(queue_worker_old, queue_worker_new)

# Now update the metadata scan in queue_worker
meta_old = '''                        async for m in app.get_chat_history(TARGET_BOT, limit=30):'''
meta_new = '''                        for bot in target_bots:
                            async for m in app.get_chat_history(bot, limit=30):'''
                            
content = content.replace(meta_old, meta_new)

with open('cinescraper.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done")