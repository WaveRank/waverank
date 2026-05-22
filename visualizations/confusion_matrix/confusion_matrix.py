"""
Generate and save a confusion matrix from a CSV of model predictions.

Expected CSV columns:
- label (int): true class index
- pred (int): predicted class index

Uses GENRE_NAMES to label axes, outputs a PNG image.
"""

# ----- IMPORTS -----
from pathlib import Path
import pandas as pd
import json
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay


SCALING = 100

def generate_confusion_matrix(predictions_path, class_names_path, output_path):
    """
    Load predictions from CSV and generate a labeled confusion matrix plot.

    Side effects:
    - Reads from predictions_path and class_names_path
    - Writes image to output_path
    """

    # Read genre names
    with open(class_names_path) as f:
        genre_names = json.load(f)

    # Read true and predicted values
    pred_df = pd.read_csv(predictions_path)
    y_true = pred_df["label"].values
    y_pred = pred_df["pred"].values

    # Plot confusion matrix
    fig, ax = plt.subplots()

    cm = confusion_matrix(y_true, y_pred, normalize="true") * SCALING
    cm = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=genre_names, 
    ).plot(ax=ax, values_format=".0f")

    ax.set_title("Confusion Matrix")
    plt.setp(ax.get_xticklabels(), rotation=45)
    plt.tight_layout()
    plt.savefig(output_path / "confusion_matrix.png")
    plt.close(fig)


if __name__ == "__main__":
    generate_confusion_matrix()
