from PySide6.QtWidgets import QMainWindow,QWidget,QVBoxLayout
from qt_task.buttons import Buttons
from qt_task.stack import Stack
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self._buttons=Buttons()
        self._stack=Stack()
        central_widget=QWidget()
        layout=QVBoxLayout(central_widget)
        layout.addWidget(self._stack)
        layout.addWidget(self._buttons)
        self.setCentralWidget(central_widget)
        self._buttons.start.connect(self._stack.start_counter)
        self._buttons.pause.connect(self._stack.pause)
        self._buttons.reset.connect(self._stack.reset)
        self._stack.timer_stopped.connect(self._switch_buttons)
    def _switch_buttons(self,state:bool):
        self._buttons.timer_paused=state