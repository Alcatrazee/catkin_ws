#include "ros/ros.h"
#include "data_server/msg_service.h"

bool respond(data_server::msg_service::Request &req,data_server::msg_service::Response &res)
{
  static float count=0;
  res.gps_long = 113.12345+count;
  res.gps_lat = 23.12345+count;
  res.IMU_Pitch = 0.15;
  res.IMU_Roll = 0.05;
  res.IMU_Yaw = 235.5;
  res.VEL_Left = 100;
  res.VEL_Right = 100;
  res.TimeStamp = 123.000500;
  count+=0.1;
  ROS_INFO("request received",req.request_flag);
  return true;
}


int main(int argc,char **argv)
{
  ros::init(argc,argv,"Data_Server");				        //node name
  ros::NodeHandle n;							//make a handle
  
  ros::ServiceServer service = n.advertiseService("Data_Server",respond);	//server name
  ROS_INFO("data ready");
  ros::spin();
  
  return 0;
}
