from PySide6.QtWidgets import QStackedWidget,QLineEdit,QLabel,QWidget
from PySide6.QtGui import QIntValidator
from PySide6.QtCore import QTimer,Signal
class Stack(QStackedWidget):
    timer_stopped=Signal(bool)
    def __init__(self,parent:QWidget|None=None):
        super().__init__(parent)
        self._time_in=0
        self._timer=QTimer()
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._decrement)


        self._input=QLineEdit()
        self._input.setPlaceholderText("Enter time here...")

        self._label=QLabel()
        self._validation=QIntValidator(1,5940)
        self._input.setValidator(self._validation)


        self.addWidget(self._input)
        self.addWidget(self._label)



    def start_counter(self):
        if self._timer.isActive():
            return
        if self._time_in==0:
            if not self._input.text():
                return
            self._time_in=int(self._input.text())
        minutes=str(self._time_in//60)
        seconds=str(self._time_in % 60)
        if len(minutes)==1:
           minutes='0'+minutes
        if len(seconds)==1:
            seconds='0'+seconds
        self._label.setText(f"{minutes}:{seconds}")
        self.setCurrentIndex(1)
        self._timer.start()
        
            


    def _decrement(self):
        if self._time_in>=1:
            self._time_in-=1
            minutes=str(self._time_in//60)
            seconds=str(self._time_in % 60)
            if len(minutes)==1:
                minutes='0'+minutes
            if len(seconds)==1:
                seconds='0'+seconds
            self._label.setText(f"{minutes}:{seconds}")
        else:
            self._label.setText("00:00")
            self._timer.stop()
            self._input.clear()
            self.setCurrentIndex(0)
            self.timer_stopped.emit(True)


    def reset(self):
        self._timer.stop()
        self._input.clear()
        self.setCurrentIndex(0)
        self._time_in=0    
        self._label.clear()
        self.timer_stopped.emit(True)
        
    def pause(self):
        self._timer.stop()

        
