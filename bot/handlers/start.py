from pyrogram import filters
from pyrogram.types import Message

def register(app):
    @app.on_message(filters.command("start") & filters.private)
    async def start_command(client, message: Message):
        await message.reply_text("👋 Welcome to Video Editor Bot! Use /help to see commands.")

    @app.on_message(filters.command("help") & filters.private)
    async def help_command(client, message: Message):
        await message.reply_text("Available Commands:\n/merge\n/trim\n/compress\n/rename\n/screenshot ...")
