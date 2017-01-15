import os

from models.factories.image_factory import ImageFactory


class ImageRepository(object):
    __image_directory = None
    __index = 0
    __images = []

    def __init__(self, image_directory):
        self.__image_directory = image_directory
        self.__images = filter(lambda element: os.path.isfile(os.path.join(image_directory, element)),
                               os.listdir(image_directory))
        self.__images.sort(key=lambda f: int(filter(str.isdigit, f)))

    def retrieve_image(self, index):
        return self.__images[index]

    def retrieve_next_image(self):
        if self.__index == len(self.__images):
            self.__index = 0
        else:
            image_path = self.__images[self.__index]
            self.__index += 1
            return ImageFactory.create_image_from_path(os.path.join(self.__image_directory, image_path))
