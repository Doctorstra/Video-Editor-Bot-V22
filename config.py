"""
Configuration module for the Video Editor Bot
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Bot configuration class"""
    
    # Telegram Bot Configuration
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    API_ID = int(os.getenv("API_ID", "0"))
    API_HASH = os.getenv("API_HASH")
    
    # MongoDB Configuration
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "video_editor_bot")
    
    # Channel Configuration
    LOG_CHANNEL_ID = os.getenv("LOG_CHANNEL_ID")
    BROADCAST_AS_COPY = os.getenv("BROADCAST_AS_COPY", "True") == "True"
    
    # Admin Configuration
    ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]
    
    # File Settings
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "2000"))  # in MB
    DOWNLOAD_PATH = os.getenv("DOWNLOAD_PATH", "./downloads")
    UPLOAD_PATH = os.getenv("UPLOAD_PATH", "./uploads")
    
    # Feature Toggles
    ENABLE_BROADCAST = os.getenv("ENABLE_BROADCAST", "True") == "True"
    ENABLE_URL_UPLOAD = os.getenv("ENABLE_URL_UPLOAD", "True") == "True"
    ENABLE_WATERMARK = os.getenv("ENABLE_WATERMARK", "True") == "True"
    
    # Ensure directories exist
    os.makedirs(DOWNLOAD_PATH, exist_ok=True)
    os.makedirs(UPLOAD_PATH, exist_ok=True)
    os.makedirs("logs", exist_ok=True)
