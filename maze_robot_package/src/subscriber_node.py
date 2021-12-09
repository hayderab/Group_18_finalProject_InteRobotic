#!/usr/bin/env python3

import rospy
# importing the module for knowing the Odometry of the robot.
from nav_msgs.msg import OccupancyGrid, Odometry
# importing the transform converter between Euler and Quaternion
from tf.transformations import euler_from_quaternion
import maze_dictionary


class SubscriberNode:

    def __init__(self):
        self._dict_gird = {}
        self._width_length = 0
        self._height_length = 0
        self._current_position_x = 0
        self._current_position_y = 0
        self._dummy_dict = {}  # can be deleted later

        # yaw = current heading of the robot (to the left or to the right - in radians in respect to the maze coordinates)
        # pointing forward - yaw = 0
        # pointing left - yaw > 0
        # pointing right - yaw < 0
        self._roll = self._pitch = self._yaw = 0.0  # Euler angles - # Measurement of the roll/pitch/yaw/ component of the rotation of the robot

    # Getter methods
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

    def get_yaw(self):
        return self._yaw

    # can be deleted later
    def get_dummyDict(self):
        return self._dummy_dict

    def callback_rotation(self, data):
        orientation_q = data.pose.pose.orientation
        # Creating a list with the 4 values that compose the orientation quaternion of the position message
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        # Assigning their values to roll, pitch and yaw variables through the euler_from_quaternion conversion
        (self._roll, self._pitch, self._yaw) = euler_from_quaternion(orientation_list)

    # DO NOT FORGET to uncomment its rospy.Subscriber for /odom from the listener() method
    def callback_position(self, data):
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
        rospy.Subscriber("/map", OccupancyGrid, self.callback_map)  # take maps data from the OccupancyGrid
        rospy.Subscriber("/odom", Odometry, self.callback_position)  # take robots' position data from the Odometry
        rospy.Subscriber('/odom', Odometry, self.callback_rotation)  # take robot's orientation data from the Odometry
