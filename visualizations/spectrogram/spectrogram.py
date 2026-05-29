"""
Utility for generating a mel spectrogram visualization.
Uses shared CNN preprocessing function with different parameters to generate 
a spectrogram image tailored for human viewing, and embeds it in a pyplot 
figure with labels.
This visualization is tailored for human viewing, not CNN input.

Citation (5/14):
https://medium.com/analytics-vidhya/understanding-the-mel-spectrogram-fca2afa2ce53
"""
import matplotlib.pyplot as plt
import librosa.display
import numpy as np
from model.src.audio.audio_utils import make_spectrogram
from visualizations.config import SPECTROGRAM_IMG_SIZE, SPECTROGRAM_N_FFT, SPECTROGRAM_HOP_LEN, SPECTROGRAM_N_MELS


# Styling
FIG_SIZE = (12, 15)
TEXT_COLOR = "white"
TICK_FONT = "DejaVu Sans"
plt.rcParams["axes.unicode_minus"] = False


def style_axes(ax):
    ax.tick_params(colors=TEXT_COLOR, labelsize=14, length=6, width=1.1)

    for spine in ax.spines.values():
        spine.set_edgecolor("white")
        spine.set_linewidth(1)

    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontfamily(TICK_FONT)

    
def generate_spectrogram(y, sr, output_path):
    """
    Generate a mel spectrogram graph of the given audio time series.
    This visualization is tailored for human viewing, not CNN input.
    Args:
        y (np.ndarray): audio time series
        sr (int): sample rate
        output_dir (Path): path of directory to save graph into
    Side Effects:
        Graph saved to disk at output_path
    """
    mel_spectrogram = make_spectrogram(y, sr, SPECTROGRAM_N_FFT, SPECTROGRAM_HOP_LEN, SPECTROGRAM_N_MELS)

    # Plot graph
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    img = librosa.display.specshow(
        mel_spectrogram,
        sr=sr,
        hop_length=SPECTROGRAM_HOP_LEN,
        x_axis="time",
        y_axis="mel",
        fmax=8000,
        cmap="magma",
        ax=ax
    )

    # Axis labeks
    ax.set_xlabel("Time (frames)", color=TEXT_COLOR, fontsize=22, labelpad=18)
    ax.set_ylabel( "Frequency (Mel bins)", color=TEXT_COLOR, fontsize=22, labelpad=18)
    style_axes(ax)

    # Colorbar
    cbar = plt.colorbar(img, ax=ax, pad=0.02, fraction=0.035, aspect=40)
    cbar.ax.tick_params(colors=TEXT_COLOR, labelsize=12)
    for label in cbar.ax.get_yticklabels():
        label.set_fontfamily(TICK_FONT)
    cbar.set_ticks([-80, -60, -40, -20, 0])
    cbar.set_ticklabels(["-80 dB", "-60 dB", "-40 dB", "-20 dB", "0 dB"])

    # Final layout
    fig.patch.set_alpha(0)
    ax.set_facecolor((0, 0, 0, 0))
    fig.subplots_adjust(left=0.10, right=0.86, top=0.96, bottom=0.10)

    fig.savefig(output_path, dpi=300, transparent=True)
    plt.close(fig)
