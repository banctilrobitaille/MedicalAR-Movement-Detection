import cv2

from exception.exceptions import UnableToCreateImageException
from models.image import Image


class ImageFactory(object):
    @staticmethod
    def create_image_from_path(image_path):
        try:
            original_image = cv2.imread(image_path)
            rgb_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
            return Image(image_path, rgb_image, original_image)
        except Exception as e:
            raise UnableToCreateImageException(
                    "".join(["Unable to create the image from the provided path: ", image_path]))

    @staticmethod
    def create_from_rgb_image(rgb_image):
        return Image("", rgb_image, None)
