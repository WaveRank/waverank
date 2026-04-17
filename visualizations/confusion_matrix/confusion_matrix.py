"""
Generate and save a confusion matrix from a CSV of model predictions.

Expected CSV columns:
- label (int): true class index
- pred (int): predicted class index

Uses GENRE_NAMES to label axes, outputs a PNG image.
"""
import os
import pandas as pd
import json
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay


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
    ax.set_title("Confusion Matrix")

    ConfusionMatrixDisplay.from_predictions(
        y_true=y_true, 
        y_pred=y_pred, 
        display_labels=genre_names, 
        ax=ax
    )
    
    plt.setp(ax.get_xticklabels(), rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, f"confusion_matrix.png"))
    plt.close(fig)
    
    
# Runnable with default paths
if __name__ == "__main__":
    generate_confusion_matrix()
