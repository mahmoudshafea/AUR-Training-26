import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool
from functools import partial
import time

class GOTOGOAL_client(Node):
    def __init__(self):
        super().__init__("go_to_goal_client")
        self.get_logger().info("GOTOGOAL Client Node Started!!")

        self.send_request()



    def send_request(self):
        
        self.client = self.create_client(SetBool, "setbool")

        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Service not available, waiting again...")

        self.request = SetBool.Request()
        self.request.data=False
        future = self.client.call_async(self.request) ##that is where the client send a request to the server
        future.add_done_callback(partial(self.service_callback, data=self.request.data))# when a respond comes in call this function

        time.sleep(5)

        self.request = SetBool.Request()
        self.request.data=True
        future = self.client.call_async(self.request) ##that is where the client send a request to the server
        future.add_done_callback(partial(self.service_callback, data=self.request.data))# when a respond comes in call this function




    def service_callback(self, future, data):
        try:
            response = future.result()
            self.get_logger().info(f"Service response:{response.message} My request:{data}")
        except Exception as e:
            self.get_logger().error(f"Service call failed: {e}")

def main():
    rclpy.init()
    node = GOTOGOAL_client()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()