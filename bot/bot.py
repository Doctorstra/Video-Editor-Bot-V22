from pyrogram import Client
from configs import API_ID, API_HASH, BOT_TOKEN

from bot.handlers import start, merge

app = Client("video_editor_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Register handlers
start.register(app)
merge.register(app)

if __name__ == "__main__":
    print("🤖 Bot started...")
    app.run()
