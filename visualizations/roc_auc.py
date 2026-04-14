"""
Generate and save ROC (Receiver Operator Characteristic) curves and AUC (area under curve) for all genres and the currently trained model. Uses CSV of model predictions.

Expected CSV columns:
- label (int): true class index
- pred (int): predicted class index

Axes are:
- fpr: False positive rates for each possible threshold
- tpr: True positive rates for each possible threshold

Uses GENRE_NAMES to label curves, outputs a PNG image.
"""

PREDICTIONS_PATH = "../../embeddings.csv"
OUTPUT_PATH = "roc_auc.png"

# Order of genre names must match CNN model
GENRE_NAMES = ["blues", "classical", "country", "disco", "hiphop", "jazz", "metal", "pop", "reggae", "rock"]