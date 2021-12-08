#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import policy_iteration


class PublisherNode:
    @staticmethod
    def mover(sub):
        pub = rospy.Publisher('cmd_vel', Twist, queue_size=100)
        rate = rospy.Rate(10)  # 10hz - do not send /cmd_vel commands too quickly

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
                    if direction == "right":
                        move.linear.x = 1.0  # Turn right
                        print(current_position_tuple, coordinates, direction)
                    elif direction == "left":
                        move.linear.x = -1.0  # Turn left
                        print(current_position_tuple, coordinates, direction)
                    elif direction == "up":  # Go up
                        pass
                    else:  # Go down
                        pass
            pub.publish(move)
            rate.sleep()

    @staticmethod
    def talker(sub_obj):
        # POLICY ITERATION can be called here
        print(policy_iteration.policy_generate(sub_obj.get_dictGrid(), sub_obj.get_width_length(),
                                               sub_obj.get_height_length(), 0.9, 1.0))
