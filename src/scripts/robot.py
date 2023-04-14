"""
robot.py - Robot model for teleop.py

Date Modified: 2023-04-07
Author: Creed Zagrzebski <zagrzebski1516@uwlax.edu>
"""

import pygame as pg
from pygame.locals import *
from settings import *
import tf
import numpy as np

class Model(pg.sprite.Sprite):
    def __init__(self, x, y, group):
        super().__init__(group)
        
        # load image and scale it
        self.image = pg.Surface((SPRITE_SIZE, SPRITE_SIZE))
        self.image .fill(YELLOW)
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        self.direction = 0
        self.x = x
        self.y = y
        self.pw = np.array([0, 0, 0])
        
    def move(self, v=0, a=0):
        # Calculate new heading with respect to global frame
        self.direction += a * DT
        
        # Get displacement with respect to local frame
        pl = np.array([v * DT, 0, 0])
        
        # Generate transformation matrix from ROS tf library and extract rotation matrix 
        # from homogeneous matrix
        rot_z = tf.transformations.rotation_matrix(self.direction, ZAXIS) [:3, :3]
        
        # Transform displacement to global frame
        self.pw = np.dot(rot_z, pl)
  
    def update(self):
        # Translate robot to new position in global frame
        self.rect.x -= self.pw[1] * STEP_SIZE
        self.rect.y -= self.pw[0] * STEP_SIZE
         
class RobotModel(Model):
    def __init__(self, x, y, group):
        super().__init__(x, y, group)
        self.image = pg.image.load('tank.png')
        self.image = pg.transform.scale(self.image, (self.image.get_rect().width / SPRITE_SIZE, self.image.get_rect().height / SPRITE_SIZE))
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
    def update(self):
        # Perform rotation
        self.image = pg.transform.rotate(self.original_image, np.rad2deg(self.direction))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.old_direction = self.direction
        
        super().update()
        