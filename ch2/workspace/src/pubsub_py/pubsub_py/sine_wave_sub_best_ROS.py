import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import matplotlib.pyplot as plt


class SinusoidalSubscriber(Node):

    def __init__(self):
        super().__init__("sinusoidal_subscriber")   # register a node /sinusoidal_subscriber
        self.data = []
        self.start_time = None

        # Event 1
        self.subscription = self.create_subscription(
            Float64,
            "sinusoidal_signal",        # topic
            self.callback,
            10                          # queue size
        )

        # Event 2
        self.timer = self.create_timer(
            0.1,                    # timer expires every 0.1 sec
            self.check_finished     # call after expiration
        )

    def callback(self, msg):

        # first time
        if self.start_time is None:
            self.start_time = self.get_clock().now()

        self.data.append(msg.data)

    def check_finished(self):
        # ignore timer if collection is not started yet
        if self.start_time is None:
            return

        elapsed = (self.get_clock().now() - self.start_time).nanoseconds / 1e9

        # plot ofter 15 sec is over
        if elapsed >= 15:
            plt.plot(self.data)
            plt.show()

            self.destroy_node()
            rclpy.shutdown()


def main():
    rclpy.init()
    node = SinusoidalSubscriber()
    rclpy.spin(node)


if __name__ == "__main__":
    main()