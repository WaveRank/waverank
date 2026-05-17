"""
Utilities for managing uploaded files and generated directories.
This module provides helpers for:
- creating uniquely named subdirectories to avoid filename collisions
- removing expired directories after a configured lifetime

Citations (5/15):
https://www.geeksforgeeks.org/python/delete-files-older-than-n-days-in-python/
"""
import os
import shutil
from pathlib import Path
import time
import uuid
from webapp.server.config import UPLOAD_DIR, GRAPH_DIR, HOURS_TO_LIVE


def create_unique_dir(dir):
    """
    Create a uniquely named subdirectory inside the given directory.

    Args:
        dir (Path): directory in which the subdirectory will be created
    Returns:
        str: generated subdirectory name
    """
    unique_dir_name = str(uuid.uuid4().hex[:8])
    path = dir / unique_dir_name

    path.mkdir(exist_ok=True)

    return unique_dir_name


def delete_old_subdirs(dir, hours_to_live=HOURS_TO_LIVE):
    """
    Delete subdirectories older than the configured lifetime.
    Non-directory files are ignored.

    Args:
        dir (Path): directory containing generated subdirectories
        hours_to_live (number): maximum allowed age of subdirectories, in hours
    """
    SEC_IN_HOUR = 3600
    list_of_contents = os.listdir(dir)
    current_time = time.time()

    for filename in list_of_contents:
        path = dir / filename
        last_modified = os.stat(path).st_mtime

        if (current_time - last_modified > hours_to_live * SEC_IN_HOUR):
            if path.is_dir():
                shutil.rmtree(path)
