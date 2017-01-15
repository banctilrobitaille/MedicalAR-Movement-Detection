import os
from PyQt5.QtGui import QImage


class Image(QImage):
    __path = None

    def __init__(self, *__args):
        QImage.__init__(self, *__args)
