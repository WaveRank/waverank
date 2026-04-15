"""
Generate and save a confusion matrix from a CSV of model predictions.

Expected CSV columns:
- label (int): true class index
- pred (int): predicted class index

Uses GENRE_NAMES to label axes, outputs a PNG image.
"""
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay


PREDICTIONS_PATH = "../../embeddings.csv"
OUTPUT_PATH = "confusion_matrix.png"

# Order of genre names must match CNN model
GENRE_NAMES = ["blues", "classical", "country", "disco", "hiphop", "jazz", "metal", "pop", "reggae", "rock"]


def generate_confusion_matrix():
    """
    Load predictions from CSV and generate a labeled confusion matrix plot.

    Side effects:
    - Reads from PREDICTIONS_PATH
    - Writes image to OUTPUT_PATH
    """
    df = pd.read_csv(PREDICTIONS_PATH)

    label = df["label"].values
    pred = df["pred"].values

    # Plot confusion matrix
    fig, ax = plt.subplots()
    ConfusionMatrixDisplay.from_predictions(y_true=label, y_pred=pred, display_labels=GENRE_NAMES, ax=ax)
    ax.set_title("Confusion Matrix")
    plt.setp(ax.get_xticklabels(), rotation=45)
    fig.tight_layout()
    plt.savefig(OUTPUT_PATH)
    

if __name__ == "__main__":
    generate_confusion_matrix()
