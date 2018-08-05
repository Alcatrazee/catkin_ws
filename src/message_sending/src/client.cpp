#include "ros/ros.h"
#include "message_sending/msgsend.h"
#include <cstdlib>

int main(int argc,char **argv)
{
  ros::init(argc,argv,"Client");						      //node name
  ros::NodeHandle n;
  
  ros::ServiceClient client = n.serviceClient<message_sending::msgsend>("add_3_int"); //client of server:add_3_int
  message_sending::msgsend srv;							      //make a service,which contains elements of file msgsend.srv
  srv.request.A = atoll(argv[1]);
  srv.request.B = atoll(argv[2]);
  srv.request.C = atoll(argv[3]);

  if (client.call(srv))
  {
    ROS_INFO("sum = %d",srv.response.sum);
  }
  else
  {
    ROS_ERROR("failed.");
    return 1;
  }
  return 0;
}
