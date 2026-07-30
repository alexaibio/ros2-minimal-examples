# Chapter 3: Supplementary tools for ROS2

Note:
- It is supposed to be run in VSCode as `Open in Docker`. Make sure you have a right `.devcontainer` folder.
- make sure you run `XQuartz` if you are on MacOs and set `xhost +localhost` or `xhost +host.docker.internal`
- 

## Turtlesim
Start sequence if you are on MacOS:
- `open -a XQuartz` 
- `XQuartz → Preferences → Security` - Allow connections from network clients
- `xhost +localhost`
- `ros2 run turtlesim turtlesim_node`

