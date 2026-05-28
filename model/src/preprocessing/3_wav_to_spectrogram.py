"""
Converts .wav files to magma colormapped spectrograms.
Assumes that dataset has already been split into training/validation/testing sets.

Citations (4/9/26): 
https://librosa.org/doc/main/generated/librosa.feature.melspectrogram.html
https://medium.com/analytics-vidhya/understanding-the-mel-spectrogram-fca2afa2ce53
"""

# ----- IMPORTS -----
from pathlib import Path
from model.src.audio.audio_utils import load_audio, make_spectrogram, spectrogram_to_image
from shared.paths import DATA_DIR, DATASET_DIR

# ----- CONFIGURATION -----
INPUT_DIR = DATA_DIR / "segmented_dataset"
OUTPUT_DIR = DATASET_DIR

# ----- MAIN PIPELINE -----
OUTPUT_DIR.mkdir(exist_ok=True)
for split_path in INPUT_DIR.iterdir():
    for genre_in in split_path.iterdir():
        genre_out = OUTPUT_DIR / split_path.name / genre_in.name
        genre_out.mkdir(parents=True, exist_ok=True)

        # Get all .wav files in this genre folder
        wav_files = []
        for file in genre_in.iterdir():
            if file.suffix.lower() == ".wav":
                wav_files.append(file)

        # Process each .wav file
        for wav_file in wav_files:

            # Load audio
            y, sr = load_audio(wav_file)
            if y is None:
                print(f"Skipping {wav_file.name}: failed to load")
                continue

            # Extract spectrogram and convert to image
            mel_db = make_spectrogram(y, sr)
            img = spectrogram_to_image(mel_db)

            # Save output image
            output_path = genre_out / f"{wav_file.stem}.png"
            img.save(output_path)

# ----- SUMMARY -----
print("\nAll spectrograms generated successfully! :)\n")
