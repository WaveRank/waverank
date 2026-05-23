import os
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()

# Environment-based configuration
PORT = int(os.getenv("PORT", 5000))
MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 10 * 1024 * 1024))
MAX_YOUTUBE_LENGTH = 600        # 10 minutes in seconds

# Static application configuration
# File upload constraints
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'mp4'}

# Paths
SERVER_DIR = Path(__file__).resolve().parent
GRAPH_DIR = SERVER_DIR / "graphs"
UPLOAD_DIR = SERVER_DIR / "uploads"

# Graphs
HOURS_TO_LIVE = 0.5
