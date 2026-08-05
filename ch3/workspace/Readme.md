# Chapter 3: Supplementary tools for ROS2

Note 1:
- It is supposed to be run in VSCode as `Open in Docker`. Make sure you have a right `.devcontainer` folder.

Note 2: Running turtlesim on macOS
- turtlesim renders its GUI using the X11 windowing system. Since macOS does not include an X11 server by default, if you are using MacOS it is neccesary to run X11 emulator -  `XQuartz` 
- If you are running ROS 2 inside Docker, allow the Docker container to connect to your local X11 server by adding the host from where the graphics command will come to local X11, i.e to set `xhost +localhost`
- make sute in  `XQuartz`  settgins that remote connections are allowed


## Turtlesim
Start sequence if you are on MacOS:
- `open -a XQuartz` 
- `XQuartz → Preferences → Security` - Allow connections from network clients
- `xhost +localhost`
- check if XQuartz is accesible from docker by running in docker `xclock`
  
  Run it : `ros2 run turtlesim turtlesim_node`

## Using CLI to publish topics

### Tupic Publishing
Pattern: `ros2 topic pub <topic_name> <message_type> '<message_data>'`

For example (publish every 0.5Hz):
`ros2 topic pub -r 0.5 /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 1.8}}"`

### Service request

Pattern: `ros2 service call <service_name> <service_type> '<request_parameters>'`

For example (create a new turtle):
`ros2 service call /spawn turtlesim/srv/Spawn "{x: 2.0, y: 2.0, theta: 0.0, name: 'turtle2'}"`


## Node Parameters: turtle_ctrl
This is a node that publishes a velocity command to move the turtle with the following parameters
- two parameters for velocity scaling
- two for velocity thershold 


## Launch Files
