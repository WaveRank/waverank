"""
Shared audio utilities for the dataset processing and inference pipeline.

Usage: "from shared.audio_utils import SR, segment_audio, spectrogram_to_image"
    - Import what is needed in your script with the above format
"""

# ----- IMPORTS -----
import librosa
import numpy as np
import matplotlib.cm as cm
from PIL import Image

# ----- CONFIGURATION -----
IMG_SIZE = (224, 224)   # image size for spectrograms fed into model
SR = 22050              # sampling rate of y (audio-time series)
N_FFT = 2048            # length of fft window
HOP_LENGTH = 512        # num of samples between successive frames
N_MELS = 128            # num of mel bands to generate
SEGMENT_SEC = 10        # length of audio segment (seconds)
HOP_SEC = 5             # hop length between each audio segment (can overlap)


# ----- HELPER FUNCTIONS -----
def load_audio(path):
    """
    Load an audio file using librosa.
    Args:
        path (str): path to audio file
    Returns:
        tuple: (y, sr) audio time series and sample rate, or (None, None) on failure
    """
    try:
        return librosa.load(path, sr=SR, mono=True)
    except Exception:
        return None, None


def segment_audio(y, sr):
    """
    Segment audio into fixed-length overlapping chunks.
    Ignores final partial segment to avoid silence-padded audio.
    Args:
        y (np.ndarray): audio time series
        sr (int): sample rate
    Returns:
        list: list of audio segments as np.ndarray, or empty list if audio is too short
    """
    segment_len = SEGMENT_SEC * sr
    hop_len = HOP_SEC * sr
    num_segments = len(range(0, len(y) - segment_len + 1, hop_len))
    segments = []
    for i in range(num_segments):
        start = i * hop_len
        end = start + segment_len
        segments.append(y[start:end])
    return segments


def make_spectrogram(segment, sr):
    """
    Convert an audio segment into a log-mel spectrogram.
    Args:
        segment (np.ndarray): audio time series
        sr (int): sample rate
    Returns:
        np.ndarray: log-mel spectrogram in dB scale
    """
    mel = librosa.feature.melspectrogram(
        y=segment,
        sr=sr,
        n_fft=N_FFT,
        hop_length=HOP_LENGTH,
        n_mels=N_MELS
    )
    return librosa.power_to_db(mel, ref=np.max)


def spectrogram_to_image(mel):
    """
    Normalize a log-mel spectrogram and convert to a PIL Image using the magma 
    colormap.
    Args:
        mel (np.ndarray): log-mel spectrogram in dB scale
    Returns:
        PIL.Image: RGB image resized to IMG_SIZE
    """
    mel = np.clip(mel, -80, 0)
    mel = (mel + 80) / 80
    colored = cm.magma(mel)  # returns RGBA
    img = (colored[:, :, :3] * 255).astype(np.uint8)  # drop alpha, keep RGB
    return Image.fromarray(img, mode="RGB").resize(IMG_SIZE)
