import threading

from pynput import keyboard
from rclpy.node import Node
from rclpy.duration import Duration
from sensor_msgs.msg import Joy


class JoyNode(Node):
    def __init__(self):
        super().__init__('joy_node')

        self.publisher = self.create_publisher(
            Joy,
            '/joy',
            10
        )

        self.lock = threading.RLock()
        self.emergency_until = None

        self.timer = self.create_timer(
            0.05,
            self.check_emergency
        )

        self.listener = keyboard.Listener(
            on_press=self.key_pressed,
            on_release=self.key_released
        )

        self.listener.start()

        self.axes = [0.0, 0.0]
        self.gripper = 0

    def key_pressed(self, key):
        with self.lock:
            if self.is_emergency_active():
                return

            try:
                if key.char == 'w':
                    self.axes[0] = 1.0
                elif key.char == 's':
                    self.axes[0] = -1.0
                elif key.char == 'a':
                    self.axes[1] = -1.0
                elif key.char == 'd':
                    self.axes[1] = 1.0
                elif key.char == 'g':
                    self.gripper = 1
            except AttributeError:
                pass

            self.publish_joy()

    def key_released(self, key):
        with self.lock:
            if self.is_emergency_active():
                return

            try:
                if key.char in ('w', 's'):
                    self.axes[0] = 0.0
                elif key.char in ('a', 'd'):
                    self.axes[1] = 0.0
                elif key.char == 'g':
                    self.gripper = 0
            except AttributeError:
                pass

            self.publish_joy()

    def publish_joy(self):
        msg = Joy()
        msg.axes = list(self.axes)
        msg.buttons = [self.gripper]

        self.publisher.publish(msg)

    def trigger_emergency(self):
        with self.lock:
            self.axes = [0.0, 0.0]
            self.gripper = 0

            self.publisher.publish(Joy(
                axes=[0.0, 0.0],
                buttons=[0]
            ))

            self.emergency_until = (
                self.get_clock().now() + Duration(seconds=5)
            )

    def is_emergency_active(self):
        if self.emergency_until is None:
            return False

        return self.get_clock().now() < self.emergency_until

    def check_emergency(self):
        with self.lock:
            if self.emergency_until is None:
                return

            if self.get_clock().now() >= self.emergency_until:
                self.emergency_until = None

    def destroy_node(self):
        self.listener.stop()
        super().destroy_node()