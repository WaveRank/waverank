"""
Configuration file for the genre classification CNN model.

Defines all the hyperparameters, augmentation, and training settings for the 
entire model pipeline. This includes the dataset parameters, learning rates,
model architecture, training, evaluation, and tuning scripts.
"""

import os
import random
import numpy as np
import tensorflow as tf


# ----- CONFIGURATIONS -----
# Paths
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_PATH, "dataset/")
SAVE_PATH = os.path.join(BASE_PATH, "webapp/server/model/")

# Model
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
SEED = 42

# Training
TRAINING_EPOCHS = 100
FINE_TUNE_EPOCHS = 100
INITIAL_LEARNING_RATE = 5e-4
FINE_LEARNING_RATE = 8e-5
DEPTH = 175
DROPOUT_RATE = 0.5
WEIGHT_DECAY = 1e-5

# Augmentation
USE_CUTMIX = False
USE_SPECAUG = True
TIME_MASK_WIDTH = 25
FREQ_MASK_WIDTH = 25
ALPHA = 1.0
CUTMIX_PROB = 0.5

# Tuning
N_TRIALS = 15


def set_seeds():
    """
    Sets global random seed for reproducibility
    """
    os.environ["PYTHONHASHSEED"] = str(SEED)
    random.seed(SEED)
    np.random.seed(SEED)
    tf.random.set_seed(SEED)