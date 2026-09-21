# The package drives a pendulum simulation instead of simple sliders. 

  It publishes `/joint_states` with a sine wave to animate the revolute_joint, which causes `robot_state_publisher` to compute and broadcast TF transforms. 
  
  It then reads back the transform from `base_link` to `pole_link` and logs it — demonstrating the full loop of publishing joint states and observing the resulting robot geometry.



# How to run

  ## terminal 1
  `ros2 launch pendulum_robot_description robot_description.launch.py`

  ## terminal 2
  `ros2 launch pendulum_robot_description display.launch.py
`
  ## terminal 3
  `ros2 run pendulum_state state_publisher_and_tf`

  display.launch.py starts joint_state_publisher_gui (manual sliders) and rviz2. Terminal 3 replaces the sliders with the automatic sine wave — but running
  both at the same time will conflict since they'd both publish to /joint_states. You'd pick one or the other.


# JointStatePublisher
- Publishes `/joint_states` for a single revolute joint driven by a sine wave.
- It also reads back the resulting TF transform from `base_link` to `pole_link`, demonstrating how joint states propagate through `robot_state_publisher` into the TF tree.
- Requires `pendulum_robot_description` to be running so that `robot_state_publisher` has a robot model to work with.

# Gazebo


# Isaac Sim
  ## Requirements
  - NVIDIA GPU + driver, with the NVIDIA Container Toolkit installed
  - An NGC account and API key: `docker login nvcr.io` (one-time)

  ## How to run
  `docker compose -f docker-compose-isaac_ubuntu.yaml up`

  This starts both the `ros2` container (same as `docker-compose-ubuntu.yaml`) and the `isaac-sim` container together, sharing the
  host network.

  Once Isaac Sim's GUI is open, enable **Window → Extensions → ROS2 Bridge** so it can publish/subscribe on the same ROS 2 topics
  as your nodes running in the `ros2` container.
