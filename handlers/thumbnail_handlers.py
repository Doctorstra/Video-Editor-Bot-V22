"""
Thumbnail handlers
"""
from telegram import Update
from telegram.ext import ContextTypes
from database import db
import logging

logger = logging.getLogger(__name__)

async def set_thumbnail_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /set_thumbnail command"""
    await update.message.reply_text(
        "🖼️ **Set Permanent Thumbnail**\n\n"
        "Send me an image to set as your permanent thumbnail.\n"
        "This thumbnail will be used for all your videos."
    )

async def show_thumbnail_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /show_thumbnail command"""
    user_id = update.effective_user.id
    thumbnail_id = await db.get_thumbnail(user_id)
    
    if thumbnail_id:
        await update.message.reply_photo(
            photo=thumbnail_id,
            caption="🖼️ Your current permanent thumbnail"
        )
    else:
        await update.message.reply_text(
            "You don't have a permanent thumbnail set.\n"
            "Use /set_thumbnail to set one!"
        )

async def delete_thumbnail_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /delete_thumbnail command"""
    user_id = update.effective_user.id
    await db.delete_thumbnail(user_id)
    await update.message.reply_text("✅ Permanent thumbnail deleted!")

async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming photos for thumbnail"""
    user_id = update.effective_user.id
    photo = update.message.photo[-1]  # Get highest resolution
    
    # Save thumbnail
    await db.save_thumbnail(user_id, photo.file_id)
    
    await update.message.reply_text(
        "✅ Permanent thumbnail saved!\n\n"
        "This will be used for all your videos.\n"
        "Use /show_thumbnail to view it or /delete_thumbnail to remove it."
    )
