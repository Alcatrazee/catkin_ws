# encoding=utf8
#!/usr/bin/env python
from data_server_py.srv import *
import rospy
import serial
import numpy as np

serial_num = '/dev/ttyUSB0'
clear_buff = [0 for x in range(100)]
IMU_DATA = {'ax': 0, 'ay': 0, 'az': 0, 'gx': 0, 'gy': 0, 'gz': 0}
Vel_Wheel = {'L': 0, 'R': 0}
GPS_DATA = {'lat': 0, 'NorS': ' ', 'long': 0, 'EorW': ' ',
            'ground_speed': 0, 'altitute': 0, 'PDOP': 0}
TIME = {'GPS': 0, 'IMU': 0}


def process(buff):
    joined = ''.join(buff)
    joined = joined.split()
    if joined[0] == 'IMU':
        process_IMU_data(joined)
    elif joined[0] == 'GPS':
        process_GPS_data(joined)
    joined = clear_buff


def process_IMU_data(input_param):

    buff = np.float32(input_param[1:15])
    IMU_DATA['ax'] = buff[0]+buff[1]/100
    IMU_DATA['ay'] = buff[2]+buff[3]/100
    IMU_DATA['az'] = buff[4]+buff[5]/100
    IMU_DATA['gx'] = buff[6]+buff[7]/100
    IMU_DATA['gy'] = buff[8]+buff[9]/100
    IMU_DATA['gz'] = buff[10]+buff[11]/100

    Vel_Wheel['L'] = buff[12]
    Vel_Wheel['R'] = buff[13]

    TIME['IMU'] = np.float32(input_param[15])/200
    print(IMU_DATA)


def process_GPS_data(input_param):

    GPS_DATA['lat'] = np.float32(input_param[1])
    GPS_DATA['NorS'] = input_param[2]
    GPS_DATA['long'] = np.float32(input_param[3])
    GPS_DATA['EorW'] = input_param[4]
    GPS_DATA['ground_speed'] = np.float32(input_param[5])
    GPS_DATA['altitute'] = np.float32(input_param[6])
    GPS_DATA['PDOP'] = np.float32(input_param[7])

    TIME['GPS'] = np.float32(input_param[8])*5/1000


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
    counter = 0
    all = 0

    buff = [0 for x in range(100)]
    ser = serial.Serial(serial_num, 115200)
    while rospy.is_shutdown():
        all = ser.read(1)
        buff[counter] = all
        if buff[0] == 'I' or buff[0] == 'G':
            counter = counter+1
            if buff[counter-1] == '\n' and buff[counter-2] == '\r' and (buff[0] == 'I' or buff[0] == 'G'):
                process(buff[0:counter-1])
                counter = 0
        else:
            counter = 0
            buff = clear_buff
    ser.close()
