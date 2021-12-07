#!/usr/bin/env python3

import rospy
from nav_msgs.msg import OccupancyGrid, Odometry
import helper


class Subscriber:

    def __init__(self):
        self._dict_gird = {}

    # getter method
    def get_dictGrid(self):
        return self._dict_gird

    # DO NOT FORGET to uncomment its Subscriber from the listener() method
    @staticmethod
    def callback_coordinates(data):
        print("x:")
        rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.pose.pose.position.x)  # print robot x position

        print("y:")
        rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.pose.pose.position.y)  # print robot y position

    def callback_map(self, data):
        # rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)  # print grids occupancy

        # Returns/Saves a dictionary of the coordinates (x, y) and reward of every cell
        self._dict_gird = helper.cell_coordinates_reward(data)

    def listener(self):
        rospy.Subscriber("/map", OccupancyGrid, self.callback_map)  # take data from the OccupancyGrid
        # rospy.Subscriber("/odom", Odometry, callback_coordinates)  # take data from the Odometry
