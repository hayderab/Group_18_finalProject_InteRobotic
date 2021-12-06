#!/usr/bin/env python3

import rospy
from nav_msgs.msg import OccupancyGrid, Odometry
import global_file
import helper


# DO NOT FORGET to uncomment its Subscriber from the listener() method
def callback_coordinates(data):
    print("x:")
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.pose.pose.position.x)  # print robot x position

    print("y:")
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.pose.pose.position.y)  # print robot y position


def callback_map(data):
    # rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)  # print grids occupancy
    # Returns/Saves a dictionary of the coordinates (x, y) and reward of every cell
    global_file.dict_glob_grid = helper.cell_coordinates_reward(data)


def listener():
    # rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/map", OccupancyGrid, callback_map)  # take data from the OccupancyGrid
    # rospy.Subscriber("/odom", Odometry, callback_coordinates)  # take data from the Odometry

    # spin() simply keeps python from exiting until this node is stopped
    # rospy.spin()
