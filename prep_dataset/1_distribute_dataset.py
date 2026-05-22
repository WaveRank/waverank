"""
Splits the GTZAN dataset into training, validation, and testing sets.
"""

# ----- IMPORTS -----
import os
import shutil

# ----- CONFIGURATION -----
BASE_PATH = "./"
INPUT_DIR = os.path.join(BASE_PATH, "Data/genres_original")
OUTPUT_DIR = os.path.join(BASE_PATH, "Data/distributed_dataset")

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
for genre in os.listdir(INPUT_DIR):
    # Get all .wav files, then split them into train/val/test
    genre_path = os.path.join(INPUT_DIR, genre)
    files = [file for file in os.listdir(genre_path) if file.endswith(".wav")]
    files.sort() 
    split = split_files(files)

    # Create corresponding output folders and copy files
    for split_name, split_files_list in split.items():
        out_dir = os.path.join(OUTPUT_DIR, split_name, genre)
        os.makedirs(out_dir, exist_ok=True)

        # Copy each file into new location
        for file in split_files_list:
            src = os.path.join(genre_path, file)
            dst = os.path.join(out_dir, file)
            shutil.copy2(src, dst)

# ----- SUMMARY -----
print("\nAll WAV files sorted into train/val/test successfully! :)\n")