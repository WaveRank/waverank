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
import os
import random
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
import os
import librosa
import soundfile as sf
import numpy as np

# ----- CONFIGURATION -----
SAVE_PATH = "webapp/server/model/"
DATASET_PATH = "dataset/"
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
TRAINING_EPOCHS = 100
FINE_TUNE_EPOCHS = 100

# Tuning parameters for best results as of 4/30 -- work in progress
INITIAL_LEARNING_RATE = 5e-5
FINE_LEARNING_RATE = 1e-6
DEPTH = 175
DROPOUT_RATE = 0.5
TIME_MASK_WIDTH = 25
FREQ_MASK_WIDTH = 25

# Set global random seed for reproducibility
SEED = 42
os.environ["PYTHONHASHSEED"] = str(SEED)
random.seed(SEED)
np.random.seed(SEED)
tf.random.set_seed(SEED)

# ----- LOAD DATASETS -----
print("Loading Training Set:")
train_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_PATH + "train",
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

print("Loading Validation Set:")
val_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_PATH + "val",
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

print("Loading Test Set:")
test_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_PATH + "test",
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False   
)

# Extract class (genre) names, save for reference
class_names = train_ds.class_names
print("Classes:", class_names)
with open(os.path.join(SAVE_PATH, "class_names.json"), "w") as f:
    json.dump(class_names, f)


def spec_augment(images, labels):
    """
    Applies spectrogram augmentation to mask out random frequency and time
    regions of each image in a batch. This function calls a helper per each
    single image in the batch.

    Args:
        images (tf.Tensor): Batch of spectrogram images.
        labels (tf.Tensor): Batch of integer genre labels.
    Returns:
        Tuple of (augmented images, unchanged labels).
    """

    aug_images = tf.map_fn(spec_augment_helper, images)
    return aug_images, labels


def spec_augment_helper(image):
    """
    Takes one single tensor/image and applies spectrogram augmentation, then
    returns that tensor/image.
    """

    # Pick width and start points for each dimension
    freq_width = tf.random.uniform(
        shape=[], maxval=FREQ_MASK_WIDTH, dtype=tf.dtypes.int32
    )
    freq_start = tf.random.uniform(
        shape=[], maxval=IMG_SIZE[0] - freq_width, dtype=tf.dtypes.int32
    )
    time_width = tf.random.uniform(
        shape=[], maxval=TIME_MASK_WIDTH, dtype=tf.dtypes.int32
    )
    time_start = tf.random.uniform(
        shape=[], maxval=IMG_SIZE[1] - time_width, dtype=tf.dtypes.int32
    )

    # Draw frequency and time masks
    freq_mask = tf.concat(
        [
            tf.ones([freq_start, IMG_SIZE[1], 3]),
            tf.zeros([freq_width, IMG_SIZE[1], 3]),
            tf.ones([IMG_SIZE[0] - freq_start - freq_width, IMG_SIZE[1], 3]),
        ],
        0,
    )
    time_mask = tf.concat(
        [
            tf.ones([IMG_SIZE[0], time_start, 3]),
            tf.zeros([IMG_SIZE[0], time_width, 3]),
            tf.ones([IMG_SIZE[0], IMG_SIZE[1] - time_start - time_width, 3]),
        ],
        1,
    )

    # Combine into one mask, apply to image and return masked image
    mask = freq_mask * time_mask
    return mask * image


# ----- PREPROCESSING -----
train_ds = train_ds.map(lambda x, y: (preprocess_input(x), y))
val_ds   = val_ds.map(lambda x, y: (preprocess_input(x), y))
test_ds  = test_ds.map(lambda x, y: (preprocess_input(x), y))

# Spectrogram Augmentation on training data (comment out if desired)
train_ds = train_ds.map(spec_augment)

# Prefetch (improves performance)
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.prefetch(AUTOTUNE)
val_ds   = val_ds.prefetch(AUTOTUNE)
test_ds  = test_ds.prefetch(AUTOTUNE)

# ----- BUILD MODEL -----
base_model = ResNet50(
    weights='imagenet',
    include_top=False,
    input_shape=(*IMG_SIZE, 3)
)
base_model.trainable = False

# Extract and pool features
x = base_model.output
x = layers.GlobalAveragePooling2D()(x)

# Embedding layer
embedding = layers.Dense(128, activation='relu', name="embedding")(x)
x = layers.Dropout(DROPOUT_RATE)(embedding)
outputs = layers.Dense(len(class_names), activation='softmax')(x)

