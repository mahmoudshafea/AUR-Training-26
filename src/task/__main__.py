import rclpy

from PySide6.QtWidgets import QApplication

from task.gui.window import Window


def main():
    rclpy.init()

    app = QApplication()

    window = Window()

    app.exec()


if __name__ == '__main__':
    main()