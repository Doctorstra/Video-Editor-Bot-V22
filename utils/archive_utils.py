"""
Archive utilities for compression and extraction
"""
import os
import tarfile
import zipfile
import logging
import subprocess

logger = logging.getLogger(__name__)

class ArchiveProcessor:
    """Archive processing utilities"""
    
    @staticmethod
    async def create_archive(input_files: list, output_file: str, 
                            archive_type: str = 'zip') -> bool:
        """Create archive from files"""
        try:
            if archive_type == 'zip':
                with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for file in input_files:
                        zipf.write(file, os.path.basename(file))
            elif archive_type == 'tar':
                with tarfile.open(output_file, 'w') as tar:
                    for file in input_files:
                        tar.add(file, arcname=os.path.basename(file))
            elif archive_type == 'rar':
                # Use rar command if available
                cmd = ['rar', 'a', output_file] + input_files
                subprocess.run(cmd, check=True)
            else:
                return False
            return True
        except Exception as e:
            logger.error(f"Error creating archive: {e}")
            return False
    
    @staticmethod
    async def extract_archive(archive_file: str, output_dir: str) -> bool:
        """Extract archive"""
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            if archive_file.endswith('.zip'):
                with zipfile.ZipFile(archive_file, 'r') as zipf:
                    zipf.extractall(output_dir)
            elif archive_file.endswith(('.tar', '.tar.gz', '.tgz')):
                with tarfile.open(archive_file, 'r:*') as tar:
                    tar.extractall(output_dir)
            elif archive_file.endswith('.rar'):
                cmd = ['unrar', 'x', archive_file, output_dir]
                subprocess.run(cmd, check=True)
            else:
                return False
            return True
        except Exception as e:
            logger.error(f"Error extracting archive: {e}")
            return False
