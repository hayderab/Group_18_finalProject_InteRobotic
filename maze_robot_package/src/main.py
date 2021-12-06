#!/usr/bin/env python3

import rospy
import publisher_node
import subscriber_node

if __name__ == '__main__':
    try:
        rospy.init_node('Pub_and_Sub', anonymous=True)  # run publisher and subscriber together as single node
        subscriber_node.listener()
        rospy.sleep(1)  # sleep for 1 second (subscriber behavior - need sometime to retrieve the data)
        publisher_node.talker()
        rospy.spin()  # spin() simply keeps python from exiting until this node is stopped

    except rospy.ROSInterruptException:
        pass
