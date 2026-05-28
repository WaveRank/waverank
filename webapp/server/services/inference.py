"""
Inference pipeline receives audio file, then processes it and feeds it to
pretrained model, which then returns a ranked list of genre predictions and
percentages.

Usage in webapp: "from inference import predict_genre"
    - Should load up the model only once instead of for each call?

Citations (5/3/26):
https://www.geeksforgeeks.org/machine-learning/save-and-load-models-in-tensorflow/
https://www.geeksforgeeks.org/deep-learning/tf-keras-models-load_model-in-tensorflow/
https://docs.github.com/en/repositories/working-with-files/managing-large-files
https://stackoverflow.com/questions/32231892/typeerror-with-int-for-jsonify-from-flask
"""

# ----- IMPORTS -----
import os
from pathlib import Path
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"    # Suppresses TF startup logs
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import preprocess_input
import numpy as np
import json
from model.src.audio.audio_utils import load_audio, segment_audio, make_spectrogram, spectrogram_to_image
from shared.paths import MODEL_ARTIFACTS_DIR

# ----- MODEL LOADING -----
# Load the model and class names
loaded_model = tf.keras.models.load_model(MODEL_ARTIFACTS_DIR / "final_model.keras")
with open(MODEL_ARTIFACTS_DIR / "class_names.json", "r") as f:
    class_names = json.load(f)

# ----- INFERENCE -----
def predict_genre(filepath):
    """
    Uses pretrained CNN to predict the genres of a given song.

    Args:
        filepath (str): path to song to be inspected

    Returns:
        dictionary with the probability for each genre
    """

    # Load and segment audio into correct length/overlap for model
    audio_file, sr = load_audio(filepath)
    if audio_file is None:  # Audio file failed to load
        return dict(zip(class_names, [0] * len(class_names)))
    segments = segment_audio(audio_file, sr)
    if not segments:        # Song clip is too short to segment
        return dict(zip(class_names, [0] * len(class_names)))

    # Convert segments to spectrograms
    spectrograms = []
    for segment in segments:
        img = spectrogram_to_image(make_spectrogram(segment, sr))
        img = preprocess_input(np.array(img))
        spectrograms.append(img)

    # Feed spectrograms to model and collect output confidences
    spect_stack = np.stack(spectrograms)
    model_results = loaded_model.predict(spect_stack)

    # Do averaging/math on output for final combined predictions and return
    model_results = np.mean(model_results, axis=0).tolist()
    return dict(zip(class_names, model_results))

if __name__ == "__main__":
    # result = predict_genre((MODEL_PATH / "model/song.mp3"))
    # print(result)
    pass
