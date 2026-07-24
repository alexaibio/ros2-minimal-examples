import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from action_pkg.action import LinearControl


class LinearControlClient(Node):
    """
    ROS2 Node as Action client
    """

    def __init__(self):
        super().__init__('linear_control_action_client')    # visible with ros2 node list
        self._action_client = ActionClient(
            self, 
            action_type=LinearControl,          # I want to communicate with this action
            action_name='linear_control')

    def send_goal(self, initial_position, goal_position, linear_velocity):
        """
        Prepare the action request 
        
        :param initial_position: goal
        :param goal_position: goal
        :param linear_velocity: goal
        """

        # Create a goal, described in LinearControl.action
        goal_msg = LinearControl.Goal()
        goal_msg.initial_position = initial_position
        goal_msg.goal_position = goal_position
        goal_msg.linear_velocity = linear_velocity

        # Connets to the server: blocks until the server exists.
        self._action_client.wait_for_server()

        # Send the goal asynchronically (non blocking)
        # call this callback when the server publish feedback
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg, 
            feedback_callback=self.feedback_callback)
        
        # when the future finishes, call this callback
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    # It the goal has been accepted, we can define a new callback to listen its result    
    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info('Result: {0}'.format(result.motion_done))
        rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info('Received feedback: {0}'.format(feedback.distance))
        

def main(args=None):
    rclpy.init(args=args)
    action_client = LinearControlClient()

    initial_position = 0.0
    goal_position = 1.7
    linear_velocity = 0.2

    future = action_client.send_goal(initial_position, goal_position, linear_velocity)
 
    rclpy.spin(action_client)


if __name__ == '__main__':
    main()
