"""
Launch file to run Turtlesim with parameters
 - ros2 launch turtle_ctrl_launch launch_with_param.launch.py
"""
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

   ld = LaunchDescription()
    
   # to laucnh the controller node (with parameers)
   ctrl_node = Node(
       package='turtle_ctrl',             # ros2 run turtle_ctrl turtle_control_param
       executable='turtle_control_param',
       name='control_with_param',         # new name
       output='screen',                   # Show the node's output in the terminal
       parameters=[
            {"linear_velocity_scale": 0.1},
            {"angular_velocity_scale": 1.0}
       ],
       remappings=[
           ('/turtle1/cmd_vel', '/cmd_vel'),
       ]
   )
    
   # turtle.launch.py - just a turtle without params
   included_launch_path = PathJoinSubstitution([
       get_package_share_directory('turtle_ctrl_launch'),	
       'turtle.launch.py'
   ])
   print(" included_launch_path: ", get_package_share_directory('turtle_ctrl_launch'))
    
   # Start Node 1 (Turtle without prams)
   ld.add_action( IncludeLaunchDescription(                   # launch it
        PythonLaunchDescriptionSource(included_launch_path)   # This is a Python launch file
                  ) 
   )
   
   # Start Node 2 (Trutle with params)
   ld.add_action(ctrl_node)

   return ld
