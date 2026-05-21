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
    
    # Compute spectrum
    windowed = y * np.hanning(len(y))
    spectrum = np.abs(np.fft.rfft(windowed))

    # Plot graph
    fig, ax = plt.subplots()
    ax.plot(spectrum, color=GRAPH_COLOR)
    ax.set_title('Spectrum')
    ax.set_xlabel('Frequency Bin')
    ax.set_ylabel('Amplitude')

    fig.savefig(output_path)
    plt.close(fig)

    return output_filename
