"""
Generate and save a top k accuracy visualization using confidences.csv
from CNN model predictions.

Expected CSV columns:
- label (int): true class index 
- confidence genre predictions per song

Uses CLASS_NAMES_PATH to extract genre_names that grab 
probability values per genre.
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json


CONFIDENCES_PATH = "../../confidences.csv"
CLASS_NAMES_PATH = "../../class_names.json"
OUTPUT_PATH = "top_k.png"


def top_k_acc(k, labels, confidences):
    """
    Uses k values, labels, and probability values to sort confidence values as
    indices and returns the mean of correct genre predictions.
    """

    total_labels = len(labels)
    top_k_pred = np.argsort(confidences, axis=1)[:, -k:]
    accuracy = np.mean([labels[i] in top_k_pred[i] for i in range(total_labels)])

    return accuracy


def generate_topk(conf_path, class_names_path, output_path):
    """
    Loads the confidences CSV and generates a top k accuracy
    visualization.

    Side effects:
    - Reads from CONFIDENCES_PATH
    - Writes image to OUTPUT_PATH
    """

    # Get the genre names
    with open(class_names_path) as f:
        genre_names = json.load(f)

    # Read the CSV file
    df = pd.read_csv(conf_path)

    # Generates the label values and confidences values per song
    labels = df['label'].values
    confidences = df[genre_names].values

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
    plt.savefig(output_path)


if __name__ == "__main__":
    generate_topk(
        conf_path=CONFIDENCES_PATH,
        class_names_path=CLASS_NAMES_PATH,
        output_path=OUTPUT_PATH
    )