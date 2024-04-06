
from setting import *
# 蛇的类
class Snake(object):
    
    def __init__(self,positions,color,is_ikun=False):
        
        self.length = INIT_LENGTH
        self.positions = positions
        #self.direction = [random.choice([pygame.K_LEFT, pygame.K_RIGHT]), random.choice([pygame.K_UP, pygame.K_DOWN])]
        self.directions = ((0,1),(0,-1),(1,0),(-1,0))
        self.direction = (0,0)
        self.color = color
        self.score = 0
        self.max_heart = 5
        self.heart = 5
        self.shield = 0
        self.is_win = False
        self.is_fail = False
        self.is_HP = False
        self.is_shielded = False
        self.shield_broke = False
        self.is_deduct = False
        self.is_ikun = is_ikun
        self.speed = 100
        self.invincible_time()
    def get_speed(self):
        return self.speed
    def add_shield(self):
        self.is_shielded = True
        self.shield+=1
        self.color = (0,255,255)
        pygame.time.set_timer(ADD_SHIELD, 1000)
    def add_HP(self):
        self.is_HP = True
        self.heart+=1
        self.color = (0,255,0)
        pygame.time.set_timer(ADD_HP, 1000)
    def  get_health_percentage(self) -> float:
        return self.heart/self.max_heart
    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0]*-1, point[1]*-1) == self.direction:
            return
        else:
            self.direction = point
    #吃机制
    def eat(self,food):
        self.length += 1
        self.score += 1
        buff=random.choice([self.add_shield,self.add_HP])
        buff()
        food.randomize_position()
        if self.is_ikun:
            KUN_SOUND.play()
    #扣血机制
    def HP_deduction(self):
        if self.is_invincibe is False:
            if self.shield>=1:
                self.shield-=1
                self.color = (135,206,235)
                SHIELD_SOUND.play()
                self.shield_broke = True
                pygame.time.set_timer(SHIELD_BROKEN, 3000)
            elif self.heart > 1:
                self.heart -= 1
                self.color = RED
                PUNCH_SOUND.play()
                self.is_deduct = True
                pygame.time.set_timer(HP_DEDUCT, 500)
            else:
                PUNCH_SOUND.play()
                self.heart = 0
                self.is_fail = True
                
    def move(self):
        
        cur = self.get_head_position()
        x, y = self.direction
        x = Decimal(str(x))
        y = Decimal(str(y))
        x = float(Decimal(str(cur[0])) +(x*block_size_decimal))
        y = float(Decimal(str(cur[1])) +(y*block_size_decimal))
        new = (x, y)
        # if len(self.positions) > 2 and new in self.positions[2:]:
        #if new in self.positions:
            #self.reset()
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
    #无敌机制   
    def invincible_time(self):
        self.is_invincibe = True
        
        pygame.time.set_timer(INVINCIBLE_TIME, 5000)
    #获取身体位置
    def get_body_positions(self):
        body_positions = []
        for i in range(1, len(self.positions)):
            body_positions.append(self.positions[i])
        return body_positions
    #检查是否撞墙
    def check_position(self):
        cur = self.get_head_position()
        new_x=cur[0]
        new_y = cur[1]
        if new_x <(width-full_width)/2 or new_x>(width+full_width)/2 or new_y <0 or new_y>height:
            return False
        return True
    #检查是否撞到敌人
    def check_hit(self,enenmy):
        if self.get_head_position() == enenmy.get_head_position() and self.is_win is False and enenmy.is_win is False:
            self.HP_deduction()
        if self.get_head_position() in enenmy.get_body_positions() and self.is_win is False and enenmy.is_win is False and enenmy.is_fail is False:
            self.HP_deduction()
    def check_eat(self,food):
        if self.get_head_position() == food.position:
            self.eat(food)
    #重置
    def reset(self,positions):
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
    
    def modify_positions(self,norm_block_size,full_block_size,is_fullscreen):
        
        if is_fullscreen:
            for i in range(0,len(self.positions)):
                x,y = self.positions[i]
                x = Decimal(str(x))
                y = Decimal(str(y))
                x = float((x/norm_block_size)*full_block_size+Decimal(str((width-full_width)/2)))
                y = float((y/norm_block_size)*full_block_size)
                self.positions[i] = (x,y)
        if is_fullscreen is False:
            for i in range(0, len(self.positions)):
                x, y = self.positions[i]
                y = Decimal(str(y))
                x = float((Decimal(str(x-(width-full_width)/2))/full_block_size)*norm_block_size)
                y = float((y/full_block_size)*norm_block_size)
                self.positions[i] = (x, y)
    def draw(self, surface):
        
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (block_size, block_size))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, WHITE, r, 1)
        if self.is_ikun:
            head=self.get_head_position()
            kun_img = pygame.image.load("kunkun.png").convert()
            kun_img = pygame.transform.scale(kun_img, (block_size, block_size))
            surface.blit(kun_img, (head[0], head[1]))
