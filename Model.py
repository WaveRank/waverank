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

Citation(4/21/26):
https://keras.io/examples/vision/cutmix/

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

os.environ["TF_DETERMINISTIC_OPS"] = "1"

import random
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from sklearn.metrics import f1_score
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json

# ----- CONFIGURATION -----
SAVE_PATH = "webapp/server/model/"
DATASET_PATH = "dataset/"
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
TRAINING_EPOCHS = 100
FINE_TUNE_EPOCHS = 100

# Vary these for DoE partial factorial tests
INITIAL_LEARNING_RATE = 5e-5
FINE_LEARNING_RATE = 1e-6
DEPTH = 175
DROPOUT_RATE = 0.5
TIME_MASK_WIDTH = 25
FREQ_MASK_WIDTH = 25
ALPHA = 1.0
CUTMIX_PROB = 0.5

# Set augmentation
USE_CUTMIX = False
USE_SPECAUG = True

# Controls label format and loss funcs
LOSS = 'categorical_crossentropy' if USE_CUTMIX else 'sparse_categorical_crossentropy'
LABEL_MODE = 'categorical' if USE_CUTMIX else 'int'

# Set global random seed for reproducibility
SEED = 42
os.environ["PYTHONHASHSEED"] = str(SEED)
random.seed(SEED)
np.random.seed(SEED)
tf.random.set_seed(SEED)


# ----- SPEC AUGMENTATION -----
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


# ----- CUTMIX AUGMENTATION -----
def get_lambda():
    """
    Takes an alpha value for the beta distribution
    to return a lambda mixing ratio
    """
    
    beta_dist = np.random.beta(ALPHA, ALPHA)
    lambda_tf = tf.constant(beta_dist, dtype=tf.float32)

    return lambda_tf


