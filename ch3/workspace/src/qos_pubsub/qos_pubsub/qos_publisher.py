"""
Pub?Sub communication with Quality of Service profile
"""
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy


class SensorPublisher(Node):
    def __init__(self):
        super().__init__('sensor_publisher')        # Node name
        
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,         # Every message should reach the subscriber.
            durability=DurabilityPolicy.TRANSIENT_LOCAL,    # publisher keeps recent messages in memory
            depth=100                                       # Store up to 100 messages
        )

        self.publisher_ = self.create_publisher(String, 'data', qos_profile)
        self.timer = self.create_timer(0.3, self.publish_sensor_data_callback)       # Publish at 3 Hz
        
        self.counter = 0

    def publish_sensor_data_callback(self):
        """
        At every tick, publish data
        """
        msg = String()
        msg.data = f'Sensor data {self.counter}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.counter += 1


def main(args=None):
    rclpy.init(args=args)
    sensor_publisher = SensorPublisher()

    try:
        rclpy.spin(sensor_publisher)
    except KeyboardInterrupt:
        pass
    finally:
        print("SHutting down...")
        sensor_publisher.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
        print("done.")

if __name__ == '__main__':
    main()

