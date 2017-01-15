import cv2
import numpy as np

from models.factories.image_factory import ImageFactory


class ImageHelper(object):
    @staticmethod
    def __extract_skin_mask_from(image):
        # HSV skin threshold based on experiment, these value might need to be changed depending on the skin color
        lower_hsv_skin_threshold = np.array([0, 80, 80], dtype="uint8")
        upper_hsv_skin_threshold = np.array([13, 255, 255], dtype="uint8")

        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        skin_mask = cv2.inRange(hsv_image, lower_hsv_skin_threshold, upper_hsv_skin_threshold)

        # Erode and dilate to eliminate possible artifact in the mask
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
        skin_mask = cv2.erode(skin_mask, kernel, iterations=1)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        skin_mask = cv2.dilate(skin_mask, kernel, iterations=3)

        # Closing the mask in order to reduce the number of possible holes
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (40, 40))
        skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_CLOSE, kernel, iterations=1)

        return cv2.GaussianBlur(skin_mask, (3, 3), 0)

    @staticmethod
    def compute_patient_movement(current_position, previous_position):
        gray_scaled_previous_position = cv2.cvtColor(previous_position.raw_data, cv2.COLOR_BGR2GRAY)
        hsv_previous_position = np.zeros_like(previous_position.raw_data)
        hsv_previous_position[..., 1] = 255

        gray_scaled_current_position = cv2.cvtColor(current_position.raw_data, cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(gray_scaled_previous_position, gray_scaled_current_position, None, 0.5, 3,
                                            15, 3, 5, 1.2, 0)
        magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        hsv_previous_position[..., 0] = angle * 180 / np.pi / 2
        hsv_previous_position[..., 2] = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
        bgr_movement_image = cv2.cvtColor(hsv_previous_position, cv2.COLOR_HSV2BGR)

        skin_mask = ImageHelper.__extract_skin_mask_from(current_position.raw_data)
        previous_mask = ImageHelper.__extract_skin_mask_from(previous_position.raw_data)
        overlayed_image = np.zeros((skin_mask.shape[0], skin_mask.shape[1], 3), dtype=np.uint8)
        current_position_data = current_position.raw_data

        moved = not(np.array(skin_mask) == np.array(previous_mask)).all()

        for i in range(0, bgr_movement_image.shape[0]):
            for j in range(0, bgr_movement_image.shape[1]):
                if skin_mask[i][j] > 0:
                    overlayed_image[i][j][0] = current_position_data[i][j][0]
                    overlayed_image[i][j][1] = current_position_data[i][j][1]
                    overlayed_image[i][j][2] = current_position_data[i][j][2]

                elif bgr_movement_image[i][j][1] > 50 or bgr_movement_image[i][j][2] > 50:
                    overlayed_image[i][j][0] = 0.3 * bgr_movement_image[i][j][0] + 0.7 * current_position_data[i][j][0]
                    overlayed_image[i][j][1] = 0.3 * bgr_movement_image[i][j][1] + 0.7 * current_position_data[i][j][1]
                    overlayed_image[i][j][2] = 0.3 * bgr_movement_image[i][j][2] + 0.7 * current_position_data[i][j][2]
                else:
                    overlayed_image[i][j][0] = current_position_data[i][j][0]
                    overlayed_image[i][j][1] = current_position_data[i][j][1]
                    overlayed_image[i][j][2] = current_position_data[i][j][2]

        return [ImageFactory.create_from_rgb_image(cv2.cvtColor(overlayed_image, cv2.COLOR_BGR2RGB)), moved]
