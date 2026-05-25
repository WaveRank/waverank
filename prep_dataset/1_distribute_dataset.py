"""
Splits the GTZAN dataset into training, validation, and testing sets.
"""

# ----- IMPORTS -----
from pathlib import Path 
import shutil

# ----- CONFIGURATION -----
INPUT_DIR = Path("Data/genres_original")
OUTPUT_DIR = Path("Data/distributed_dataset")
SPLITS = {"train": 0.8, "val": 0.1, "test": 0.1}

# ----- HELPER FUNCTIONS -----
def split_files(files):
    """Splits a sorted list of files into sets."""
    # Calculate split indices
    n = len(files)
    train_end = int(n * SPLITS["train"])
    val_end = train_end + int(n * SPLITS["val"])

    # Return dictionary of split file lists
    return {
        "train": files[:train_end],
        "val": files[train_end:val_end],
        "test": files[val_end:]
    }

# ----- MAIN PIPELINE -----
for genre_path in INPUT_DIR.iterdir():
    # Get all .wav files, then split them into train/val/test
    files = sorted(f for f in genre_path.iterdir()
                   if f.suffix.lower() ==".wav")
    split = split_files(files)

    # Create corresponding output folders and copy files
    for split_name, split_files_list in split.items():
        out_dir = OUTPUT_DIR / split_name / genre_path.name
        out_dir.mkdir(parents=True, exist_ok=True)

        # Copy each file into new location
        for file in split_files_list:
            shutil.copy2(file, out_dir / file.name)

# ----- SUMMARY -----
print("\nAll WAV files sorted into train/val/test successfully! :)\n")