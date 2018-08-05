#include "data_server/msg_service.h"
#include "ros/ros.h"
#include <cstdlib>

int main(int argc, char **argv) {
  ros::init(argc, argv, "Client");
  ros::NodeHandle n;
  ros::Rate loop_rate(1);

  ros::ServiceClient client =
      n.serviceClient<data_server::msg_service>("Data_Server");
  data_server::msg_service srv;
  srv.request.request_flag = 1;

  while (ros::ok()) {
    if (client.call(srv)) // call the data server
    {
      ROS_INFO("gps.long = %f", srv.response.gps_long);
      ROS_INFO("gps.lat = %f", srv.response.gps_lat);
      ROS_INFO("IMU.Pitch = %f", srv.response.IMU_Pitch);
      ROS_INFO("IMU.Roll = %f", srv.response.IMU_Roll);
      ROS_INFO("IMU.Yaw = %f", srv.response.IMU_Yaw);
      ROS_INFO("VEL_Left = %f", srv.response.VEL_Left);
      ROS_INFO("VEL_Right = %f", srv.response.VEL_Right);
      ROS_INFO("TimeStamp = %f", srv.response.TimeStamp);
    } else {
      ROS_ERROR("failed.");
      return 1;
    }
    loop_rate.sleep();
  }
  return 0;
}
