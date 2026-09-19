from PySide6.QtWidgets import QHBoxLayout,QWidget,QPushButton
from PySide6.QtCore import Signal

class Buttons(QWidget):
    start=Signal()
    pause=Signal()
    reset=Signal()
    def __init__(self,parent:QWidget|None=None):
        self._start_button=QPushButton("START")
        self._reset_button=QPushButton("RESET")
        self._start_button.clicked.connect()
        self._reset_button.clicked.connect()


