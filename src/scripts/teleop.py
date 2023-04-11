"""
teleop.py - Teleoperation control for ROS robots using Differential Drive Control

Date Modified: 2023-04-07
Author: Creed Zagrzebski <zagrzebski1516@uwlax.edu>
"""

import pygame as pg
import sys
from robot import RobotModel
from settings import *
from pygame.locals import * 
from geometry_msgs.msg import Twist
import rospy
import threading

class Teleop():
    def __init__(self):
        pg.init()
        pg.display.set_caption("Teleop Control")
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pg.time.Clock()
        self.running = True
        self.all_sprites = pg.sprite.Group()
        self.robot_model = RobotModel((SCREEN_WIDTH/2), (SCREEN_HEIGHT/2), self.all_sprites)
        
        # initialize ROS
        rospy.init_node('teleop')
        self.pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        self.tw = Twist()
        self.tw.linear.x = 0
        self.tw.linear.y = 0  
        self.ros_clock = rospy.Rate(ROS_RATE)
        
    
    def run(self):
        #self.thread = threading.Thread(target=self.ros_loop)
        #self.thread.start()
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            
    def events(self):
        for event in pg.event.get():
            if event.type == QUIT:
                self.running = False
                self.thread.join()
                sys.exit()
            
            if event.type == KEYDOWN:
                if event.key == K_a:
                    self.tw.angular.z = ANGULAR_SPEED
                if event.key == K_d:
                    self.tw.angular.z = -ANGULAR_SPEED
                if event.key == K_w:
                    self.tw.linear.x = FORWARD_SPEED
                if event.key == K_s:
                    self.tw.linear.x = -FORWARD_SPEED
                    
            if event.type == KEYUP:
                if event.key == K_a or event.key == K_d:
                    self.tw.angular.z = 0
                if event.key == K_w or event.key == K_s:
                    self.tw.linear.x = 0
                    
            self.robot_model.move(v=self.tw.linear.x, a=self.tw.angular.z) 
                    
    def update(self):
        self.all_sprites.update()
        self.pub.publish(self.tw)

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def ros_loop(self):
        while not rospy.is_shutdown():
            self.pub.publish(self.tw)
            self.ros_clock.sleep()

if __name__ == "__main__":
    teleop = Teleop()
    teleop.run()