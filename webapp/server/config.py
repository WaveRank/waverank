import os
from dotenv import load_dotenv

load_dotenv()

# Environment-based configuration
PORT = int(os.getenv("PORT", 5000))
MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 10 * 1024 * 1024))

# Static application configuration
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'mp4'}
UPLOAD_FOLDER = "uploads"
