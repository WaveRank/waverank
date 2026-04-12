"""
Segments the GTZAN dataset, where each 30-second audio track is divided into ten
non-overlapping 3-second segments to expand the dataset size by 10x.
Assumes that dataset has already been split into training/validation/testing sets.

Note: One of the jazz .wav files is corrupted and is thus skipped.

Citation (4/9/26): 
https://stackoverflow.com/questions/60105626/split-audio-on-timestamps-librosa
"""
import os
import librosa
import soundfile as sf
import numpy as np

# ----- CONFIGURATION -----
BASE_PATH = "/mnt/d/CS PROJECTS/467_Assignments/"
INPUT_DIR = os.path.join(BASE_PATH, "Data/distributed_dataset")
OUTPUT_DIR = os.path.join(BASE_PATH, "Data/segmented_dataset")

SEGMENT_SEC = 3
MAX_SEC = 30
skipped_files = []

# ----- HELPER FUNCTIONS -----
def load_audio(path):
    """Load an audio file using librosa."""
    try:
        return librosa.load(path, sr=None, mono=True)
    except Exception:
        return None, None

def pad_if_needed(segment, target_len):
    """Pad an audio segment with zeros if it is shorter than the target length."""
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

            # Trim to max duration (default: 3s)
            y = y[:MAX_SEC * sr]
            segment_len = SEGMENT_SEC * sr
            base = os.path.splitext(file)[0]

            # Split into fixed-size segments
            num_segments = int(np.ceil(len(y) / segment_len))
            for i in range(num_segments):
                start = i * segment_len
                end = start + segment_len

                segment = pad_if_needed(y[start:end], segment_len)

                out_path = os.path.join(genre_out, f"{base}_{i}.wav")
                sf.write(out_path, segment, sr)

# ----- SUMMARY -----
print("\nAll WAV files segmented successfully! :)")

if skipped_files:
    print("Skipped files:")
    for file in skipped_files:
        print("-", file)

print("\n")
