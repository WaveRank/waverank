import os
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()

# Environment-based configuration
PORT = int(os.getenv("PORT", 5000))
MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 10 * 1024 * 1024))

# Static application configuration
# File upload constraints
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'mp4'}

# Paths
SERVER_DIR = Path(__file__).resolve().parent
GRAPH_DIR = SERVER_DIR / "graphs"
UPLOAD_DIR = SERVER_DIR / "uploads"

# Graphs
HOURS_TO_LIVE = 1
