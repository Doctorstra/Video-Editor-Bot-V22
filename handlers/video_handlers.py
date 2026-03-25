"""
Video processing handlers
"""
from telegram import Update
from telegram.ext import ContextTypes
from utils.video_utils import VideoProcessor
from config import Config
from database import db
import os
import logging

logger = logging.getLogger(__name__)

# Store user states for multi-step operations
user_states = {}

async def compress_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /compress command"""
    await update.message.reply_text(
        "📹 **Video Compressor**\n\n"
        "Please send me the video you want to compress.\n"
        "Then choose compression mode:\n"
        "• HEVC (better compression, slower)\n"
        "• Fast (faster, good compression)"
    )
    user_states[update.effective_user.id] = {'action': 'compress'}

async def trim_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /trim command"""
    if len(context.args) < 2:
        await update.message.reply_text(
            "Usage: /trim <start_time> <duration>\n\n"
            "Example: /trim 00:00:10 00:00:30\n"
            "(Trim from 10 seconds, duration 30 seconds)\n\n"
            "Then send the video file."
        )
        return
    
    start_time = context.args[0]
    duration = context.args[1]
    
    user_states[update.effective_user.id] = {
        'action': 'trim',
        'start_time': start_time,
        'duration': duration
    }
    
    await update.message.reply_text(
        f"✂️ Ready to trim video!\n"
        f"Start: {start_time}\n"
        f"Duration: {duration}\n\n"
        f"Please send the video file."
    )

async def merge_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /merge command"""
    await update.message.reply_text(
        "🔗 **Video Merger**\n\n"
        "Send me 2 or more videos to merge.\n"
        "Send /done when you've sent all videos."
    )
    user_states[update.effective_user.id] = {
        'action': 'merge',
        'files': []
    }

async def rename_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /rename command"""
    if not context.args:
        await update.message.reply_text(
            "Usage: /rename <new_name>\n\n"
            "Example: /rename MyVideo.mp4\n\n"
            "Then send the video file."
        )
        return
    
    new_name = ' '.join(context.args)
    user_states[update.effective_user.id] = {
        'action': 'rename',
        'new_name': new_name
    }
    
    await update.message.reply_text(
        f"📝 Ready to rename to: {new_name}\n\n"
        f"Please send the video file."
    )

async def encode_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /encode command"""
    await update.message.reply_text(
        "🔄 **Video Encoder**\n\n"
        "Send me the video to encode.\n"
        "Supported formats: MP4, MKV, AVI, MOV"
    )
    user_states[update.effective_user.id] = {'action': 'encode'}

async def screenshot_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /screenshot command"""
    timestamp = context.args[0] if context.args else "00:00:01"
    
    await update.message.reply_text(
        f"📸 **Screenshot Generator**\n\n"
        f"Timestamp: {timestamp}\n\n"
        f"Send me the video file."
    )
    user_states[update.effective_user.id] = {
        'action': 'screenshot',
        'timestamp': timestamp
    }

async def metadata_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /metadata command"""
    await update.message.reply_text(
        "ℹ️ **Video Metadata Viewer**\n\n"
        "Send me a video to view its metadata."
    )
    user_states[update.effective_user.id] = {'action': 'metadata'}

async def extract_audio_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /extract_audio command"""
    await update.message.reply_text(
        "🎵 **Audio Extractor**\n\n"
        "Send me a video to extract its audio."
    )
    user_states[update.effective_user.id] = {'action': 'extract_audio'}

async def extract_subs_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /extract_subs command"""
    await update.message.reply_text(
        "📝 **Subtitle Extractor**\n\n"
        "Send me a video to extract subtitles."
    )
    user_states[update.effective_user.id] = {'action': 'extract_subs'}

async def add_watermark_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /add_watermark command"""
    await update.message.reply_text(
        "🏷️ **Watermark Adder**\n\n"
        "First, send me the watermark image.\n"
        "Then send the video."
    )
    user_states[update.effective_user.id] = {
        'action': 'add_watermark',
        'step': 'watermark'
    }

async def storage_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /storage command"""
    user_id = update.effective_user.id
    storage = await db.get_storage(user_id)
    storage_formatted = VideoProcessor.format_size(storage)
    
    max_storage = Config.MAX_FILE_SIZE * 1024 * 1024  # Convert MB to bytes
    max_formatted = VideoProcessor.format_size(max_storage)
    
    percentage = (storage / max_storage * 100) if max_storage > 0 else 0
    
    storage_text = f"""
💾 **Storage Information**

Used: {storage_formatted}
Limit: {max_formatted}
Usage: {percentage:.1f}%

