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
from shared.audio_utils import make_spectrogram
from visualizations.config import SPECTROGRAM_IMG_SIZE, SPECTROGRAM_N_FFT, SPECTROGRAM_HOP_LEN, SPECTROGRAM_N_MELS


def generate_spectrogram(y, sr, output_path):
    """
    Generate mel spectrogram graph of audio file at given path.
    This visualization is tailored for human viewing, not CNN input.
    Args:
        filepath (PosixPath): path of audio file
        output_dir (PosixPath): path of directory to save graph into
    Returns:
        output_filename (str): name of created graph
    Side Effects:
        Graph saved to disk at output_path
    """
    mel_spectrogram = make_spectrogram(y, sr, SPECTROGRAM_N_FFT, SPECTROGRAM_HOP_LEN, SPECTROGRAM_N_MELS)

    # Plot graph
    fig, ax = plt.subplots()
    img = librosa.display.specshow(
        mel_spectrogram , 
        y_axis='mel',
        x_axis='time',
        ax=ax,
        fmax=8000,
        sr=sr,
        n_fft=SPECTROGRAM_N_FFT,
        hop_length=SPECTROGRAM_HOP_LEN
    )
    ax.set_title('Mel Spectrogram')
    fig.colorbar(img, ax=ax, format='%+2.0f dB')

    fig.savefig(output_path)
    plt.close(fig)
