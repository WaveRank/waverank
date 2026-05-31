"""
Utilities for downloading audio file from youtube link.
This module provides:
- a utility function for downloading audio from YouTube links

Citations (5/20):
https://github.com/yt-dlp/yt-dlp
"""
import yt_dlp
import os
from shared.paths import UPLOAD_DIR
from webapp.server.config import MAX_YOUTUBE_LENGTH
from webapp.server.services.file_io import create_unique_dir

def get_cookies_path():
    """
    Returns the path to the youtube cookies file from Hugging Face.
    """
    if os.getenv("RAILWAY_ENVIRONMENT"):
        path = os.getenv("COOKIES_PATH")
        print(
            f"Cookies path: {path}, exists: {os.path.exists(path) if path else False}",
            flush=True,
        )
        return path
    return None

def download_youtube_audio(link):
    """
    Downloads the audio for the youtube video at the link provided.
    Args:
        link (str): YouTube video link
    Returns:
        filepath, filename (str, str): Path to and title of audio file
    """

    # Set info extraction options
    ydl_opts = {
        'quiet': True,
        'noplaylist': True,
        'cookiefile': get_cookies_path(),
    }

    # Check video information to validate
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=False)
        info = ydl.sanitize_info(info)

        # Safeguard against livestreams, non-videos, and long videos
        if info is None or 'duration' not in info:
            if info and info.get('is_live'):
                raise ValueError("Livestreams are not supported")
            else:
                raise ValueError("Video not found")
        if info['duration'] > MAX_YOUTUBE_LENGTH:
            raise ValueError(f"Video exceeds maximum duration ({MAX_YOUTUBE_LENGTH // 60} min)")
        new_upload_subdir = create_unique_dir(UPLOAD_DIR)
        filepath = UPLOAD_DIR / new_upload_subdir / "audio" # yt-dlp adds extension
        filename = info['title']

    # Set download options
    ydl_opts['format'] = 'bestaudio/best'
    ydl_opts['outtmpl'] = str(filepath)
    ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3'}]

    # Actually download audio
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])
    
    return filepath.with_suffix('.mp3'), filename
