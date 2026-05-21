"""
Utilities for downloading audio file from youtube link.
This module provides:
- stuff

Citations (5/20):
"""
import yt_dlp
from webapp.server.config import UPLOAD_DIR
from webapp.server.services.file_io import create_unique_dir

def download_youtube_audio(link):
    """
    Downloads the audio for the youtube video at the link provided.
    Args:
        link (str): YouTube video link
    Returns:
        filepath, filename (str, str): Path to and title of audio file
    """
    new_upload_subdir = create_unique_dir(UPLOAD_DIR)
    filepath = UPLOAD_DIR / new_upload_subdir / "audio" # yt-dlp appends extension
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': str(filepath),
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # ydl.download([link])
        info = ydl.extract_info(link, download=True)
        info = ydl.sanitize_info(info)
        filename = info['title']
    
    return filepath.with_suffix('.mp3'), filename