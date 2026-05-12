import tensorflow as tf
from config import *


def get_callbacks(phase):
    if phase == 1:
        callbacks = [
            # Early Stopping
            tf.keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=5,
                restore_best_weights=True
            ),

            # Reduce LR
            tf.keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-6
            )
        ]

    elif phase == 2:
        callbacks = [
            # Early Stopping
            tf.keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=5,
                restore_best_weights=True
            ),

            # Reduce LR
            tf.keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.3,
                patience=7,
                min_lr=1e-8
            )
        ]

    return callbacks


def initial_train(model, train_ds, val_ds):
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=INITIAL_LEARNING_RATE),
        loss=LOSS,
        metrics=['accuracy']
    )

    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=TRAINING_EPOCHS,
        callbacks=get_callbacks(1)
    )

    return history


def fine_tune(model, base_model, train_ds, val_ds):
    base_model.trainable = True

    # Fine-tune only last layers
    for layer in base_model.layers[:-DEPTH]:
        layer.trainable = False

    # Recompile with lower learning rate
    model.compile(
        optimizer=tf.keras.optimizers.Adam(FINE_LEARNING_RATE, weight_decay=WEIGHT_DECAY),
        loss=LOSS,
        metrics=['accuracy']
    )

    # Train again
    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=FINE_TUNE_EPOCHS,
        callbacks=get_callbacks(2)
    )

    return model