import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64

import threading

import matplotlib.pyplot as plt


class SinusoidalSubscriber(Node):
    def __init__(self):
        super().__init__('sinusoidal_subscriber')
        
        # callback - A function invoked everytime a new data is published on a topic.
        self.sub = self.create_subscription(
            Float64, 
            'sinusoidal_signal', 
            self.sinu_sub_callback,     # topic
            10
            )
        
        self.first_data_arrived = False
        self.sinu_values = None
        
        # Time in seconds to store new data 
        self.logging_time = 15
            
    def sinu_sub_callback( self, msg ):
        self.sinu_values = msg.data
        self.first_data_arrived = True
        
    def log_data(self):
        rate = self.create_rate(10)     # Node method
        sinu_data = []
        
        # Wait the first data arrived	
        while(self.first_data_arrived == False):
            rate.sleep()        # object that lets me run a loop at 10 Hz.
        
        self.get_logger().info('Starting logging sine wave!')
        t = 0.0
        
        # log for only 15 sec and then destroy the node
        # use custom-made loop
        while (t < self.logging_time):
            sinu_data.append( self.sinu_values )            
            t = t + 0.1 
            rate.sleep()    # 10Hz
       	    
        self.destroy_node() 
        
        # Generate the plot
        plt.plot(sinu_data)

        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Sine wave data')
        plt.show()
        
        rclpy.shutdown() 
                

def main(args=None):
    rclpy.init(args=args) 
    sinusoidal_subscriber = SinusoidalSubscriber()
     
    # Start a new thread that logs the data running in parallel with the rest of the code
    t = threading.Thread(target=sinusoidal_subscriber.log_data, args=[])
    t.start()
        
    rclpy.spin(sinusoidal_subscriber) 

   
if __name__ == '__main__':
    main()

