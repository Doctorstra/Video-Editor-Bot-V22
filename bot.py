"""
Main bot application
"""
import logging
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, CallbackQueryHandler
)
from config import Config
from database import db
from handlers import (
    start_handler, help_handler, stats_handler, about_handler,
    broadcast_handler, stats_all_handler, button_handler,
    compress_handler, trim_handler, merge_handler, rename_handler,
    encode_handler, screenshot_handler, metadata_handler,
    extract_audio_handler, extract_subs_handler, add_watermark_handler,
    storage_handler, video_handler,
    set_thumbnail_handler, show_thumbnail_handler, delete_thumbnail_handler,
    photo_handler,
    archive_handler, extract_handler, download_handler,
    generate_link_handler, document_handler, done_handler
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('logs/bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

async def error_handler(update, context):
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}")
    
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "❌ An error occurred while processing your request.\n"
            "Please try again later."
        )

async def post_init(application: Application):
    """Initialize bot after startup"""
    await db.connect()
    logger.info("Bot started successfully!")

async def post_shutdown(application: Application):
    """Cleanup after shutdown"""
    await db.close()
    logger.info("Bot shut down successfully!")

def main():
    """Main function to start the bot"""
    if not Config.BOT_TOKEN:
        logger.error("BOT_TOKEN not found! Please set it in .env file")
        return
    
    # Create application
    application = Application.builder().token(Config.BOT_TOKEN).build()
    
    # Add handlers
    # Basic commands
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("help", help_handler))
    application.add_handler(CommandHandler("stats", stats_handler))
    application.add_handler(CommandHandler("about", about_handler))
    application.add_handler(CommandHandler("broadcast", broadcast_handler))
    application.add_handler(CommandHandler("stats_all", stats_all_handler))
    
    # Video processing commands
    application.add_handler(CommandHandler("compress", compress_handler))
    application.add_handler(CommandHandler("trim", trim_handler))
    application.add_handler(CommandHandler("merge", merge_handler))
    application.add_handler(CommandHandler("rename", rename_handler))
    application.add_handler(CommandHandler("encode", encode_handler))
    application.add_handler(CommandHandler("screenshot", screenshot_handler))
    application.add_handler(CommandHandler("metadata", metadata_handler))
    application.add_handler(CommandHandler("extract_audio", extract_audio_handler))
    application.add_handler(CommandHandler("extract_subs", extract_subs_handler))
    application.add_handler(CommandHandler("add_watermark", add_watermark_handler))
    application.add_handler(CommandHandler("storage", storage_handler))
    
    # Thumbnail commands
    application.add_handler(CommandHandler("set_thumbnail", set_thumbnail_handler))
    application.add_handler(CommandHandler("show_thumbnail", show_thumbnail_handler))
    application.add_handler(CommandHandler("delete_thumbnail", delete_thumbnail_handler))
    
    # Archive and download commands
    application.add_handler(CommandHandler("archive", archive_handler))
    application.add_handler(CommandHandler("extract", extract_handler))
    application.add_handler(CommandHandler("download", download_handler))
    application.add_handler(CommandHandler("generate_link", generate_link_handler))
    application.add_handler(CommandHandler("done", done_handler))
    
    # Message handlers
    application.add_handler(MessageHandler(filters.VIDEO, video_handler))
    application.add_handler(MessageHandler(filters.PHOTO, photo_handler))
    application.add_handler(MessageHandler(filters.Document.ALL, document_handler))
    
    # Callback query handler for inline buttons
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Error handler
    application.add_error_handler(error_handler)
    
    # Post init and shutdown
    application.post_init = post_init
    application.post_shutdown = post_shutdown
    
    # Start bot
    logger.info("Starting bot...")
    application.run_polling(allowed_updates=["message", "callback_query"])

if __name__ == "__main__":
    main()
