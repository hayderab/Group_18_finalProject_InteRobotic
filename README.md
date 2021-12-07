# Group_18_finalProject_InteRobotic
Intelligent Robotic Group 18 Final Project

## How to run
1. Copy and place the "_maze_robot_package_" folder at: _'/home/'$USER'/catkin_ws/src'_
2. Re-built your catkin, in a new terminal type: " _cd ~/catkin_ws_ " and then " _catkin_make_ "
3. Copy and paste the "_maze_robot_package.sh_" file at (your home folder): _'/home/'$USER'/'_
4. Be sure that the "_main.py_" file is executable: " _chmod u+x '/home/'$USER'/catkin_ws/src/maze_robot_package/src/main.py'_ "
5. Be sure that the script (.sh file) is executable: " _chmod u+x maze_robot_package.sh_ "
6. In a new terminal, run: " _./maze_robot_package.sh_ "
7. In a new terminal, you can run a file for testing: " _rosrun maze_robot_package main.py_ "

After the above steps, Stage ROS should be executed (due to step 6) and on your terminal you should see the grid's dictionary (due to step 7).

**Note**: As a target, I setup the cells in the centre of the maze (8 <= x <= 10 and 9 <= y <= 11) given _reward = 10_

## Extra
If you face any issues, try to rebuild the package from scratch, please use the following link as a guide: 
https://duckietown.mit.edu/media/pdfs/1rpRisFoCYUm0XT78j-nAYidlh-cDtLCdEbIaBCnx9ew.pdf
