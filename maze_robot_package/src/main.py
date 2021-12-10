#!/usr/bin/env python3

import rospy
import publisher_node
import subscriber_node

if __name__ == '__main__':
    try:
        # centralize the initialization of the node to run Publisher and Subscriber nodes at once
        rospy.init_node('maze_robot_node', anonymous=True)
        pub = publisher_node.PublisherNode()  # create a PublisherNode object
        sub = subscriber_node.SubscriberNode()  # create a SubscriberNode object

        sub.listener()  # run what is inside the SubscriberNode class: 1.get the grid data & 2.generate a grid dictionary
        rospy.sleep(1)  # sleep for 1 second (subscriber behavior - need sometime to retrieve the data)

        # transfer the current Subscriber object to the Publisher
        pub.talker(sub)  # transfer the dictionary and apply policy iteration

        rospy.spin()  # spin() simply keeps python from exiting until this node is stopped

    except rospy.ROSInterruptException:
        pass
