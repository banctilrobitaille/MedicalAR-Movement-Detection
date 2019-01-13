from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSlot


class ImageFrame(QFrame):
    __image = None
    __label = None
    __layout = None

    def __init__(self, surgery_controller, parent=None, *args, **kwargs):
        QFrame.__init__(self, parent=parent, *args, **kwargs)
        surgery_controller.patient_position_update.connect(self.__update_layout_content_with)
        self.setLineWidth(2)
        self.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.setStyleSheet("color:green")
        self.__label = QLabel(self)
        self.__layout = QHBoxLayout()
        self.__layout.addWidget(self.__label)
        self.setLayout(self.__layout)

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, image):
        self.__image = image
        self.__update_layout_content_with(image)

    @pyqtSlot(object, bool)
    def __update_layout_content_with(self, image, moved):
        self.__label.setPixmap(QPixmap(image))
        self.__label.adjustSize()
        if moved:
            self.setStyleSheet("color:yellow")
        else:
            self.setStyleSheet("color:green")
