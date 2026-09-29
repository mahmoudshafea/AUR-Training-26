from rclpy.node import Node
from std_msgs.msg import Float32


class WorkerNode(Node):
    def __init__(self, mediator):
        super().__init__('worker_node')

        self.mediator = mediator

        self.subscription = self.create_subscription(
            Float32,
            '/robot/battery',
            self.battery_callback,
            10
        )

    def battery_callback(self, msg):
        self.mediator.update_battery(msg.data)