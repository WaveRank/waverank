"""
Inference pipeline receives audio file, then processes it and feeds it to
pretrained model, which then returns a ranked list of genre predictions and
percentages.

Usage in webapp: "from inference import predict_genre"
    - Should load up the model only once instead of for each call

Citations (5/3/26):
https://www.geeksforgeeks.org/machine-learning/save-and-load-models-in-tensorflow/
https://www.geeksforgeeks.org/deep-learning/tf-keras-models-load_model-in-tensorflow/
https://docs.github.com/en/repositories/working-with-files/managing-large-files
https://stackoverflow.com/questions/32231892/typeerror-with-int-for-jsonify-from-flask

Citation (5/30/26):
https://huggingface.co/docs/huggingface_hub/guides/download
"""

# ----- IMPORTS -----
import os
from pathlib import Path
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import preprocess_input
import numpy as np
import json
import threading
from concurrent.futures import ThreadPoolExecutor

from model.src.audio.audio_utils import segment_audio, make_spectrogram, spectrogram_to_image
from shared.paths import MODEL_ARTIFACTS_DIR

# ----- MODEL LOADING -----
# Load the model and class names
def _load_model():
    model_artifacts_dir = MODEL_ARTIFACTS_DIR

    if os.getenv("RAILWAY_ENVIRONMENT"):
        # Production: download from Hugging Face
        from huggingface_hub import hf_hub_download
        model_path = hf_hub_download(
            repo_id="emilyfhuntley/waverank",
            filename="final_model.keras",
            cache_dir="/tmp/model_cache",
            token=os.getenv("HF_TOKEN")
        )
        class_names_path = hf_hub_download(
            repo_id="emilyfhuntley/waverank",
            filename="class_names.json",
            cache_dir="/tmp/model_cache",
            token=os.getenv("HF_TOKEN")
        )
        hf_hub_download(
            repo_id="emilyfhuntley/waverank",
            filename="youtube_cookies.txt",
            cache_dir="/tmp/model_cache",
            token=os.getenv("HF_TOKEN")
        )

    else:
        # Local: load from repo as usual
        model_path = model_artifacts_dir / "final_model.keras"
        class_names_path = model_artifacts_dir / "class_names.json"

    _model = tf.keras.models.load_model(model_path)
    with open(class_names_path, "r") as f:
        _class_names = json.load(f)
    return _model, _class_names

model_lock = threading.Lock()
loaded_model, class_names = _load_model()

# ----- INFERENCE -----
def preprocess(segment, sr):
    """
    Convert the given audio segment to a spectrogram image and apply TF preprocessing
    """
    img = spectrogram_to_image(make_spectrogram(segment, sr))
    img = preprocess_input(np.array(img))
    return img

def predict_genre(audio_file, sr):
    """
    Uses pretrained CNN to predict the genres of a given song.

    Args:
        filepath (str): path to song to be inspected

    Returns:
        dictionary with the probability for each genre
    """
    batch_size = 8

    # Load and segment audio into correct length/overlap for model
    segments = segment_audio(audio_file, sr)
    if not segments:        # Song clip is too short to segment
        return dict(zip(class_names, [0] * len(class_names)))

    # Get predictions for the audio segments, in batches to reduce memory usage
    sums = None
    count = 0

    for i in range(0, len(segments), batch_size):
        # Convert segments to spectrograms
        batch_segments = segments[i: i+batch_size]
        batch_imgs = [preprocess(segment, sr) for segment in batch_segments]

        # Feed spectrograms to model and collect output confidences
        batch_arr = np.stack(batch_imgs)

        with model_lock:  # Guard against Tensorflow race conditions
            batch_predictions = loaded_model.predict(batch_arr, verbose=0)

        if sums is None:
            sums = np.sum(batch_predictions, axis=0)
        else:
            sums += np.sum(batch_predictions, axis=0)
        count += len(batch_predictions)

    # Do averaging on output for final combined predictions and return
    model_results = (sums / count).tolist()
    return dict(zip(class_names, model_results))


if __name__ == "__main__":
    pass
