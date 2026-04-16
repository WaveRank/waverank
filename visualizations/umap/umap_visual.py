"""
Generate and save a umap visualization using the embeddings.csv from 
CNN model predictions

Expected CSV columns:
- 128 dimensional embedding vectors
- label (int): true class index

Uses GENRE_NAMES to label colors, outputs a PNG image representing the UMAP
"""

import matplotlib.pyplot as plt
import pandas as pd
import umap

EMBEDDINGS_PATH = "../../embeddings.csv"
OUTPUT_PATH = "umap.png"

RANDOM_STATE = 42

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


def generate_umap():
    """
    Loads the embeddings CSV and generates a UMAP visualization

    Side effects:
    - Reads from EMBEDDINGS_PATH
    - Writes image to OUTPUT_PATH
    """
    df = pd.read_csv(EMBEDDINGS_PATH)

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
        GENRE_NAMES, 
        title="Genres", 
        ncol=2, 
        loc="lower left", 
        fontsize=7
    )
    plt.title("UMAP")
    plt.savefig(OUTPUT_PATH)


if __name__ == "__main__":
    generate_umap()