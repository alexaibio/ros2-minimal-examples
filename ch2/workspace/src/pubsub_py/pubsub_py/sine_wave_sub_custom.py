"""
Pub/sub communication example for extended message
"""
import matplotlib
print("Backend =", matplotlib.get_backend())
import matplotlib.pyplot as plt

import rclpy
from rclpy.node import Node
from msgs_pkg.msg import SineWave


class SinusoidalSubscriber(Node):
    def __init__(self):
        super().__init__("sinusoidal_subscriber")   # register a node /sinusoidal_subscriber
        self.data = []
        self.start_time = None

        # Event 1
        self.subscription = self.create_subscription(
            SineWave,
            "sinusoidal_signal_custom",         # topic
            self.callback,
            10                                  # queue size
        )

        # Event 2
        self.timer = self.create_timer(
            0.1,                    # timer expires every 0.1 sec
            self.check_finished     # call after expiration
        )

        self.get_logger().info("Subscriber has been initialized...")

    def callback(self, msg):
        # first time
        if self.start_time is None:
            self.start_time = self.get_clock().now()

        self.data.append(msg.signal.data)

    def check_finished(self):
        # ignore timer if collection is not started yet
        if self.start_time is None:
            return

        elapsed = (self.get_clock().now() - self.start_time).nanoseconds / 1e9

        # plot ofter 15 sec is over
        if elapsed >= 15:
            self.get_logger().info("15 seconds are finished, plot the data and destroy node")
            plt.plot(self.data)
            #plt.show()
            plt.savefig("plot.png")

            self.destroy_node()
            rclpy.shutdown()


def main():
    rclpy.init()
    node = SinusoidalSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()