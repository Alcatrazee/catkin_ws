#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from message_publisher_py_version.msg import pubmsg
import serial
import numpy as np

serial_num = '/dev/ttyUSB0'
clear_buff = [0 for x in range(100)]
IMU_DATA = {'ax': 0, 'ay': 0, 'az': 0, 'gx': 0, 'gy': 0, 'gz': 0}
Vel_Wheel = {'L': 0, 'R': 0}
GPS_DATA = {'lat': 0, 'NorS': ' ', 'long': 0, 'EorW': ' ',
            'ground_speed': 0, 'altitute': 0, 'PDOP': 0}
TIME = {'GPS': 0, 'IMU': 0}

msg = pubmsg()


def process(buff):
    joined = ''.join(buff)
    joined = joined.split()
    if joined[0] == 'IMU':
        process_IMU_data(joined)
    elif joined[0] == 'GPS':
        process_GPS_data(joined)
    joined = clear_buff


def process_IMU_data(input_param):
    try:
        buff = np.float32(input_param[1:15])
        msg.acc_x = IMU_DATA['ax'] = buff[0]+buff[1]/100
        msg.acc_y = IMU_DATA['ay'] = buff[2]+buff[3]/100
        msg.acc_z = IMU_DATA['az'] = buff[4]+buff[5]/100
        msg.gx = IMU_DATA['gx'] = buff[6]+buff[7]/100
        msg.gy = IMU_DATA['gy'] = buff[8]+buff[9]/100
        msg.gz = IMU_DATA['gz'] = buff[10]+buff[11]/100

        msg.vel_Left = Vel_Wheel['L'] = buff[12]
        msg.vel_Right = Vel_Wheel['R'] = buff[13]

        TIME['IMU'] = np.float32(input_param[15])/200
        print(TIME['IMU'])
    except ValueError:
        pass


def process_GPS_data(input_param):
    try:
        msg.gps_lat = GPS_DATA['lat'] = np.float32(input_param[1])
        GPS_DATA['NorS'] = input_param[2]
        msg.gps_long = GPS_DATA['long'] = np.float32(input_param[3])
        GPS_DATA['EorW'] = input_param[4]
        GPS_DATA['ground_speed'] = np.float32(input_param[5])
        msg.gps_altitute = GPS_DATA['altitute'] = np.float32(input_param[6])
        msg.gps_PDOP = GPS_DATA['PDOP'] = np.float32(input_param[7])

        msg.GPS_TimeStamp = TIME['GPS'] = np.float32(input_param[8])*5/1000
    except ValueError:
        pass


def talker():
    pub = rospy.Publisher('Data_from_MCU', pubmsg)
    rospy.init_node('Data_Center', anonymous=True)
    rate = rospy.Rate(10)
    counter = 0
    all = 0
    buff = [0 for x in range(100)]
    ser = serial.Serial(serial_num, 115200)

    while not rospy.is_shutdown():
        all = ser.read(1)
        buff[counter] = all
        if buff[0] == 'I' or buff[0] == 'G':
            counter = counter+1
            if buff[counter-1] == '\n' and buff[counter-2] == '\r' and (buff[0] == 'I' or buff[0] == 'G'):
                process(buff[0:counter-1])
                counter = 0
                pub.publish(msg)
        else:
            counter = 0
            buff = clear_buff
    ser.close()


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
