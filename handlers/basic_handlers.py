"""
Basic command handlers for the bot
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import db
from config import Config
import logging

logger = logging.getLogger(__name__)

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    await db.add_user(user.id, user.username, user.first_name)
    
    welcome_text = f"""
🎬 **Welcome to All-in-One Video Editor Bot!**

Hello {user.first_name}! 👋

I'm your complete video toolkit on Telegram. I can help you with:

🎞️ **Video Operations**
• Merge multiple videos
• Trim videos to perfect length
• Compress videos (HEVC/Fast)
• Rename video files
• Encode to different formats

🎨 **Advanced Editing**
• Generate screenshots
• Add watermarks
• Extract/Add subtitles
• Extract/Add audio
• Set permanent thumbnails

📦 **File Management**
• Create archives (zip, tar, rar)
• Extract archives
• View metadata
• Track storage usage

🌐 **Download/Upload**
• URL uploader (streaming platforms)
• Direct link generator

**Get Started:**
Use /help to see all available commands!
"""
    
    keyboard = [
        [InlineKeyboardButton("📖 Help", callback_data="help"),
         InlineKeyboardButton("ℹ️ About", callback_data="about")],
        [InlineKeyboardButton("📊 My Stats", callback_data="stats")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = """
📚 **Available Commands:**

**Video Operations:**
/merge - Merge multiple videos
/trim - Trim video (start_time end_time)
/compress - Compress video (hevc/fast)
/rename - Rename video file
/encode - Encode video to different format

**Media Extraction:**
/screenshot - Generate screenshot from video
/extract_audio - Extract audio from video
/extract_subs - Extract subtitles from video
/add_audio - Add audio to video
/add_subs - Add subtitles to video

**Watermark & Thumbnail:**
/add_watermark - Add watermark to video
/set_thumbnail - Set permanent thumbnail
/show_thumbnail - Show your thumbnail
/delete_thumbnail - Delete your thumbnail

**Archives:**
/archive - Create archive (zip/tar/rar)
/extract - Extract archive

**Info & Settings:**
/metadata - View video metadata
/storage - Check storage usage
/stats - View your statistics

**Download/Upload:**
/download - Download from URL
/generate_link - Generate direct download link

**Admin Only:**
/broadcast - Send message to all users
/stats_all - View bot statistics

Use these commands with video files!
"""
    
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def stats_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats command"""
    user_id = update.effective_user.id
    storage = await db.get_storage(user_id)
    
    from utils.video_utils import VideoProcessor
    storage_formatted = VideoProcessor.format_size(storage)
    
    stats_text = f"""
📊 **Your Statistics:**

💾 Storage Used: {storage_formatted}
👤 User ID: `{user_id}`

Use /storage for detailed storage information.
"""
    
    await update.message.reply_text(stats_text, parse_mode='Markdown')

async def about_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /about command"""
    about_text = """
🎬 **All-in-One Video Editor Bot**

Version: 1.0.0
Powered by FFmpeg & Python

**Features:**
✅ 15+ Video Processing Tools
✅ MongoDB Integration
✅ Broadcast Support
✅ Permanent Thumbnail Support
✅ Storage Tracking
✅ Multiple Format Support

**Developer:**
Made with ❤️ for Telegram users

**Support:**
For issues or suggestions, contact the admin.

*Transform videos like a pro!* 🎥✨
"""
    
    await update.message.reply_text(about_text, parse_mode='Markdown')

async def broadcast_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /broadcast command (admin only)"""
    user_id = update.effective_user.id
    
    if user_id not in Config.ADMIN_IDS:
        await update.message.reply_text("⛔ This command is only for admins.")
        return
    
    if not context.args:
        await update.message.reply_text(
            "Usage: /broadcast <message>\n\n"
            "The message will be sent to all users."
        )
        return
    
    message = ' '.join(context.args)
    users = await db.get_all_users()
    
    success = 0
    failed = 0
    
    status_msg = await update.message.reply_text("📢 Broadcasting message...")
    
    for user in users:
        try:
            await context.bot.send_message(
                chat_id=user['user_id'],
                text=message,
                parse_mode='Markdown'
            )
            success += 1
        except Exception as e:
            failed += 1
            logger.error(f"Failed to send to {user['user_id']}: {e}")
    
    await status_msg.edit_text(
        f"✅ Broadcast Complete!\n\n"
        f"Success: {success}\n"
        f"Failed: {failed}"
    )

async def stats_all_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats_all command (admin only)"""
    user_id = update.effective_user.id
    
    if user_id not in Config.ADMIN_IDS:
        await update.message.reply_text("⛔ This command is only for admins.")
        return
    
    total_users = await db.get_users_count()
    
    stats_text = f"""
📊 **Bot Statistics:**

👥 Total Users: {total_users}

Database: MongoDB
Status: ✅ Active
"""
    
    await update.message.reply_text(stats_text, parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline button callbacks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "help":
        await help_handler(update, context)
    elif query.data == "about":
        await about_handler(update, context)
    elif query.data == "stats":
        await stats_handler(update, context)
