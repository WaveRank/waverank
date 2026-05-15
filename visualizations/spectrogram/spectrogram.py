"""
Citation (5/14):
https://medium.com/analytics-vidhya/understanding-the-mel-spectrogram-fca2afa2ce53
"""
import sys
import os
import matplotlib.pyplot as plt
import numpy as np
from shared.audio_utils import load_audio, make_spectrogram, spectrogram_to_image
from webapp.server.config import GRAPH_DIR
from webapp.server.services.file_io import get_basename


def generate_spectrogram(filepath):
    base_name = get_basename(filepath)
    output_name = base_name + "_spectrogram.png"
    output_path = os.path.join(GRAPH_DIR, output_name)

    waveform, sr = load_audio(filepath)
    spectrogram = make_spectrogram(waveform, sr)
    spectrogram_graph = spectrogram_to_image(spectrogram)

    spectrogram_graph.save(output_path)

    return output_path
