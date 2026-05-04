"""
Tests genre predictions by inference.py, using a folder of random songs.
"""

import os
import json
from inference import predict_genre

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SONG_DIR = os.path.join(BASE_DIR, "../../Data/test_songs")

# Walk directory to find each song and process it
songs = [file for file in os.listdir(SONG_DIR) if file.endswith((".wav", ".mp3", ".mp4"))]
results = {}
for song in songs:
    try:
        song_prediction = predict_genre(os.path.join(SONG_DIR, song))
        results[song] = song_prediction
    except Exception as e:
        print(f"Skipping {song}: {e}")
        results[song] = "error"

# JSONIFYYYYYYY
with open(os.path.join(BASE_DIR, "test_results.json"), "w") as outfile:
    json.dump(results, outfile, indent=4)