# Build and compile model
model = tf.keras.Model(inputs=base_model.input, outputs=outputs)
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=INITIAL_LEARNING_RATE),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Set early stopping for when val_loss stops improving after 5 epochs
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=5,
    restore_best_weights=True
)

# model.summary()  # Optional, prints architecture of the model

# ----- TRAIN MODEL -----
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=TRAINING_EPOCHS,
    callbacks=[early_stopping]
)

# Plot and save training curves
plt.figure()
plt.plot(history.history['accuracy'], label='train')
plt.plot(history.history['val_accuracy'], label='val')
plt.legend()
plt.title("Accuracy")
plt.savefig("accuracy_curve.png", dpi=300)
print("Saved accuracy_curve.png")
plt.close()

plt.figure()
plt.plot(history.history['loss'], label='train')
plt.plot(history.history['val_loss'], label='val')
plt.legend()
plt.title("Loss")
plt.savefig("loss_curve.png", dpi=300)
print("Saved loss_curve.png")
plt.close()

# Evaluate
test_loss, test_acc = model.evaluate(test_ds)
print("Test accuracy:", test_acc)

# ----- FINE-TUNING -----
base_model.trainable = True

# Fine-tune only last layers
for layer in base_model.layers[:-DEPTH]:
    layer.trainable = False

# Recompile with lower learning rate
model.compile(
    optimizer=tf.keras.optimizers.Adam(FINE_LEARNING_RATE),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Fine-tuning (Note: separate instances required — EarlyStopping is stateful)
early_stopping_finetune = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=5,
    restore_best_weights=True
)

# Train again
model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=FINE_TUNE_EPOCHS,
    callbacks=[early_stopping_finetune]
)

# Evaluate
test_loss, test_acc = model.evaluate(test_ds)
print("Test accuracy after fine-tuning:", test_acc)

# Save entire model for future use
os.makedirs(SAVE_PATH, exist_ok=True)
model.save(os.path.join(SAVE_PATH, 'final_model.keras'))

# ----- EMBEDDING MODEL -----
embedding_model = tf.keras.Model(
    inputs=model.input,
    outputs=model.get_layer("embedding").output
)

# Extract embeddings
def extract_embeddings(dataset, emb_model, clf_model):
    """Extracts embeddings, predictions, and confidence scores from dataset."""
    embeddings = []
    labels = []
    preds = []
    confidences = []

    for images, y in dataset:
        # Embedding vectors and class probabilities
        emb = emb_model.predict(images, verbose=0)
        prob = clf_model.predict(images, verbose=0)

        # Predicted class index and confidence of prediction
        pred = np.argmax(prob, axis=1)
        conf = np.max(prob, axis=1)

        embeddings.append(emb)
        labels.append(y.numpy())
        preds.append(pred)
        confidences.append(conf)

    # Combine into single arrays
    return (
        np.vstack(embeddings),
        np.hstack(labels),
        np.hstack(preds),
        np.hstack(confidences)
    )

# Run embedding extraction on test set
x_emb, y_true, y_pred, conf = extract_embeddings(
    test_ds,
    embedding_model,
    model
)
df = pd.DataFrame(x_emb)

# Add metadata columns
df["label"] = y_true
df["pred"] = y_pred
df["confidence"] = conf
df["label_name"] = [class_names[i] for i in y_true]
df["pred_name"] = [class_names[i] for i in y_pred]

# Save to CSV
df.to_csv("embeddings.csv", index=False)
print("Saved embeddings.csv")

# Extract prediction confidence for each song per genre
def extract_confidences(dataset, clf_model):
    """Extracts all genre confidence scores from dataset for each song."""
    labels = []
    confidences = []

    for images, y in dataset:
        # Class probabilities
        prob = clf_model.predict(images, verbose=0)
        labels.append(y.numpy())
        confidences.append(prob)

    # Combine into single arrays
    return (
        np.hstack(labels),
        np.vstack(confidences)
    )

# Run embedding extraction on test set
y_true, confidences = extract_confidences(
    test_ds,
    model
)
df = pd.DataFrame(confidences)

# Add metadata columns
df.columns = class_names
df["label"] = y_true
df["label_name"] = [class_names[i] for i in y_true]

# Save to CSV
df.to_csv("confidences.csv", index=False)
print("Saved confidences.csv")
