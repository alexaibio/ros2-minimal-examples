# Minimal ROS2 Examples



## Intro
This repository is based on the book Ultimate Robotics Programming with ROS 2 and Python by Jonathan Cacace. The examples have been reorganized, simplified, and cleaned up to make them easier to understand and experiment with

The repository is organized by book chapters. Each chapter contains its own ROS 2 workspace together with a corresponding Docker configuration, allowing every chapter to be run independently using Docker or VS Code Dev Containers.


## Running ROS 2 with Docker
There are several ways to work with ROS2
- install it locally, but be aware that on MacOS it is probably not the best choice
- Use Docker with the official ROS2 image.

In each workspace of this repo there is a docker-compose file which is OS specific (ubuntu and macos), you can either just run it with

`docker compose -f docker-compose-macos.yaml up`

and then connect to it with

`docker exec -it ros2container bash`

Now you can use an external editor to edit files in workspace directly. The workspace is mounted into the container as a volume, so you can edit the files directly using your preferred editor.

Alternatively, you can open the workspace in VS Code using `Dev Containers: Reopen in Container`


## Chapter 1: basic examples
- Pub/Sub communication, server and client nodes
- Service communication, server and client nodes
- Action communication, server and client nodes
