from PySide6.QtCore import QObject, Signal, Property, Slot


class Mediator(QObject):
    battery_changed = Signal()

    def __init__(self):
        super().__init__()
        self._battery_level = 0.0

    @Property(float, notify=battery_changed)
    def batteryLevel(self):
        return self._battery_level

    @Slot(float)
    def update_battery(self, value):
        self._battery_level = value
        self.battery_changed.emit()