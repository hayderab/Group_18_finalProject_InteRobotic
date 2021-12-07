#!/usr/bin/env python3

import rospy
import publisher
import subscriber

if __name__ == '__main__':
    try:
        rospy.init_node('maze_robot_node', anonymous=True)  # centralize the initialization of the node
        pub = publisher.Publisher()  # create a Publisher object
        sub = subscriber.Subscriber()  # create a Subscriber object

        sub.listener()  # run what is inside the Subscriber class: 1.get the grid data & 2.generate a grid dictionary
        rospy.sleep(1)  # sleep for 1 second (subscriber behavior - need sometime to retrieve the data)
        pub.talker(sub)  # transfer the current Subscriber object to the Publisher (to use its grid_dictionary there)

        rospy.spin()  # spin() simply keeps python from exiting until this node is stopped

    except rospy.ROSInterruptException:
        pass
