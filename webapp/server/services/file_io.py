from werkzeug.utils import secure_filename
import os
from webapp.server.config import UPLOAD_DIR


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
