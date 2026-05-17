"""
Citation (5/14):
https://medium.com/analytics-vidhya/understanding-the-mel-spectrogram-fca2afa2ce53
"""
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from shared.audio_utils import load_audio
from visualizations.config import GRAPH_COLOR

# Reduce number of samples
def downsample_waveform(y, factor=1000):
    return y[::factor]

# Generate waveform graph of audio file at given path, save to disk, and return filename.
# This visualization is tailored for human viewing, not CCN input.
def generate_waveform(filepath, output_dir):
    output_filename = filepath.stem + "_waveform.png"
    output_path = output_dir / output_filename

    y, _ = load_audio(filepath)
    
    # Reduce number of samples (too many looks like a filled rectangle)
    y = downsample_waveform(y)

    # Set graph amplitude scale as -1 to 1
    peak = np.max(np.abs(y))
    if peak > 0:
        y = y / peak

    # plot graph
    plt.figure()
    plt.plot(y, color=GRAPH_COLOR)
    plt.title('Waveform')
    plt.xlabel('Time (samples)')
    plt.ylabel('Amplitude')

    plt.savefig(output_path)
    plt.close()

    return output_filename
