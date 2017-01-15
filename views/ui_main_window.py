from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout
from views.ui_image_frame import ImageFrame


class MainWindow(QWidget):
    __surgery_controller = None
    __image_frame = None

    def __init__(self, title, surgery_controller, *args, **kwargs):
        QWidget.__init__(self, None, *args, **kwargs)
        self.__surgery_controller = surgery_controller
        self.__initialize_with(title)
        self.__image_frame = ImageFrame(surgery_controller, parent=self)

        layout = QHBoxLayout()
        layout.addWidget(self.__image_frame)
        self.setLayout(layout)
        self.show()
        self.__surgery_controller.start_surgery()

    def __initialize_with(self, title=None):
        self.setWindowTitle(title)
        self.resize(640, 400)
        self.__center()
        self.setStyleSheet("background-color: dark-gray;")

    def __center(self):
        window_geometry = self.geometry()
        current_screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        center_point = QApplication.desktop().screenGeometry(current_screen).center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())
