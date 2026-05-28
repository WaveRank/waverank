from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Data
DATA_DIR = PROJECT_ROOT / "data"
DATASET_DIR = DATA_DIR / "dataset"

# Model
MODEL_ARTIFACTS_DIR = PROJECT_ROOT / "model" / "artifacts"

# Visualizations
VISUALIZATIONS_OUTPUT_DIR = PROJECT_ROOT / "visualizations" / "output"

# Server
SERVER_DIR = PROJECT_ROOT / "webapp" / "server"
ARTIFACTS_DIR = SERVER_DIR / "artifacts"
GRAPH_DIR = ARTIFACTS_DIR / "graphs"
UPLOAD_DIR = ARTIFACTS_DIR / "uploads"