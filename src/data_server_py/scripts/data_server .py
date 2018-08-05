#!/usr/bin/env python

from data_server_py.srv import *
import rospy


def handle_server(req):
    print "i've got the request"
    resp = data_server_py_srvResponse()
    resp.acc_x = 0.1
    resp.acc_y = 0.12
    resp.acc_z = 9.8
    resp.gx = 0.01
    resp.gy = 0.1
    resp.gz = 1
    resp.gps_lat = 123.456
    resp.gps_long = 23.456
    resp.gps_PDOP = 12.56
    resp.gps_num_of_satellite = 18
    resp.steps_Left = 123
    resp.steps_Right = 456
    resp.TimeStamp = 113.56868
    resp.msg_ID = 115200
    return resp


def data_server():
    rospy.init_node("server_node")
    server = rospy.Service("data_server", data_server_py_srv, handle_server)
    print "data ready"
    rospy.spin()


if __name__ == "__main__":
    data_server()
