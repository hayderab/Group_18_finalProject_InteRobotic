#!/usr/bin/env python

# MAY I USE THIS FILE FOR THE ROTATION (NOT TESTED YET), REF: https://www.theconstructsim.com/ros-qa-135-how-to-rotate-a-robot-to-a-desired-heading-using-feedback-from-odometry/
import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from geometry_msgs.msg import Twist
import math

roll = pitch = yaw = 0.0
target = 90
kp = 0.5


def get_rotation(msg):
    global roll, pitch, yaw
    orientation_q = msg.pose.pose.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll, pitch, yaw) = euler_from_quaternion(orientation_list)
    print(yaw)


rospy.init_node('rotate_robot')

sub = rospy.Subscriber('/odom', Odometry, get_rotation)
pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
r = rospy.Rate(10)
command = Twist()

while not rospy.is_shutdown():
    # quat = quaternion_from_euler (roll, pitch,yaw)
    # print quat
    target_rad = target * math.pi / 180
    command.angular.z = kp * (target_rad - yaw)
    pub.publish(command)
    print("target={} current:{}", target, yaw)
    r.sleep()
