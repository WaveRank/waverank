"""
Generate and save ROC (Receiver Operator Characteristic) curves and AUC (area
under curve) for all genres and saved models in visualizations_output folder.
Can either look at all models or only the specified models. Uses CSV of model
predictions.

Expected CSV layout:
- one column per genre (class), with header as genre name
- one row per song, each cell containing confidence value for that genre/song
- label (int): true class index

Axes are:
- fpr: False positive rates for each possible threshold
- tpr: True positive rates for each possible threshold

Uses genre names to label curves, outputs a PNG image with ROC and AUC for each
genre/model.

Citations:
https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_curve.html
https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html
"""

import sys

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
from sklearn import preprocessing, metrics


def load_runs(base_path):
    """Return list of (run_name, df, genre_names) for each valid run folder.

    Args:
        base_path: path to search for valid run folders

    Returns:
        runs: list of (run_name, df, genre_names) for each valid run folder
    """

    runs = []

    # Loop over each folder in base_path
    for run_name in sorted(os.listdir(base_path)):
        run_dir = os.path.join(base_path, run_name)
        conf_path = os.path.join(run_dir, "confidences.csv")
        names_path = os.path.join(run_dir, "class_names.json")

        # Only works on folders with both files
        if os.path.isfile(conf_path) and os.path.isfile(names_path):
            with open(names_path) as f:
                genre_names = json.load(f)
            df = pd.read_csv(conf_path)

            # Store run name, confidences, and genres as tuple in runs list
            runs.append((run_name, df, genre_names))

    return runs


def generate_comparison_roc(base_path, output_path, models=None):
    """
    Load prediction confidences from each run subfolder and generate overlaid
    ROC/AUC curves per genre across all runs (or a specified subset).
    Args:
        base_path: path to the folder containing run subfolders
        output_path: path to save the output PNG
        models: optional list of run folder names to include. If None, all valid runs are used.
    Side effects:
    - Reads confidences.csv and class_names.json from each run subfolder
    - Writes comparison image to output_path
    """

    # Retrieve all valid runs from folder
    runs = load_runs(base_path)

    # Only keep the specified models, if they are specified
    if models:
        runs = [r for r in runs if r[0] in models]          # r[0] = run name
        if not runs:
            print(f"No matching runs found for: {models}")
            return
        
    # Grabs genre names from the first run (assumed consistent) and counts them
    genre_names = runs[0][2]
    n_genres = len(genre_names)

    # Creates a 2×5 grid of subplots (one per genre)
    fig, axes = plt.subplots(2, 5, figsize=(18, 8))
    fig.suptitle("WaveRank ROC Curves — Model Comparison", fontsize=20)
    axes = axes.flatten()

    # Loops over each genre, grabs its subplot, and draws the diagonal baseline
    for genre_idx in range(n_genres):
        ax = axes[genre_idx]
        ax.plot([0,1], [0, 1], linestyle="--", color="silver", zorder=0)

        # Loops over each model and draws one curve on each genre per model
        for run_name, df, g_names in runs:
            label_col = df["label"].values
            bin_labels = preprocessing.label_binarize(      # Binarize labels
                label_col, classes=list(range(n_genres))
            )
            true_binary = bin_labels[:, genre_idx]
            scores = df[g_names[genre_idx]]
            fpr, tpr, _ = metrics.roc_curve(true_binary, scores)
            auc_score = metrics.roc_auc_score(true_binary, scores)
            ax.plot(fpr, tpr, label=f"{run_name} (AUC={auc_score:.2f})", alpha=0.6)
        
        ax.set_xlim(-0.05, 1.05)
        ax.set_ylim(-0.05, 1.05)
        ax.set_box_aspect(1)
        ax.xaxis.set_major_locator(tck.MultipleLocator(0.5))
        ax.yaxis.set_major_locator(tck.MultipleLocator(0.5))
        ax.set_xlabel("FPR")
        ax.set_ylabel("TPR")
        ax.set_title(genre_names[genre_idx])
        ax.legend(fontsize=8, loc="lower right")
    
    plt.tight_layout(pad=1.5, h_pad=1.5)
    out = os.path.join(output_path, "comparison_roc_auc.png")
    plt.savefig(out, dpi=300)
    plt.close()
    print(f"Saved comparison plot to {out}")


if __name__ == "__main__":
    BASE_OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "../../visualizations_output")
    generate_comparison_roc(BASE_OUTPUT_PATH, BASE_OUTPUT_PATH, ["run_1", "run_2"])
