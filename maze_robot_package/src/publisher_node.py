#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import policy_iteration


class PublisherNode:
    @staticmethod
    def mover():
        pub = rospy.Publisher('cmd_vel', Twist, queue_size=100)
        # rate = rospy.Rate(10) # 10hz

        while not rospy.is_shutdown():
            base_data = Twist()
            base_data.linear.x = 1  # For now just run the robot to the right

            pub.publish(base_data)
        # rate.sleep()

    @staticmethod
    def talker(sub_obj):

        # POLICY ITERATION can be written here
        print(policy_iteration.policy_generate(sub_obj.get_dictGrid(), sub_obj.get_width_length(), sub_obj.get_height_length(), 0.9, 1.0))
