#!/usr/bin/env python3

import rospy
import publisher_node
import subscriber_node

if __name__ == '__main__':
    try:
        # Centralize the initialization of the node to run Publisher and Subscriber nodes at once
        rospy.init_node('maze_robot_node', anonymous=True, disable_signals=True)
        pub = publisher_node.PublisherNode()  # create a PublisherNode object
        sub = subscriber_node.SubscriberNode()  # create a SubscriberNode object

        sub.listener()  # run what is inside the SubscriberNode class: 1.get the grid data & 2.generate a grid dictionary
        rospy.sleep(1)  # sleep for 1 second (subscriber behavior - need some time to retrieve the data)

        # Publish move commands to the robot based on the policy iteration (require data from the Subscriber)
        # Use the current SubscriberNode object as a parameter (now Publisher can communicate with the Subscriber)
        pub.talker(sub)

        rospy.spin()  # spin() simply keeps python from exiting until this node is stopped

    except rospy.ROSInterruptException:
        pass
