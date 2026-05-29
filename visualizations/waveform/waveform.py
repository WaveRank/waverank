"""
Utilities for generating an audio signal waveform visualization.
This visualization is tailored for human viewing, not CNN input.

Citation (5/14):
https://medium.com/analytics-vidhya/understanding-the-mel-spectrogram-fca2afa2ce53
"""
import matplotlib.pyplot as plt
import numpy as np
from visualizations.config import GRAPH_COLOR_WF, WAVEFORM_DOWNSAMPLE_FACTOR


# Styling
FIG_SIZE = (12, 6.75)
TEXT_COLOR = "white"
TICK_FONT = "DejaVu Sans"
COMMON_MARGINS = dict(left=0.12, right=0.95, top=0.90, bottom=0.20)
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
def downsample_waveform(y, factor):
    """
    Reduce number of samples of a given waveform.
    """
    return y[::factor]


def generate_waveform(y, sr, output_path):
    """
    Generate a waveform graph of the given audio time series.
    Args:
        y (np.ndarray): audio time series
        output_dir (Path): path of directory to save graph into
    Side Effects:
        Graph saved to disk at output_path
    """
    # Reduce number of samples (too many looks like a filled rectangle)
    y_ds = downsample_waveform(y, WAVEFORM_DOWNSAMPLE_FACTOR)

    # Set graph amplitude scale as -1 to 1
    peak = np.max(np.abs(y_ds))
    if peak > 0:
        y_ds = y_ds / peak

    # X-axis in seconds
    duration = len(y) / sr
    time = np.linspace(0, duration, len(y_ds))

    # Plot graph
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    ax.plot(time, y_ds, color=GRAPH_COLOR_WF, linewidth=1)
    ax.set_xlabel("Time (seconds)", color=TEXT_COLOR, fontsize=20, labelpad=18)
    ax.set_ylabel("Amplitude", color=TEXT_COLOR, fontsize=20, labelpad=18)

    style_axes(ax)
    finalize(fig, ax, COMMON_MARGINS)

    fig.savefig(output_path, dpi=300, transparent=True)
    plt.close(fig)
