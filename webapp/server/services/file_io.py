"""
Utilities for managing uploaded files and generated directories.
This module provides helpers for:
- creating uniquely named subdirectories to avoid filename collisions
- removing expired directories after a configured lifetime

Citations (5/15):
https://www.geeksforgeeks.org/python/delete-files-older-than-n-days-in-python/
"""
import shutil
from pathlib import Path
import time
import uuid
from shared.paths import UPLOAD_DIR, GRAPH_DIR
from webapp.server.config import MINUTES_TO_LIVE


def create_unique_dir(dir):
    """
    Create a uniquely named subdirectory inside the given directory.

    Args:
        dir (Path): directory in which the subdirectory will be created
    Returns:
        (str): generated subdirectory name
    """
    unique_dir_name = str(uuid.uuid4().hex[:8])
    filepath = dir / unique_dir_name

    filepath.mkdir(parents=True, exist_ok=True)

    return unique_dir_name


def delete_old_subdirs(dir, minutes_to_live=MINUTES_TO_LIVE):
    """
    Delete subdirectories older than the configured lifetime.
    Non-directory files are ignored.

    Args:
        dir (Path): directory containing generated subdirectories
        hours_to_live (number): maximum allowed age of subdirectories, in hours
    """
    SEC_IN_MINUTE = 60
    list_of_contents = dir.iterdir()
    current_time = time.time()

    for filename in list_of_contents:
        filepath = dir / filename
        last_modified = filepath.stat().st_mtime

        if (current_time - last_modified > minutes_to_live * SEC_IN_MINUTE):
            if filepath.is_dir():
                shutil.rmtree(filepath)
