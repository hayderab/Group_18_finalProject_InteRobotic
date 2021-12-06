#!/usr/bin/env python3

import global_file
import rospy
from geometry_msgs.msg import Twist


def mover():
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=100)
    # rospy.init_node('Mover', anonymous=True)
    # rate = rospy.Rate(10) # 10hz

    while not rospy.is_shutdown():
        base_data = Twist()
        base_data.linear.x = 1  # For now just run the robot to the right

        pub.publish(base_data)
    # rate.sleep()


def talker():
    # rospy.init_node('Mover', anonymous=True)

    # POLICY ITERATION can be written here
    print(global_file.dict_glob_grid)
