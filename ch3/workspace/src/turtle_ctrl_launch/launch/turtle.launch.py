"""
Launch file to run default Turtlesim 
The only goal is to remane the standard topics
"""
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    """
    Every Python launch file must define this function.
    - ros2 launch ...  -> calls generate_launch_description()
    - expects it to have a LaunchDescription inside the script.
    """
    ld = LaunchDescription()
    
    new_input_topic = "/cmd_vel"
    new_output_topic = "/pose"
    
    # node action - how the node should be launched
    sim_node = Node(
       package='turtlesim',         # this is built-in turtlesim node
       executable='turtlesim_node', # look at: ros2 run turtlesim turtlesim_node
       name='sim',                  # rename the default node name turtlesim to sim
       remappings=[
           ('/turtle1/cmd_vel', new_input_topic),   # use a simpler topic name /cmd_vel
           ('/turtle1/pose', new_output_topic),
       ]
    )
    
    ld.add_action(sim_node)
    
    return ld
