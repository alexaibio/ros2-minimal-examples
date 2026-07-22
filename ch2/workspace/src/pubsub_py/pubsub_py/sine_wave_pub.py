#!/usr/bin/env python3

# Run: ros2 run pubsub_py sine_wave_pub

import rclpy
from rclpy.node import Node

# Import the datatype to publish towards the ROS2 network
from std_msgs.msg import Float64

import math


class SinusoidalPublisher(Node):

    def __init__(self):
        super().__init__('sinusoidal_publisher')

        self.publisher = self.create_publisher(Float64, 'sinusoidal_signal', 10)

        """
        EVENT SOURCE - Create timer to publish sinusoidal signal
        Note: we dont have to store it in self.timer, only self.create_timer is important!
        might also be
            create_publisher()
            create_subscription()
            create_service()
            create_timer()
        """
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.i = 0

    def timer_callback(self):       
        amplitude = 2.10
        frequency = 0.1
        msg = Float64()

        # Calculate the sine wave signal at time i
        msg.data = amplitude * math.sin(2 * math.pi * frequency * self.i )
        
        # Publish the data
        self.publisher.publish(msg)
            
        # Increment counter
        self.i += 0.1


def main(args=None):
	rclpy.init(args=args)                  # nitializes the ROS middleware.

	sinusoidal_publisher = SinusoidalPublisher()

    # EVENt LOOP - execute callback by timer
    # cooperative scheduling (not preeemtive - выполнение не прерывается)
	rclpy.spin(sinusoidal_publisher)       

	sinusoidal_publisher.destroy_node()
	rclpy.shutdown()                       # free ROS runtime


if __name__ == '__main__':
	main()

