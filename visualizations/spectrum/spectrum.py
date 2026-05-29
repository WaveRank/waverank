"""
Utility for generating a FFT-based audio spectrum visualization.
This visualization is tailored for human viewing, not CNN input.

Citation (5/14):
https://medium.com/analytics-vidhya/understanding-the-mel-spectrogram-fca2afa2ce53
"""
import matplotlib.pyplot as plt
import numpy as np
from visualizations.config import GRAPH_COLOR_FS


# Styling
FIG_SIZE = (12, 6.75)
TEXT_COLOR = "white"
TICK_FONT = "DejaVu Sans"
SPECTRUM_MARGINS = dict(left=0.16, right=0.95, top=0.90, bottom=0.20)
plt.rcParams["axes.unicode_minus"] = False


def style_axes(ax):
    ax.tick_params(colors=TEXT_COLOR, labelsize=14, length=6, width=1.1)

    for spine in ax.spines.values():
        spine.set_edgecolor("white")
        spine.set_linewidth(1)

    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontfamily(TICK_FONT)


def finalize(fig, ax, margins):
    fig.patch.set_alpha(0)
    ax.set_facecolor((0, 0, 0, 0))
    fig.subplots_adjust(**margins)


# Main functions
def generate_spectrum(y, sr, output_path):
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

    # FFT
    fft = np.fft.rfft(windowed)
    magnitude = np.abs(fft)

    # X-axis in frequency (Hz)
    freqs = np.fft.rfftfreq(len(y), d=1 / sr)

    # Plot graph
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    ax.plot(freqs, magnitude, color=GRAPH_COLOR_FS, linewidth=1)
    ax.set_xscale("log")
    ax.set_xlabel("Frequency (Hz)", color=TEXT_COLOR, fontsize=20, labelpad=18)
    ax.set_ylabel("Magnitude", color=TEXT_COLOR, fontsize=20, labelpad=18)

    style_axes(ax)
    finalize(fig, ax, SPECTRUM_MARGINS)

    fig.savefig(output_path, dpi=300, transparent=True)
    plt.close(fig)
