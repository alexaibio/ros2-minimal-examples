import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy


class SensorSubscriber(Node):
    def __init__(self):
        super().__init__('sensor_subscriber')

        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            depth=100
        )

        self.subscription = self.create_subscription(
            String,
            'data',
            self.listener_callback,
            qos_profile
        )

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')


def main(args=None):
    rclpy.init(args=args)
    sensor_subscriber = SensorSubscriber()

    # thereis only one way to stop spin, it is by ctrl-c, 
    try:
        rclpy.spin(sensor_subscriber)
    except KeyboardInterrupt:
        pass
    finally:
        print("Shutting down..")
        sensor_subscriber.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
        print("done.")

if __name__ == '__main__':
    main()

