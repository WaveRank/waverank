import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.applications import ResNet50

import model.config as cfg


def build_model(class_names):
    """
    Builds the ResNet50 base model initialized with ImageNet weights.
    The model is frozen for the initial training and adds a 
    GlobalAveragePooling2D layer, 128 dense embedding layer, and
    DROPOUT regularization. 

    Args:
        - class_names: a list of the genre class labels for output size

    Returns:
        - base_model: ResNet50 base model instance
        - model: fully compiled keras model for training
    """
    base_model = ResNet50(
        weights='imagenet',
        include_top=False,
        input_shape=(*cfg.IMG_SIZE, 3)
    )
    base_model.trainable = False

    # Extract and pool features
    x = base_model.output
    x = layers.GlobalAveragePooling2D()(x)

    # Embedding layer
    embedding = layers.Dense(128, activation='relu', name="embedding")(x)
    x = layers.Dropout(cfg.DROPOUT_RATE)(embedding)
    outputs = layers.Dense(len(class_names), activation='softmax')(x)

    model = tf.keras.Model(inputs=base_model.input, outputs=outputs)
    
    return base_model, model