"""
Database module for MongoDB operations
"""
from motor.motor_asyncio import AsyncIOMotorClient
from config import Config
import logging

logger = logging.getLogger(__name__)

class Database:
    """MongoDB database handler"""
    
    def __init__(self):
        self.client = None
        self.db = None
        
    async def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = AsyncIOMotorClient(Config.MONGODB_URI)
            self.db = self.client[Config.DATABASE_NAME]
            # Test connection
            await self.client.admin.command('ping')
            logger.info("Connected to MongoDB successfully")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            
    async def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")
    
    # User operations
    async def add_user(self, user_id, username=None, first_name=None):
        """Add or update user in database"""
        user_data = {
            "user_id": user_id,
            "username": username,
            "first_name": first_name
        }
        await self.db.users.update_one(
            {"user_id": user_id},
            {"$set": user_data},
            upsert=True
        )
    
    async def get_user(self, user_id):
        """Get user from database"""
        return await self.db.users.find_one({"user_id": user_id})
    
    async def get_all_users(self):
        """Get all users from database"""
        cursor = self.db.users.find({})
        return await cursor.to_list(length=None)
    
    async def get_users_count(self):
        """Get total users count"""
        return await self.db.users.count_documents({})
    
    # Thumbnail operations
    async def save_thumbnail(self, user_id, file_id):
        """Save user's permanent thumbnail"""
        await self.db.users.update_one(
            {"user_id": user_id},
            {"$set": {"thumbnail": file_id}},
            upsert=True
        )
    
    async def get_thumbnail(self, user_id):
        """Get user's permanent thumbnail"""
        user = await self.get_user(user_id)
        return user.get("thumbnail") if user else None
    
    async def delete_thumbnail(self, user_id):
        """Delete user's permanent thumbnail"""
        await self.db.users.update_one(
            {"user_id": user_id},
            {"$unset": {"thumbnail": ""}}
        )
    
    # Storage tracking
    async def update_storage(self, user_id, file_size):
        """Update user's storage usage"""
        await self.db.users.update_one(
            {"user_id": user_id},
            {"$inc": {"storage_used": file_size}},
            upsert=True
        )
    
    async def get_storage(self, user_id):
        """Get user's storage usage"""
        user = await self.get_user(user_id)
        return user.get("storage_used", 0) if user else 0

# Global database instance
db = Database()
