#!/usr/bin/env python3

# Importing the rospy module
import rospy
# Import Twist() function to make the robot rotate once obtained the proper angle
from geometry_msgs.msg import Twist
# Import files
import policy_iteration
import helper
import time


class PublisherNode:

    @staticmethod
    def mover(sub_node, policy_dict):
        move = Twist()
        pub = rospy.Publisher('cmd_vel', Twist, queue_size=100)
        rate = rospy.Rate(10)  # 10hz - do not send /cmd_vel commands too quickly
        kp = 1.7  # variable to control rotation speed (hyperparameter)
        current_direction_str = "DEFAULT"  # random default value

        print("Robot is moving...")
        time.sleep(1)  # Show the message for 1 sec

        while not rospy.is_shutdown():

            move.linear.x = 0  # put linear.x velocity back to 0 (the robot is not going forwards anymore)
            move.angular.z = 0  # put rotation velocity back to 0 (the robot is not rotating anymore)

            # Get the current position of the robot from the Subscriber and convert it into an Occupancy Grid format
            # keep just the first 2 digits of the floats (for easier comparison)
            current_x = int(
                (float("{0:.1f}".format(sub_node.get_current_position_x()))) // 0.1)  # Occupancy Grid format x
            
            # Convert the coordinate to be a multiple of 2
            if (current_x % 2) == 1:
                current_x -= 1

            current_y = int(
                (float("{0:.1f}".format(sub_node.get_current_position_y()))) // 0.1)  # Occupancy Grid format y
            
            # Convert the coordinate to be a multiple of 2
            if (current_y % 2) == 1:
                current_y -= 1

            current_yaw = sub_node.get_yaw()  # Get the current yaw angle from the current Subscriber object
            formatted_current_yaw = float("{0:.1f}".format(sub_node.get_yaw()))  # Keep the first 2 digits

            # Terminate rospy if the robot has reached the terminal state
            if policy_dict[(current_x, current_y)][5]:
                rospy.signal_shutdown("Reached terminal state")
                print("Congratulations!!! The robot has reached the terminal state!")
                time.sleep(5)  # Show the message for 5 secs
                break

            # Get the current heading of the Robot
            current_direction_str = helper.find_direction(current_direction_str, current_yaw)

            # The robot tells the policy where it is on the map, the policy tells where to go next
            current_position_tuple = (current_x, current_y)  # 1. current position of the robot in a tuple
            print(current_position_tuple)

            # 2. Get the target heading from the policy dictionary, based on the given robot current position
            target_direction = policy_dict[current_position_tuple][6]

            # Calculate the target rotation (in radians) which the robot needs in order to move to the next state
            rotate_target_rad = helper.calculate_rotation(target_direction, current_direction_str)

            # Keep just the first 2 digits of the floats (for easier comparison)
            formatted_rotate_target_rad = float("{0:.1f}".format(rotate_target_rad))

            # If the robot has not yet achieved the required rotation, keep rotating
            if formatted_rotate_target_rad != formatted_current_yaw:

                # Reference: https://www.theconstructsim.com/ros-qa-135-how-to-rotate-a-robot-to-a-desired-heading-using-feedback-from-odometry/
                # control rotation speed * (difference between the target rotation and the current rotation of the robot)
                # If difference is big, the robot will rotate faster
                move.angular.z = kp * (
                        rotate_target_rad - current_yaw)  # rotate/angular speed
                print("rotate")

            else:  # If the robot achieved the required rotation, go straight
                move.linear.x = 0.5  # linear speed (try to keep it small)
                print(target_direction)

            pub.publish(move)  # move the robot (publish the move)
            rate.sleep()  # give some time to pass the info

    # Publisher ("talker") node which:
    # 1. Received the required map's and robot's data from the Subscriber node
    # 2. Stores/Loads the policy dictionary into/from a pickle file (optional-uncomment)
    # 3. Stores the policy dictionary into a .txt file for easier analysing (optional-uncomment)
    # 4. Move the robot based on the policy
    def talker(self, sub_node):

        # Run the policy
        # policy_dict = policy_iteration.policy_iteration(sub_node.get_maze_dict(), sub_node.get_width_length(),
        #                                                 sub_node.get_height_length(), 0.9)

        # Store the policy dictionary in a pickle file (in the project's directory)
        # helper.create_dict_pickle(policy_dict, "pickle_dict.pickle")

        # Load the pickle file (from the project's data directory)
        # works for the same terminal state when the policy was created, and for any starting point
        policy_pickle_dict = helper.load_dict_pickle("pickle_dict.pickle")

        # Test/Print the given policy for analysing
        # helper.test_policy(policy_dict, (20, 20))

        # Store the pickle dictionary into a text file (in your desktop folder)
        # helper.save_to_text_file(policy_pickle_dict, "policy.txt")

        # Move the robot based on the policy iteration
        self.mover(sub_node, policy_pickle_dict)
