from PyQt5.QtWidgets import QFrame


class ImageFrame(QFrame):
    def __init__(self, parent=None, flags=None, *args, **kwargs):
        QFrame.__init__(self, parent=parent, flags=flags, *args, **kwargs)
