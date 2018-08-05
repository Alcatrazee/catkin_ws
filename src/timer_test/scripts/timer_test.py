#!/usr/bin/env python
import rospy


def timer1_callback(event):
    print('timer1 called at ' + str(event.current_real))


if __name__ == '__main__':
    rospy.init_node('timer_test')
    rospy.Timer(rospy.Duration(1), timer1_callback)
    rospy.spin()
