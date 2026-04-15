"""
Loads embeddings from CSV and generates t-SNE visualization plots for
genre, prediction accuracy, and confidence.

Citations (4/15/26):
https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.legend.html
https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html
https://www.datacamp.com/tutorial/introduction-t-sne
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# ----- CONFIGURATION -----
CSV_PATH = "../../embeddings.csv"
N_EMBEDDINGS = 128
N_COMPONENTS_PCA = 50
N_COMPONENTS_TSNE = 2
PERPLEXITY = 30
LEARNING_RATE = 200
RANDOM_STATE = 42

GENRES = [
    "blues", "classical", "country", "disco", "hiphop",
    "jazz", "metal", "pop", "reggae", "rock"
]

# ----- HELPER FUNCTIONS -----
def plot_tsne(data_tsne, values, mode):
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
        plot_title = "t-SNE: Genre"
        handles, _ = scatter.legend_elements()
        plt.legend(handles, GENRES,
                   title="Genres",
                   loc="upper left",
                   bbox_to_anchor=(1.02, 1))
        plt.subplots_adjust(right=0.8)

    # Accuracy visualization
    elif mode == "accuracy":
        plot_title = "t-SNE: Accuracy"
        handles, _ = scatter.legend_elements()
        plt.legend(handles, ["Incorrect", "Correct"],
                   title="Prediction",
                   loc="upper left",
                   bbox_to_anchor=(1.02, 1))
        plt.subplots_adjust(right=0.8)

    # Confidence visualization
    elif mode == "confidence":
        plot_title = "t-SNE: Confidence"
        plt.colorbar(scatter, label="Confidence")

    # Save plot
    plt.title(plot_title)
    plt.savefig(f"output/tsne_{mode}.jpeg", dpi=100)
    plt.close()

# ----- PREP DATA -----
os.makedirs("output", exist_ok=True)
df = pd.read_csv(CSV_PATH)

# Split embeddings from metadata
data = df.iloc[:, :N_EMBEDDINGS].values
labels = df["label"]
preds = df["pred"]
label_names = df["label_name"]
pred_names = df["pred_name"]
confidence = df["confidence"]

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
print("It may take a while for the images to save to the output folder. Give it a minute! :)")
plot_tsne(data_tsne, labels, "genre")
plot_tsne(data_tsne, (labels == preds), "accuracy")
plot_tsne(data_tsne, confidence, "confidence")
