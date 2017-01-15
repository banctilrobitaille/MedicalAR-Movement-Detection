from PyQt5.QtGui import QImage


class Image(object):
    __path = None
    __raw_data = None
    __rgb_image = None

    def __init__(self, path, rgb_data, raw_data):
        self.__rgb_image = QImage(rgb_data, rgb_data.shape[1], rgb_data.shape[0], rgb_data.shape[1] * 3,
                                  QImage.Format_RGB888)
        self.__path = path
        self.__raw_data = raw_data

    @property
    def path(self):
        return self.__path

    @property
    def raw_data(self):
        return self.__raw_data

    @property
    def rgb_image(self):
        return self.__rgb_image
