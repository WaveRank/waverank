"""
Utilities for validating uploaded audio files.
This module provides:
- a fast extension-based filename check for early rejection
- authoritative validation by attempting to decode the file as audio
"""

import librosa
from webapp.server.config import MAX_CONTENT_LENGTH, ALLOWED_EXTENSIONS


def allowed_file(filename):
    """
    Perform a fast extension-based validation check.
    Args:
        filename (str): uploaded filename
    Returns:
        bool: True if file extension is allowed, otherwise False
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def decodable_audio_file(path):
    """
    Validate an audio file by attempting to decode it with librosa.
    Args:
        path (Path): path to uploaded audio file
    Returns:
        bool: True if audio decoding succeeds, otherwise False
    """
    try:
        librosa.load(path)
        return True
    except Exception as e:
        print("Decode error:", repr(e))
        return False
