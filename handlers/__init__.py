"""
Handlers package initialization
"""
from .basic_handlers import (
    start_handler, help_handler, stats_handler,
    about_handler, broadcast_handler, stats_all_handler,
    button_handler
)
from .video_handlers import (
    compress_handler, trim_handler, merge_handler,
    rename_handler, encode_handler, screenshot_handler,
    metadata_handler, extract_audio_handler, extract_subs_handler,
    add_watermark_handler, storage_handler, video_handler
)
from .thumbnail_handlers import (
    set_thumbnail_handler, show_thumbnail_handler,
    delete_thumbnail_handler, photo_handler
)
from .archive_handlers import (
    archive_handler, extract_handler, download_handler,
    generate_link_handler, document_handler, done_handler
)

__all__ = [
    'start_handler', 'help_handler', 'stats_handler',
    'about_handler', 'broadcast_handler', 'stats_all_handler',
    'button_handler',
    'compress_handler', 'trim_handler', 'merge_handler',
    'rename_handler', 'encode_handler', 'screenshot_handler',
    'metadata_handler', 'extract_audio_handler', 'extract_subs_handler',
    'add_watermark_handler', 'storage_handler', 'video_handler',
    'set_thumbnail_handler', 'show_thumbnail_handler',
    'delete_thumbnail_handler', 'photo_handler',
    'archive_handler', 'extract_handler', 'download_handler',
    'generate_link_handler', 'document_handler', 'done_handler'
]
