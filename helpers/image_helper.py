import cv2
import numpy as np


class ImageHelper(object):
    @staticmethod
    def extract_skin_mask_from(image):
        # HSV skin threshold based on experiment, these value might need to be changed depending on the skin color
        lower_hsv_skin_threshold = np.array([0, 80, 80], dtype="uint8")
        upper_hsv_skin_threshold = np.array([13, 255, 255], dtype="uint8")

        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        skin_mask = cv2.inRange(hsv_image, lower_hsv_skin_threshold, upper_hsv_skin_threshold)

        # Erode and dilate to eliminate possible artifact in the mask
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
        skin_mask = cv2.erode(skin_mask, kernel, iterations=1)
        skin_mask = cv2.dilate(skin_mask, kernel, iterations=1)

        # Closing the mask in order to reduce the number of possible holes
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (40, 40))
        skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_CLOSE, kernel, iterations=1)

        return cv2.GaussianBlur(skin_mask, (3, 3), 0)
