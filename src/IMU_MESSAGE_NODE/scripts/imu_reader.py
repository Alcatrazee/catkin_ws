#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from IMU_MESSAGE_NODE.msg import Imu

IMU_DATA = {'ax': 0, 'ay': 0, 'az': 0, 'gx': 0, 'gy': 0, 'gz': 0}


def callback(Imu):
    IMU_DATA['ax'] = Imu.linear_acceleration.x
    IMU_DATA['ay'] = Imu.linear_acceleration.y
    IMU_DATA['az'] = Imu.linear_acceleration.z
    IMU_DATA['gx'] = Imu.angular_velocity.x
    IMU_DATA['gy'] = Imu.angular_velocity.y
    IMU_DATA['gz'] = Imu.angular_velocity.z
    rospy.loginfo("%f\t%f\t%f", IMU_DATA['ax'], IMU_DATA['ay'], IMU_DATA['az'])


def listener():
    rospy.init_node('IMU_DATA_LISTENER', anonymous=True)
    rospy.Subscriber("data_from_imu", Imu, callback)
    rospy.spin()


if __name__ == "__main__":
    listener()
