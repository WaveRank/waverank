"""
Segments the GTZAN dataset, where each 30-second audio track is divided into
segments of a given size to expand the dataset size.
Assumes that dataset has already been split into training/validation/testing sets.

Note: One of the jazz .wav files is corrupted and is thus skipped.

Citation (4/9/26): 
https://stackoverflow.com/questions/60105626/split-audio-on-timestamps-librosa
"""

# ----- IMPORTS -----
from pathlib import Path
import soundfile as sf
from model.src.audio.audio_utils import load_audio, segment_audio
from shared.paths import DATA_DIR

# ----- CONFIGURATION -----
INPUT_DIR = DATA_DIR / "distributed_dataset"
OUTPUT_DIR = DATA_DIR / "segmented_dataset"
MAX_SEC = 30
skipped_files = []


# ----- MAIN PIPELINE -----
for split_path in INPUT_DIR.iterdir():
    for genre_in in split_path.iterdir():
        genre_out =  OUTPUT_DIR / split_path.name / genre_in.name
        genre_out.mkdir(parents=True, exist_ok=True)

        for file in genre_in.iterdir():

            # Skip non-audio files
            if file.suffix.lower() != ".wav":
                continue

            # Load audio
            y, sr = load_audio(file)
            if y is None:
                skipped_files.append(file)
                continue

            # Trim to max length and split into fixed-size overlapping segments
            y = y[:MAX_SEC * sr]
            segments = segment_audio(y, sr)
            for i, segment in enumerate(segments):
                out_path = genre_out / f"{file.stem}_{i}.wav"
                sf.write(out_path, segment, sr)

# ----- SUMMARY -----
print("\nAll WAV files segmented successfully! :)")

if skipped_files:
    print("Skipped files:")
    for file in skipped_files:
        print("-", file)

print("\n")
