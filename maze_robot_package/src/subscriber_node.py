#!/usr/bin/env python3

import rospy
from nav_msgs.msg import OccupancyGrid, Odometry  # importing the module for knowing the Odometry of the robot
from tf.transformations import euler_from_quaternion  # importing the transform converter between Euler and Quaternion
import maze_dictionary


class SubscriberNode:

    def __init__(self):
        self._maze_dict = {}
        self._width_length = 0
        self._height_length = 0
        self._current_position_x = 0
        self._current_position_y = 0

        # yaw = current heading of the robot (to the left or to the right - in radians in respect to the maze coordinates)
        # pointing EAST (x-axis directly) - yaw = 0
        # pointing NORTH - yaw > 0
        # pointing SOUTH and then WEST - yaw < 0
        self._roll = self._pitch = self._yaw = 0.0  # Euler angles - # Measurement of the roll/pitch/yaw/ component of the rotation of the robot

    # Getter methods
    def get_maze_dict(self):
        return self._maze_dict

    def get_width_length(self):
        return self._width_length

    def get_height_length(self):
        return self._height_length

    def get_current_position_x(self):
        return self._current_position_x

    def get_current_position_y(self):
        return self._current_position_y

    # We need the yaw angle only
    def get_yaw(self):
        return self._yaw

    # Calls robot's current orientation data
    def callback_orientation(self, data):
        # Reference: https://www.theconstructsim.com/ros-qa-135-how-to-rotate-a-robot-to-a-desired-heading-using-feedback-from-odometry/
        orientation_q = data.pose.pose.orientation
        # Creating a list with the 4 values that compose the orientation quaternion of the position message
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        # Assigning their values to roll, pitch and yaw variables through the euler_from_quaternion conversion
        (self._roll, self._pitch, self._yaw) = euler_from_quaternion(orientation_list)

    # Calls robot's current position data
    def callback_position(self, data):
        # print("x:")
        # rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.pose.pose.position.x)  # print robot x position

        # print("y:")
        # rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.pose.pose.position.y)  # print robot y position

        self._current_position_x = data.pose.pose.position.x
        self._current_position_y = data.pose.pose.position.y

    # Calls the maze's occupancy grid data and processes them in a dictionary
    # Returns the maze dictionary, height and with length of that map
    def callback_map(self, data):
        # rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)  # print grids occupancy

        # These data will be needed for the policy implementation
        self._maze_dict, self._width_length, self._height_length, = maze_dictionary.maze_dict_grid(data)

    # Every call executed from here
    def listener(self):
        rospy.Subscriber("/map", OccupancyGrid, self.callback_map)  # Subscribe to the OccupancyGrid's topic
        rospy.Subscriber("/odom", Odometry, self.callback_position)  # Subscribe Odometry's topic for position data
        rospy.Subscriber('/odom', Odometry, self.callback_orientation)  # Subscribe Odometry's topic for orientation
