from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout


class MainWindow(QWidget):
    def __init__(self, title, flags=None, *args, **kwargs):
        QWidget.__init__(self, flags, *args, **kwargs)
        self.setWindowTitle(title)
        self.resize(1024, 768)
        self.__center()
        self.show()

    def __center(self):
        window_geometry = self.geometry()
        current_screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        center_point = QApplication.desktop().screenGeometry(current_screen).center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())
