#!/usr/bin/env python3

# Importing the rospy module
import rospy
# Import Twist() function to make the robot rotate once obtained the proper angle.
from geometry_msgs.msg import Twist
# Import files
import policy_iteration
import helper


class PublisherNode:

    @staticmethod
    def mover(sub_node, given_dict):
        move = Twist()
        pub = rospy.Publisher('cmd_vel', Twist, queue_size=100)
        rate = rospy.Rate(10)  # 10hz - do not send /cmd_vel commands too quickly
        kp = 1.7  # variable to control rotation speed (hyperparameter)
        current_direction_str = "EAST"  # random default value

        while not rospy.is_shutdown():

            move.linear.x = 0  # put linear.x velocity back to 0 (the robot is not going forwards anymore)
            move.angular.z = 0  # put rotation velocity back to 0 (the robot is not rotating anymore)

            # keep just the first 2 digits of the floats (for easier comparison)
            current_x = int(
                (float("{0:.1f}".format(sub_node.get_current_position_x()))) // 0.1)  # Occupancy Grid format x
            current_y = int(
                (float("{0:.1f}".format(sub_node.get_current_position_y()))) // 0.1)  # Occupancy Grid format y
            current_yaw = sub_node.get_yaw()
            formatted_current_yaw = float("{0:.1f}".format(sub_node.get_yaw()))

            current_direction_str = helper.find_direction(current_direction_str, current_yaw)

            # put current x,y in a tuple to compare with the dictionary's tuple
            current_position_tuple = (current_x, current_y)

            target_direction = given_dict[current_position_tuple][6]
            # calculate the rotation (in radians) which the robot needs in order to do to move to the next state
            rotate_target_rad = helper.calculate_rotation(target_direction, current_direction_str)

            # keep just the first 2 digits of the floats (for easier comparison)
            formatted_rotate_target_rad = float("{0:.1f}".format(rotate_target_rad))
            # If the robot has not yet achieved the required rotation, keep rotating
            if formatted_rotate_target_rad != formatted_current_yaw:

                # control rotation speed * (difference between the target rotation and the current rotation of the robot)
                # if difference is big, the robot will rotate faster
                move.angular.z = kp * (
                        rotate_target_rad - current_yaw)  # Speed of the velocity to rotate
                print("rotate")

            else:  # If the robot achieved the required rotation, go straight
                move.linear.x = 1.0
                print("forwards")

            pub.publish(move)  # move the robot (publish the move)
            rate.sleep()  # give sometime to pass the info

    def talker(self, sub_node):

        # Run the policy
        print("Running Policy Iteration...")
        policy_dict = policy_iteration.policy_iteration(sub_node.get_dictGrid(), sub_node.get_width_length(),
                                                    sub_node.get_height_length(), 0.9)
        # Create a pickle of that policy
        helper.create_dict_pickle(policy_dict, "pickle_dict.pickle")

        policy_pickle_dict = helper.load_dict_pickle("pickle_dict.pickle")

        print("Robot is moving...")
        self.mover(sub_node, policy_pickle_dict)
