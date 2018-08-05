#!/usr/bin/env python
import rospy
from mavros_msgs.srv import CommandTOL

if __name__ == "__main__":
    rospy.init_node('service_client')
    rospy.wait_for_service('/mavros/cmd/land')
    try:
        handle_respon = rospy.ServiceProxy('/mavros/cmd/land',CommandTOL)
        response = handle_respon(0,0,0,0,0)
        if response.success == True:
            print('land command received!')
    except rospy.ServiceException, e:
        print "service call failed %s" % e