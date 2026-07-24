import rclpy
import math 
from rclpy.node import Node

from rclpy.action import ActionServer
from action_pkg.action import LinearControl


class LinearControlServer(Node):
    """
    Action server Node
    """

    def __init__(self):
        super().__init__('linear_control_action_server')
        self._action_server = ActionServer(
            self,
            action_type=LinearControl,      # link to interface from action_pkg: goal/result/feedback
            action_name='linear_control',   # visible with  'ros2 action list'
            execute_callback=self.execute_callback)
        
    def execute_callback(self, goal_handle): 
        """
        Callback, executed when an action request comes (goal is sent by a client)
        goal_handle contains: 
         - request, status, feedback
         - functions: goal_handle.succeed(), goal_handle.abort(), goal_handle.canceled()
        
        :param self: Description
        :param goal_handle: a data structure came from LinearControl.action request interface, contains initial_position etc 
        """  
        # read the Goal   
        curr_pos = goal_handle.request.initial_position
        goal_pos = goal_handle.request.goal_position
        velocity = goal_handle.request.linear_velocity
        self.get_logger().info(
            f"Received goal: start={curr_pos:.3f}, "
            f"goal={goal_pos:.3f}, velocity={velocity:.3f}"
        )
        
        dist = abs(curr_pos - goal_pos)       # initial distance
        rate = self.create_rate(50)
        dt = 1.0 / 50.0                       # run at 50Hz
        
        feedback_msg = LinearControl.Feedback()     # defined in LinearControl.action feedback section        
        
        # While the goal has not been reached
        while dist > 1e-2:
        
            # Simulate the motion: move at vel at every step
            step = velocity * dt
            if curr_pos < goal_pos:
                curr_pos = min(curr_pos + step, goal_pos)       # prevent overshooting
            else:
                curr_pos = max(curr_pos - step, goal_pos)   
            
            # Calcualte new distance and set feedback
            dist = math.fabs(curr_pos - goal_pos) 

            # set and publish a feedback
            feedback_msg.distance = dist
            goal_handle.publish_feedback(feedback_msg)

            rate.sleep()
            
        self.get_logger().info("Goal reached successfully.")
        goal_handle.succeed()
        result = LinearControl.Result()
        result.motion_done = True
        return result
        

def main(args=None):
    rclpy.init(args=args)
    linear_control_action_server = LinearControlServer()
    rclpy.spin(linear_control_action_server)
    
if __name__ == '__main__':
    main()
    
    