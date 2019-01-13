import cv2
import numpy as np

from models.factories.image_factory import ImageFactory


class ImageHelper(object):
    @staticmethod
    def __extract_skin_mask_from(image):
        # HSV skin threshold based on experiment, these value might need to be changed depending on the skin color
        lower_hsv_skin_threshold = np.array([0, 40, 50], dtype="uint8")
        upper_hsv_skin_threshold = np.array([12, 255, 255], dtype="uint8")

        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        skin_mask = cv2.inRange(hsv_image, lower_hsv_skin_threshold, upper_hsv_skin_threshold)
        #cv2.bilateralFilter(skin_mask, 3, 10, 10)

        cv2.medianBlur(skin_mask, 5, skin_mask)
        # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        # skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_CLOSE, kernel, iterations=3)

        # Erode and dilate to eliminate possible artifact in the mask
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4))
        skin_mask = cv2.erode(skin_mask, kernel, iterations=1)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4))
        skin_mask = cv2.dilate(skin_mask, kernel, iterations=3)

        # Closing the mask in order to reduce the number of possible holes
        return skin_mask

    @staticmethod
    def compute_patient_movement(current_position, previous_position):
        gray_scaled_previous_position = cv2.cvtColor(previous_position.raw_data, cv2.COLOR_BGR2GRAY)
        hsv_previous_position = np.zeros_like(previous_position.raw_data)
        hsv_previous_position[..., 1] = 255

        gray_scaled_current_position = cv2.cvtColor(current_position.raw_data, cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(gray_scaled_previous_position, gray_scaled_current_position, None, 0.80, 3,
                                            15, 3, 7, 1.5, 0)
        magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        hsv_previous_position[..., 0] = angle * 180 / np.pi / 2
        hsv_previous_position[..., 2] = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
        bgr_movement_image = cv2.cvtColor(hsv_previous_position, cv2.COLOR_HSV2BGR)

        skin_mask = ImageHelper.__extract_skin_mask_from(current_position.raw_data)
        current_position_data = current_position.raw_data

        test = cv2.bitwise_and(bgr_movement_image, bgr_movement_image, mask=cv2.bitwise_not(skin_mask))

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (30, 30))
        skin_mask_2 = cv2.dilate(skin_mask, kernel, iterations=2)

        real_mask = cv2.bitwise_and(skin_mask_2, cv2.bitwise_not(skin_mask))
        test = cv2.bitwise_and(bgr_movement_image, bgr_movement_image, mask=real_mask)

        output = cv2.addWeighted(current_position_data, 1, test, 0.7, 0.0)

        return [ImageFactory.create_from_rgb_image(cv2.cvtColor(output, cv2.COLOR_BGR2RGB)), True]
