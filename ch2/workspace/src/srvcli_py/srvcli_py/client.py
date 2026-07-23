import sys
import rclpy
from rclpy.node import Node

from srv_pkg.srv import JointConversion     # Import the service message type used to fill the request


class JointConversionClient(Node):

    def __init__(self):
        super().__init__('joint_conversion_client')

	    # Create the service client object and wait that it appears online
        self.cli = self.create_client(
            srv_type=JointConversion, 
            srv_name='joint_conversion')

        while not self.cli.wait_for_service(timeout_sec=3.0):
            self.get_logger().info('service not available, waiting again...')


    def send_request(self, j_values: list):
    
        # Fill the request part, considering the 7 joint values    
        req = JointConversion.Request()
        for joint_msg, value in zip(req.joint_input, j_values):
            joint_msg.data = value

        # Call the server: The result is a future object that can be used to monitor its status
        # note: it returns immediately (async) - returna a future (result will be available later)
        self.future = self.cli.call_async(req)
        
        # wait that the server replies
        # in general cae we can do /while not future.done():/ and not to block execution, here is just an example
        rclpy.spin_until_future_complete(self, self.future)
        
        # The result is returned to the main function
        return self.future.result()


def main(args=None):

    rclpy.init(args=args)

    conversion_client = JointConversionClient()
    
    joint_values = [1.0, 0.78, 1.6, 0.0, 1.57, 0.3, 1.2]
  
    response = conversion_client.send_request(joint_values)
    print("Joint conversion results:")
    for i, (inp, out) in enumerate(zip(joint_values, response.joint_output), start=1):
        print(f"  Joint {i}: {inp:.2f} rad  ->  {out.data:.2f}°")

    conversion_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
