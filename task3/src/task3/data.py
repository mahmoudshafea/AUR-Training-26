from PySide6.QtCore import QObject, QTimer, Property, Signal


class MyData(QObject):
    hours_changed = Signal()
    mins_changed = Signal()
    secs_changed = Signal()

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)

        self._hours_in = 0
        self._mins_in = 0
        self._secs_in = 0

        self._timer = QTimer(self)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._increment)
        self._timer.start()

    def get_hours(self):
        return self._hours_in

    def set_hours(self, data: int):
        self._hours_in = data
        self.hours_changed.emit()

    hours = Property(int, get_hours, set_hours, notify=hours_changed)

    def get_mins(self):
        return self._mins_in

    def set_mins(self, data: int):
        self._mins_in = data
        self.mins_changed.emit()

    mins = Property(int, get_mins, set_mins, notify=mins_changed)

    def get_secs(self):
        return self._secs_in

    def set_secs(self, data: int):
        self._secs_in = data
        self.secs_changed.emit()

    secs = Property(int, get_secs, set_secs, notify=secs_changed)

    def _increment(self):
        self.secs += 1

        if self.secs >= 60:
            self.secs = 0
            self.mins += 1

        if self.mins >= 60:
            self.mins = 0
            self.hours += 1

        if self.hours >= 12:
            self.hours = 0