def patch(lambda_val, img_height, img_width):
    """
    Determines the size of the image patch that will be used
    in the cutmix augmentation for cropping

    Returns:
        Positional offsets of the patch (x1, y1) and the dimensions
        height and width of the patch (target_h, target_w)
    """

    ratio = tf.sqrt(1.0 - lambda_val)

    # Get the size of the patch of image
    cut_height = tf.cast(tf.cast(img_height, tf.float32) * ratio, tf.int32)
    cut_width = tf.cast(tf.cast(img_width, tf.float32) * ratio, tf.int32)

    # Find a random point on the image
    cut_x = tf.random.uniform([], 0, img_width, dtype=tf.int32)
    cut_y = tf.random.uniform([], 0, img_height, dtype=tf.int32)

    # Define the full dimensions of patch
    y1 = tf.clip_by_value(cut_y - cut_height // 2, 0, img_height)
    x1 = tf.clip_by_value(cut_x - cut_width // 2, 0, img_width)
    y2 = tf.clip_by_value(cut_y + cut_height // 2, 0, img_height)
    x2 = tf.clip_by_value(cut_x + cut_width // 2, 0, img_width)

    # Extract x and y lengths of the patch
    target_w = tf.maximum(x2 - x1, 1)
    target_h = tf.maximum(y2 - y1, 1)

    return x1, y1, target_h, target_w


def cutmix(train_ds_one, train_ds_two):
    """
    Applies the cutmix augmentation to the spectrograms. This function 
    takes two shuffled train datasets, gets the paired image and label, 
    then applies cropping and patching to the spectrogram image.

    Returns:
        Mixed image tensor and label
    """

    img_h, img_w = IMG_SIZE[0], IMG_SIZE[1]

    (image1, label1), (image2, label2) = train_ds_one, train_ds_two

    lambda_val = get_lambda()

    # Get the bounding box offsets, heights and widths
    x1, y1, target_h, target_w = patch(lambda_val, img_h, img_w)

    # Takes image 2 and crops a patch of the image
    cropped_img2 = tf.image.crop_to_bounding_box(image2, y1, x1, target_h, target_w)
    image2 = tf.image.pad_to_bounding_box(cropped_img2, y1, x1, img_h, img_w)

    # Takes image 1 and creates a hole to place the patch
    cropped_img1 = tf.image.crop_to_bounding_box(image1, y1, x1, target_h, target_w)
    image1_patch = tf.image.pad_to_bounding_box(cropped_img1, y1, x1, img_h, img_w)

    # Subtract the patch from the full image to get a hole in the image
    image1 = image1 - image1_patch

    # Combine the images
    cutmix_image = image1 + image2

    # Recalculate lambda to match correct pixel ratios after cropping
    lambda_val = 1 - tf.cast(target_h * target_w, tf.float32) / tf.cast(img_h * img_w, tf.float32)
    
    # Using adjusted lambda to create new label of mixed genre ratios
    cutmix_label = lambda_val * label1 + (1 - lambda_val) * label2


    return cutmix_image, cutmix_label


def cutmix_chances(train_ds_one, train_ds_two):
    """
    Determines the chance that each sample gets mixing
    """
    (image1, label1), (image2, label2) = train_ds_one, train_ds_two

    probability = tf.random.uniform([]) < CUTMIX_PROB

    return tf.cond(
        probability,
        lambda: cutmix(train_ds_one, train_ds_two),
        lambda: (image1, label1)
    )


# ----- LOAD DATASETS -----
def load_dataset(set, shuffle=False):
    """
    Loads training, validation, and testing datasets depending 
    on if using CutMix or Spec Augmentations or both
    """
    
    print(f"Loading {set} set...")
    
    return tf.keras.utils.image_dataset_from_directory(
    	DATASET_PATH + set,
    	image_size=IMG_SIZE,
    	batch_size=None,
    	shuffle=shuffle,
    	label_mode=LABEL_MODE
    )

# Get datasets
train_ds = load_dataset("train", shuffle=True)
val_ds = load_dataset("val", shuffle=True).batch(BATCH_SIZE)
test_ds = load_dataset("test").batch(BATCH_SIZE)

# Get class names
class_names = train_ds.class_names

if USE_CUTMIX:
    train_ds_one = (
        train_ds.shuffle(len(train_ds), seed=SEED)
    )

    train_ds_two = (
        train_ds.shuffle(len(train_ds), seed=SEED + 1)
    )

    train_ds = (
        tf.data.Dataset.zip((train_ds_one, train_ds_two))
        .map(cutmix_chances, num_parallel_calls=tf.data.AUTOTUNE)
        .batch(BATCH_SIZE, drop_remainder=True)
    )

# Training set if cutmix is not used
else:
    train_ds = train_ds.batch(BATCH_SIZE)

# Extract class (genre) names, save for reference
print("Classes:", class_names)
with open("class_names.json", "w") as f:
    json.dump(class_names, f)

# ----- PREPROCESSING -----
train_ds = train_ds.map(lambda x, y: (preprocess_input(x), y)).cache()
val_ds   = val_ds.map(lambda x, y: (preprocess_input(x), y)).cache()
test_ds  = test_ds.map(lambda x, y: (preprocess_input(x), y)).cache()

# Spectrogram Augmentation on training data (comment out if desired)
if USE_SPECAUG:
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
    loss=LOSS,
    metrics=['accuracy']
)

# model.summary()  # Optional, prints architecture of the model

callbacks = [
    # Early Stopping
    tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True
    )
]

# ----- TRAIN MODEL -----
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=TRAINING_EPOCHS,
    callbacks=callbacks
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
    loss=LOSS,
    metrics=['accuracy']
)

# Fine-tuning (Note: separate instances required — EarlyStopping is stateful)
callbacks_finetune = [
    # Early Stopping
    tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True
    )
]

# Train again
model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=FINE_TUNE_EPOCHS,
    callbacks=callbacks_finetune
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

        if LABEL_MODE == 'categorical':
            label = np.argmax(y.numpy(), axis=1)
        else:
            label = y.numpy()

        embeddings.append(emb)
        labels.append(label)
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

# F1 Score
macro_f1 = f1_score(y_true, y_pred, average="macro")
print(f"F1 Score: {macro_f1}")

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
        if LABEL_MODE == 'categorical':
            labels.append(np.argmax(y.numpy(), axis=1))
        else:
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