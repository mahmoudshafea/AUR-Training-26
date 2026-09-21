from PySide6.QtWidgets import QApplication
from qt_task.window import Window
def main() -> None:
    app=QApplication()
    window=Window()
    window.show()
    app.exec()
