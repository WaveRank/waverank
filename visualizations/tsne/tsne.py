"""
Loads embeddings from CSV and generates t-SNE visualization plots for
genre, prediction accuracy, and confidence.

Citations (4/15/26):
https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.legend.html
https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html
https://www.datacamp.com/tutorial/introduction-t-sne
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import json

# ----- CONFIGURATION -----
N_EMBEDDINGS = 128
N_COMPONENTS_PCA = 50
N_COMPONENTS_TSNE = 2
PERPLEXITY = 30
LEARNING_RATE = 200
RANDOM_STATE = 42

# ----- HELPER FUNCTIONS -----
def plot_tsne(data_tsne, values, mode, output_path, genre_names=None):
    """Generates and saves a t-SNE scatter plot."""
    plt.figure(figsize=(8, 6))
    scatter = plt.scatter(
        data_tsne[:, 0],
        data_tsne[:, 1],
        c=values,
        s=10,
        cmap={
            "genre": "tab10",
            "accuracy": "coolwarm",
            "confidence": "viridis"
        }[mode]
    )

    # Genre visualization
    if mode == "genre":
        plt.title("t-SNE: Genre")
        handles, _ = scatter.legend_elements()
        plt.legend(handles, genre_names,
                   title="Genres",
                   loc="upper left",
                   bbox_to_anchor=(1.02, 1))
        plt.subplots_adjust(right=0.8)

    # Accuracy visualization
    elif mode == "accuracy":
        plt.title("t-SNE: Accuracy")
        handles, _ = scatter.legend_elements()
        plt.legend(handles, ["Incorrect", "Correct"],
                   title="Prediction",
                   loc="upper left",
                   bbox_to_anchor=(1.02, 1))
        plt.subplots_adjust(right=0.8)

    # Confidence visualization
    elif mode == "confidence":
        plt.title("t-SNE: Confidence")
        plt.colorbar(scatter, label="Confidence")

    # Save plot
    plt.savefig((output_path / f"tsne_{mode}.jpeg"), dpi=100)
    plt.close()


# ----- MAIN PIPELINE -----
def generate_tsne(predictions_path, class_names_path, output_path):

    # ----- PREP DATA -----
    df = pd.read_csv(predictions_path)

    # Split embeddings from metadata
    data = df.iloc[:, :N_EMBEDDINGS].values
    labels = df["label"]
    preds = df["pred"]
    label_names = df["label_name"]
    pred_names = df["pred_name"]
    confidence = df["confidence"]

    # Get class names
    with open(class_names_path) as f:
        genre_names = json.load(f)

    # ----- PCA & T-SNE -----
    data_pca = PCA(n_components=N_COMPONENTS_PCA).fit_transform(data)

    tsne = TSNE(
        n_components=N_COMPONENTS_TSNE,
        perplexity=PERPLEXITY,
        learning_rate=LEARNING_RATE,
        random_state=RANDOM_STATE
    )

    data_tsne = tsne.fit_transform(data_pca)

    # ----- PLOT AND SAVE AS JPEG -----
    plot_tsne(data_tsne, labels, "genre", output_path, genre_names)
    plot_tsne(data_tsne, (labels == preds), "accuracy", output_path)
    plot_tsne(data_tsne, confidence, "confidence", output_path)

if __name__ == "__main__":
    generate_tsne()