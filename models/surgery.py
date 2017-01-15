from PyQt5.QtCore import pyqtSignal, QObject


class Surgery(QObject):
    patient_position_update = pyqtSignal(object, object, name="Surgery progress")

    __patient = None
    __type = None
    __images_repository = None

    def __init__(self, patient=None, type=None, images_repository=None):
        QObject.__init__(self)
        self.__patient = patient
        self.__type = type
        self.__images_repository = images_repository

    def next_step(self):
        self.__patient.current_position = self.__images_repository.retrieve_next_image()
        self.patient_position_update.emit(self.__patient.current_position, self.__patient.previous_position)
