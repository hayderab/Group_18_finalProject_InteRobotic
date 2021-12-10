#!/bin/bash

gnome-terminal -x bash -c "roscore" xdotool getactivewindow windowminimize
sleep 4
gnome-terminal -x bash -c "rosrun map_server map_server '/home/'$USER'/catkin_ws/src/maze_robot_package/data/maps/maze.yaml'" xdotool getactivewindow windowminimize
sleep 4
gnome-terminal -x bash -c "rosrun stage_ros stageros '/home/'$USER'/catkin_ws/src/maze_robot_package/data/maps/maze.world'" xdotool getactivewindow windowminimize
sleep 4
gnome-terminal -x bash -c "roslaunch socspioneer keyboard_teleop.launch" xdotool getactivewindow windowminimize
