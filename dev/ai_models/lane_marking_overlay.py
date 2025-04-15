import numpy as np
import cv2
from PIL import Image
from moviepy.editor import VideoFileClip
from keras.models import load_model
import csv
import os

class LaneDetector:
    """
    A class to handle lane detection and averaging lane predictions.
    """
    def _init_(self, model_path='full_CNN_model.h5', fps=30):
        self.model = load_model(model_path, compile=False, custom_objects={})
        self.recent_predictions = []
        self.avg_lane_prediction = []
        self.frame_count = 0
        self.fps = fps
        self.lane_drift_threshold = 0.02  # meters
        self.offset_log = []

        self.csv_path = "lane_offset_log.csv"
        with open(self.csv_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Frame", "Timestamp(s)", "Offset(m)", "Direction", "Drift Warning", "Lane Detected"])

    # def _init_(self, model_path='full_CNN_model.h5'):
    #     """
    #     Initializes the lane detector with a pre-trained model.

    #     Parameters:
    #     model_path (str): Path to the pre-trained Keras model.
    #     """
    #     self.model = load_model(model_path, compile=False, custom_objects={})
    #     self.recent_predictions = []
    #     self.avg_lane_prediction = []

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
        image_array = image_array.astype(np.uint8)
        img = Image.fromarray(image_array)
        img = img.resize(target_size)
        return np.array(img)

    def get_lane_line_pixels(self, binary_mask):
        height, width = binary_mask.shape
        nonzero = binary_mask.nonzero()
        nonzeroy = np.array(nonzero[0])
        nonzerox = np.array(nonzero[1])

        midpoint = width // 2
        left_inds = nonzerox < midpoint
        right_inds = nonzerox >= midpoint

        leftx = nonzerox[left_inds]
        lefty = nonzeroy[left_inds]
        rightx = nonzerox[right_inds]
        righty = nonzeroy[right_inds]

        return leftx, lefty, rightx, righty

    def calculate_vehicle_offset(self, binary_mask, leftx, lefty, rightx, righty):
        height, width = binary_mask.shape
        xm_per_pix = 3.7 / 700  # Meters per pixel

        if len(leftx) == 0 or len(rightx) == 0:
            return None

        left_fit = np.polyfit(lefty, leftx, 2)
        right_fit = np.polyfit(righty, rightx, 2)

        y_eval = height
        left_x = left_fit[0]*(y_eval**2) + left_fit[1]*y_eval + left_fit[2]
        right_x = right_fit[0]*(y_eval**2) + right_fit[1]*y_eval + right_fit[2]

        lane_center = (left_x + right_x) / 2.0
        car_position = width / 2.0
        offset_pixels = car_position - lane_center
        offset_meters = offset_pixels * xm_per_pix

        return offset_meters

    def log_offset(self, offset, detected):
        self.frame_count += 1
        timestamp = self.frame_count / self.fps

        if offset is not None:
            direction = "Left" if offset < 0 else "Right"
            abs_offset = abs(offset)
            drift_warning = "Yes" if abs_offset > self.lane_drift_threshold else "No"
        else:
            direction = "Unknown"
            abs_offset = "N/A"
            drift_warning = "No"

        self.offset_log.append((self.frame_count, timestamp, offset, direction, drift_warning, detected))

        with open(self.csv_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.frame_count, f"{timestamp:.2f}", abs_offset, direction, drift_warning, "Yes" if detected else "No"])

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
        # blank_layer = np.zeros_like(self.avg_lane_prediction, dtype=np.uint8)
        # lane_overlay = np.dstack((blank_layer, self.avg_lane_prediction, blank_layer))

        # Convert to grayscale and threshold to get binary lane mask
        gray_mask = self.avg_lane_prediction.astype(np.uint8)
        _, binary_mask = cv2.threshold(gray_mask, 127, 255, cv2.THRESH_BINARY)
        binary_mask = binary_mask // 255  # Normalize to 0/1

        # Get lane line pixels and calculate offset
        leftx, lefty, rightx, righty = self.get_lane_line_pixels(binary_mask)
        offset = self.calculate_vehicle_offset(binary_mask, leftx, lefty, rightx, righty)

        detected = True if len(leftx) > 0 and len(rightx) > 0 else False
        self.log_offset(offset, detected)

        # Decide color based on offset
        threshold = 0.02  # meters
        if offset is not None and abs(offset) > threshold:
            # Red overlay for lane drift
            r = self.avg_lane_prediction.astype(np.uint8)
            lane_overlay = np.dstack((r, np.zeros_like(r), np.zeros_like(r)))
            warning_text = "Lane Drift Warning!"
        else:
            # Green overlay for normal
            g = self.avg_lane_prediction.astype(np.uint8)
            lane_overlay = np.dstack((np.zeros_like(g), g, np.zeros_like(g)))
            warning_text = None

        # Resize overlay to original frame
        orig_size = (input_image.shape[1], input_image.shape[0])
        lane_overlay_resized = self.resize_image(lane_overlay, orig_size)

        # Overlay on original
        output_image = cv2.addWeighted(input_image, 1, lane_overlay_resized, 1, 0)

        # Annotate
        font = cv2.FONT_HERSHEY_SIMPLEX
        if offset is not None:
            direction = "left" if offset < 0 else "right"
            abs_offset = abs(offset)
            text = f"Vehicle is {abs_offset:.2f} m {direction} of center"
        else:
            text = "Lane not detected"

        cv2.putText(output_image, text, (50, 50), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Add lane drift warning (if any)
        if warning_text:
            cv2.putText(output_image, warning_text, (50, 100), font, 1.2, (0, 0, 255), 3, cv2.LINE_AA)

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


if _name_ == '_main_':
    # Paths for input and output videos
    input_video = "demo.mp4"
    output_video = "processed_lane_detection.mp4"

    # Process the video with lane detection
    process_video(input_video, output_video)
