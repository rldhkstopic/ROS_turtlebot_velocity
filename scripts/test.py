#!/usr/bin/env python
#linear drive(translation)

from __future__ import print_function

import rospy
import math
import tf
import sys, select, os, time

from math import cos, sin, degrees, sqrt

from nav_msgs.msg import Odometry
from std_msgs.msg import String
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3
from tf.transformations import euler_from_quaternion

def to_positive_angle(th):
    while True:
        if th < 0:
            th += 360
        if th > 0:
            ans = th % 360
            return ans
            break

def Distance2D(pos_x, pos_y):
    dist = sqrt((pos_x**2)+(pos_y**2))
    return dist

def pub_cmdv(): # Write turtlebot velocity
    pub = rospy.Publisher('/counter', Twist, queue_size=3)

def sub_odom():
    odom = rospy.Subscriber('/odom',Odometry, callback_odom)

def sub_chat():
    chat =  rospy.Subscriber('chatter', String, callback_chat)

def callback_odom(data):
    global odom_x, odom_y, odom_z
    odom_x = data.pose.pose.position.x
    odom_y = data.pose.pose.position.y

    q1 = data.pose.pose.orientation.x
    q2 = data.pose.pose.orientation.y
    q3 = data.pose.pose.orientation.z
    q4 = data.pose.pose.orientation.w
    q = (q1, q2, q3, q4)

    e = euler_from_quaternion(q)

    odom_z = degrees(e[2])
    odom_z = to_positive_angle(odom_z)

def callback_chat(data):
    global opt_x, opt_y, opt_dist, opt_dist2
    opt = data.data.split("|")
    opt_x = opt[1]
    opt_y = opt[2]
    opt_dist = opt[4]

    print("[OPT] X : {:3d} Y : {:3d} D : {:3f}".format(opt_x, opt_y, opt_dist))  


def listner():
    rospy.init_node('turtlebot3_teleop', anonymous=True)


cur_x, cur_y = (0.0, 0.0)
if __name__=="__main__":
    currentTime = rospy.Time.now()
    lastTime = rospy.Time.now()

    sub_odom()
    sub_chat()
    while not rospy.is_shutdown():
        currentTime = rospy.Time.now()
        
        local_x = opt_x + cos(opt_y) * dist
        local_y = opt_x + sin(opt_y) * dist
        local_z = opt_y + dist / 0.093

        gap_x = (odom_x - local_x)/odom_x * 100
        gap_y = (odom_y - local_y)/odom_z * 100
        gap_z = (odom_z - local_z)/odom_z * 100

        print("POSITION GAP|| X : ", gap_x, "Y : ", gap_y, "Z : ", gap_z)

        dist = (currentTime - lastTime).to_sec()
        lastTime = rospy.Time.now()
        rate.sleep()