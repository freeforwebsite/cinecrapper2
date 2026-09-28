import asyncio
from pyrogram import Client
from dotenv import load_dotenv
import os

load_dotenv()
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
session_string = os.environ.get("SESSION_STRING")

app = Client("temp_sender", api_id=api_id, api_hash=api_hash, session_string=session_string)

async def main():
    async with app:
        await app.send_document(
            chat_id=-1004371706867, # CONTROLLER ROOM
            document="clean_tags_list.txt",
            caption="Here is the clean tags list as requested! 📄"
        )
        print("Sent!")

asyncio.run(main())