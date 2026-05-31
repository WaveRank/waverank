"""
Tests genre predictions by inference.py, using a folder of random songs.
"""

# ----- IMPORTS -----
from pathlib import Path
import json
from webapp.server.services.inference import predict_genre
from model.src.audio.audio_utils import load_audio
from shared.paths import PROJECT_ROOT, DATA_DIR

# Configuration
INPUT_DIR = DATA_DIR / "test_songs"
OUTPUT_DIR = PROJECT_ROOT / "tests" / "artifacts"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Walk directory to find each song and process it
song_paths = [f for f in INPUT_DIR.iterdir()
         if f.suffix.lower() in (".wav", ".mp3", ".mp4")]
results = {}
for song_path in song_paths:
    try:
        y, sr = load_audio(song_path)
        song_prediction = predict_genre(y, sr)
        results[song_path.name] = song_prediction   
    except Exception as e:
        print(f"Skipping {song_path.name}: {e}")
        results[song_path.name] = "error" 

# Save results
with open(OUTPUT_DIR / "inference_test_results.json", "w") as outfile: 
    json.dump(results, outfile, indent=4)
