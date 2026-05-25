"""
Configuration file for the genre classification CNN model.

Defines all the hyperparameters, augmentation, and training settings for the 
entire model pipeline. This includes the dataset parameters, learning rates,
model architecture, training, evaluation, and tuning scripts.
"""

# ----- IMPORTS -----
from pathlib import Path
import os
import random
import numpy as np
import tensorflow as tf


# ----- CONFIGURATIONS -----
# Paths
BASE_PATH = Path(__file__).resolve().parent.parent
DATASET_PATH = BASE_PATH / "dataset"
SAVE_PATH = BASE_PATH / "webapp/server/model"   

# Model
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
SEED = 42

# Training
TRAINING_EPOCHS = 100
FINE_TUNE_EPOCHS = 100
INITIAL_LEARNING_RATE = 2e-4
FINE_LEARNING_RATE = 8e-5
DEPTH = 80
DROPOUT_RATE = 0.5
WEIGHT_DECAY = 1e-5

# Augmentation
USE_CUTMIX = True
USE_SPECAUG = True
TIME_MASK_WIDTH = 15
FREQ_MASK_WIDTH = 10
ALPHA = 1.0
CUTMIX_PROB = 0.5

# Tuning
N_TRIALS = 30


def set_seeds():
    """
    Sets global random seed for reproducibility
    """
    os.environ["PYTHONHASHSEED"] = str(SEED)
    random.seed(SEED)
    np.random.seed(SEED)
    tf.random.set_seed(SEED)