#!/usr/bin/env python
import roslib
import rospy
roslib.load_manifest('my_tf')
import tf
import turtlesim.msg


def turtle_pose_handle(msg, turtlename):
    br = tf.TransformBroadcaster()
    br.sendTransform((msg.x, msg.y, 0),
                     tf.transformations.quaternion_from_euler(0, 0, msg.theta),
                     rospy.Time.now(),
                     turtlename,
                     "world")


if __name__ == '__main__':
    rospy.init_node('turtle_tf_broadcaster')
    turtlename = rospy.get_param('~turtle')
    rospy.Subscriber('/%s/pose' % turtlename, turtlesim.msg.Pose,
                     turtle_pose_handle, turtlename)
    rospy.spin()
