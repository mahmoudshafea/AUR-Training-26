import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose


class GoToMultipleNode(Node):

    def __init__(self):
        super().__init__("GoToMultipleGoalNode")
        self.get_logger().info("GoToMultipleGoalNode started")

        self.kp_linear=1.5
        self.kp_angular=6.0

        self.distance_tolerance=0.1
        self.angle_tolerance=0.05

        self.current_pose=None
        self.goal_reached=False

        self.goals=[(8.0, 8.0),
                    (3.0, 8.0),
                    (3.0, 3.0),
                    (8.0, 3.0)]
        self.i=0


        self.subscriber=self.create_subscription(Pose,"/turtle1/pose",self.pose_callback,10)
        self.publisher=self.create_publisher(Twist,"/turtle1/cmd_vel",10)
        self.create_timer(0.05,self.control_loop)

    def pose_callback(self,msg):
        self.current_pose=msg

    def normalize_angle(self,angle):
        while angle > math.pi:
           angle -= 2 * math.pi
        while angle < -math.pi:
           angle += 2 * math.pi
        return angle

    def control_loop(self):
       if self.current_pose==None or self.goal_reached:
          return
       
       msg=Twist()
       dx=self.goals[self.i][0]-self.current_pose.x
       dy=self.goals[self.i][1]-self.current_pose.y
       distance_error=math.sqrt((dx**2)+(dy**2))
       target_angle=math.atan2(dy,dx)
       heading_error=self.normalize_angle(target_angle-self.current_pose.theta)

       if distance_error<self.distance_tolerance:
            if self.i==3:
                msg.linear.x=0.0
                msg.angular.z=0.0
                self.goal_reached=True
                self.publisher.publish(msg)
                return
            else:
              self.i+=1
              return
       if abs(heading_error)>self.angle_tolerance:
          msg.linear.x=0.0
          msg.angular.z=self.kp_angular*heading_error
       else:
        msg.linear.x=min(self.kp_linear*distance_error,2.0)
        msg.angular.z=self.kp_angular*heading_error
       self.publisher.publish(msg)
       

def main():
      rclpy.init()
      node = GoToMultipleNode()
      rclpy.spin(node)
      node.destroy_node()
      rclpy.shutdown()

