#include "ros/ros.h"
#include "std_msgs/String.h"

int main(int argc,char **argv)
{
  ros::init(argc,argv,"publisher");
  ros::NodeHandle n;
  ros::Publisher chatter_pub = n.advertise<std_msgs::String>("message",1000);
  ros::Rate loop_rate(10);

  while(ros::ok())
  {
    std_msgs::String msg;
    std::stringstream ss;
    ss << " message ";
    msg.data = ss.str();
    chatter_pub.publish(msg);
    ros::spinOnce();
    loop_rate.sleep();
  }
  return 0;
}
