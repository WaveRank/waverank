"""
Citations (5/15):
https://www.geeksforgeeks.org/python/delete-files-older-than-n-days-in-python/
"""
from werkzeug.utils import secure_filename
import os
import time
from webapp.server.config import UPLOAD_DIR, GRAPH_DIR, HOURS_TO_LIVE


def save_file(file):
    """
    Sanitizing filename, save file
    Args:
        file (file)
    Returns:
        filename (str), filepath (PosixPath)
    Side Effects:
        saves file to disk at filepath
    """
    # Prevent path traversal or unsafe characters
    filename = secure_filename(file.filename)

    filepath = os.path.join(UPLOAD_DIR, filename)
    file.save(filepath)
    return filename, filepath


# Return base filename without extension from a given filepath
def get_basename(filepath):
    filename = os.path.basename(filepath)
    base_name = os.path.splitext(filename)[0]
    return base_name


# Delete files older than the given limit
def delete_old_files(dir, hours_to_live=HOURS_TO_LIVE):
    SEC_IN_HOUR = 3600
    list_of_files = os.listdir(dir)
    current_time = time.time()

    for filename in list_of_files:
        filepath = os.path.join(dir, filename)
        last_modified = os.stat(filepath).st_mtime

        if (current_time - last_modified > hours_to_live * SEC_IN_HOUR):
            print(f"removing old file: {filepath}")
            os.remove(filepath)
