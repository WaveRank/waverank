"""
Generate and save ROC (Receiver Operator Characteristic) curves and AUC (area
under curve) for all genres and the currently trained model. Uses CSV of model
predictions.

Expected CSV layout:
- one column per genre (class), with header as genre name
- one row per song, each cell containing confidence value for that genre/song
- label (int): true class index

Axes are:
- fpr: False positive rates for each possible threshold
- tpr: True positive rates for each possible threshold

Uses GENRE_NAMES to label curves, outputs a PNG image with ROC and AUC for each
genre.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
from sklearn import (
    preprocessing,
    metrics,
)

CONFIDENCES_PATH = "../../confidences.csv"
OUTPUT_PATH = "roc_auc.png"

# Order of genre names must match CNN model
GENRE_NAMES = [
    "blues",
    "classical",
    "country",
    "disco",
    "hiphop",
    "jazz",
    "metal",
    "pop",
    "reggae",
    "rock",
]


def generate_roc_auc():
    """
    Load prediction confidences from CSV and generate labeled ROC/AUC curves
    per genre.

    Side effects:
    - Reads from CONFIDENCES_PATH
    - Writes image to OUTPUT_PATH
    """

    # Read CSV into pandas dataframe
    df = pd.read_csv(CONFIDENCES_PATH)
    label = df["label"].values

    # Binarize genre labels for one vs all
    bin_labels = preprocessing.label_binarize(
        label, classes=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    )

    # Build ROC/AUC subplots for each genre
    plt.figure(figsize=(15, 7))
    plt.suptitle("WaveRank ROC Curves by Genre", fontsize=20)
    for genre in range(10):
        true_binary = bin_labels[:, genre]
        scores = df[GENRE_NAMES[genre]]
        (fpr, tpr, thresholds) = metrics.roc_curve(true_binary, scores)
        auc_score = metrics.roc_auc_score(true_binary, scores)

        ax = plt.subplot(2, 5, genre + 1)
        plt.plot(fpr, tpr)
        plt.axline( (0,0),slope=1,linestyle="--",color="silver")
        ax.set_xlim(-0.05, 1.05)
        ax.set_ylim(-0.05, 1.05)
        ax.set_box_aspect(1)
        ax.xaxis.set_major_locator(tck.MultipleLocator(0.5))
        ax.yaxis.set_major_locator(tck.MultipleLocator(0.5))
        plt.xlabel("FPR")
        plt.ylabel("TPR")
        plt.title(f"{GENRE_NAMES[genre]}; AUC={auc_score:.2f}")

    plt.tight_layout(pad=1.5, h_pad=1.5)
    plt.savefig(OUTPUT_PATH, dpi=300)


if __name__ == "__main__":
    generate_roc_auc()
