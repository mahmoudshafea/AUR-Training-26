from PySide6.QtWidgets import QHBoxLayout,QWidget,QPushButton
from PySide6.QtCore import Signal

class Buttons(QWidget):
    start=Signal()
    pause=Signal()
    reset=Signal()
    def __init__(self):
        super().__init__()
        self._start_button=QPushButton("START")
        self._reset_button=QPushButton("RESET")
        self.__timer_paused=True

        self._layout=QHBoxLayout(self)
        self._layout.addWidget(self._start_button)
        self._layout.addWidget(self._reset_button)

        self._start_button.clicked.connect(self._b1_clicked)
        self._reset_button.clicked.connect(self._b2_clicked)

        

    @property
    def timer_paused(self)->bool:
        return self.__timer_paused

    @timer_paused.setter
    def timer_paused(self,state:bool)->None:
        self.__timer_paused = state
        if self.__timer_paused:
            self._start_button.setText("START")
        else:
            self._start_button.setText("PAUSE")

    def _b1_clicked(self)->None:
        if self.timer_paused:
            self.timer_paused=False
            self.start.emit()
        else:
            self.timer_paused=True
            self.pause.emit()

        
    def _b2_clicked(self)->None:
        self.reset.emit()
        

