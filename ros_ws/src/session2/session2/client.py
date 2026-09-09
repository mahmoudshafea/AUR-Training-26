import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts
   
class Client(Node):
    def __init__(self):
        super().__init__("client")
        self.get_logger().info("Client node started")
        self.cli=self.create_client(AddTwoInts,"add_two_ints")
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Server not available yet")
        self.request=AddTwoInts.Request()
        self.request.a=5
        self.request.b=7
        future=self.cli.call_async(self.request)
        future.add_done_callback(self.service_callback)
    def service_callback(self,future):
        try:
            response=future.result()
            self.get_logger().info(f"Service response:{response.sum}")
        except Exception as e:
            self.get_logger().error(f"Service call failed{e}")
        


def main():
    rclpy.init()
    node=Client()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
