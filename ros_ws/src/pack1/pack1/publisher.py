import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class Publisher(Node):
    def __init__(self):
        super().__init__("publisher")
        self.get_logger().info("Publisher started")
        self.publisher=self.create_publisher(Twist,"/turtle1/cmd_vel",10)
        self.create_timer(1,self.moving_callback)
    def moving_callback(self):
        direction=Twist()
        direction.linear.x=2.0
        direction.angular.x=1.0
        self.publisher.publish(direction)

def main():
    rclpy.init()
    node=Publisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
