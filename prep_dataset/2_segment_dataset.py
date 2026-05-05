"""
Segments the GTZAN dataset, where each 30-second audio track is divided into
segments of a given size to expand the dataset size.
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
BASE_PATH = "./"
INPUT_DIR = os.path.join(BASE_PATH, "Data/distributed_dataset")
OUTPUT_DIR = os.path.join(BASE_PATH, "Data/segmented_dataset")

SR = 22050 
SEGMENT_SEC = 10
MAX_SEC = 30
HOP_SEC = 5         # 50% overlap
skipped_files = []

# ----- HELPER FUNCTIONS -----
def load_audio(path):
    """Load an audio file using librosa."""
    try:
        return librosa.load(path, sr=SR, mono=True)
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

            # Trim to max duration 
            y = y[:MAX_SEC * sr]
            segment_len = SEGMENT_SEC * sr
            hop_len = HOP_SEC * sr
            base = os.path.splitext(file)[0]

            # Split into fixed-size, overlapping segments
            num_segments = len(range(0, len(y) - segment_len + 1, hop_len))
            for i in range(num_segments):
                start = i * hop_len
                end = start + segment_len
                segment = y[start:end]
                out_path = os.path.join(genre_out, f"{base}_{i}.wav")
                sf.write(out_path, segment, sr)

# ----- SUMMARY -----
print("\nAll WAV files segmented successfully! :)")

if skipped_files:
    print("Skipped files:")
    for file in skipped_files:
        print("-", file)

print("\n")