{'⚠️ Storage almost full!' if percentage > 80 else '✅ Storage OK'}
"""
    
    await update.message.reply_text(storage_text, parse_mode='Markdown')

async def video_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming video files"""
    user_id = update.effective_user.id
    
    if user_id not in user_states:
        await update.message.reply_text(
            "Please use a command first!\n"
            "Example: /compress, /trim, /merge, etc."
        )
        return
    
    state = user_states[user_id]
    action = state.get('action')
    
    # Download the video
    video = update.message.video or update.message.document
    if not video:
        await update.message.reply_text("Please send a valid video file!")
        return
    
    status_msg = await update.message.reply_text("⏳ Processing your video...")
    
    try:
        # Download file
        file = await context.bot.get_file(video.file_id)
        input_path = os.path.join(Config.DOWNLOAD_PATH, f"{user_id}_{video.file_name or 'video.mp4'}")
        await file.download_to_drive(input_path)
        
        # Process based on action
        if action == 'compress':
            output_path = os.path.join(Config.UPLOAD_PATH, f"compressed_{video.file_name or 'video.mp4'}")
            success = await VideoProcessor.compress_video(input_path, output_path, 'fast')
            
            if success:
                with open(output_path, 'rb') as video_file:
                    await context.bot.send_video(
                        chat_id=update.effective_chat.id,
                        video=video_file,
                        caption="✅ Video compressed successfully!"
                    )
                os.remove(output_path)
            else:
                await status_msg.edit_text("❌ Failed to compress video!")
        
        elif action == 'trim':
            output_path = os.path.join(Config.UPLOAD_PATH, f"trimmed_{video.file_name or 'video.mp4'}")
            success = await VideoProcessor.trim_video(
                input_path, output_path,
                state['start_time'], state['duration']
            )
            
            if success:
                with open(output_path, 'rb') as video_file:
                    await context.bot.send_video(
                        chat_id=update.effective_chat.id,
                        video=video_file,
                        caption="✅ Video trimmed successfully!"
                    )
                os.remove(output_path)
            else:
                await status_msg.edit_text("❌ Failed to trim video!")
        
        elif action == 'screenshot':
            output_path = os.path.join(Config.UPLOAD_PATH, f"screenshot_{user_id}.jpg")
            success = await VideoProcessor.generate_screenshot(
                input_path, output_path,
                state.get('timestamp', '00:00:01')
            )
            
            if success:
                with open(output_path, 'rb') as photo_file:
                    await context.bot.send_photo(
                        chat_id=update.effective_chat.id,
                        photo=photo_file,
                        caption="✅ Screenshot generated!"
                    )
                os.remove(output_path)
            else:
                await status_msg.edit_text("❌ Failed to generate screenshot!")
        
        elif action == 'metadata':
            info = await VideoProcessor.get_video_info(input_path)
            
            if info and 'format' in info:
                fmt = info['format']
                metadata_text = f"""
ℹ️ **Video Metadata:**

📁 Filename: {fmt.get('filename', 'N/A')}
⏱️ Duration: {float(fmt.get('duration', 0)):.2f}s
📦 Size: {VideoProcessor.format_size(int(fmt.get('size', 0)))}
🎬 Format: {fmt.get('format_name', 'N/A')}
📊 Bitrate: {int(fmt.get('bit_rate', 0)) // 1000}kbps
"""
                await status_msg.edit_text(metadata_text, parse_mode='Markdown')
            else:
                await status_msg.edit_text("❌ Failed to get metadata!")
        
        elif action == 'extract_audio':
            output_path = os.path.join(Config.UPLOAD_PATH, f"audio_{user_id}.mp3")
            success = await VideoProcessor.extract_audio(input_path, output_path)
            
            if success:
                with open(output_path, 'rb') as audio_file:
                    await context.bot.send_audio(
                        chat_id=update.effective_chat.id,
                        audio=audio_file,
                        caption="✅ Audio extracted successfully!"
                    )
                os.remove(output_path)
            else:
                await status_msg.edit_text("❌ Failed to extract audio!")
        
        elif action == 'rename':
            new_name = state['new_name']
            output_path = os.path.join(Config.UPLOAD_PATH, new_name)
            
            # Simply copy with new name
            import shutil
            shutil.copy(input_path, output_path)
            
            with open(output_path, 'rb') as video_file:
                await context.bot.send_video(
                    chat_id=update.effective_chat.id,
                    video=video_file,
                    caption=f"✅ Renamed to: {new_name}"
                )
            os.remove(output_path)
        
        # Clean up
        if os.path.exists(input_path):
            os.remove(input_path)
        
        # Update storage
        file_size = video.file_size or 0
        await db.update_storage(user_id, file_size)
        
        # Clear state
        if action != 'merge':  # Don't clear for merge (multi-file)
            user_states.pop(user_id, None)
        
        if action not in ['metadata']:
            await status_msg.delete()
    
    except Exception as e:
        logger.error(f"Error processing video: {e}")
        await status_msg.edit_text(f"❌ Error: {str(e)}")
