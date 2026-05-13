"""
Reorganizes the FMA small dataset into a GTZAN-compatible folder structure.
Reads genre labels from FMA metadata (tracks.csv), then copies audio files
into Data/genres_original/<genre>/<track_id>.wav so that the rest of the
existing pipeline (scripts 1-3) works without modification.
 
Expected input layout:
    fma_metadata/tracks.csv
    fma_small/
        000/000002.mp3
        000/000003.mp3
        ...
 
Output layout (mirrors GTZAN genres_original):
    Data/genres_original/
        Hip-Hop/000002.wav
        Pop/000010.wav
        ...
 
Citations (4/30/26):
    https://github.com/mdeff/fma  (dataset + utils)
    https://librosa.org/doc/main/generated/librosa.load.html
"""

import os
import ast
import numpy as np
import pandas as pd
import librosa
import soundfile as sf
 
# ----- CONFIGURATION -----
BASE_PATH       = "./"
FMA_AUDIO_DIR   = os.path.join(BASE_PATH, "Data/fma_medium")
FMA_META_PATH   = os.path.join(BASE_PATH, "Data/fma_metadata/tracks.csv")
OUTPUT_DIR      = os.path.join(BASE_PATH, "Data/fma_med_genres_original")

# Use only the 'small' subset (8000 tracks, 8 genres)
TARGET_SUBSET   = "medium"
SR_OUT          = 22050     # resample to match script 3's SR expectation
skipped_files   = []
 
# ----- LOAD METADATA -----
# tracks.csv has a two-level header; mirroring the fma utils.load() approach
# without requiring the full utils.py dependency.
tracks = pd.read_csv(FMA_META_PATH, index_col=0, header=[0, 1])
 
# Keep only the 'small' subset rows
subset_mask = tracks[("set", "subset")] == TARGET_SUBSET
small_tracks = tracks[subset_mask].copy()
 
print(f"Tracks in '{TARGET_SUBSET}' subset: {len(small_tracks)}")
 
# Build a mapping: track_id (int) -> top-level genre string
# The genre_top column lives under the 'track' top-level header
genre_series = small_tracks[("track", "genre_top")].dropna()
print(f"Tracks with a top-level genre: {len(genre_series)}")
 
# ----- HELPER FUNCTIONS -----
def track_id_to_path(audio_dir, track_id):
    """
    FMA stores files as zero-padded 6-digit names inside 3-digit subdirectories.
    e.g. track 2  -> fma_small/000/000002.mp3
         track 10 -> fma_small/000/000010.mp3
    """
    tid_str  = f"{track_id:06d}"
    subdir   = tid_str[:3]
    filename = f"{tid_str}.mp3"
    return os.path.join(audio_dir, subdir, filename)
 
def load_and_resample(path, sr_out):
    """Load an MP3 with librosa and return (samples, sample_rate)."""
    try:
        y, sr = librosa.load(path, sr=sr_out, mono=True)
        return y, sr
    except Exception as e:
        return None, None
 
# ----- MAIN PIPELINE -----
for track_id, genre in genre_series.items():
    src_path = track_id_to_path(FMA_AUDIO_DIR, track_id)
 
    # Skip if the audio file doesn't exist (some FMA tracks are missing)
    if not os.path.isfile(src_path):
        skipped_files.append((track_id, "file not found"))
        continue
 
    # Load + resample
    y, sr = load_and_resample(src_path, SR_OUT)
    if y is None:
        skipped_files.append((track_id, "load error"))
        continue
 
    # Sanitize genre name for use as a directory name
    safe_genre = genre.replace("/", "-").replace(" ", "_")
 
    # Build output path: Data/genres_original/<genre>/<track_id>.wav
    genre_dir  = os.path.join(OUTPUT_DIR, safe_genre)
    os.makedirs(genre_dir, exist_ok=True)
 
    out_name = f"{track_id:06d}.wav"
    out_path = os.path.join(genre_dir, out_name)
 
    sf.write(out_path, y, sr)
 
# ----- SUMMARY -----
total   = len(genre_series)
written = total - len(skipped_files)
print(f"\nDone! {written}/{total} tracks written to {OUTPUT_DIR}")
 
if skipped_files:
    print(f"\nSkipped {len(skipped_files)} tracks:")
    for tid, reason in skipped_files:
        print(f"  track {tid:06d} — {reason}")
 
print(
    "\nYou can now run the rest of the pipeline in order:\n"
    "  python 1_distribute_dataset.py\n"
    "  python 2_segment_dataset.py\n"
    "  python 3_wav_to_spectrogram.py\n"
)
 
