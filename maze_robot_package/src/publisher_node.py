#!/usr/bin/env python3

# Importing the rospy module
import rospy
# Import Twist() function to make the robot rotate once obtained the proper angle.
from geometry_msgs.msg import Twist
# Importing math package for square roots, sinus and other calculations
import math
# Import policy_iteration.py file
import policy_iteration


class PublisherNode:
    @staticmethod
    def mover(sub):
        pub = rospy.Publisher('cmd_vel', Twist, queue_size=100)
        rate = rospy.Rate(10)  # 10hz - do not send /cmd_vel commands too quickly
        kp = 2  # variable to control rotation speed (hyperparameter)

        while not rospy.is_shutdown():
            move = Twist()
            # keep just the 2 digits of the floats (same as we did with the dictionary)
            current_x = float("{0:.1f}".format(sub.get_current_position_x()))
            current_y = float("{0:.1f}".format(sub.get_current_position_y()))
            # put current x,y in a tuple to compare with the dictionary's tuple
            current_position_tuple = (current_x, current_y)
            for coordinates, direction in sub.get_dummyDict().items():
                # If the coordinates of the robot are included to the given dictionary (if are the same)
                # the robot checks what the dictionary says to do at that state, then it applies that action
                if current_position_tuple == coordinates:  # compare the two tuples
                    if direction == "forwards":
                        move.linear.x = 1.0  # Speed of the velocity to go forwards
                        print(direction)
                    elif direction == "backwards":
                        move.linear.x = -1.0  # Speed of the velocity to go backwards
                        print(direction)
                    elif direction == "up":  # Go up
                        rotate_target_degrees = 90  # how many degrees the robot will rotate
                        rotate_target_rad = rotate_target_degrees * math.pi / 180  # convert degrees to radians because yaw angle is in radians
                        # control rotation speed * (difference between the target rotation and the current rotation of the robot)

                        # If the robot has not yet achieved the required rotation, keep rotating
                        if float("{0:.1f}".format(rotate_target_rad)) != float("{0:.1f}".format(sub.get_yaw())):
                            # if difference is big, the robot will rotate faster
                            move.angular.z = kp * (
                                    rotate_target_rad - sub.get_yaw())  # Speed of the velocity to rotate
                            pub.publish(move)
                            print("rotate 90°")

                        else:  # If the robot achieved the required rotation, go straight
                            move.angular.z = 0  # put rotation velocity back to 0 (the robot is not rotating anymore)
                            rate.sleep()
                            move.linear.x = 1.0
                            pub.publish(move)
                            print("forwards")

                    else:  # Go down
                        rotate_target_degrees = -90  # how many degrees the robot will rotate
                        rotate_target_rad = rotate_target_degrees * math.pi / 180  # convert degrees to radians because yaw angle is in radians
                        # control rotation speed * (difference between the target rotation and the current rotation of the robot)

                        # If the robot has not yet achieved the required rotation, keep rotating
                        if float("{0:.1f}".format(rotate_target_rad)) != float("{0:.1f}".format(sub.get_yaw())):
                            # if difference is big, the robot will rotate faster
                            move.angular.z = kp * (
                                    rotate_target_rad - sub.get_yaw())  # Speed of the velocity to rotate
                            pub.publish(move)
                            print("rotate -90°")

                        else:  # If the robot achieved the required rotation, go straight
                            move.angular.z = 0  # put rotation velocity back to 0 (the robot is not rotating anymore)
                            rate.sleep()
                            move.linear.x = 1.0
                            pub.publish(move)
                            print("forwards")

            pub.publish(move)  # move the robot (publish the move)
            rate.sleep()  # give sometime to pass the info

    @staticmethod
    def talker(sub_obj):
        # POLICY ITERATION can be called here
        print(policy_iteration.policy_generate(sub_obj.get_dictGrid(), sub_obj.get_width_length(),
                                               sub_obj.get_height_length(), 0.9, 1.0))
