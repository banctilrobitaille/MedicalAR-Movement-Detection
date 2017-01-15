import sys
from PyQt5.QtWidgets import QApplication
from views.ui_main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow("Patient moving detection V0.1")

    sys.exit(app.exec_())
