"""
Converts .wav files to magma colormapped spectrograms.
Assumes that dataset has already been split into training/validation/testing sets.

Citations (4/9/26): 
https://librosa.org/doc/main/generated/librosa.feature.melspectrogram.html
https://medium.com/analytics-vidhya/understanding-the-mel-spectrogram-fca2afa2ce53
"""

# ----- IMPORTS -----
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from shared.audio_utils import load_audio, make_spectrogram, spectrogram_to_image

# ----- CONFIGURATION -----
BASE_PATH = "./"
INPUT_DIR = os.path.join(BASE_PATH, "Data/segmented_dataset")
OUTPUT_DIR = os.path.join(BASE_PATH, "dataset")

# ----- MAIN PIPELINE -----
os.makedirs(OUTPUT_DIR, exist_ok=True)

for split_name in os.listdir(INPUT_DIR):
    split_path = os.path.join(INPUT_DIR, split_name)

    for genre in os.listdir(split_path):
        genre_in = os.path.join(split_path, genre)
        genre_out = os.path.join(OUTPUT_DIR, split_name, genre)
        os.makedirs(genre_out, exist_ok=True)

        # Get all .wav files in this genre folder
        wav_files = []
        for file in os.listdir(genre_in):
            if file.lower().endswith(".wav"):
                wav_files.append(file)

        for wav_file in wav_files:

            # Load audio
            wav_path = os.path.join(genre_in, wav_file)
            y, sr = load_audio(wav_path)
            if y is None:
                print(f"Skipping {wav_file}: failed to load")
                continue

            # Extract spectrogram and convert to image
            mel_db = make_spectrogram(y, sr)
            img = spectrogram_to_image(mel_db)

            # Save output image
            output_name = os.path.splitext(wav_file)[0] + ".png"
            output_path = os.path.join(genre_out, output_name)
            img.save(output_path)

# ----- SUMMARY -----
print("\nAll spectrograms generated successfully! :)\n")
