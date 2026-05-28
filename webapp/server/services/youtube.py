"""
Utilities for downloading audio file from youtube link.
This module provides:
- a utility function for downloading audio from YouTube links

Citations (5/20):
https://github.com/yt-dlp/yt-dlp
"""
import yt_dlp
from shared.paths import UPLOAD_DIR
from webapp.server.config import MAX_YOUTUBE_LENGTH
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
    filepath = UPLOAD_DIR / new_upload_subdir / "audio" # yt-dlp adds extension
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': str(filepath),
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}],
        'quiet': True,
        'noplaylist': True,
    }


    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=False)
        info = ydl.sanitize_info(info)

        # Safeguard against long videos
        if info and info['duration'] > MAX_YOUTUBE_LENGTH:
            raise ValueError(f"Video exceeds maximum duration ({MAX_YOUTUBE_LENGTH // 60} min)")
        filename = info['title']
        ydl.download([link])
    
    return filepath.with_suffix('.mp3'), filename
