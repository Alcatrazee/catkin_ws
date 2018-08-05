#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from omni_robot_tf_rviz.msg import omni_robot_tf_msg
from geometry_msgs.msg import Pose2D
from geometry_msgs.msg import Twist
import tf
import serial
import numpy as np

serial_num = '/dev/ttyUSB0'
clear_buff = [0 for x in range(100)]
ROBOT_STATE = {'pos_x': 0, 'pos_y': 0, 'theta': 0,
               'v_x': 0, 'v_y': 0, 'omega': 0, 'timestamp': 0}

msg = omni_robot_tf_msg()
Pose = Pose2D()
Twist_msg = Twist()
br = tf.TransformBroadcaster()


def process(buff):
    joined = ''.join(buff)
    joined = joined.split()
    if joined[0] == 'IMU':
        process_IMU_data(joined)
    joined = clear_buff


def process_IMU_data(input_param):
    try:
        buff = np.float32(input_param[1:12])
        Pose.x = msg.posx = ROBOT_STATE['pos_x'] = buff[0]
        Pose.y = msg.posy = ROBOT_STATE['pos_y'] = buff[1]
        Pose.theta = msg.theta = ROBOT_STATE['theta'] = buff[2]+buff[3]/100
        Twist_msg.linear.x = msg.vx = ROBOT_STATE['v_x'] = buff[4]+buff[5]/100
        Twist_msg.linear.y = msg.vy = ROBOT_STATE['v_y'] = buff[6]+buff[7]/100
        Twist_msg.angular.z = msg.omega = ROBOT_STATE['omega'] = buff[8]+buff[9]/100
        msg.timestamp = ROBOT_STATE['timestamp'] = buff[10]/100
    except ValueError:
        pass


def subcrib_callback(msg, ser):
    message = 'G'
    message = message + str(np.int(msg.x)) + ' ' + str(np.int(msg.y)) + '\r\n'
    ser.write(message.encode())


def talker():
    pub = rospy.Publisher('ALL_DATA', omni_robot_tf_msg, queue_size=10)
    pos_msg = rospy.Publisher('Position', Pose2D, queue_size=10)
    twist_msg = rospy.Publisher('Twist', Twist, queue_size=10)
    rospy.init_node('Data_Center', anonymous=True)
    counter = 0
    all = 0
    buff = [0 for x in range(100)]
    ser = serial.Serial(serial_num, 115200)
    subcr = rospy.Subscriber('robot/cml/pos', Pose2D, subcrib_callback, ser)
    while not rospy.is_shutdown():
        all = ser.read(1)
        buff[counter] = all
        if buff[0] == 'I' or buff[0] == 'G':
            counter = counter+1
            if buff[counter-1] == '\n' and buff[counter-2] == '\r' and buff[0] == 'I':
                process(buff[0:counter-2])
                counter = 0
                pub.publish(msg)
                twist_msg.publish(Twist_msg)
                pos_msg.publish(Pose)
                br.sendTransform((Pose.x, Pose.y, 0),
                                 tf.transformations.quaternion_from_euler(
                                     0, 0, Pose.theta/180*3.14),
                                 rospy.Time.now(),
                                 "world",
                                 "robot")

        else:
            counter = 0
            buff = clear_buff
    ser.close()


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
