"""
This script implements a fully convolutional neural network (CNN) 
for detecting lane markings in road images. The input images are 
expected to be 80x160x3 (RGB), and the labels are 80x160x1 (single 
G channel with lane markings). The output is overlaid onto the 
original image for visualization.
"""

import numpy as np
import pickle
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from keras.models import Sequential, load_model
from keras.layers import (
    Activation, Dropout, UpSampling2D, Conv2D, MaxPooling2D, Conv2DTranspose, BatchNormalization
)
from tensorflow.keras.preprocessing.image import ImageDataGenerator


def build_lane_detection_model(input_shape, pool_size):
    """
    Constructs a fully convolutional neural network (CNN) 
    for lane detection.

    Parameters:
    - input_shape (tuple): The shape of the input image (height, width, channels).
    - pool_size (tuple): Pooling size for max-pooling layers.

    Returns:
    - model (keras.models.Sequential): The compiled CNN model.
    """
    model = Sequential()

    # Input normalization
    model.add(BatchNormalization(input_shape=input_shape))

    # Convolutional layers with ReLU activations
    model.add(Conv2D(8, (3, 3), activation='relu', padding='valid', name='Conv1'))
    model.add(Conv2D(16, (3, 3), activation='relu', padding='valid', name='Conv2'))
    model.add(MaxPooling2D(pool_size=pool_size))

    model.add(Conv2D(16, (3, 3), activation='relu', padding='valid', name='Conv3'))
    model.add(Dropout(0.2))
    model.add(Conv2D(32, (3, 3), activation='relu', padding='valid', name='Conv4'))
    model.add(Dropout(0.2))
    model.add(Conv2D(32, (3, 3), activation='relu', padding='valid', name='Conv5'))
    model.add(Dropout(0.2))
    model.add(MaxPooling2D(pool_size=pool_size))

    model.add(Conv2D(64, (3, 3), activation='relu', padding='valid', name='Conv6'))
    model.add(Dropout(0.2))
    model.add(Conv2D(64, (3, 3), activation='relu', padding='valid', name='Conv7'))
    model.add(Dropout(0.2))
    model.add(MaxPooling2D(pool_size=pool_size))

    # Upsampling and transposed convolutions for lane reconstruction
    model.add(UpSampling2D(size=pool_size))
    model.add(Conv2DTranspose(64, (3, 3), activation='relu', padding='valid', name='Deconv1'))
    model.add(Dropout(0.2))
    model.add(Conv2DTranspose(64, (3, 3), activation='relu', padding='valid', name='Deconv2'))
    model.add(Dropout(0.2))

    model.add(UpSampling2D(size=pool_size))
    model.add(Conv2DTranspose(32, (3, 3), activation='relu', padding='valid', name='Deconv3'))
    model.add(Dropout(0.2))
    model.add(Conv2DTranspose(32, (3, 3), activation='relu', padding='valid', name='Deconv4'))
    model.add(Dropout(0.2))
    model.add(Conv2DTranspose(16, (3, 3), activation='relu', padding='valid', name='Deconv5'))
    model.add(Dropout(0.2))

    model.add(UpSampling2D(size=pool_size))
    model.add(Conv2DTranspose(16, (3, 3), activation='relu', padding='valid', name='Deconv6'))

    # Final layer for lane segmentation (1-channel output)
    model.add(Conv2DTranspose(1, (3, 3), activation='relu', padding='valid', name='Output'))

    return model


def train_lane_detection_model():
    """
    Loads the dataset, preprocesses it, and trains the CNN model.
    """

    # Load training data
    train_images = pickle.load(open("full_CNN_train.p", "rb"))
    labels = pickle.load(open("full_CNN_labels.p", "rb"))

    # Convert to numpy arrays
    train_images = np.array(train_images)
    labels = np.array(labels) / 255  # Normalize labels

    # Shuffle and split dataset
    train_images, labels = shuffle(train_images, labels)
    X_train, X_val, y_train, y_val = train_test_split(train_images, labels, test_size=0.1)

    # Training parameters
    batch_size = 128
    epochs = 10
    pool_size = (2, 2)
    input_shape = X_train.shape[1:]

    # Build the CNN model
    model = build_lane_detection_model(input_shape, pool_size)

    # Data augmentation using image generator
    data_gen = ImageDataGenerator(channel_shift_range=0.2)
    data_gen.fit(X_train)

    # Compile the model
    model.compile(optimizer='Adam', loss='mean_squared_error')

    # Train the model
    model.fit(data_gen.flow(X_train, y_train, batch_size=batch_size), 
              steps_per_epoch=len(X_train) // batch_size, 
              epochs=epochs, 
              validation_data=(X_val, y_val))

    # Save the trained model
    model.save('full_CNN_model.h5')

    # Display model summary
    model.summary()


if __name__ == '__main__':
    train_lane_detection_model()
