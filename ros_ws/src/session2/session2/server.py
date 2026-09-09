import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts
class Server(Node):
    def __init__(self):
        super().__init__("server")
        self.get_logger().info("Server node started")
        self.srv=self.create_service(AddTwoInts,"add_two_ints",self.add_callback)
    def add_callback(self,request,response):
        response.sum=request.a+request.b
        self.get_logger().info(f"Incomng request{request.a},{request.b},sending back response {response.sum}")
        return response
        


def main():
    rclpy.init()
    node=Server()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
