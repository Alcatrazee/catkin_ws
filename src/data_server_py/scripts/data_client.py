#!/usr/bin/env python

import sys
import rospy
from data_server_py.srv import *


def data_server_client():
    rospy.wait_for_service('data_server')
    try:
        handle_respon = rospy.ServiceProxy('data_server', data_server_py_srv)
        response = handle_respon(1)
        return response
    except rospy.ServiceException, e:
        print "service call failed %s" % e


if __name__ == "__main__":
    rospy.init_node("data_server_client")
    rate = rospy.Rate(4)
    while not rospy.is_shutdown():
        re = data_server_client()
        print "%f " % (re.acc_x)
        print "%f " % (re.acc_y)
        print "%f " % (re.acc_z)
        print "%f " % (re.gx)
        print "%f " % (re.gx)
        print "%f " % (re.gx)
        print "%f " % (re.gps_long)
        print "%f " % (re.gps_lat)
        print "%f " % (re.gps_PDOP)
        print "%d " % (re.gps_num_of_satellite)
        print "%f " % (re.steps_Left)
        print "%f " % (re.steps_Right)
        print "%f " % (re.TimeStamp)
        print "%d " % (re.msg_ID)
        rate.sleep()
