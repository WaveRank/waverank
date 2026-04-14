"""
Generate and save ROC (Receiver Operator Characteristic) curves and AUC (area under curve) for all genres and the currently trained model. Uses CSV of model predictions.

Expected CSV columns:
- label (int): true class index

Axes are:
- fpr: False positive rates for each possible threshold
- tpr: True positive rates for each possible threshold

Uses GENRE_NAMES to label curves, outputs a PNG image.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing, metrics

CONFIDENCES_PATH = "../../confidences.csv"
OUTPUT_PATH = "roc_auc.png"

# Order of genre names must match CNN model
GENRE_NAMES = ["blues", "classical", "country", "disco", "hiphop", "jazz", "metal", "pop", "reggae", "rock"]


def generate_roc_auc():
    """ docstring goes here later lol """

    # Read CSV into pandas dataframe
    df = pd.read_csv(CONFIDENCES_PATH)
    label = df["label"].values

    # Binarize genre labels for 1 vs all fashion
    bin_labels = preprocessing.label_binarize(label, classes=[0,1, 2, 3, 4, 5, 6, 7, 8, 9])
    
    # Loop through each genre by index
    for genre in range(10):

        # Pull binarized labels for all songs for this genre
        true_binary = bin_labels[:, genre]

        # Pull confidence data for all songs for this genre
        scores = df[GENRE_NAMES[genre]]

        # Build ROC curve and AUC for this genre
        fpr, tpr, thresholds = metrics.roc_curve(true_binary, scores)
        auc_score = metrics.roc_auc_score(true_binary, scores)

        # Plot each genre AOC as subplot

        plt.subplot(2, 5, genre+1)
        plt.plot(fpr, tpr)
        plt.xlabel("FPR")
        plt.ylabel("TPR")
        plt.title(f"{GENRE_NAMES[genre]}; AUC ={auc_score:.2f}")

    plt.tight_layout()
    plt.savefig(OUTPUT_PATH)

if __name__ == "__main__":
    generate_roc_auc()