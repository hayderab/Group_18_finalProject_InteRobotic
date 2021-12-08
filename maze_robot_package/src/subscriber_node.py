#!/usr/bin/env python3

import rospy
from nav_msgs.msg import OccupancyGrid, Odometry
import maze_dictionary


class SubscriberNode:

    def __init__(self):
        self._dict_gird = {}
        self._width_length = 0
        self._height_length = 0
        self._current_position_x = 0
        self._current_position_y = 0
        self._dummy_dict = {}  # can be deleted later

    # getter method
    def get_dictGrid(self):
        return self._dict_gird

    def get_width_length(self):
        return self._width_length

    def get_height_length(self):
        return self._height_length

    def get_current_position_x(self):
        return self._current_position_x

    def get_current_position_y(self):
        return self._current_position_y

    # can be deleted later
    def get_dummyDict(self):
        return self._dummy_dict

    # DO NOT FORGET to uncomment its rospy.Subscriber for /odom from the listener() method
    def callback_coordinates(self, data):
        # print("x:")
        # rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.pose.pose.position.x)  # print robot x position

        # print("y:")
        # rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.pose.pose.position.y)  # print robot y position

        self._current_position_x = data.pose.pose.position.x
        self._current_position_y = data.pose.pose.position.y

    def callback_map(self, data):
        # rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)  # print grids occupancy

        # Returns/Saves a dictionary of the coordinates (x, y) and reward of every cell
        self._dict_gird, self._width_length, self._height_length, self._dummy_dict = maze_dictionary.maze_dict_grid(
            data)  # self._dummy_dict can be deleted later

    def listener(self):
        rospy.Subscriber("/map", OccupancyGrid, self.callback_map)  # take data from the OccupancyGrid
        rospy.Subscriber("/odom", Odometry, self.callback_coordinates)  # take data from the Odometry
