import asyncio
asyncio.set_event_loop(asyncio.new_event_loop())

from pyrogram import Client
from dotenv import load_dotenv
import os

load_dotenv()
api_id = int(os.environ.get("API_ID", 36869346))
api_hash = os.environ.get("API_HASH", "9abc474ef05c5e46b2210b02eb4c81fc")
session_string = os.environ.get("SESSION_STRING", "BQIylOIARk_Pe9Ht1f0Fi6IdiugjQpgOnm7HOgdQc9nT3CKD96C99R_WUgHfaqa-EYzlI9X_ohBQaGTnpSjoAsdzDkiM0bC4tNs0CsDYNVCnYY1UbiU6zXKsuV0QjhavAsm5-1NOL4ik42GjEenAU0zDDeeYGWEBPN-aPkhAOtSdzs-dufE_Y2dsho0qdH1n5IvAsEWaqqW8v4YDv88kiYtIevn4d2YLENmgtXKow631sx3oEXsJMl_DyvfxQkz7PKWDxOvJPSk-chU41EmdfPZL54GZvbCiEcfow-9MLk-Xrq1Klrcn8dJfCxpBIT2hUaWRTdndw5Ba-2Ner0-lWqbT61jMRAAAAABS84xMAA")

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