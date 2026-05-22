from pathlib import Path
import json
import numpy as np
import src.config as cfg
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import preprocess_input


# ----- LOAD DATASETS -----
def load_dataset(set, shuffle=False):
    """
    Loads training, validation, and testing datasets
    """
    
    print(f"Loading {set} set...")
    
    return tf.keras.utils.image_dataset_from_directory(
    	cfg.DATASET_PATH / set,
    	image_size=cfg.IMG_SIZE,
    	batch_size=None,
    	shuffle=shuffle,
    	label_mode='categorical'
    )


def get_datasets():
    """
    Prepares the train, validation, and test datasets for training.
    Applies shuffling, optional augmentations (CutMix, Spectrogram Augmentation), 
    and prefetch autotune for performance. 

    Returns:
        - Train dataset
        - Validation dataset
        - Test dataset
        - Class names
    """
    train_ds = load_dataset("train", shuffle=True)
    val_ds = load_dataset("val", shuffle=True).batch(cfg.BATCH_SIZE)
    test_ds = load_dataset("test").batch(cfg.BATCH_SIZE)

    # Extract class (genre) names, save for reference
    class_names = train_ds.class_names
    print("Classes:", class_names)
    with open(cfg.BASE_PATH / "class_names.json", "w") as f:
        json.dump(class_names, f)

    if cfg.USE_CUTMIX:
        train_ds_one = (
            train_ds.shuffle(len(train_ds), seed=cfg.SEED)
        )

        train_ds_two = (
            train_ds.shuffle(len(train_ds), seed=cfg.SEED + 1)
        )

        train_ds = (
            tf.data.Dataset.zip((train_ds_one, train_ds_two))
            .map(cutmix_chances, num_parallel_calls=tf.data.AUTOTUNE)
            .batch(cfg.BATCH_SIZE, drop_remainder=True)
        )

    # Training set if cutmix is not used
    else:
        train_ds = train_ds.batch(cfg.BATCH_SIZE)

    # ----- PREPROCESSING -----
    train_ds = train_ds.map(lambda x, y: (preprocess_input(x), y)).cache()
    val_ds   = val_ds.map(lambda x, y: (preprocess_input(x), y)).cache()
    test_ds  = test_ds.map(lambda x, y: (preprocess_input(x), y)).cache()

    # Spectrogram Augmentation on training data
    if cfg.USE_SPECAUG:
        train_ds = train_ds.map(spec_augment)

    # Prefetch (improves performance)
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.prefetch(AUTOTUNE)
    val_ds   = val_ds.prefetch(AUTOTUNE)
    test_ds  = test_ds.prefetch(AUTOTUNE)

    return train_ds, val_ds, test_ds, class_names


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
        shape=[], maxval=cfg.FREQ_MASK_WIDTH, dtype=tf.dtypes.int32
    )
    freq_start = tf.random.uniform(
        shape=[], maxval=cfg.IMG_SIZE[0] - freq_width, dtype=tf.dtypes.int32
    )
    time_width = tf.random.uniform(
        shape=[], maxval=cfg.TIME_MASK_WIDTH, dtype=tf.dtypes.int32
    )
    time_start = tf.random.uniform(
        shape=[], maxval=cfg.IMG_SIZE[1] - time_width, dtype=tf.dtypes.int32
    )

    # Draw frequency and time masks
    freq_mask = tf.concat(
        [
            tf.ones([freq_start, cfg.IMG_SIZE[1], 3]),
            tf.zeros([freq_width, cfg.IMG_SIZE[1], 3]),
            tf.ones([cfg.IMG_SIZE[0] - freq_start - freq_width, cfg.IMG_SIZE[1], 3]),
        ],
        0,
    )
    time_mask = tf.concat(
        [
            tf.ones([cfg.IMG_SIZE[0], time_start, 3]),
            tf.zeros([cfg.IMG_SIZE[0], time_width, 3]),
            tf.ones([cfg.IMG_SIZE[0], cfg.IMG_SIZE[1] - time_start - time_width, 3]),
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
    
    beta_dist = np.random.beta(cfg.ALPHA, cfg.ALPHA)
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

    img_h, img_w = cfg.IMG_SIZE[0], cfg.IMG_SIZE[1]

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

    probability = tf.random.uniform([]) < cfg.CUTMIX_PROB

    return tf.cond(
        probability,
        lambda: cutmix(train_ds_one, train_ds_two),
        lambda: (image1, label1)
    )
