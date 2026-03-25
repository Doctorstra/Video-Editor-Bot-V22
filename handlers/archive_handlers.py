"""
Archive and download handlers
"""
from telegram import Update
from telegram.ext import ContextTypes
from utils.archive_utils import ArchiveProcessor
from utils.download_utils import DownloadProcessor
from config import Config
import os
import logging

logger = logging.getLogger(__name__)

user_archive_states = {}

async def archive_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /archive command"""
    if not context.args:
        await update.message.reply_text(
            "Usage: /archive <type>\n\n"
            "Types: zip, tar, rar\n"
            "Example: /archive zip\n\n"
            "Then send files to archive. Send /done when finished."
        )
        return
    
    archive_type = context.args[0].lower()
    if archive_type not in ['zip', 'tar', 'rar']:
        await update.message.reply_text("Invalid type! Use: zip, tar, or rar")
        return
    
    user_id = update.effective_user.id
    user_archive_states[user_id] = {
        'type': archive_type,
        'files': []
    }
    
    await update.message.reply_text(
        f"📦 Creating {archive_type.upper()} archive\n\n"
        f"Send me files to add. Send /done when finished."
    )

async def extract_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /extract command"""
    await update.message.reply_text(
        "📂 **Archive Extractor**\n\n"
        "Send me an archive file to extract.\n"
        "Supported: zip, tar, rar"
    )

async def download_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /download command"""
    if not context.args:
        await update.message.reply_text(
            "Usage: /download <url>\n\n"
            "Supported:\n"
            "• Direct URLs\n"
            "• Streaming platforms (MX Player, Hotstar, etc.)"
        )
        return
    
    url = context.args[0]
    user_id = update.effective_user.id
    
    status_msg = await update.message.reply_text("⏳ Downloading...")
    
    try:
        output_path = os.path.join(Config.DOWNLOAD_PATH, f"download_{user_id}.mp4")
        
        # Try streaming download first
        success = await DownloadProcessor.download_from_streaming(url, output_path)
        
        if not success:
            # Try direct download
            success = await DownloadProcessor.download_from_url(url, output_path)
        
        if success and os.path.exists(output_file):
            with open(output_file, 'rb') as video_file:
                await context.bot.send_video(
                    chat_id=update.effective_chat.id,
                    video=video_file,
                    caption="✅ Downloaded successfully!"
                )
            os.remove(output_file)
            await status_msg.delete()
        else:
            await status_msg.edit_text("❌ Failed to download from URL!")
    
    except Exception as e:
        logger.error(f"Download error: {e}")
        await status_msg.edit_text(f"❌ Error: {str(e)}")

async def generate_link_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /generate_link command"""
    await update.message.reply_text(
        "🔗 **Direct Link Generator**\n\n"
        "Send me a file to generate a direct download link."
    )

async def document_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming documents"""
    user_id = update.effective_user.id
    document = update.message.document
    
    # Check if in archive state
    if user_id in user_archive_states:
        # Download and add to archive list
        file = await context.bot.get_file(document.file_id)
        file_path = os.path.join(Config.DOWNLOAD_PATH, document.file_name)
        await file.download_to_drive(file_path)
        
        user_archive_states[user_id]['files'].append(file_path)
        
        await update.message.reply_text(
            f"✅ Added: {document.file_name}\n"
            f"Total files: {len(user_archive_states[user_id]['files'])}\n\n"
            f"Send more files or /done to create archive."
        )
        return
    
    # Check if it's an archive for extraction
    if document.file_name.endswith(('.zip', '.tar', '.rar', '.tar.gz', '.tgz')):
        status_msg = await update.message.reply_text("⏳ Extracting archive...")
        
        try:
            file = await context.bot.get_file(document.file_id)
            archive_path = os.path.join(Config.DOWNLOAD_PATH, document.file_name)
            await file.download_to_drive(archive_path)
            
            output_dir = os.path.join(Config.UPLOAD_PATH, f"extracted_{user_id}")
            success = await ArchiveProcessor.extract_archive(archive_path, output_dir)
            
            if success:
                # Send extracted files
                for root, dirs, files in os.walk(output_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'rb') as doc_file:
                                await context.bot.send_document(
                                    chat_id=update.effective_chat.id,
                                    document=doc_file,
                                    filename=file
                                )
                        except:
                            pass
                
                await status_msg.edit_text("✅ Archive extracted successfully!")
                
                # Cleanup
                import shutil
                shutil.rmtree(output_dir)
            else:
                await status_msg.edit_text("❌ Failed to extract archive!")
            
            os.remove(archive_path)
        
        except Exception as e:
            logger.error(f"Extract error: {e}")
            await status_msg.edit_text(f"❌ Error: {str(e)}")

async def done_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /done command for multi-file operations"""
    user_id = update.effective_user.id
    
    if user_id in user_archive_states:
        state = user_archive_states[user_id]
        
        if len(state['files']) < 1:
            await update.message.reply_text("No files to archive!")
            return
        
        status_msg = await update.message.reply_text("⏳ Creating archive...")
        
        try:
            archive_type = state['type']
            output_file = os.path.join(
                Config.UPLOAD_PATH,
                f"archive_{user_id}.{archive_type}"
            )
            
            success = await ArchiveProcessor.create_archive(
                state['files'], output_file, archive_type
            )
            
            if success and os.path.exists(output_file):
                with open(output_file, 'rb') as doc_file:
                    await context.bot.send_document(
                        chat_id=update.effective_chat.id,
                        document=doc_file,
                        caption=f"✅ {archive_type.upper()} archive created!"
                    )
                os.remove(output_file)
            else:
                await status_msg.edit_text("❌ Failed to create archive!")
            
            # Cleanup
            for file in state['files']:
                if os.path.exists(file):
                    os.remove(file)
        
        except Exception as e:
            logger.error(f"Archive error: {e}")
            await status_msg.edit_text(f"❌ Error: {str(e)}")
        
        finally:
            user_archive_states.pop(user_id, None)
            await status_msg.delete()
