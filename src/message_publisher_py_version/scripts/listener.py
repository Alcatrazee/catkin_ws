#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from message_publisher_py_version.msg import pubmsg

IMU_DATA = {'ax': 0, 'ay': 0, 'az': 0, 'gx': 0, 'gy': 0, 'gz': 0}
Vel_Wheel = {'L': 0, 'R': 0}
GPS_DATA = {'lat': 0, 'NorS': ' ', 'long': 0, 'EorW': ' ',
            'ground_speed': 0, 'altitute': 0, 'PDOP': 0}
TIME = {'GPS': 0, 'IMU': 0}


def callback(pubmsg):
    IMU_DATA['ax'] = pubmsg.acc_x
    IMU_DATA['ay'] = pubmsg.acc_y
    IMU_DATA['az'] = pubmsg.acc_z
    IMU_DATA['gx'] = pubmsg.gx
    IMU_DATA['gy'] = pubmsg.gy
    IMU_DATA['gz'] = pubmsg.gz

    Vel_Wheel['L'] = pubmsg.vel_Left
    Vel_Wheel['R'] = pubmsg.vel_Right

    TIME['IMU'] = pubmsg.IMU_TimeStamp

    rospy.loginfo("%f %f %f %f %f %f", pubmsg.acc_x, pubmsg.acc_y,
                  pubmsg.acc_z, pubmsg.gx, pubmsg.gy, pubmsg.gz)


def listener():
    rospy.init_node('Data_Receiver', anonymous=True)
    rospy.Subscriber("Data_from_MCU", pubmsg, callback)
    rospy.spin()


if __name__ == '__main__':
    listener()
