FROM osrf/ros:humble-desktop

# ---- user config ----
# Note that for MacOs it is not neccesary, only if your host machine is UBUNTU
ARG UID=501
ARG GID=20


# not to ask interactive questions during package installation
ENV DEBIAN_FRONTEND=noninteractive     

# ---- system + ROS dev tools ----
RUN apt-get update && apt-get install -y \
    sudo \
    ros-dev-tools \
    git \
    curl \
    wget \
    nano \
    vim \
    less \
    && rm -rf /var/lib/apt/lists/*


# ---- create matching user ----
# create home folder (-m) etc
# gives the user passwordless sudo access - append text into the file

RUN useradd -m -u $UID -g $GID -s /bin/bash rosuser && \
    echo "rosuser ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers     

# ---- fix ownership ----
RUN chown -R $UID:$GID /home/rosuser

# ---- ROS sourcing ----
RUN echo "source /opt/ros/humble/setup.bash" >> /home/rosuser/.bashrc && \
    echo '[ -f ~/ros2_ws/install/setup.bash ] && source ~/ros2_ws/install/setup.bash' >> /home/rosuser/.bashrc


# ---- shell customization ----
RUN echo 'export PS1="\e[0;34m[\u@\h:\e[0;33m \W\e[0;34m]\$ \e[m "' >> /home/rosuser/.bashrc && \
    echo "alias ls='ls --color=auto'" >> /home/rosuser/.bashrc && \
    echo "alias ll='ls -l --color=auto'" >> /home/rosuser/.bashrc && \
    echo "alias la='ls -la --color=auto'" >> /home/rosuser/.bashrc && \
    echo "alias ..='cd ..'" >> /home/rosuser/.bashrc

USER rosuser
WORKDIR /home/rosuser

CMD ["/bin/bash"]