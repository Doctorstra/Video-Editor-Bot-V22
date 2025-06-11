from pyrogram import filters
from pyrogram.types import Message
from ..utils.ffmpeg_utils import merge_videos

videos_to_merge = {}

def register(app):
    @app.on_message(filters.command("merge") & filters.private)
    async def merge_command(client, message: Message):
        user_id = message.from_user.id
        videos_to_merge[user_id] = []
        await message.reply_text("Send me the video files you want to merge. Type /done when finished.")

    @app.on_message(filters.video & filters.private)
    async def collect_videos(client, message: Message):
        user_id = message.from_user.id
        if user_id in videos_to_merge:
            file = await message.download()
            videos_to_merge[user_id].append(file)
            await message.reply_text("✅ Video added. Send more or type /done.")

    @app.on_message(filters.command("done") & filters.private)
    async def done_merging(client, message: Message):
        user_id = message.from_user.id
        if user_id not in videos_to_merge or not videos_to_merge[user_id]:
            return await message.reply("No videos to merge.")
        await message.reply("⚙️ Merging videos...")
        output_path = f"merged_{user_id}.mp4"
        merge_videos(videos_to_merge[user_id], output_path)
        await message.reply_video(output_path, caption="✅ Merged Video")
        videos_to_merge.pop(user_id)
