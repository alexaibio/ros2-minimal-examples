import rclpy
import time
from srv_pkg.srv import JointConversion
from rclpy.node import Node


# Node class
class JointConversionService(Node):

    def __init__(self):
        super().__init__('joint_conversion_service')    # Name of the Node
	
	    # Create the service object. Here we specify the function that is invoked when the service is called
        self.srv = self.create_service(
            srv_type=JointConversion,       # interface, defined in srv_pkg
            srv_name='joint_conversion', 
            callback=self.joint_conversion_callback)
        
        # A random set of values representing the offset to add to the joint vector
        self.offset = [0.2, 0.2, 0.2, 0.5, 0.5, 0.5, 0.0]

    def joint_conversion_callback(self, request, response):
        
        # Save the input vector of joints into a list
        j_values = [joint.data for joint in request.joint_input]
                   
        # Apply the offset
        result = [x + y for x, y in zip(j_values, self.offset)]
        
        # Transform from rad to degree
        result = [(x * 180.0) / 3.1415 for x in result]

	    # Retro transofrm the list into the result field of the service
        for out_joint, value in zip(response.joint_output, result):
            out_joint.data = value

        # Just wait a bit, to check the output on the terminal
        time.sleep(5)
        print("Conversion performed")
        return response


def main(args=None):
    rclpy.init(args=args)
    conversion = JointConversionService()
    rclpy.spin(conversion)
    rclpy.shutdown()

if __name__ == '__main__':
    main()

