#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import tty
import termios
import time
'''import rospy
from geometry_msgs.msg import Pose2D
from geometry_msgs.msg import Twist
'''


def make_message(command):
    message = 'V'
    if(command[0] == 1 and command[1] == 0):
        message = message+'00100'
    elif(command[0] == 0 and command[1] == 1):
        message = message+'-0100'
    else:
        message = message+'00000'

    if(command[2] == 1 and command[3] == 0):
        message = message+'00100'
    elif(command[2] == 0 and command[3] == 1):
        message = message+'-0100'
    else:
        message = message+'00000'
    return message


if __name__ == '__main__':
    '''
    rospy.init_node('key_capture', anonymous=True)
    pub = rospy.Publisher('cme/vel', Twist)
    rate = rospy.Rate(50)
    '''
    print "Reading form keybord"
    while True:  # not rospy.is_shutdown():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        command = [0, 0, 0, 0, 0, 0]
        # old_settings[3]= old_settings[3] & ~termios.ICANON & ~termios.ECHO
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        if(ch == 'w'):
            command[0] = 1
            command[1] = 0
        elif (ch == 's'):
            command[1] = 1
            command[0] = 0
        if(ch == 'a'):
            command[2] = 1
            command[3] = 0
        elif(ch == 'd'):
            command[2] = 0
            command[3] = 1

        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        if(ch == 'w'):
            command[0] = 1
            command[1] = 0
        elif (ch == 's'):
            command[1] = 1
            command[0] = 0
        if(ch == 'a'):
            command[2] = 1
            command[3] = 0
        elif(ch == 'd'):
            command[2] = 0
            command[3] = 1

        message = make_message(command)
        print(message)
        if(ch == 'q'):
            exit()
#        rate.sleep()
