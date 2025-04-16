import numpy as np
import pickle
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import (
    Activation, Dropout, UpSampling2D, Conv2D, MaxPooling2D, Conv2DTranspose, BatchNormalization
)
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import mlflow
import mlflow.keras
import logging

logging.basicConfig(level=logging.INFO)

def build_lane_detection_model(input_shape, pool_size):
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

    model.add(Conv2DTranspose(1, (3, 3), activation='sigmoid', padding='valid'))  # 使用 sigmoid 以便后续支持 IoU

    return model


def train_lane_detection_model():
    logging.info("Starting training pipeline")

    train_images = pickle.load(open("full_CNN_train.p", "rb"))
    labels = pickle.load(open("full_CNN_labels.p", "rb"))

    train_images = np.array(train_images)
    labels = np.array(labels) / 255.0

    train_images, labels = shuffle(train_images, labels)
    X_train, X_val, y_train, y_val = train_test_split(train_images, labels, test_size=0.1)

    batch_size = 128
    epochs = 10
    pool_size = (2, 2)
    input_shape = X_train.shape[1:]

    model = build_lane_detection_model(input_shape, pool_size)
    data_gen = ImageDataGenerator(channel_shift_range=0.2)
    data_gen.fit(X_train)

    model.compile(optimizer='adam', loss='mean_squared_error')

    # Start MLflow tracking here
    with mlflow.start_run(run_name="LaneDetection_CNN"):
        mlflow.log_param("batch_size", batch_size)
        mlflow.log_param("epochs", epochs)
        mlflow.log_param("loss", "mean_squared_error")
        mlflow.log_param("pool_size", pool_size)

        history = model.fit(
            data_gen.flow(X_train, y_train, batch_size=batch_size),
            steps_per_epoch=len(X_train) // batch_size,
            epochs=epochs,
            validation_data=(X_val, y_val)
        )

        # Log metrics
        final_loss = history.history["loss"][-1]
        val_loss = history.history["val_loss"][-1]
        mlflow.log_metric("final_loss", final_loss)
        mlflow.log_metric("val_loss", val_loss)

        # Save model
        model_path = "full_CNN_model.h5"
        model.save(model_path)
        mlflow.keras.log_model(model, "model")

        mlflow.log_artifact(model_path)

        logging.info(f"Training completed with val_loss={val_loss}")

        model.summary()

if __name__ == '__main__':
    train_lane_detection_model()
