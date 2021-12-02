#!/usr/bin/env python
import rospy

from nav_msgs.msg import OccupancyGrid, Odometry

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)  # print grids occupancy
    # rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.pose.pose.position.x)  # print robot x position


def listener():
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("/map", OccupancyGrid, callback)  # take data from the OccupancyGrid
    # rospy.Subscriber("/odom", Odometry, callback)  # take data from the Odometry

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    listener()