"""
A Turtle controller node.
An intermediate class to call Turtle Node with several additional parameters in between
"""

import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import SetParametersResult
from std_msgs.msg import String
from geometry_msgs.msg import Twist


class TurtleControl(Node):
    """
    A node to control Turle with additional parameters
    """
    def __init__(self):
    
        super().__init__('turtle_control_param')        # register the Node
  
  		# Define parameters list      
        self.declare_parameter('linear_velocity_scale',  1.0)
        self.declare_parameter('angular_velocity_scale', 1.0)
        self.declare_parameter('max_linear_velocity',    2.0) 
        self.declare_parameter('max_angular_velocity',   2.5)
        
        # on_change callback: if someone changes a parameter, call this function.
        self.add_on_set_parameters_callback(self.parameter_callback)
        
        # publisher to publish velocity messgaes to Turtle Topic
        self.cmd_vel_publisher = self.create_publisher(
            msg_type=Twist, 
            topic='/turtle1/cmd_vel', 
            qos_profile=10              # queue size
            )
       
        # read parameters to the class instance
        #self.linear_velocity_scale = self.get_parameter('linear_velocity_scale').get_parameter_value().double_value 
        self.linear_velocity_scale = self.get_parameter("linear_velocity_scale").value
        self.angular_velocity_scale = self.get_parameter('angular_velocity_scale').get_parameter_value().double_value 
        self.max_linear_velocity  = self.get_parameter('max_linear_velocity').get_parameter_value().double_value 
        self.max_angular_velocity  = self.get_parameter('max_angular_velocity').get_parameter_value().double_value 
        
        self.get_logger().info(f"linear_velocity_scale:  {self.linear_velocity_scale}")
        self.get_logger().info(f"angular_velocity_scale: {self.angular_velocity_scale}")
        self.get_logger().info(f"max_linear_velocity:  {self.max_linear_velocity}")
        self.get_logger().info(f"max_angular_velocity:  {self.max_angular_velocity}")
        
        # velocity and angle which is sent to turtle
        self.vel_x = 1.0 * self.linear_velocity_scale
        self.ang_vel_z = 1.0 * self.angular_velocity_scale
        
        self.timer = self.create_timer(0.5, self.timer_callback)
        
    def timer_callback(self):  
        """
        Every tick publish the velocity message
        """     
        v = Twist()                         # standard ROS message for robot velocity
        v.linear.x = self.vel_x
        v.angular.z = self.ang_vel_z     
        self.cmd_vel_publisher.publish(v)   # Publish

    def parameter_callback(self, params):
        """
        On_change parameters callback. 
        Must return SetParametersResult(successful=True) or False
        """
        # Temporary variables
        linear_scale = self.linear_velocity_scale
        angular_scale = self.angular_velocity_scale
        max_linear = self.max_linear_velocity
        max_angular = self.max_angular_velocity

        # Apply requested changes to temporary variables
        for param in params:
            if param.name == 'linear_velocity_scale':
                linear_scale = param.value
            elif param.name == 'angular_velocity_scale':
                angular_scale = param.value
            elif param.name == 'max_linear_velocity':
                max_linear = param.value
            elif param.name == 'max_angular_velocity':
                max_angular = param.value

        # Validate
        if self.vel_x * linear_scale > max_linear:
            return SetParametersResult(successful=False)

        if self.ang_vel_z * angular_scale > max_angular:
            return SetParametersResult(successful=False)

        # Commit changes
        self.linear_velocity_scale = linear_scale
        self.angular_velocity_scale = angular_scale
        self.max_linear_velocity = max_linear
        self.max_angular_velocity = max_angular

        self.vel_x *= self.linear_velocity_scale
        self.ang_vel_z *= self.angular_velocity_scale

        return SetParametersResult(successful=True)


def main(args=None):
    
    rclpy.init(args=args)
    node = TurtleControl()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:       # SIGINT by Ctrl-C, allow destroy and shutdown
        print("Stopping by user...")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

