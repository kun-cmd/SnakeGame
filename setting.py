import pygame
import pygame_gui
from pygame.locals import *
from pygame import mixer
import random
import sys
from pygame_gui.core import ObjectID
from pygame_gui import elements
from decimal import Decimal
import math
mixer.init()
# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GOLD = (240,230,140)
#定义音乐
SHIELD_SOUND = pygame.mixer.Sound('glass-breaks.wav')
KUN_SOUND = pygame.mixer.Sound('kun.wav')
PUNCH_SOUND = pygame.mixer.Sound('punch.wav')
#定义事件
INVINCIBLE_TIME = pygame.USEREVENT
ADD_SHIELD = pygame.USEREVENT+1
ADD_HP = pygame.USEREVENT+2
HP_DEDUCT = pygame.USEREVENT+3
SHIELD_BROKEN = pygame.USEREVENT+4
ACC_EVENT1 =  pygame.USEREVENT+5
ACC_EVENT2 =  pygame.USEREVENT+6
MOVE_EVENT =  pygame.USEREVENT+7
SLOW_EVENT1 =  pygame.USEREVENT+8
SLOW_EVENT2 =  pygame.USEREVENT+9
#帧率
FPS = 60
width, height = 800, 600
block_size = height/3*4/40
block_size_decimal = Decimal(str(block_size))
# 定义蛇的属性
INIT_LENGTH = 5
full_width = 800
NORMAL_SPEED = 100