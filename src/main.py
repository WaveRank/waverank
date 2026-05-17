"""
Builds an image classification model using a pretrained ResNet50 backbone.

Citations (4/9/26):
https://www.tensorflow.org/api_docs/python/tf/keras/applications/resnet/preprocess_input
https://www.tensorflow.org/api_docs/python/tf/keras/applications/ResNet50
https://www.tensorflow.org/api_docs/python/tf/keras/preprocessing/image_dataset_from_directory
https://www.tensorflow.org/guide/data_performance
https://www.tensorflow.org/guide/keras/functional_api
https://www.tensorflow.org/guide/keras/transfer_learning

Citation (4/12/26):
https://keras.io/guides/functional_api/#extract-and-reuse-nodes-in-the-graph

Citation (4/20/2026):
https://medium.com/data-science/audio-deep-learning-made-simple-part-3-data-preparation-and-augmentation-24c6e1f6b52 (Spectrogram Augmentation section)

Citation (4/21/26):
https://keras.io/examples/vision/cutmix/

Citation (5/06/26):
https://keras.io/keras_tuner/api/tuners/bayesian/

Things to try to improve the model:
- Add data augmentation
- Tune learning rate (initial training and fine-tuning separately)
- Adjust batch size 
- Adjust fine-tuning depth (# of unfrozen ResNet layers)
- Increase embedding size 
- Tune dropout rate 
- Increase input image resolution 
- Adjust # of training and fine-tuning epochs
- And more! These are just some ideas
"""

from config import *
from dataset import get_datasets
from model import build_model
from sklearn.metrics import f1_score
from training import initial_train, fine_tune
from evaluate import *


# ----- MAIN PIPELINE -----

# Set global random seed for reproducibility
set_seeds()

# Get testing, val, and training datasets, and class names
train_ds, val_ds, test_ds, class_names = get_datasets()

# Build model
base_model, model = build_model(class_names)

# Initial training and evaluation
model, history = initial_train(model, train_ds, val_ds)
save_curves(history)
evaluate_model(model, test_ds, phase=1)

# Fine tune training and evaluation
model = fine_tune(model, base_model, train_ds, val_ds)
evaluate_model(model, test_ds, phase=2)

# Extract embeddings
emb_model = embedding_model(model)
y_true, y_pred = save_embeddings(test_ds, emb_model, model, class_names)

macro_f1 = f1_score(y_true, y_pred, average="macro")
print(f"F1 Score: {macro_f1}")
