import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.action.client import ClientGoalHandle
from rclpy.task import Future

from action_pkg.action import LinearControl


class LinearControlClient(Node):
    """
    ROS2 Node as Action client
    """

    def __init__(self):
        super().__init__('linear_control_action_client')    # visible with ros2 node list
        self._action_client: ActionClient = ActionClient(
            self, 
            action_type=LinearControl,          # I want to communicate with this action
            action_name='linear_control')

    def send_goal(self, initial_position: float, goal_position: float, linear_velocity: float) -> None:
        """
        Prepare and send the action request 
        
        :param initial_position: goal
        :param goal_position: goal
        :param linear_velocity: goal
        """

        # Create a goal, described in LinearControl.action
        goal_msg = LinearControl.Goal()
        goal_msg.initial_position = initial_position
        goal_msg.goal_position = goal_position
        goal_msg.linear_velocity = linear_velocity

        # Connect to the server: blocks execution until the server is up.
        self.get_logger().info("Waiting for action server...")
        self._action_client.wait_for_server()

        # Send the goal asynchronically (non blocking)
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg, 
            feedback_callback=self.feedback_callback    # call this callback when the server publish feedback
            )
        
        # Future #1: waiting for goal accepting
        # (the whule event loop is hidden in rclpy.spin)
        self._send_goal_future.add_done_callback(self.goal_response_callback)
     
    def goal_response_callback(self, future: Future):
        """
        Goal has been accepted, define a new callback to listen its result 
        """
        goal_handle: ClientGoalHandle = future.result()

        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')

        # Future #1: waiting for result
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        """
        Goal is finished
        """
        result = future.result().result
        self.get_logger().info('Result: {0}'.format(result.motion_done))
        rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info('Received feedback: {0}'.format(feedback.distance))
        

def main(args=None):
    rclpy.init(args=args)

    action_client: LinearControlClient = LinearControlClient()

    initial_position = 0.0
    goal_position = 1.7
    linear_velocity = 0.2

    action_client.send_goal(
        initial_position, 
        goal_position, 
        linear_velocity)
 
    rclpy.spin(action_client)


if __name__ == '__main__':
    main()
