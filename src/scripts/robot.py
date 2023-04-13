import pygame as pg
from pygame.locals import *
from settings import *
import tf
import numpy as np

class RobotModel(pg.sprite.Sprite):
    def __init__(self, x, y, group):
        super().__init__(group)
        
        self.image = pg.image.load('tank.png')
        self.image = pg.transform.scale(self.image, (self.image.get_rect().width / SPRITE_SIZE, self.image.get_rect().height / SPRITE_SIZE))
        
        # prevent image from getting distored
        self.original_image = self.image.copy()
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        self.direction = 0
        self.old_direction = 0
        self.x = x
        self.y = y
        self.pw = np.array([0, 0, 0])
        self.angle_change = 0
        
    def move(self, v=0, a=0):
        
        # Calculate new heading
        self.direction += a * DT
        
        # Get displacement with respect to local frame
        pl = np.array([-v * DT, 0, 0])
        
        # Generate transformation matrix from ROS tf library and extract rotation matrix 
        # from homogeneous matrix
        rot_z = tf.transformations.rotation_matrix(self.direction, ZAXIS) [:3, :3]
        
        # Transform displacement to global frame
        self.pw = np.dot(rot_z, pl)
  

    def update(self):
        self.rect.x += self.pw[1] * STEP_SIZE
        self.rect.y += self.pw[0] * STEP_SIZE
        
        if(self.direction != self.old_direction):
            self.image = pg.transform.rotate(self.original_image, self.direction * 180/np.pi)
            self.rect = self.image.get_rect(center=self.rect.center)
            print(self.direction)
            self.old_direction = self.direction
        
       