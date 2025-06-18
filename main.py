# bot/main.py
import logging
from pyrogram import Client, filters
from .config import API_ID, API_HASH, 7293809673:AAFGuFiQH85yGkckT5yql3Nx39iLinJScKg
from .handlers import (
    start, merge, trim, compress, rename, screenshot,
    watermark, encode, subtitle, audio, archive,
    extract_archive, download_link, url_uploader, metadata
)

logging.basicConfig(level=logging.INFO)

app = Client("video_editor_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Register handlers
start.register(app)
merge.register(app)
trim.register(app)
compress.register(app)
rename.register(app)
screenshot.register(app)
watermark.register(app)
encode.register(app)
subtitle.register(app)
audio.register(app)
archive.register(app)
extract_archive.register(app)
download_link.register(app)
url_uploader.register(app)
metadata.register(app)

if __name__ == "__main__":
    print("📡 Bot is up!")
    app.run()
