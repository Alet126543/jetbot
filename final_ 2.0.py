#!/usr/bin/env python
import rclpy

from geometry_msgs.msg import Twist

import sys, select, termios, tty

import time

Pi = 3.14159
Nu_max = 1.5     # Максимальное количество оборотов/сек
L = 0.117        # Расстояние между колёсами в метрах
r = 0.065        # Радиус колеса в метрах

settings = termios.tcgetattr(sys.stdin)

def set_motors_m(pub, pub_n, left_speed, right_speed): 
    speed = Twist()
    speed.linear.x = (left_speed + right_speed) * 0.35 
    speed.linear.y = 0.0; speed.linear.z = 0.0
    speed.angular.x = 0.0; speed.angular.y = 0.0 
    speed.angular.z =  2 * Pi * Nu_max * r * (right_speed - left_speed) * 0.7 / L   
    
    speed_n = Twist()
    speed_n.linear.x = left_speed * 0.7
    speed_n.linear.y = right_speed * 0.7
    speed_n.linear.z = 0.0
    speed_n.angular.x = 0.0
    speed_n.angular.y = 0.0 
    speed_n.angular.z = 0.0

    pub.publish(speed)
    pub_n.publish(speed_n)


def main(args=None):	
    if args is None: 
        args = sys.argv
    rclpy.init()
    node = rclpy.create_node('Publisher-speed')	
    pub = node.create_publisher(Twist, 'cmd_vel', 10)
    pub_n = node.create_publisher(Twist, 'normal', 10)
    while 1:
        x = float(input( "left_speed = " ))
        y = float(input( "right_speed = " ))
        t = float(input( "time = " ))
        if x == 0 and y == 0 and t == 0:
            break
        set_motors_m(pub, pub_n, x, y)
        time.sleep(t)
        set_motors_m(pub, pub_n, 0, 0)
        print('Goal comleted\n')
        print('\n--- \n\n')

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

