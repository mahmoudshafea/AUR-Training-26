import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from std_srvs.srv import SetBool

class GoToGoal(Node):
    def __init__(self):
        super().__init__('go_to_goal')
        self.declare_parameter('TARGET_X', 0.0)
        self.declare_parameter('TARGET_Y', 0.0)
        self.declare_parameter('KP_LINEAR',0.0)
        self.declare_parameter('KP_ANGULAR',0.0)
        self.declare_parameter('DISTANCE_TOLERANCE', 0.0)
        self.declare_parameter('ANGLE_TOLERANCE',0.0)
        self.declare_parameter('LOOP_RATE',0)
        self.declare_parameter('CURRENT_POSE',None)
        self.declare_parameter('GOAL_REACHED',False)



        self.target_x = self.get_parameter('TARGET_X').value
        self.target_y = self.get_parameter('TARGET_Y').value
        self.kp_linear = self.get_parameter('KP_LINEAR').value
        self.kp_angular = self.get_parameter('KP_ANGULAR').value
        self.distance_tolerance = self.get_parameter('DISTANCE_TOLERANCE').value
        self.angle_tolerance = self.get_parameter('ANGLE_TOLERANCE').value
        self.loop_rate = self.get_parameter('LOOP_RATE').value

        self.current_pose=self.get_parameter('CURRENT_POSE').value
        self.goal_reached=self.get_parameter('GOAL_REACHED').value


        # ROS 2 Publisher & Subscriber
        self.cmd_vel_publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.pose_subscriber = self.create_subscription(
            Pose, '/turtle1/pose', self.pose_callback, 10
        )

        #Service server el hayakhod men elclient elboolean w y check 3aleh w ba3daha yehoto f variable astakhdemo felcontrol callback
        self.srv = self.create_service(SetBool,"setbool",self.check_boolean)


        # Control Loop running at 20 Hz
        self.timer = self.create_timer(1.0 / self.loop_rate, self.control_loop)


        self.get_logger().info(f'Navigating turtle to target goal: ({self.target_x}, {self.target_y})')
        self.activation=False

    def check_boolean(self,request,response):
        if request.data is False:
            self.activation=False
        else:
            self.activation=True
        response.success=True
        response.message="Request done"
        return response



    def pose_callback(self, msg: Pose):
        """Update current position and heading from /turtle1/pose stream."""
        self.current_pose = msg

    def normalize_angle(self, angle: float) -> float:
        """Keep heading angle within [-pi, pi] to avoid unnecessary 360-degree turns."""
        while angle > math.pi:
            angle -= 2.0 * math.pi
        while angle < -math.pi:
            angle += 2.0 * math.pi
        return angle

    def control_loop(self):
        """Proportional Control Loop."""
        if self.current_pose is None or self.goal_reached or self.activation is False:
            return

        # 1. Calculate Cartesian Errors
        dx = self.target_x - self.current_pose.x
        dy = self.target_y - self.current_pose.y

        # Euclidean Distance Error: sqrt((x_g - x)^2 + (y_g - y)^2)
        distance_error = math.sqrt(dx**2 + dy**2)

        # Desired Heading Angle: atan2(dy, dx)
        target_angle = math.atan2(dy, dx)
        heading_error = self.normalize_angle(target_angle - self.current_pose.theta)

        msg = Twist()

        # 2. Check if Goal is Reached
        if distance_error < self.distance_tolerance:
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.cmd_vel_publisher.publish(msg)
            self.goal_reached = True
            self.get_logger().info('Goal Reached Successfully!')
            return

        # 3. Proportional Control Logic
        # If heading error is large, align facing direction first before moving forward
        if abs(heading_error) > self.angle_tolerance:
            msg.linear.x = 0.0
            msg.angular.z = self.kp_angular * heading_error
        else:
            # Scale forward speed and heading alignment concurrently
            msg.linear.x = min(self.kp_linear * distance_error, 2.0)  # Cap speed at 2.0 m/s
            msg.angular.z = self.kp_angular * heading_error

        self.cmd_vel_publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = GoToGoal()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
