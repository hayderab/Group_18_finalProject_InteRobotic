#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist


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
    def talker(subscriber_object):

        # POLICY ITERATION can be written here
        print(subscriber_object.get_dictGrid())
