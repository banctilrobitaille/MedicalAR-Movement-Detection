import time

from PyQt5.QtCore import QThread, pyqtSlot, pyqtSignal, QObject

from helpers.image_helper import ImageHelper


class SurgeryController(QObject):
    patient_position_update = pyqtSignal(object)

    __surgery = None
    __surgery_worker = None

    def __init__(self):
        QObject.__init__(self)

    @property
    def surgery(self):
        return self.__surgery

    def register(self, surgery):
        self.__surgery = surgery
        self.__surgery.patient_position_update.connect(self.__on_patient_position_update)
        return self

    def start_surgery(self):
        self.__surgery_worker = SurgeryWorker(self.__surgery)
        self.__surgery_worker.start()

    @pyqtSlot(object, object)
    def __on_patient_position_update(self, current_position, previous_position):
        if previous_position is None:
            return current_position.rgb_image
        else:
            self.patient_position_update.emit(
                    ImageHelper.compute_patient_movement(current_position, previous_position).rgb_image)


class SurgeryWorker(QThread):
    __running = False
    __surgery = None

    def __init__(self, surgery):
        QThread.__init__(self)
        self.__surgery = surgery

    def run(self):
        self.__running = True
        while self.__running:
            self.__surgery.next_step()
            time.sleep(5)
