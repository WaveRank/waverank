"""
Hyperparameter tuning script used for CNN model optimization using Optuna.

Performs automated hyperparameter optimization across multiple training trials
to identify the optimal model configuration. Bayesian Optimization is used to
explore and adaptively select the best hyperparameter combinations per trial.

The tunable parameters include the initial LR, fine-tune LR, dropout rate,
depth, spec augmentation masking widths, cutmix probability...
"""

import optuna
import config as cfg
import tensorflow as tf
from model import build_model
from dataset import get_datasets
from sklearn.metrics import f1_score
from training import initial_train, fine_tune
from evaluate import extract_embeddings, embedding_model


def tuning_pipeline():
    """
    Follows the main model pipeline with the exception of embedding extractions
    and other visualizations.
    """
    # Set global random seed for reproducibility
    cfg.set_seeds()

    # DATA
    train_ds, val_ds, test_ds, class_names = get_datasets()

    # MODEL
    base_model, model = build_model(class_names)

    # Initial training
    model, history = initial_train(model, train_ds, val_ds)
    test_loss, test_acc = model.evaluate(test_ds)
    print("Test accuracy:", test_acc)

    # Fine tuning
    model = fine_tune(model, base_model, train_ds, val_ds)
    test_loss, test_acc = model.evaluate(test_ds)
    print("Test accuracy after fine-tuning:", test_acc)

    # Evaluate model for val accuracy
    val_loss, val_acc = model.evaluate(val_ds)
    print("Val accuracy:", val_acc)

    return val_acc


def optimize_config(trials):
    """
    Configures the chosen hyperparameters for each trial by using values
    from a defined search range. 

    Args:
        - trials: trial object from optuna

    Returns:
        - Val accuracy from model
    """
    # Reset tf internal state between trials
    tf.keras.backend.clear_session()

    # Configure sample float/int values on a given range per trial
    cfg.INITIAL_LEARNING_RATE = trials.suggest_float("initial_lr", 1e-5, 1e-3, log=True)
    cfg.FINE_LEARNING_RATE = trials.suggest_float("fine_lr", 1e-4, 5e-4, log=True)
    cfg.DROPOUT_RATE = trials.suggest_float("dropout", 0.2, 0.6)
    cfg.DEPTH = trials.suggest_int("depth", 50, 175)

    return tuning_pipeline()


def optimization():
    """
    Creates and runs the optuna study using Bayesian Optimization.
    Searches for best hyperparameters across N_TRIALS and prints
    the best performing results.
    """
    # Initialize optuna study to track trials
    study = optuna.create_study(direction="maximize", sampler=optuna.samplers.TPESampler(seed=cfg.SEED))
    study.optimize(optimize_config, n_trials=cfg.N_TRIALS)

    # Best trial stats
    print("\nBEST TRIAL RUN:")
    print(f"Val acc: {study.best_trial.value}")
    print(f"Params:  {study.best_trial.params}")

    print("\nBEST HYPERPARAMETERS:")
    print(f"INITIAL_LEARNING_RATE = {study.best_trial.params['initial_lr']}")
    print(f"FINE_LEARNING_RATE    = {study.best_trial.params['fine_lr']}")
    print(f"DROPOUT_RATE          = {study.best_trial.params['dropout']}")
    print(f"DEPTH                 = {study.best_trial.params['depth']}")


if __name__ == "__main__":
    optimization()