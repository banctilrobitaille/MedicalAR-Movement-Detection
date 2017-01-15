from PyQt5.QtCore import pyqtSignal


class Patient(object):
    patient_has_moved = pyqtSignal(object)

    __name = None
    __current_position = None
    __previous_position = None

    def __init__(self):
        pass

    @property
    def current_position(self):
        return self.__current_position

    @current_position.setter
    def current_position(self, current_position):
        self.__previous_position = self.__current_position
        self.__current_position = current_position

    @property
    def previous_position(self):
        return self.__previous_position

    @previous_position.setter
    def previous_position(self, previous_position):
        self.__previous_position = previous_position
