"""
Runs multiple visual analyses, including generating confusion matrix, ROC/AUC curves, 
top-k accuracy, t-SNE, and UMAP plots, and saves them to a run-specific output directory.

The output folder can be either user-defined (via input prompt) or automatically generated 
as sequential run folders (e.g., run_1, run_2, ...) under the base output path.
"""

import os
from visualizations.confusion_matrix.confusion_matrix import generate_confusion_matrix
from visualizations.roc_auc.roc_auc import generate_roc_auc
from visualizations.top_k.top_k import generate_topk
from visualizations.tsne.tsne import generate_tsne
from visualizations.umap.umap_visual import generate_umap

# ----- CONFIGURATION -----
BASE_OUTPUT_PATH = "visualizations_output"
CLASS_NAMES_PATH = "class_names.json"
CONFIDENCES_PATH = "confidences.csv"
PREDICTIONS_PATH = "embeddings.csv"

# ----- HELPER FUNCTIONS -----
def run_visualization(function, visualization):
    print(f"Generating {visualization}...")
    function()
    print(f"\033[1m{visualization} done!\033[0m")

def get_output_dir(base_output_path):
    user_input = input("Enter a run name (or leave blank for auto): ").strip()

    # Case 1: User provides a run name
    if user_input:
        run_path = os.path.join(base_output_path, user_input)
        os.makedirs(run_path, exist_ok=True)
        return run_path

    # Case 2: Automatically name output folder if no run name provided
    else: 
        i = 1
        while True:
            run_path = os.path.join(base_output_path, f"run_{i}")
            if not os.path.exists(run_path):
                os.makedirs(run_path)
                return run_path
            i += 1    

# ----- MAIN PIPELINE -----
print("\033[32mGenerating visualizations...\n\033[0m")
OUTPUT_PATH = get_output_dir(BASE_OUTPUT_PATH)

run_visualization(lambda: generate_confusion_matrix(PREDICTIONS_PATH, CLASS_NAMES_PATH, OUTPUT_PATH), "Confusion Matrix")
run_visualization(lambda: generate_roc_auc(CONFIDENCES_PATH, CLASS_NAMES_PATH, OUTPUT_PATH), "ROC and AUC Curves")
run_visualization(lambda: generate_topk(CONFIDENCES_PATH, CLASS_NAMES_PATH, OUTPUT_PATH), "Top-k Accuracy Score")
run_visualization(lambda: generate_tsne(PREDICTIONS_PATH, CLASS_NAMES_PATH, OUTPUT_PATH), "t-SNE Plot")
run_visualization(lambda: generate_umap(PREDICTIONS_PATH, CLASS_NAMES_PATH, OUTPUT_PATH), "UMAP Plot")

print("\033[32m\nAll done! :)\n\033[0m")
