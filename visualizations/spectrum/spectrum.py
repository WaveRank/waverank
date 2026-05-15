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


def generate_spectrum(filepath):
    base_name = get_basename(filepath)
    filename = base_name + "_spectrum.png"
    output_path = os.path.join(GRAPH_DIR, filename)

    y, _ = load_audio(filepath)

    # compute spectrum
    n_fft = 2048
    frame = y[:n_fft]
    windowed = frame * np.hanning(len(frame))
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

    return filename
