#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from IMU_MESSAGE_NODE.msg import Imu
import serial
import numpy as np

IMU_DATA = Imu()

if __name__ == "__main__":
    rospy.init_node('IMU_DATA_PUBLISHER', anonymous=True)
    pub = rospy.Publisher('data_from_imu', Imu,queue_size=10)
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        IMU_DATA.angular_velocity.x = 123.456
        IMU_DATA.angular_velocity.y = 456.789
        IMU_DATA.angular_velocity.z = 789.123
        IMU_DATA.orientation.x = 3.14
        IMU_DATA.orientation.y = 3.14
        IMU_DATA.orientation.z = 3.14
        IMU_DATA.orientation.w = 1
        IMU_DATA.linear_acceleration.x = 1.8
        IMU_DATA.linear_acceleration.y = 1.232
        IMU_DATA.linear_acceleration.z = 1.56
        pub.publish(IMU_DATA)
        rate.sleep()
