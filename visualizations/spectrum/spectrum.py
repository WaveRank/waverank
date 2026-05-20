"""
Utility for generating a FFT-based audio spectrum visualization.
This visualization is tailored for human viewing, not CNN input.

Citation (5/14):
https://medium.com/analytics-vidhya/understanding-the-mel-spectrogram-fca2afa2ce53
"""
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from shared.audio_utils import load_audio
from visualizations.config import GRAPH_COLOR


def generate_spectrum(filepath, output_dir):
    """
    Generate a spectrum graph of the audio file at the given path.
    Args:
        filepath (PosixPath): path of audio file
        output_dir (PosixPath): path of directory to save graph into
    Returns:
        output_filename (str): name of created graph
    Side Effects:
        Graph saved to disk at output_path
    """
    output_filename = filepath.stem + "_spectrum.png"
    output_path = output_dir / output_filename

    y, _ = load_audio(filepath)
    
    # compute spectrum
    windowed = y * np.hanning(len(y))
    spectrum = np.abs(np.fft.rfft(windowed))

    # plot graph
    plt.figure()
    plt.clf()
    plt.plot(spectrum, color=GRAPH_COLOR)
    plt.title('Spectrum')
    plt.xlabel('Frequency Bin')
    plt.ylabel('Amplitude')

    plt.savefig(output_path)
    plt.close()

    return output_filename
