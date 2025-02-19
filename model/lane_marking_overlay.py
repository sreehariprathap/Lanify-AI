import numpy as np
import cv2
from PIL import Image
from moviepy.editor import VideoFileClip
from keras.models import load_model


class LaneDetector:
    """
    A class to handle lane detection and averaging lane predictions.
    """

    def __init__(self, model_path='full_CNN_model.h5'):
        """
        Initializes the lane detector with a pre-trained model.

        Parameters:
        model_path (str): Path to the pre-trained Keras model.
        """
        self.model = load_model(model_path, compile=False, custom_objects={})
        self.recent_predictions = []
        self.avg_lane_prediction = []

    @staticmethod
    def resize_image(image_array, target_size):
        """
        Resize an image array to a given target size.

        Parameters:
        image_array (numpy.ndarray): Input image array.
        target_size (tuple): Target size (width, height).

        Returns:
        numpy.ndarray: Resized image.
        """
        image_array = (image_array * 255).astype(np.uint8)  # Convert from [0,1] float to uint8 [0,255]
        img = Image.fromarray(image_array)
        img = img.resize(target_size, Image.LANCZOS)
        return np.array(img)

    def detect_lane(self, input_image):
        """
        Detects lanes on the given road image.

        Parameters:
        input_image (numpy.ndarray): Original road image.

        Returns:
        numpy.ndarray: Image with detected lanes overlaid.
        """

        # Preprocess the image for model input
        processed_img = self.resize_image(input_image, (160, 80))  # Resize to (width, height)
        processed_img = np.array(processed_img)[None, :, :, :]  # Expand dimensions for model input

        # Predict lane markings using the model
        predicted_lane = self.model.predict(processed_img)[0] * 255  # Un-normalize output

        # Store recent lane detections (only keep the last 5)
        self.recent_predictions.append(predicted_lane)
        if len(self.recent_predictions) > 5:
            self.recent_predictions.pop(0)

        # Compute the average lane detection
        self.avg_lane_prediction = np.mean(np.array(self.recent_predictions), axis=0)

        # Create an RGB lane overlay (green channel for lanes)
        blank_layer = np.zeros_like(self.avg_lane_prediction, dtype=np.uint8)
        lane_overlay = np.dstack((blank_layer, self.avg_lane_prediction, blank_layer))

        # Resize the overlay to match the original input image
        lane_overlay_resized = self.resize_image(lane_overlay, (1280, 720))

        # Merge the detected lane overlay with the original image
        output_image = cv2.addWeighted(input_image, 1, lane_overlay_resized, 1, 0)

        return output_image


def process_video(input_video_path, output_video_path, model_path='full_CNN_model.h5'):
    """
    Process a video file to detect lanes in each frame.

    Parameters:
    input_video_path (str): Path to the input video file.
    output_video_path (str): Path to save the processed output video.
    model_path (str): Path to the pre-trained Keras model.
    """

    # Initialize the LaneDetector with the specified model
    lane_detector = LaneDetector(model_path)

    # Load input video and process frame-by-frame
    input_clip = VideoFileClip(input_video_path)
    processed_clip = input_clip.fl_image(lane_detector.detect_lane)

    # Write the output video
    processed_clip.write_videofile(output_video_path, audio=False)


if __name__ == '__main__':
    # Paths for input and output videos
    input_video = "demo.mp4"
    output_video = "processed_lane_detection.mp4"

    # Process the video with lane detection
    process_video(input_video, output_video)
