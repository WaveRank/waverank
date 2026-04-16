"""
Generate and save a top k accuracy visualization using confidences.csv
from CNN model predictions.

Expected CSV columns:
- label (int): true class index 
- confidence genre predictions per song

Uses GENRE_NAMES to grab probability values per genre.
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

CONFIDENCES_PATH = "../../confidences.csv"
OUTPUT_PATH = "top_k.png"

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
    "rock"
]


def top_k_acc(k, labels, confidences):
    """
    Uses k values, labels, and probability values to sort confidence values as
    indices and returns the mean of correct genre predictions.
    """

    total_labels = len(labels)
    top_k_pred = np.argsort(confidences, axis=1)[:, -k:]
    accuracy = np.mean([labels[i] in top_k_pred[i] for i in range(total_labels)])

    return accuracy


def generate_topk():
    """
    Loads the confidences CSV and generates a top k accuracy
    visualization.

    Side effects:
    - Reads from CONFIDENCES_PATH
    - Writes image to OUTPUT_PATH
    """

    # Read the CSV file
    df = pd.read_csv(CONFIDENCES_PATH)

    # Generates the label values and confidences values per song
    labels = df['label'].values
    confidences = df[GENRE_NAMES].values

    k_val = [1, 2, 3, 5, 10]

    # Generate the prediction scores for each k value
    scores = [top_k_acc(k, labels, confidences) for k in k_val]

    plt.figure()
    plt.plot(k_val, scores, marker='o')
    plt.title("Top-k Accuracy")
    plt.xlabel("k-Values")
    plt.ylabel("Accuracy")
    plt.xticks(k_val)
    plt.yticks(np.arange(0.6, 1.02, 0.02))
    plt.savefig(OUTPUT_PATH)


if __name__ == "__main__":
    generate_topk()