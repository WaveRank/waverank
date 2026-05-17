"""
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
    Create a uniquely named subdirectory in the given directory and return its path.
    """
    unique_dir_name = str(uuid.uuid4().hex[:8])
    path = dir / unique_dir_name

    path.mkdir(exist_ok=True)

    return unique_dir_name


def delete_old_subdirs(dir, hours_to_live=HOURS_TO_LIVE):
    """
    Deletes subdirectories of the given directory if older than the given limit.
    """
    SEC_IN_HOUR = 3600
    list_of_subdirs = os.listdir(dir)
    current_time = time.time()

    for subdir in list_of_subdirs:
        path = dir / subdir
        last_modified = os.stat(path).st_mtime

        if (current_time - last_modified > hours_to_live * SEC_IN_HOUR):
            shutil.rmtree(path)
