"""
Citation (5/14):
https://medium.com/analytics-vidhya/understanding-the-mel-spectrogram-fca2afa2ce53
"""
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from shared.audio_utils import load_audio
from visualizations.config import GRAPH_COLOR


# Generate spectrum graph of audio file at given path, save to disk, and return filename.
def generate_spectrum(filepath, output_dir):
    output_filename = filepath.stem + "_spectrum.png"
    output_path = output_dir / output_filename

    y, _ = load_audio(filepath)

    print(np.max(np.abs(y)))
    
    # compute spectrum
    n_fft = 2048
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
