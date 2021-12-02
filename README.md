# Group_18_finalProject_InteRobotic
Intelligent Robotic Group 18 Final Project

## How to run
1. Copy and place the "_maze_robot_package_" folder at: _'/home/'$USER'/catkin_ws/src'_
2. Re-built your catkin, in a new terminal type: " _cd ~/catkin_ws_ " and then " _catkin_make_ "
3. Copy and paste the "_maze_robot_package.sh_" file at (your home folder): _'/home/'$USER'/'_
4. Be sure that the script (.sh file) is executable: " _chmod + u+x maze_robot_package.sh_ "
5. In a new terminal, run: " _./maze_robot_package.sh_ "
6. In a new terminal, you can run a file for testing: " _rosrun maze_robot_package subscriber_node.py_ "

After the above steps, Stage ROS should be executed (due to step 5) and you should see the maze's occupancy grid data on your latest terminal window (due to step 6).

## Extra
If you want to see how to run the "publisher_node.py" file, please visit the following link: 
https://duckietown.mit.edu/media/pdfs/1rpRisFoCYUm0XT78j-nAYidlh-cDtLCdEbIaBCnx9ew.pdf