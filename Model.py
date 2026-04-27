"""
Builds an image classification model using a pretrained ResNet50 backbone.

Citations (4/9/26):
https://www.tensorflow.org/api_docs/python/tf/keras/applications/resnet/preprocess_input
https://www.tensorflow.org/api_docs/python/tf/keras/applications/ResNet50
https://www.tensorflow.org/api_docs/python/tf/keras/preprocessing/image_dataset_from_directory
https://www.tensorflow.org/guide/data_performance
https://www.tensorflow.org/guide/keras/functional_api
https://www.tensorflow.org/guide/keras/transfer_learning
https://stackoverflow.com/questions/67171002/how-to-build-a-tensorflow-model-with-more-than-one-input
https://stackoverflow.com/questions/48889482/feeding-npy-numpy-files-into-tensorflow-data-pipeline
https://stackoverflow.com/questions/40666316/how-to-get-tensorflow-tensor-dimensions-shape-as-int-values
https://www.tensorflow.org/guide/data

Citation (4/12/26):
https://keras.io/guides/functional_api/#extract-and-reuse-nodes-in-the-graph

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
from tensorflow.keras import layers, models
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras import Input
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json

# ----- CONFIGURATION -----
DATASET_PATH = "dataset/"
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
TRAINING_EPOCHS = 10
FINE_TUNE_EPOCHS = 5

# Get features statistics for normalization
FEAT_STD  = tf.constant(np.load("feat_std.npy"), dtype=tf.float32)
FEAT_MEAN = tf.constant(np.load("feat_mean.npy"), dtype=tf.float32)
FEAT_SIZE = FEAT_MEAN.shape.as_list()[0]

# Set global random seed for reproducibility
SEED = 42
os.environ["PYTHONHASHSEED"] = str(SEED)
random.seed(SEED)
np.random.seed(SEED)
tf.random.set_seed(SEED)

# ----- LOAD DATASETS -----

def load_npy(path):
    path = path.item() if isinstance(path, np.ndarray) else path
    path = path.decode("utf-8") if isinstance(path, bytes) else path
    return np.load(path).astype(np.float32)

def load_img(path):
    image = tf.io.read_file(path)
    image = tf.image.decode_png(image, channels=3)
    return image

def load_sample(base_path: str, label):
    """Takes a file path (without extension) and genre label.
    Returns a tuple of ((image, features tensor), genre label).
    """
    img_path  = tf.strings.join([base_path, ".png"])
    feat_path = tf.strings.join([base_path, ".npy"])

    image = load_img(img_path)
    image = tf.image.resize(image, IMG_SIZE)
    image = preprocess_input(image)

    feat = tf.numpy_function(load_npy, [feat_path], tf.float32)
    feat.set_shape([FEAT_SIZE])
    feat = (feat - FEAT_MEAN) / FEAT_STD

    # feat = tf.zeros_like(feat)  # Uncomment this line to zero out (~disable) features

    return (image, feat), label
    # return image, label


def build_file_list(split_dir, label_map):
    """ 
    Takes one of the split dataset directories (train, val, test)
    Expects genre subdirectories in split_dir which contain the .png and .npy files.
    """
    base_paths = []
    labels = []

    for class_name, label in label_map.items():
        class_dir = os.path.join(split_dir, class_name)

        for file in sorted(os.listdir(class_dir)):
            if file.endswith(".png"):
                base = file[:-4]
                base_path = os.path.join(class_dir, base)

                if not os.path.exists(base_path + ".npy"):
                    continue

                base_paths.append(base_path)
                labels.append(label)

    return base_paths, labels


def build_dataset(paths, labels, training=False):
    ds = tf.data.Dataset.from_tensor_slices((paths, labels))
    if training:
        ds = ds.shuffle(buffer_size=len(paths), seed=SEED)
    ds = ds.map(load_sample, num_parallel_calls=tf.data.AUTOTUNE)
    ds = ds.batch(BATCH_SIZE)
    ds = ds.prefetch(tf.data.AUTOTUNE)
    return ds


# Extract class (genre) names, save for reference
class_names = sorted(os.listdir(DATASET_PATH + "train"))
label_map = {name: i for i, name in enumerate(class_names)}
print("Classes:", class_names)
with open("class_names.json", "w") as f:
    json.dump(class_names, f)

# ----- LOAD DATASETS -----
train_paths, train_labels = build_file_list(DATASET_PATH + "train", label_map)
val_paths, val_labels = build_file_list(DATASET_PATH + "val", label_map)
test_paths, test_labels = build_file_list(DATASET_PATH + "test", label_map)

print("Loading Training Set:")
train_ds = build_dataset(train_paths, train_labels, training=True)

# debug
# for (img, feat), y in train_ds.take(1):
#     print(img.shape)
#     print(feat.shape)
#     print(feat[0])  # actual values


print("Loading Validation Set:")
val_ds   = build_dataset(val_paths, val_labels, training=True)
print("Loading Test Set:")
test_ds  = build_dataset(test_paths, test_labels)


# ----- BUILD MODEL -----
base_model = ResNet50(
    weights='imagenet',
    include_top=False,
    input_shape=(*IMG_SIZE, 3)
)
base_model.trainable = False

# Combine image input and feature input
image_input = base_model.input
x = base_model.output
x = layers.GlobalAveragePooling2D()(x)

feature_input = Input(shape=(FEAT_SIZE,))
f = layers.BatchNormalization()(feature_input)
# f = layers.Dense(128, activation='relu')(f)

# Project image and feature inputs into the same space to give them similar weight
x_proj = layers.Dense(256, activation='relu')(x)
f_proj = layers.Dense(256, activation='relu')(f)

combined = layers.concatenate([x_proj, f_proj])
# combined = x

# Embedding Layer
embedding = layers.Dense(128, activation='relu', name="embedding")(combined)
x = layers.Dropout(0.5)(embedding)
output = layers.Dense(len(class_names), activation='softmax')(x)

# Build and compile model
model = tf.keras.Model(inputs=[image_input, feature_input], outputs=output)
# model = tf.keras.Model(inputs=image_input, outputs=output)
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)
# model.summary()  # Optional, prints architecture of the model

# ----- TRAIN MODEL -----

# debug 
for _, y in train_ds.take(3):
    print(np.bincount(y.numpy(), minlength=10))

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=TRAINING_EPOCHS
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
for layer in base_model.layers[:-50]:
    layer.trainable = False

# Recompile with lower learning rate
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Train again
model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=FINE_TUNE_EPOCHS
)

# Evaluate
test_loss, test_acc = model.evaluate(test_ds)
print("Test accuracy after fine-tuning:", test_acc)

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

    for (images, features), y in dataset:
    # for images, y in dataset:
        # Embedding vectors and class probabilities
        emb = emb_model.predict([images, features], verbose=0)
        prob = clf_model.predict([images, features], verbose=0)
        # emb = emb_model.predict(images, verbose=0)
        # prob = clf_model.predict(images, verbose=0)

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

    for (images, features), y in dataset:
    # for images, y in dataset:
        # Class probabilities
        prob = clf_model.predict([images, features], verbose=0)
        # prob = clf_model.predict(images, verbose=0)
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