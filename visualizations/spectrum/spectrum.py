"""
Utility for generating a FFT-based audio spectrum visualization.
This visualization is tailored for human viewing, not CNN input.

Citation (5/14):
https://medium.com/analytics-vidhya/understanding-the-mel-spectrogram-fca2afa2ce53
"""
import matplotlib.pyplot as plt
import numpy as np
from visualizations.config import GRAPH_COLOR


def generate_spectrum(y, output_path):
    """
    Generate a spectrum graph of the given audio time series.
    Args:
        y (np.ndarray): audio time series
        output_dir (Path): path of directory to save graph into
    Side Effects:
        Graph saved to disk at output_path
    """
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
