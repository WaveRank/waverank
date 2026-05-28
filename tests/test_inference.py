"""
Tests genre predictions by inference.py, using a folder of random songs.
"""

# ----- IMPORTS -----
from pathlib import Path
import json
from webapp.server.services.inference import predict_genre
from shared.paths import PROJECT_ROOT, DATA_DIR

# Configuration
INPUT_DIR = DATA_DIR / "test_songs"
OUTPUT_DIR = PROJECT_ROOT / "tests" / "artifacts"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Walk directory to find each song and process it
songs = [f for f in INPUT_DIR.iterdir()
         if f.suffix.lower() in (".wav", ".mp3", ".mp4")]
results = {}
for song in songs:
    try:
        song_prediction = predict_genre(song)
        results[song.name] = song_prediction   
    except Exception as e:
        print(f"Skipping {song.name}: {e}")
        results[song.name] = "error" 

# Save results
with open(OUTPUT_DIR / "inference_test_results.json", "w") as outfile: 
    json.dump(results, outfile, indent=4)
