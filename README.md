# Group_18_finalProject_InteRobotic - University of Birmingham
This is our final project for the Intelligent Robotic module. The aim of the project was to apply the MDP technique called "policy iteration" in order for the robot to find the shortest path in the maze and reach the terminal state.

## How to run
1. Copy and place the "_maze_robot_package_" folder at: _'/home/'$USER'/catkin_ws/src'_
2. Re-built your catkin, in a new terminal type: " _cd ~/catkin_ws_ " and then " _catkin_make_ "
3. Copy and paste the "_maze_robot_package.sh_" file at (your home folder): _'/home/'$USER'/'_
4. Be sure that the "_main.py_" file is executable: " _chmod u+x '/home/'$USER'/catkin_ws/src/maze_robot_package/src/main.py'_ "
5. Be sure that the "_maze_robot_package.sh_" file is also executable: " _chmod u+x maze_robot_package.sh_ "
6. In a new terminal, run: " _./maze_robot_package.sh_ "

**After the above steps**:
1. Stage ROS should be executed
2. The pickle file containing a policy that has already been generated will be loaded.
3. Finally, you should see the robot move to reach the terminal stage in the maze following the policy instructions.

**Notes**: 
* If you want to execute the policy iteration from scratch, please uncomment the lines 98, 99 and 102 from the "_publisher_node.py_" file.
* As a terminal stage, I setup a cell in the center of the maze, specifically at the point (x = 9, y = 9).
  The terminal stage coordinates (x, y) can be changed in lines 54-55 of the "_maze_dictionary.py_" file.

## Extra
If you face any issues, try to rebuild the package from scratch, please use the following link as a guide: 
https://duckietown.mit.edu/media/pdfs/1rpRisFoCYUm0XT78j-nAYidlh-cDtLCdEbIaBCnx9ew.pdf
