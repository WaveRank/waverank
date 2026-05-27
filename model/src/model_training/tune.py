"""
Hyperparameter tuning script used for CNN model optimization using Optuna.

Performs automated hyperparameter optimization across multiple training trials
to identify the optimal model configuration. Bayesian Optimization is used to
explore and adaptively select the best hyperparameter combinations per trial.

The tunable parameters include the initial LR, fine-tune LR, dropout rate,
depth, spec augmentation masking widths, cutmix probability...
"""
import os
os.environ["TF_DETERMINISTIC_OPS"] = "1"

import optuna
import tensorflow as tf

import model.config as cfg
from model.src.model_training.model import build_model
from model.src.model_training.dataset import get_datasets
from model.src.model_training.training import initial_train, fine_tune


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
    _, test_acc = model.evaluate(test_ds)
    print("Test accuracy:", test_acc)

    # Fine tuning
    model = fine_tune(model, base_model, train_ds, val_ds)
    _, test_acc = model.evaluate(test_ds)
    print("Test accuracy after fine-tuning:", test_acc)

    # Evaluate model for val accuracy
    _, val_acc = model.evaluate(val_ds)
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
    cfg.INITIAL_LEARNING_RATE = trials.suggest_float("initial_lr", 1e-4, 5e-4, log=True)
    cfg.FINE_LEARNING_RATE = trials.suggest_float("fine_lr", 1e-5, 1e-4, log=True)
    cfg.DROPOUT_RATE = trials.suggest_float("dropout", 0.4, 0.7, step=0.1)
    cfg.DEPTH = trials.suggest_int("depth", 60, 100)

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
    print(f"VAL ACCURACY          = {study.best_trial.value}")
    print(f"INITIAL_LEARNING_RATE = {study.best_trial.params['initial_lr']}")
    print(f"FINE_LEARNING_RATE    = {study.best_trial.params['fine_lr']}")
    print(f"DROPOUT_RATE          = {study.best_trial.params['dropout']}")
    print(f"DEPTH                 = {study.best_trial.params['depth']}")

    # Top 5 trial stats
    trials = sorted(study.trials, key=lambda t: t.value, reverse=True)[:5]
    for i, trial in enumerate(trials):
        print(f"\nRank {i+1} (Trial {trial.number}):")
        print(f"  VAL ACCURACY: {trial.value}")
        for key, value in trial.params.items():
            print(f"  {key}: {value}")


if __name__ == "__main__":
    optimization()