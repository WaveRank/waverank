import os
import random
import numpy as np
import tensorflow as tf

# Paths
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(BASE_PATH, "dataset/")
OUTPUT_PATH = os.path.join(BASE_PATH, "outputs")
SAVE_PATH = os.path.join(BASE_PATH, "webapp/server/model/")

# Model
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
SEED = 42
os.environ["PYTHONHASHSEED"] = str(SEED)
random.seed(SEED)
np.random.seed(SEED)
tf.random.set_seed(SEED)

# Training
TRAINING_EPOCHS = 1
FINE_TUNE_EPOCHS = 1
INITIAL_LEARNING_RATE = 5e-5
FINE_LEARNING_RATE = 1e-5
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

# Controls label format and loss funcs
LOSS = 'categorical_crossentropy' if USE_CUTMIX else 'sparse_categorical_crossentropy'
LABEL_MODE = 'categorical' if USE_CUTMIX else 'int'