"""
Converts .wav files to grayscale spectrograms.
Assumes that dataset has already been split into training/validation/testing sets.

Citations (4/9/26): 
https://librosa.org/doc/main/generated/librosa.feature.melspectrogram.html
https://medium.com/analytics-vidhya/understanding-the-mel-spectrogram-fca2afa2ce53
"""
import os
import librosa
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# ----- CONFIGURATION -----
BASE_PATH = "./"
INPUT_DIR = os.path.join(BASE_PATH, "Data/fma_med_segmented_dataset")
OUTPUT_DIR = os.path.join(BASE_PATH, "dataset")

IMG_SIZE = (224, 224)
SR = 22050              # sampling rate of y (audio-time series)
N_FFT = 2048            # length of fft window
HOP_LENGTH = 512        # num of samples between successive frames
N_MELS = 128            # num of mel bands to generate

# ----- HELPER FUNCTIONS -----
def extract_log_mel(y, sr):
    """Convert waveform into spectrogram."""
    mel = librosa.feature.melspectrogram(
        y=y,
        sr=sr,
        n_fft=N_FFT,
        hop_length=HOP_LENGTH,
        n_mels=N_MELS
    )
    return librosa.power_to_db(mel, ref=np.max)

def to_image(mel_db):
    """Convert spectrogram into image using colormap."""
    mel_db = np.clip(mel_db, -80, 0)
    mel_db = (mel_db + 80) / 80
    colored = plt.cm.magma(mel_db)  # returns RGBA
    img = (colored[:, :, :3] * 255).astype(np.uint8)  # drop alpha, keep RGB
    return Image.fromarray(img, mode="RGB")

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
            wav_path = os.path.join(genre_in, wav_file)

            # Load audio
            y, sr = librosa.load(wav_path, sr=SR, mono=True)

            # Extract spectrogram
            mel_db = extract_log_mel(y, sr)

            # Convert to image
            img = to_image(mel_db)
            img = img.resize(IMG_SIZE)

            # Save output image
            output_name = os.path.splitext(wav_file)[0] + ".png"
            output_path = os.path.join(genre_out, output_name)
            img.save(output_path)

# ----- SUMMARY -----
print("\nAll spectrograms generated successfully! :)\n")
