import math

# Sprite Settings
SPRITE_SIZE = 20
STEP_SIZE = 50

# Screen Configurations
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 300

# Game Loop Config
FPS = 30 

# ROS Configurations
ROS_RATE = 10
FORWARD_SPEED = 0.2 # m/s
ANGULAR_SPEED = math.pi/6 # rad/s
DT = 1.0/ROS_RATE # s

# Colors
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# Rotations 
ZAXIS = (0, 0, 1)
