"""
Utility for generating a mel spectrogram visualization.
Uses shared CNN preprocessing function with different parameters to generate 
a spectrogram image tailored for human viewing, and embeds it in a pyplot 
figure with labels.
This visualization is tailored for human viewing, not CNN input.

Citation (5/14):
https://medium.com/analytics-vidhya/understanding-the-mel-spectrogram-fca2afa2ce53
"""
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import librosa
import librosa.display
from shared.audio_utils import load_audio, make_spectrogram, spectrogram_to_image
from visualizations.config import SPECTROGRAM_IMG_SIZE, SPECTROGRAM_N_FFT, SPECTROGRAM_HOP_LEN, SPECTROGRAM_N_MELS


def generate_spectrogram(filepath, output_dir):
    """
    Generate mel spectrogram graph of audio file at given path.
    This visualization is tailored for human viewing, not CNN input.
    Args:
        filepath (PosixPath): path of audio file
        output_dir (PosixPath): path of directory to save graph into
    Returns:
        output_filename (str): name of created graph
    Side Effects:
        Graph saved to disk at output_path
    """
    output_filename = filepath.stem + "_spectrogram.png"
    output_path = output_dir / output_filename
    
    y, sr = load_audio(filepath)

    mel_spect = make_spectrogram(y, sr, SPECTROGRAM_N_FFT, SPECTROGRAM_HOP_LEN, SPECTROGRAM_N_MELS)

    plt.figure()
    librosa.display.specshow(
        mel_spect, 
        y_axis='mel',
        x_axis='time',
        fmax=8000,
        sr=sr,
        n_fft=SPECTROGRAM_N_FFT,
        hop_length=SPECTROGRAM_HOP_LEN
    )
    plt.title('Mel Spectrogram')
    plt.colorbar(format='%+2.0f dB')

    plt.savefig(output_path)
    plt.close()

    return output_filename
