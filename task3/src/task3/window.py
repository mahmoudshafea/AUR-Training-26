from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout

from task3.data import MyData
from task3.input import Input
from task3.status_widget import StatusWidget


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self._data = MyData()
        self._status = StatusWidget("clock.qml", self._data)
        self._input = Input()

        self._input.time_entered.connect(self._update_time)

        central = QWidget()
        layout = QVBoxLayout(central)

        layout.addWidget(self._status)
        layout.addWidget(self._input)

        self.setCentralWidget(central)

    def _update_time(self, hours, mins, secs):
        self._data.hours = hours
        self._data.mins = mins
        self._data.secs = secs