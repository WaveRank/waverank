import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.applications import ResNet50
from config import *


def build_model(class_names):
    """
    Builds the ResNet50 model and sets up the layers
    """
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

    model = tf.keras.Model(inputs=base_model.input, outputs=outputs)
    
    return base_model, model