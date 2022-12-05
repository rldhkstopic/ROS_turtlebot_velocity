1 #include <ros/ros.h>
2 #include <tf/transform_broadcaster.h>
3 #include <nav_msgs/Odometry.h>
4
5 int main(int argc, char** argv){
6   ros::init(argc, argv, "odometry_publisher");
7
8   ros::NodeHandle n;
9   ros::Publisher odom_pub = n.advertise<nav_msgs::Odometry>("odom", 50);
10   tf::TransformBroadcaster odom_broadcaster;
11
12   double x = 0.0;
13   double y = 0.0;
14   double th = 0.0;
15
16   double vx = 0.1;
17   double vy = -0.1;
18   double vth = 0.1;
19
20   ros::Time current_time, last_time;
21   current_time = ros::Time::now();
22   last_time = ros::Time::now();
23
24   ros::Rate r(1.0);
25   while(n.ok()){
26     current_time = ros::Time::now();
27
28     //compute odometry in a typical way given the velocities of the robot
29     double dt = (current_time - last_time).toSec();
30     double delta_x = (vx * cos(th) - vy * sin(th)) * dt;
31     double delta_y = (vx * sin(th) + vy * cos(th)) * dt;
32     double delta_th = vth * dt;
33
34     x += delta_x;
35     y += delta_y;
36     th += delta_th;
37
38     //since all odometry is 6DOF we'll need a quaternion created from yaw
39     geometry_msgs::Quaternion odom_quat = tf::createQuaternionMsgFromYaw(th);
40
41     //first, we'll publish the transform over tf
42     geometry_msgs::TransformStamped odom_trans;
43     odom_trans.header.stamp = current_time;
44     odom_trans.header.frame_id = "odom";
45     odom_trans.child_frame_id = "base_link";
46
47     odom_trans.transform.translation.x = x;
48     odom_trans.transform.translation.y = y;
49     odom_trans.transform.translation.z = 0.0;
50     odom_trans.transform.rotation = odom_quat;
51
52     //send the transform
53     odom_broadcaster.sendTransform(odom_trans);
54
55     //next, we'll publish the odometry message over ROS
56     nav_msgs::Odometry odom;
57     odom.header.stamp = current_time;
58     odom.header.frame_id = "odom";
59
60     //set the position
61     odom.pose.pose.position.x = x;
62     odom.pose.pose.position.y = y;
63     odom.pose.pose.position.z = 0.0;
64     odom.pose.pose.orientation = odom_quat;
65
66     //set the velocity
67     odom.child_frame_id = "base_link";
68     odom.twist.twist.linear.x = vx;
69     odom.twist.twist.linear.y = vy;
70     odom.twist.twist.angular.z = vth;
71
72     //publish the message
73     odom_pub.publish(odom);
74
75     last_time = current_time;
76     r.sleep();
77   }
78 }
79
