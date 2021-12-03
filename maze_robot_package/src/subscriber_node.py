#!/usr/bin/env python3
import rospy

from nav_msgs.msg import OccupancyGrid, Odometry


def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)  # print grids occupancy

    # convertToGridCoordinates(data)
    # printCurrentRobotCoordinates(data)  # do not forget to uncomment the subscriber on listener()


def listener():
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("/map", OccupancyGrid, callback)  # take data from the OccupancyGrid
    # rospy.Subscriber("/odom", Odometry, callback)  # take data from the Odometry

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


def convertToGridCoordinates(data):
    width = 0
    while width < data.info.width:
        height = 0
        while height < data.info.height:
            if data.data[height * data.info.width + width] > 0:
                x = width * data.info.resolution + data.info.resolution / 2
                y = height * data.info.resolution + data.info.resolution / 2
                print("(" + "x[" + str(width) + "]" + ", " + "y[" + str(height) + "]" + "): " + str(x) + ", " + str(y))
            height += 1
        width += 1


def printCurrentRobotCoordinates(data):
    print("x:")
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.pose.pose.position.x)  # print robot x position

    print("y:")
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.pose.pose.position.y)  # print robot y position


if __name__ == '__main__':
    listener()
