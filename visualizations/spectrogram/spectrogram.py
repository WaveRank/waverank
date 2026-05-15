"""
Citation (5/14):
https://medium.com/analytics-vidhya/understanding-the-mel-spectrogram-fca2afa2ce53
"""
import sys
import os
import matplotlib.pyplot as plt
import numpy as np
from shared.audio_utils import load_audio, make_spectrogram, spectrogram_to_image
from webapp.server.config import GRAPH_DIR, IMG_SIZE, N_FFT, HOP_LENGTH, N_MELS
from webapp.server.services.file_io import get_basename


def generate_spectrogram(filepath):
    base_name = get_basename(filepath)
    filename = base_name + "_spectrogram.png"
    output_path = os.path.join(GRAPH_DIR, filename)

    waveform, sr = load_audio(filepath)
    spectrogram = make_spectrogram(waveform, sr, N_FFT, HOP_LENGTH, N_MELS)
    spectrogram_graph = spectrogram_to_image(spectrogram, IMG_SIZE)

    spectrogram_graph.save(output_path)

    return filename
