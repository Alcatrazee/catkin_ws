#include "ros/ros.h"
#include "message_sending/msgsend.h"

bool add(message_sending::msgsend::Request &req,message_sending::msgsend::Response &res)
{
  res.sum = req.A + req.B + req.C;
  ROS_INFO("A = %d B = %d C = %d sum = %d",req.A,req.B,req.C,res.sum);
  return true;
}


int main(int argc,char **argv)
{
  ros::init(argc,argv,"add_3_int_node");				//node name
  ros::NodeHandle n;							//make a handle
  
  ros::ServiceServer service = n.advertiseService("add_3_int",add);	//server name
  ROS_INFO("READY to add 3 ints.");
  ros::spin();
  
  return 0;
}
