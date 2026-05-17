import matplotlib.pyplot as plt
import tensorflow as tf
import pandas as pd
import numpy as np
import os
from config import *


def embedding_model(model):
    """
    Creates and returns a 128 dimensional embedding vector from the 
    dense embedding layer. Used for visualizations.
    """
    return tf.keras.Model(
        inputs=model.input,
        outputs=model.get_layer("embedding").output
    )


# Extract embeddings
def extract_embeddings(dataset, emb_model, clf_model):
    """
    Extracts embeddings, predictions, and confidence scores from dataset.
    """
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

        embeddings.append(emb)
        labels.append(np.argmax(y.numpy(), axis=1))
        preds.append(pred)
        confidences.append(prob)

    # Combine into single arrays
    return (
        np.vstack(embeddings),
        np.hstack(labels),
        np.hstack(preds),
        np.vstack(confidences)
    )


def save_embeddings(test_ds, emb_model, clf_model, class_names):
    """
    Extracts embeddings which are used to create a DataFrame structure with metadata
    columns and saved as a CSV file.
    Saves a CSV of the 128 dimensional vector and another for confidence values.
    """
    x_emb, y_true, y_pred, conf = extract_embeddings(
        test_ds,
        emb_model,
        clf_model
    )

    # Add metadata columns
    emb_df = pd.DataFrame(x_emb)
    emb_df["label"] = y_true
    emb_df["pred"] = y_pred
    emb_df["confidence"] = np.max(conf, axis=1)
    emb_df["label_name"] = [class_names[i] for i in y_true]
    emb_df["pred_name"] = [class_names[i] for i in y_pred]

    # Save to CSV
    emb_df.to_csv(os.path.join(BASE_PATH, "embeddings.csv"), index=False)
    print("Saved embeddings.csv")

    conf_df = pd.DataFrame(conf)
    conf_df.columns = class_names
    conf_df["label"] = y_true
    conf_df["label_name"] = [class_names[i] for i in y_true]

    # Save to CSV
    conf_df.to_csv(os.path.join(BASE_PATH, "confidences.csv"), index=False)
    print("Saved confidences.csv")


def save_curves(history):
    """
    Plots and saves training curves for accuracy and loss of both the 
    training and validation values
    """
    # Plot and save training curves
    plt.figure()
    plt.plot(history.history['accuracy'], label='train')
    plt.plot(history.history['val_accuracy'], label='val')
    plt.legend()
    plt.title("Accuracy")
    plt.savefig(os.path.join(BASE_PATH, "accuracy_curve.png"), dpi=300)
    print("Saved accuracy_curve.png")
    plt.close()

    plt.figure()
    plt.plot(history.history['loss'], label='train')
    plt.plot(history.history['val_loss'], label='val')
    plt.legend()
    plt.title("Loss")
    plt.savefig(os.path.join(BASE_PATH, "loss_curve.png"), dpi=300)
    print("Saved loss_curve.png")
    plt.close()


def evaluate_model(model, test_ds, phase):
    """
    Evaluates the trained model on the test dataset.

    Returns:
        - test loss: loss value measuring how correct predictions are
        - test acc: percentage of test samples the model classified correctly
    """
    test_loss, test_acc = model.evaluate(test_ds)
    if phase == 1:
        print("Test accuracy:", test_acc)
    elif phase == 2:
        print("Test accuracy after fine-tuning:", test_acc)

    return test_loss, test_acc