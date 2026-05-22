"""
Tests genre predictions by inference.py, using a folder of random songs.
"""

# ----- IMPORTS -----
from pathlib import Path
import json
from webapp.server.inference import predict_genre

BASE_DIR = Path(__file__).resolve().parent
SONG_DIR = BASE_DIR / "../../Data/test_songs"

# Walk directory to find each song and process it
songs = [f for f in SONG_DIR.iterdir()
         if f.suffix.lower() in (".wav", ".mp3", ".mp4")]
results = {}
for song in songs:
    try:
        song_prediction = predict_genre(song)
        results[song.name] = song_prediction   
    except Exception as e:
        print(f"Skipping {song.name}: {e}")
        results[song.name] = "error" 

# Jsonify
with open(BASE_DIR / "test_results.json", "w") as outfile: 
    json.dump(results, outfile, indent=4)
