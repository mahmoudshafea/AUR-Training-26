from PySide6.QtWidgets import QApplication

from task3.window import Window

def main() -> None:
    app = QApplication()

    window = Window()
    window.show()

    app.exec()