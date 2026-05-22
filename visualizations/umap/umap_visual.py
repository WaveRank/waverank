"""
Generate and save a umap visualization using the embeddings.csv from 
CNN model predictions

Expected CSV columns:
- 128 dimensional embedding vectors
- label (int): true class index

Uses CLASS_NAMES_PATH to extract genre_names that label colors, outputs 
a PNG image representing the UMAP
"""

# ----- IMPORTS -----
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import umap
import json
import warnings

warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    module="umap"
)
RANDOM_STATE = 42

def generate_umap(embeddings_path, class_names_path, output_path):
    """
    Loads the embeddings CSV and generates a UMAP visualization

    Side effects:
    - Reads from EMBEDDINGS_PATH
    - Writes image to OUTPUT_PATH
    """

    # Get the genre names
    with open(class_names_path) as f:
        genre_names = json.load(f)

    df = pd.read_csv(embeddings_path)

    # Extract 128 dimension vectors and true labels
    X = df.iloc[:, :-5].values
    y = df['label'].values

    # Convert embeddings to 2D for plotting
    reducer = umap.UMAP(metric='cosine', random_state=RANDOM_STATE)
    embeddings = reducer.fit_transform(X)

    # Plot UMAP
    scatter = plt.scatter(
        embeddings[:, 0], 
        embeddings[:, 1], 
        c=y, 
        s=8, 
        cmap='tab10'
    )

    handles, labels = scatter.legend_elements()
    plt.legend(
        handles, 
        genre_names, 
        title="Genres",
        fontsize=7,
        bbox_to_anchor=(1.2, 1)
    )
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.title("UMAP")
    plt.savefig((output_path / f"umap.png"))
    plt.close()


if __name__ == "__main__":
    generate_umap()