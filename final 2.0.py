#!/usr/bin/env python
import rclpy
#from rclpy.qos import qos_profile_default

from geometry_msgs.msg import Twist

import sys, select, termios, tty

import time

Pi = 3.14159
Nu_max = 1.5    # Максимальное количество оборотов/сек 
L = 0.15        # Расстояние между колёсами в метрах   # Кастомное явление, необходимо измерить и вставить полученное значение
r = 0.08        # Радиус колеса в метрах               # Кастомное явление, необходимо измерить и вставить полученное значение

settings = termios.tcgetattr(sys.stdin)

def set_motors_m(pub, left_speed, right_speed): 
    speed = Twist()
    speed.linear.x = (left_speed + right_speed) * 0.35 
    speed.linear.y = 0.0; speed.linear.z = 0.0
    speed.angular.x = 0.0; speed.angular.y = 0.0 
    speed.angular.z =  2 * Pi * Nu_max * r * (right_speed - left_speed) * 0.7 / L   
    pub.publish(speed)
 

def main(args=None):	
    if args is None: 
        args = sys.argv
    rclpy.init()
    node = rclpy.create_node('Wanted_speed')	
    pub = node.create_publisher(Twist, 'cmd_vel', 10)
    
    print("Please, select type of input: \n1. Speed in standardized units \n2.Speed in percentages \n3.Speed in metrics units\n")
    selection = input("Enter number of your selection = ")

        
    if selection == '1':     
        while 1:
            x = float(input( "left_speed = " ))
            y = float(input( "right_speed = " ))
            t = float(input( "time = " ))
            if x == 0 and y == 0 and t == 0:
                break
            set_motors_m(pub, x, y)
            time.sleep(t)
            set_motors_m(pub, 0, 0)
            print('Goal comleted\n')
            print('\n--- \n\n')

    else:
        print("This function is comming soon...")

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

