import sys
from PyQt5.QtWidgets import QApplication

from models.patient import Patient
from views.ui_main_window import MainWindow
from controllers.surgery_controller import SurgeryController
from models.surgery import Surgery
from models.surgery_types import SurgeryTypes
from models.image_repository import ImageRepository
from models.constants import FilePath

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow("Patient moving detection V0.1",
                             SurgeryController()
                             .register(Surgery(patient=Patient(), type=SurgeryTypes.ARM_SURGERY,
                                               images_repository=ImageRepository(
                                                       FilePath.IMAGE_DIRECTORY))))
    sys.exit(app.exec_())
