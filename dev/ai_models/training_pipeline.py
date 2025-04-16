import logging
import os
import pickle

import mlflow
import mlflow.keras
import numpy as np
from keras.layers import *
from keras.models import Sequential
from keras.src.layers import BatchNormalization, Conv2D, Dropout, MaxPooling2D, \
    UpSampling2D, Conv2DTranspose
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from tensorflow.keras.preprocessing.image import ImageDataGenerator

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def build_lane_model(input_shape, pool_size):
    """
    Build a CNN model for lane detection using a fully convolutional architecture.

    Args:
        input_shape (tuple): Shape of input images.
        pool_size (tuple): Size of pooling layers.

    Returns:
        keras.models.Sequential: Compiled model architecture.
    """
    model = Sequential()
    model.add(BatchNormalization(input_shape=input_shape))
    model.add(Conv2D(8, (3, 3), activation='relu', padding='valid'))
    model.add(Conv2D(16, (3, 3), activation='relu', padding='valid'))
    model.add(MaxPooling2D(pool_size=pool_size))
    model.add(Conv2D(16, (3, 3), activation='relu', padding='valid'))
    model.add(Dropout(0.2))
    model.add(Conv2D(32, (3, 3), activation='relu', padding='valid'))
    model.add(Dropout(0.2))
    model.add(Conv2D(32, (3, 3), activation='relu', padding='valid'))
    model.add(Dropout(0.2))
    model.add(MaxPooling2D(pool_size=pool_size))
    model.add(Conv2D(64, (3, 3), activation='relu', padding='valid'))
    model.add(Dropout(0.2))
    model.add(Conv2D(64, (3, 3), activation='relu', padding='valid'))
    model.add(Dropout(0.2))
    model.add(MaxPooling2D(pool_size=pool_size))
    model.add(UpSampling2D(size=pool_size))
    model.add(Conv2DTranspose(64, (3, 3), activation='relu', padding='valid'))
    model.add(Dropout(0.2))
    model.add(Conv2DTranspose(64, (3, 3), activation='relu', padding='valid'))
    model.add(Dropout(0.2))
    model.add(UpSampling2D(size=pool_size))
    model.add(Conv2DTranspose(32, (3, 3), activation='relu', padding='valid'))
    model.add(Dropout(0.2))
    model.add(Conv2DTranspose(32, (3, 3), activation='relu', padding='valid'))
    model.add(Dropout(0.2))
    model.add(Conv2DTranspose(16, (3, 3), activation='relu', padding='valid'))
    model.add(Dropout(0.2))
    model.add(UpSampling2D(size=pool_size))
    model.add(Conv2DTranspose(16, (3, 3), activation='relu', padding='valid'))
    model.add(Conv2DTranspose(1, (3, 3), activation='sigmoid', padding='valid'))
    return model


def train_lane_detection_model(batch_size=128, epochs=10):
    """
    Train the lane detection model and log metrics and model to MLflow.

    Args:
        batch_size (int): Number of samples per training batch.
        epochs (int): Number of training epochs.

    Returns:
        dict: Final loss and validation loss.
    """
    logger.info("🚦 Starting lane detection training pipeline")

    # Load dataset
    cur_path = os.path.abspath(os.path.dirname(__file__))
    model_path = os.path.join(cur_path, "../../model")

    train_images = pickle.load(open(os.path.join(model_path, "full_CNN_train.p"), "rb"))
    labels = pickle.load(open(os.path.join(model_path, "full_CNN_labels.p"), "rb"))

    train_images = np.array(train_images)
    labels = np.array(labels) / 255.0
    train_images, labels = shuffle(train_images, labels)

    X_train, X_val, y_train, y_val = train_test_split(train_images, labels, test_size=0.1)
    input_shape = X_train.shape[1:]
    pool_size = (2, 2)

    # Build and compile model
    model = build_lane_model(input_shape, pool_size)
    data_gen = ImageDataGenerator(channel_shift_range=0.2)
    data_gen.fit(X_train)
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Start MLflow run
    with mlflow.start_run(run_name="LaneDetection_Training"):
        mlflow.log_param("batch_size", batch_size)
        mlflow.log_param("epochs", epochs)
        mlflow.log_param("loss", "mean_squared_error")

        # Train model
        history = model.fit(data_gen.flow(X_train, y_train, batch_size=batch_size),
                            steps_per_epoch=len(X_train) // batch_size,
                            epochs=epochs,
                            validation_data=(X_val, y_val))

        # Log final metrics
        mlflow.log_metric("final_loss", history.history['loss'][-1])
        mlflow.log_metric("val_loss", history.history['val_loss'][-1])

        # Log full model
        mlflow.keras.log_model(model, "model")

        logger.info("✅ Training completed and model logged to MLflow")

    return {
        "loss": history.history['loss'][-1],
        "val_loss": history.history['val_loss'][-1]
    }
