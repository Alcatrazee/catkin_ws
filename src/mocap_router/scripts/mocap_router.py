#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped
from mavros_msgs.srv import CommandTOL

pub = rospy.Publisher('/mavros/mocap/pose',PoseStamped,queue_size=10)
pub_msg = PoseStamped()
last_receive_time=0
current_time=0
time_out = 2
check_time_duration = 1
flying_or_not=0

def Mocap_optitrack_cb(PoseStamped):
    global last_receive_time
    pub_msg.header.frame_id = PoseStamped.header.frame_id 
    pub_msg.header.seq = PoseStamped.header.seq 
    pub_msg.header.stamp = PoseStamped.header.stamp 
    pub_msg.pose.position.x = PoseStamped.pose.position.x
    pub_msg.pose.position.y = PoseStamped.pose.position.y
    pub_msg.pose.position.z = PoseStamped.pose.position.z
    pub_msg.pose.orientation.x = PoseStamped.pose.orientation.x
    pub_msg.pose.orientation.y = PoseStamped.pose.orientation.y
    pub_msg.pose.orientation.z = PoseStamped.pose.orientation.z
    pub_msg.pose.orientation.w = PoseStamped.pose.orientation.w
    last_receive_time = rospy.get_rostime()
    pub.publish(pub_msg)

def Mocap_monitor(event):
    current_time = rospy.get_rostime()
    print(current_time.secs)
    print(last_receive_time.secs)
    if current_time.secs-last_receive_time.secs > time_out:
        print('time out!')
        Land_breaker()

        
                                          
def Land_breaker():
    try:
        handle_respon = rospy.ServiceProxy('/mavros/cmd/land',CommandTOL)
        response = handle_respon(0,0,0,0,0)
        if response.success == True:
            print('land command received!')
    except rospy.ServiceException, e:
        print "service call failed %s" % e


if __name__ == '__main__':
    rospy.init_node('mocap_router',anonymous=True)
    last_receive_time = rospy.get_rostime()
    current_time = rospy.get_rostime()

    rospy.Subscriber('/Robot_1/pose',PoseStamped,Mocap_optitrack_cb)
    rospy.Timer(rospy.Duration(check_time_duration), Mocap_monitor)
    rospy.wait_for_service('/mavros/cmd/land')
    rospy.spin()
