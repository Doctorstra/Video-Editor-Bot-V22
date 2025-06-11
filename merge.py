# bot/handlers/merge.py
from pyrogram import filters
from pyrogram.types import Message
from ..utils.ffmpeg_utils import merge_videos

def register(app):

    @app.on_message(filters.command("merge") & filters.private)
    async def merge_handler(client, message: Message):
        await message.reply_text("Send videos to merge (as multiple messages). Then type /done")
        client.set_parse_mode(None)
        client.state = {"mode": "merge", "videos": []}

    @app.on_message(filters.document & filters.private)
    async def file_collector(client, message: Message):
        if getattr(client, "state", {}).get("mode") == "merge":
            file_path = await message.download()
            client.state["videos"].append(file_path)
            await message.reply_text("✅ Got it. Send more, or type /done")

    @app.on_message(filters.command("done") & filters.private)
    async def done_merge(client, message: Message):
        state = getattr(client, "state", {})
        videos = state.get("videos", [])
        if not videos:
            return await message.reply("No videos received.")
        output = "merged.mp4"
        await message.reply("Merging videos...")
        merge_videos(videos, output)
        await message.reply_video(output)
