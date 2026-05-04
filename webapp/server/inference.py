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

import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"    # Suppresses TF startup logs
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import preprocess_input
import numpy as np
import matplotlib.cm as cm
import json
import librosa
from PIL import Image

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model")
SEGMENT_SEC = 10
HOP_SEC = 5
IMG_SIZE = (224, 224)
SR = 22050              # sampling rate of y (audio-time series)
N_FFT = 2048            # length of fft window
HOP_LENGTH = 512        # num of samples between successive frames
N_MELS = 128            # num of mel bands to generate

# Load the model and class names
loaded_model = tf.keras.models.load_model(os.path.join(MODEL_PATH, "final_model.keras"))
with open(os.path.join(MODEL_PATH, "class_names.json"), "r") as f:
    class_names = json.load(f)

def predict_genre(filepath):
    """
    Uses pretrained CNN to predict the genres of a given song.

    Args:
        filepath: path to song to be inspected

    Returns:
        dictionary with the probability for each genre
    """

    # Load and segment audio into correct length/overlap for model
    # Ignores final partial segment to avoid silence-padded audio
    audio_file, sr = librosa.load(filepath, sr=SR, mono=True)
    segment_len = SEGMENT_SEC * sr
    hop_len = HOP_SEC * sr
    num_segments = len(range(0, len(audio_file) - segment_len + 1, hop_len))
    if num_segments == 0:       # song clip is too short
        return dict(zip(class_names, [0] * len(class_names)))
    segments = []
    for i in range(num_segments):
        start = i * hop_len
        end = start + segment_len
        segments.append(audio_file[start:end])


    # Convert segments to spectrograms
    spectrograms = []
    for segment in segments:
        mel = librosa.feature.melspectrogram(
            y=segment,
            sr=sr,
            n_fft=N_FFT,
            hop_length=HOP_LENGTH,
            n_mels=N_MELS
        )
        mel = librosa.power_to_db(mel, ref=np.max)
        mel = np.clip(mel, -80, 0)
        mel = (mel + 80) / 80
        colored = cm.magma(mel)  # returns RGBA
        img = (colored[:, :, :3] * 255).astype(np.uint8)
        img = np.array(Image.fromarray(img, mode="RGB").resize(IMG_SIZE))
        img = preprocess_input(img)
        spectrograms.append(img)

    # Feed spectrograms to model and collect output confidences
    spect_stack = np.stack(spectrograms)
    model_results = loaded_model.predict(spect_stack)

    # Do averaging/math on output for final combined predictions and return
    model_results = np.mean(model_results, axis=0).tolist()
    return dict(zip(class_names, model_results))

if __name__ == "__main__":
    result = predict_genre(os.path.join(BASE_DIR, "model/song.mp3"))
    print(result)