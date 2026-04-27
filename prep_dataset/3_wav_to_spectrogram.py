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
from PIL import Image

# ----- CONFIGURATION -----
BASE_PATH = "./"
INPUT_DIR = os.path.join(BASE_PATH, "Data/segmented_dataset")
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


def extract_features(y, sr):
    "Extract a handpicked selection of audio features from waveform"
    tempo, beat_locations = librosa.beat.beat_track(y=y, sr=sr)                 # 1 value
    centroid_mean = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))      # 1 value
    bandwidth_mean = np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr))    # 1 value
    zcr_mean = np.mean(librosa.feature.zero_crossing_rate(y))                   # 1 value
    rolloff_mean = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))        # 1 value
    contrast_mean = np.mean(librosa.feature.spectral_contrast(y=y, sr=sr), axis=1) # 7 values
    mfcc_mean = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13), axis=1)    # n_mfcc values
    chroma_mean = np.mean(librosa.feature.chroma_stft(y=y, sr=sr), axis=1)      # 12 values

    return np.hstack([
        tempo,
        # centroid_mean,  # worse
        # bandwidth_mean,  # worse
        # zcr_mean,       # better?
        # rolloff_mean,
        # contrast_mean,
        # mfcc_mean,
        # chroma_mean
    ])


# Calculate mean and std of features and save for normalization by model
def save_feat_mean_std(feat_paths):
    all_feats = []

    for path in feat_paths:
        features = np.load(path)
        all_feats.append(features)

    all_feats = np.vstack(all_feats)

    mean = all_feats.mean(axis=0)
    std = all_feats.std(axis=0) + 1e-8
    size = all_feats.shape
    print(size)

    np.save("feat_mean.npy", mean)
    np.save("feat_std.npy", std)


def to_image(mel_db):
    """Convert spectrogram into grayscale image."""
    mel_db = np.clip(mel_db, -80, 0)
    mel_db = (mel_db + 80) / 80
    img = (mel_db * 255).astype(np.uint8)
    return Image.fromarray(img, mode="L")


# ----- MAIN PIPELINE -----
os.makedirs(OUTPUT_DIR, exist_ok=True)

feat_paths = []

for split_name in os.listdir(INPUT_DIR):
    split_path = os.path.join(INPUT_DIR, split_name)

    for genre in os.listdir(split_path):
        genre_in = os.path.join(split_path, genre)
        genre_out = os.path.join(OUTPUT_DIR, split_name, genre)
        os.makedirs(genre_out, exist_ok=True)

        print(f"Generating {str(genre_in).replace(INPUT_DIR, '')[1:]} spectrograms")

        # Get all .wav files in this genre folder
        wav_files = []
        for file in os.listdir(genre_in):
            if file.lower().endswith(".wav"):
                wav_files.append(file)

        for wav_file in wav_files:
            wav_path = os.path.join(genre_in, wav_file)

            # Load audio
            y, sr = librosa.load(wav_path, sr=SR, mono=True)

            # Extract spectrogram and features
            mel_db = extract_log_mel(y, sr)
            features = extract_features(y, sr)

            # Convert to image
            img = to_image(mel_db)
            img = img.resize(IMG_SIZE)

            # Save output image
            output_name = os.path.splitext(wav_file)[0] + ".png"
            output_path = os.path.join(genre_out, output_name)
            img.save(output_path)

            # Save features array
            output_name = os.path.splitext(wav_file)[0] + ".npy"
            output_path = os.path.join(genre_out, output_name)
            np.save(output_path, features)
            feat_paths.append(output_path)


save_feat_mean_std(feat_paths)



# ----- SUMMARY -----
print("\nAll spectrograms generated successfully! :)\n")
