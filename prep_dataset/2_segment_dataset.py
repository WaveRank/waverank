"""
Segments the GTZAN dataset, where each 30-second audio track is divided into
segments of a given size to expand the dataset size.
Assumes that dataset has already been split into training/validation/testing sets.

Note: One of the jazz .wav files is corrupted and is thus skipped.

Citation (4/9/26): 
https://stackoverflow.com/questions/60105626/split-audio-on-timestamps-librosa
"""

# ----- IMPORTS -----
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import soundfile as sf
import numpy as np
from shared.audio_utils import load_audio, segment_audio

# ----- CONFIGURATION -----
BASE_PATH = "./"
INPUT_DIR = os.path.join(BASE_PATH, "Data/distributed_dataset")
OUTPUT_DIR = os.path.join(BASE_PATH, "Data/segmented_dataset")
MAX_SEC = 30       # 50% overlap
skipped_files = []

# ----- HELPER FUNCTIONS -----
# NOTE: not currently called; retained for potential use with partial segments
def pad_if_needed(segment, target_len):
    """Pad an audio segment with zeros if shorter than the target length."""
    if len(segment) < target_len:
        return np.pad(segment, (0, target_len - len(segment)), mode="constant")
    return segment

# ----- MAIN PIPELINE -----
for split_name in os.listdir(INPUT_DIR):
    split_path = os.path.join(INPUT_DIR, split_name)
   
    for genre in os.listdir(split_path):
        genre_in = os.path.join(split_path, genre)
        genre_out = os.path.join(OUTPUT_DIR, split_name, genre)
        os.makedirs(genre_out, exist_ok=True)

        for file in os.listdir(genre_in):
            # Skip non-audio files
            if not file.lower().endswith(".wav"):
                continue
            path = os.path.join(genre_in, file)

            # Load audio
            y, sr = load_audio(path)
            if y is None:
                skipped_files.append(path)
                continue

            # Trim to max length and split into fixed-size overlapping segments
            y = y[:MAX_SEC * sr]
            base = os.path.splitext(file)[0]
            segments = segment_audio(y, sr)
            for i, segment in enumerate(segments):
                out_path = os.path.join(genre_out, f"{base}_{i}.wav")
                sf.write(out_path, segment, sr)

# ----- SUMMARY -----
print("\nAll WAV files segmented successfully! :)")

if skipped_files:
    print("Skipped files:")
    for file in skipped_files:
        print("-", file)

print("\n")
