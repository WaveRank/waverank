import os
from dotenv import load_dotenv

load_dotenv()

# Environment-based configuration
PORT = int(os.getenv("PORT", 5000))
MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 10 * 1024 * 1024))
MAX_YOUTUBE_LENGTH = 600        # 10 minutes in seconds

# File upload constraints
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'mp4'}

# Graph and upload subdir age limit
MINUTES_TO_LIVE = 15
