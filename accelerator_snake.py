import pygame
import pygame_gui
import sys
import random

from snake王传恩 import *
from decimal import Decimal
from pygame_gui.core import ObjectID
#添加音频
from pygame.locals import *
from pygame import mixer
# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GOLD = (240,230,140)

class Acc_snake(Snake):
    def __init__(self, positions, color, is_ikun=False):
        super().__init__(positions, color, is_ikun)
        self.max_stamina = 100.0
        self.current_stamina = 100.0
        self.stam_recharge_tick = 0.05
        self.stam_recharge_acc = 0.0
        self.rect = pygame.Rect((Snake.get_head_position()),(block_size))
    def move(self):
        global block_size,block_size_decimal
        cur = self.get_head_position()
        x, y = self.direction
        x = Decimal(str(x))
        y = Decimal(str(y))
        x = float(Decimal(str(cur[0])) +(x*block_size_decimal))
        y = float(Decimal(str(cur[1])) +(y*block_size_decimal))
        new = (x, y)
        self.current_stamina -= 0.4
        self.current_stamina = max(self.current_stamina, 0)
        
        # if len(self.positions) > 2 and new in self.positions[2:]:
        #if new in self.positions:
            #self.reset()
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
    def reset(self, positions):
        self.length = INIT_LENGTH
        self.positions = positions
        self.direction = random.choice(self.directions)
        self.score = 0
        self.heart=5
        self.shield = 0
        self.is_HP = False
        self.is_shielded = False
        self.is_deduct = False
        self.invincible_time()
        self.max_stamina = 100.0
        self.current_stamina = 100.0
        self.stam_recharge_tick = 0.05
        self.stam_recharge_acc = 0.0
    def update_stamina(self,time_delta_secs):
        if self.current_stamina < self.max_stamina:
            self.stam_recharge_acc += time_delta_secs
            if self.stam_recharge_acc >= self.stam_recharge_tick:
                self.current_stamina += 1
                self.stam_recharge_acc = 0.0
    def get_stamina_percentage(self) -> float:
        return self.current_stamina/self.max_stamina

    def skill(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            self.speed = self.speed -30
            
