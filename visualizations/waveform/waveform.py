"""
Citation (5/14):
https://medium.com/analytics-vidhya/understanding-the-mel-spectrogram-fca2afa2ce53
"""
import os
import matplotlib.pyplot as plt
import numpy as np
from shared.audio_utils import load_audio
from webapp.server.config import GRAPH_DIR, GRAPH_COLOR
from webapp.server.services.file_io import get_basename

# Reduce number of samples for better visual representation
def downsample_waveform(y, factor=1000):
    return y[::factor]

# Generate waveform graph of audio file at given path, save to disk and return output path.
# This visualization is tailored for human viewing, not CCN input.
def generate_waveform(filepath):
    base_name = get_basename(filepath)
    filename = base_name + "_waveform.png"
    output_path = os.path.join(GRAPH_DIR, filename)

    y, _ = load_audio(filepath)

    y = downsample_waveform(y)

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

    return filename
