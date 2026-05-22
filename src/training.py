import config as cfg
import tensorflow as tf


# ----- TRAINING -----
def get_callbacks(phase):
    """
    Organizes a list of keras callbacks for a specified training phase.
    Callbacks include EarlyStopping and ReduceLROnPlateau with desired
    settings for initial and fine tune training.
    """
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
                patience=5,
                min_lr=1e-8
            )
        ]

    return callbacks


def initial_train(model, train_ds, val_ds):
    """
    Compiles and and trains model for initial training phase.
    Uses INITIAL_LEARNING_RATE and TRAINING_EPOCHS, and gets callbacks
    for phase 1.

    Returns:
        - training history: metric values recorded during training
        - model: updated model with weights
    """
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=cfg.INITIAL_LEARNING_RATE),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=cfg.TRAINING_EPOCHS,
        callbacks=get_callbacks(phase=1)
    )

    return model, history


def fine_tune(model, base_model, train_ds, val_ds):
    """
    Compiles and trains model for fine tuning phase.
    Unfreezes the entire base model and re-freeze outside depth 
    to fine-tune specific layers.
    Uses FINE_LEARNING_RATE, WEIGHT_DECAY, DEPTH, and gets callbacks 
    for phase 2.
    """
    base_model.trainable = True

    # Fine-tune only last layers
    for layer in base_model.layers[:-cfg.DEPTH]:
        layer.trainable = False

    # Freeze BatchNormalization layers
    for layer in base_model.layers:
        if isinstance(layer, tf.keras.layers.BatchNormalization):
            layer.trainable = False

    # Recompile with lower learning rate
    model.compile(
        optimizer=tf.keras.optimizers.Adam(cfg.FINE_LEARNING_RATE, weight_decay=cfg.WEIGHT_DECAY),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    # Train again
    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=cfg.FINE_TUNE_EPOCHS,
        callbacks=get_callbacks(phase=2)
    )

    return model