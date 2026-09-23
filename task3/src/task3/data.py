from PySide6.QtCore import QObject,QTimer,Property,Signal


class MyData(QObject):
    hours_changed=Signal()
    minutes_changed=Signal()
    seconds_changed=Signal()
    def __init__(self,parent:QObject|None=None):
        super().__init__(parent)

        self._timer=QTimer()
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._increment)

        self._hours_in=0
        self._minutes_in=0
        self._seconds_in=0


    @Property(int,notify=hours_changed)
    def hours(self):
        return self._hours_in

    @Property(int,notify=minutes_changed)
    def minutes(self):
        return self._minutes_in

    @Property(int,notify=seconds_changed)
    def seconds(self):
        return self._seconds_in

    @hours.setter
    def hours(self,data:int):
        self._hours_in=data
        self.hours_changed.emit()

    @minutes.setter
    def minutes(self,data:int):
        self._minutes_in=data
        self.minutes_changed.emit()

    @seconds.setter
    def seconds(self,data:int):
        self._seconds_in=data
        self.seconds_changed.emit()


    
    def _increment(self):
        self.seconds+=1
        if self.seconds>=60:
            self.seconds=0
            self.minutes+=1
        if self.minutes>=60:
            self.minutes=0
            self.hours+=1
        if self.hours>=12:
            self.hours=0


        
