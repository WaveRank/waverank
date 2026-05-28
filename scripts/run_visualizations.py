"""
Runs multiple visual analyses, including generating confusion matrix, ROC/AUC curves,
top-k accuracy, t-SNE, and UMAP plots, and saves them to a run-specific output directory.
Also preserves "Model.py", output CSVs, and class_names.json for future reference and model comparisons.

The output folder can be either user-defined (via input prompt) or automatically generated
as sequential run folders (e.g., run_1, run_2, ...) under the base output path.
"""
# ----- IMPORTS -----
from pathlib import Path
import shutil
from visualizations.confusion_matrix.confusion_matrix import (
    generate_confusion_matrix,
)
from visualizations.roc_auc.roc_auc import generate_roc_auc
from visualizations.top_k.top_k import generate_topk
from visualizations.tsne.tsne import generate_tsne
from visualizations.umap.umap_visual import generate_umap
from shared.paths import PROJECT_ROOT, VISUALIZATIONS_OUTPUT_DIR, MODEL_ARTIFACTS_DIR

# ----- CONFIGURATION -----
CLASS_NAMES_PATH = MODEL_ARTIFACTS_DIR / "class_names.json"
CONFIDENCES_PATH = MODEL_ARTIFACTS_DIR / "confidences.csv"
PREDICTIONS_PATH = MODEL_ARTIFACTS_DIR / "embeddings.csv"


# ----- HELPER FUNCTIONS -----
def run_visualization(function, visualization):
    """
    Runs a visualization function and prints status messages.
    Args:
        function (callable): visualization function to call
        visualization (str): name of the visualization for display
    """
    
    print(f"Generating {visualization}...")
    function()
    print(f"\033[1m{visualization} done!\033[0m")


def get_output_dir(base_output_dir):
    """
    Determines the output directory for a visualization run.
    Prompts the user for a run name; if blank, auto-generates a
    sequential folder name (run_1, run_2, ...) under base_output_dir.
    Args:
        base_output_dir (Path): base directory to create the run folder in
    Returns:
        Path: path to the created output directory
    """

    user_input = input("Enter a run name (or leave blank for auto): ").strip()

    # Case 1: User provides a run name
    if user_input:
        run_path = base_output_dir / user_input
        run_path.mkdir(parents=True, exist_ok=True)
        return run_path

    # Case 2: Automatically name output folder if no run name provided
    else:
        i = 1
        while True:
            run_path = base_output_dir / f"run_{i}"
            if not run_path.exists():
                run_path.mkdir(parents=True)
                return run_path
            i += 1


# ----- MAIN PIPELINE -----
print("\033[32mGenerating visualizations...\n\033[0m")
OUTPUT_PATH = get_output_dir(VISUALIZATIONS_OUTPUT_DIR)

# Generate and save visualizations
run_visualization(lambda: generate_confusion_matrix(PREDICTIONS_PATH, CLASS_NAMES_PATH, OUTPUT_PATH),"Confusion Matrix")
run_visualization(lambda: generate_roc_auc(CONFIDENCES_PATH, CLASS_NAMES_PATH, OUTPUT_PATH),"ROC and AUC Curves")
run_visualization(lambda: generate_topk(CONFIDENCES_PATH, CLASS_NAMES_PATH, OUTPUT_PATH),"Top-k Accuracy Score")
run_visualization(lambda: generate_tsne(PREDICTIONS_PATH, CLASS_NAMES_PATH, OUTPUT_PATH), "t-SNE Plot")
run_visualization(lambda: generate_umap(PREDICTIONS_PATH, CLASS_NAMES_PATH, OUTPUT_PATH), "UMAP Plot")

# Copy over CSVs, json, and model.py
shutil.copy(CONFIDENCES_PATH, OUTPUT_PATH / CONFIDENCES_PATH.name)
shutil.copy(PREDICTIONS_PATH, OUTPUT_PATH / PREDICTIONS_PATH.name)
shutil.copy(CLASS_NAMES_PATH, OUTPUT_PATH / CLASS_NAMES_PATH.name)
shutil.copytree(PROJECT_ROOT / "model" / "src", OUTPUT_PATH / "src", dirs_exist_ok=True)

print("\033[32m\nAll done! :)\n\033[0m")
