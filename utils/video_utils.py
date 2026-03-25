"""
Utility functions for video processing
"""
import os
import subprocess
import logging
from typing import Optional, Tuple
import json

logger = logging.getLogger(__name__)

class VideoProcessor:
    """Video processing utilities using FFmpeg"""
    
    @staticmethod
    async def get_video_info(file_path: str) -> dict:
        """Get video metadata"""
        try:
            cmd = [
                'ffprobe', '-v', 'quiet',
                '-print_format', 'json',
                '-show_format', '-show_streams',
                file_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return json.loads(result.stdout)
        except Exception as e:
            logger.error(f"Error getting video info: {e}")
            return {}
    
    @staticmethod
    async def merge_videos(input_files: list, output_file: str) -> bool:
        """Merge multiple videos"""
        try:
            # Create concat file
            concat_file = output_file + '.txt'
            with open(concat_file, 'w') as f:
                for file in input_files:
                    f.write(f"file '{file}'\n")
            
            cmd = [
                'ffmpeg', '-f', 'concat', '-safe', '0',
                '-i', concat_file, '-c', 'copy', output_file
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            os.remove(concat_file)
            
            if result.returncode == 0:
                return True
            else:
                logger.error(f"FFmpeg error: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"Error merging videos: {e}")
            return False
    
    @staticmethod
    async def trim_video(input_file: str, output_file: str, 
                        start_time: str, duration: str) -> bool:
        """Trim video"""
        try:
            cmd = [
                'ffmpeg', '-i', input_file,
                '-ss', start_time, '-t', duration,
                '-c', 'copy', output_file
            ]
            subprocess.run(cmd, check=True)
            return True
        except Exception as e:
            logger.error(f"Error trimming video: {e}")
            return False
    
    @staticmethod
    async def compress_video(input_file: str, output_file: str, 
                            mode: str = 'fast') -> bool:
        """Compress video"""
        try:
            if mode == 'hevc':
                cmd = [
                    'ffmpeg', '-i', input_file,
                    '-c:v', 'libx265', '-crf', '28',
                    '-c:a', 'aac', '-b:a', '128k',
                    output_file
                ]
            else:  # fast mode
                cmd = [
                    'ffmpeg', '-i', input_file,
                    '-c:v', 'libx264', '-crf', '23',
                    '-preset', 'fast',
                    '-c:a', 'aac', '-b:a', '128k',
                    output_file
                ]
            subprocess.run(cmd, check=True)
            return True
        except Exception as e:
            logger.error(f"Error compressing video: {e}")
            return False
    
    @staticmethod
    async def encode_video(input_file: str, output_file: str,
                          codec: str = 'libx264') -> bool:
        """Encode video to different format"""
        try:
            cmd = [
                'ffmpeg', '-i', input_file,
                '-c:v', codec, '-c:a', 'aac',
                output_file
            ]
            subprocess.run(cmd, check=True)
            return True
        except Exception as e:
            logger.error(f"Error encoding video: {e}")
            return False
    
    @staticmethod
    async def extract_audio(input_file: str, output_file: str) -> bool:
        """Extract audio from video"""
        try:
            cmd = [
                'ffmpeg', '-i', input_file,
                '-vn', '-acodec', 'libmp3lame',
                '-q:a', '2', output_file
            ]
            subprocess.run(cmd, check=True)
            return True
        except Exception as e:
            logger.error(f"Error extracting audio: {e}")
            return False
    
    @staticmethod
    async def add_audio(video_file: str, audio_file: str, 
                       output_file: str) -> bool:
        """Add audio to video"""
        try:
            cmd = [
                'ffmpeg', '-i', video_file, '-i', audio_file,
                '-c:v', 'copy', '-c:a', 'aac',
                '-map', '0:v:0', '-map', '1:a:0',
                output_file
            ]
            subprocess.run(cmd, check=True)
            return True
        except Exception as e:
            logger.error(f"Error adding audio: {e}")
            return False
    
    @staticmethod
    async def extract_subtitles(input_file: str, output_file: str) -> bool:
        """Extract subtitles from video"""
        try:
            cmd = [
                'ffmpeg', '-i', input_file,
                '-map', '0:s:0', output_file
            ]
            subprocess.run(cmd, check=True)
            return True
        except Exception as e:
            logger.error(f"Error extracting subtitles: {e}")
            return False
    
    @staticmethod
    async def add_subtitles(video_file: str, subtitle_file: str,
                           output_file: str) -> bool:
        """Add subtitles to video"""
        try:
            cmd = [
                'ffmpeg', '-i', video_file, '-i', subtitle_file,
                '-c', 'copy', '-c:s', 'mov_text',
                output_file
            ]
            subprocess.run(cmd, check=True)
            return True
        except Exception as e:
            logger.error(f"Error adding subtitles: {e}")
            return False
    
    @staticmethod
    async def generate_screenshot(input_file: str, output_file: str,
                                  timestamp: str = '00:00:01') -> bool:
        """Generate screenshot from video"""
        try:
            cmd = [
                'ffmpeg', '-i', input_file,
                '-ss', timestamp, '-vframes', '1',
                output_file
            ]
            subprocess.run(cmd, check=True)
            return True
        except Exception as e:
            logger.error(f"Error generating screenshot: {e}")
            return False
    
    @staticmethod
    async def add_watermark(video_file: str, watermark_file: str,
                           output_file: str, position: str = 'bottom-right') -> bool:
        """Add watermark to video"""
        try:
            # Position mapping
            positions = {
                'top-left': '10:10',
                'top-right': 'W-w-10:10',
                'bottom-left': '10:H-h-10',
                'bottom-right': 'W-w-10:H-h-10',
                'center': '(W-w)/2:(H-h)/2'
            }
            overlay_pos = positions.get(position, 'W-w-10:H-h-10')
            
            cmd = [
                'ffmpeg', '-i', video_file, '-i', watermark_file,
                '-filter_complex', f'overlay={overlay_pos}',
                '-codec:a', 'copy', output_file
            ]
            subprocess.run(cmd, check=True)
            return True
        except Exception as e:
            logger.error(f"Error adding watermark: {e}")
            return False
    
    @staticmethod
    def get_file_size(file_path: str) -> int:
        """Get file size in bytes"""
        return os.path.getsize(file_path) if os.path.exists(file_path) else 0
    
    @staticmethod
    def format_size(size_bytes: int) -> str:
        """Format bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"
