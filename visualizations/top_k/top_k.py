"""
Generate and save a top k accuracy visualization using confidences.csv
from CNN model predictions.

Expected CSV columns:
- label (int): true class index 
- confidence genre predictions per song

Uses CLASS_NAMES_PATH to extract genre_names that grab 
probability values per genre.

Citations:
https://scikit-learn.org/stable/modules/generated/sklearn.metrics.top_k_accuracy_score.html
"""

# ----- IMPORTS -----
from pathlib import Path
from sklearn.metrics import top_k_accuracy_score
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json


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

    k_val = [1, 2, 3, 5, 7, 9]

    # Generate the prediction scores for each k value
    scores = [top_k_accuracy_score(labels, confidences, k=k) for k in k_val]

    plt.figure()
    plt.plot(k_val, scores, marker='o')
    plt.title("Top-k Accuracy")
    plt.xlabel("k-Values")
    plt.ylabel("Accuracy")
    plt.xticks(k_val)
    plt.yticks(np.arange(0.6, 1.02, 0.02))
    plt.savefig(output_path / "top-k.png")
    plt.close()


if __name__ == "__main__":
    generate_topk()