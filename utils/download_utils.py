"""
Download utilities for URL downloading
"""
import os
import logging
import aiohttp
import yt_dlp

logger = logging.getLogger(__name__)

class DownloadProcessor:
    """Download processing utilities"""
    
    @staticmethod
    async def download_from_url(url: str, output_path: str) -> bool:
        """Download file from direct URL"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        with open(output_path, 'wb') as f:
                            f.write(await response.read())
                        return True
            return False
        except Exception as e:
            logger.error(f"Error downloading from URL: {e}")
            return False
    
    @staticmethod
    async def download_from_streaming(url: str, output_path: str) -> bool:
        """Download from streaming platforms using yt-dlp"""
        try:
            ydl_opts = {
                'outtmpl': output_path,
                'format': 'best',
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return True
        except Exception as e:
            logger.error(f"Error downloading from streaming platform: {e}")
            return False
    
    @staticmethod
    def generate_direct_link(file_path: str, base_url: str) -> str:
        """Generate direct download link for file"""
        # This is a placeholder - in production, you'd upload to a file server
        # and return the actual URL
        filename = os.path.basename(file_path)
        return f"{base_url}/downloads/{filename}"
