from PySide6.QtWidgets import QWidget,QHBoxLayout,QVBoxLayout,QLineEdit,QPushButton
from PySide6.QtCore import Signal
from PySide6.QtGui import QIntValidator
class Input(QWidget):
    time_entered=Signal(int,int,int)
    def __init__(self,parent:QWidget|None=None):
        super().__init__(parent)
        self._hoursin=0
        self._minutesin=0
        self._secondsin=0
        self._hlayout=QHBoxLayout()
        self._vlayout=QVBoxLayout(self)

        self._hvalidator=QIntValidator(0,11)
        self._msvalidator=QIntValidator(0,59)


        self._inputH=QLineEdit()
        self._inputM=QLineEdit()
        self._inputS=QLineEdit()

        self._inputH.setValidator(self._hvalidator)
        self._inputM.setValidator(self._msvalidator)
        self._inputS.setValidator(self._msvalidator)


        self._inputH.setPlaceholderText("hours...")
        self._inputM.setPlaceholderText("Minutes...")
        self._inputS.setPlaceholderText("Seconds...")

        self._button=QPushButton("Confirm")
        self._button.clicked.connect(self._confirm_input)

        self._hlayout.addWidget(self._inputH)
        self._hlayout.addWidget(self._inputM)
        self._hlayout.addWidget(self._inputS)
        self._vlayout.addLayout(self._hlayout)
        self._vlayout.addWidget(self._button)


    def _confirm_input(self):
        self._hoursin=int(self._inputH.text())
        self._minutesin=int(self._inputM.text())
        self._secondsin=int(self._inputS.text())
        self.time_entered.emit(self._hoursin,self._minutesin,self._secondsin)
        