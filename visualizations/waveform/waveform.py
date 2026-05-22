"""
Utilities for generating an audio signal waveform visualization.
This visualization is tailored for human viewing, not CNN input.

Citation (5/14):
https://medium.com/analytics-vidhya/understanding-the-mel-spectrogram-fca2afa2ce53
"""
import matplotlib.pyplot as plt
import numpy as np
from visualizations.config import GRAPH_COLOR, WAVEFORM_DOWNSAMPLE_FACTOR

def downsample_waveform(y, factor):
    """
    Reduce number of samples of a given waveform.
    """
    return y[::factor]


def generate_waveform(y, output_path):
    """
    Generate a waveform graph of the given audio time series.
    Args:
        y (np.ndarray): audio time series
        output_dir (Path): path of directory to save graph into
    Side Effects:
        Graph saved to disk at output_path
    """
    # Reduce number of samples (too many looks like a filled rectangle)
    y = downsample_waveform(y, WAVEFORM_DOWNSAMPLE_FACTOR)

    # Set graph amplitude scale as -1 to 1
    peak = np.max(np.abs(y))
    if peak > 0:
        y = y / peak

    # Plot graph
    fig, ax = plt.subplots()
    ax.plot(y, color=GRAPH_COLOR)
    ax.set_title('Waveform')
    ax.set_xlabel('Time (samples)')
    ax.set_ylabel('Amplitude')

    fig.savefig(output_path)
    plt.close(fig)
