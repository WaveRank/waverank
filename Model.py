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
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ----- CONFIGURATION -----
DATASET_PATH = "dataset/"
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
TRAINING_EPOCHS = 10
FINE_TUNE_EPOCHS = 5

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

# Extract class (genre) names
class_names = train_ds.class_names
print("Classes:", class_names)

# ----- PREPROCESSING -----
train_ds = train_ds.map(lambda x, y: (preprocess_input(x), y))
val_ds   = val_ds.map(lambda x, y: (preprocess_input(x), y))
test_ds  = test_ds.map(lambda x, y: (preprocess_input(x), y))

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
x = layers.Dropout(0.5)(embedding)
outputs = layers.Dense(len(class_names), activation='softmax')(x)

# Build and compile model
model = tf.keras.Model(inputs=base_model.input, outputs=outputs)
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)
# model.summary()  # Optional, prints architecture of the model

# ----- TRAIN MODEL -----
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
