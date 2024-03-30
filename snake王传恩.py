import pygame
import random
from decimal import Decimal
#添加音频
from pygame.locals import *
from pygame import mixer
# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GOLD = (240,230,140)
#定义玩家属性
if input("是否使用默认设置?(Player1(Black),Player2(Blue))(y/n):") == 'y':
    user1 = "Player1"
    user2 = "Player2"
    running = False
    color1 = BLACK
    color2 = BLUE
else:
    user1 = input("请输入玩家一的名称:")
    user2 = input("请输入玩家二的名称:")
    running = False
    color1 = input(f"请输入{user1}的颜色(r,g,b)或black or blue:")
    if color1 == "black":
        color1 = BLACK
    if color1 == "blue":
        color1 = BLUE
    color2 = input(f"请输入{user2}的颜色(r,g,b)或black or blue:")
    if color2 == "black":
        color2 = BLACK
    if color2 == "blue":
        color2 = BLUE
if input("是否开始游戏(y/n):") == "y":
    running = True
    print("贪吃蛇，启动！！！")
else:
    print("6，我无语了，重开吧")
if running:
    # 初始化pygame
    pygame.init()
mixer.init()
shield_sound = pygame.mixer.Sound('glass-breaks.wav')
kun_sound = pygame.mixer.Sound('kun.wav')
punch_sound = pygame.mixer.Sound('punch.wav')
# 设置游戏界面尺寸
is_fullscreen = False
width, height = 800, 600
full_width = 800
win = pygame.display.set_mode((width, height),RESIZABLE)
pygame.display.set_caption("贪吃蛇")



#定义事件
INVINCIBLE_TIME = pygame.USEREVENT
ADD_SHIELD = pygame.USEREVENT+1
ADD_HP = pygame.USEREVENT+2
HP_DEDUCT = pygame.USEREVENT+3
SHIELD_BROKEN = pygame.USEREVENT+4
# 定义蛇的属性
INIT_LENGTH = 5
block_size = 20
block_size_decimal = Decimal(str(block_size))
#帧率
fps = 60
snake1_win_count = 0
snake2_win_count = 0
#游戏锁定
# 蛇的类
class Snake:
    
    def __init__(self,positions,color,is_ikun=False):
        
        self.length = INIT_LENGTH
        self.positions = positions
        #self.direction = [random.choice([pygame.K_LEFT, pygame.K_RIGHT]), random.choice([pygame.K_UP, pygame.K_DOWN])]
        self.directions = ((0,1),(0,-1),(1,0),(-1,0))
        self.direction = (0,0)
        self.color = color
        self.score = 0
        self.heart = 2
        self.shield = 0
        self.is_win = False
        self.is_fail = False
        self.is_HP = False
        self.is_shielded = False
        self.shield_broke = False
        self.is_deduct = False
        self.is_ikun = is_ikun
        self.invincible_time()
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
            kun_sound.play()
    #扣血机制
    def HP_deduction(self):
        global game_lock
        if self.is_invincibe is False:
            if self.shield>=1:
                self.shield-=1
                self.color = (135,206,235)
                shield_sound.play()
                self.shield_broke = True
                pygame.time.set_timer(SHIELD_BROKEN, 3000)
            elif self.heart > 1:
                self.heart -= 1
                self.color = RED
                punch_sound.play()
                self.is_deduct = True
                pygame.time.set_timer(HP_DEDUCT, 500)
            else:
                punch_sound.play()
                self.heart = 0
                self.is_fail = True
                game_lock = True
    def move(self):
        global block_size,block_size_decimal
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
    #重置
    def reset(self,positions):
        self.length = INIT_LENGTH
        self.positions = positions
        self.direction = random.choice(self.directions)
        self.score = 0
        self.heart=2
        self.shield = 0
        self.is_HP = False
        self.is_shielded = False
        self.is_deduct = False
        self.invincible_time()
        
    def modify_positions(self,norm_block_size,full_block_size):
        global is_fullscreen
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
        global block_size
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (block_size, block_size))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, WHITE, r, 1)
        if self.is_ikun:
            head=self.get_head_position()
            kun_img = pygame.image.load("kunkun.png").convert()
            kun_img = pygame.transform.scale(kun_img, (block_size, block_size))
            surface.blit(kun_img, (head[0], head[1]))

    
#按钮类
class Button:
    def __init__(self,x,y,width,height,normal_color,hover_color,text,text_size=30) -> None:
        self.rect = pygame.Rect(x,y,width,height)
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.text=text
        self.text_size = text_size
    def draw(self,surface):
        
        color = self.normal_color
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            color = self.hover_color
        pygame.draw.rect(surface,color,self.rect)
        font = pygame.font.Font(None,self.text_size)
        text = font.render(self.text,True,BLACK)
        text_rect = text.get_rect(center = self.rect.center)
        surface.blit(text,text_rect)
    def handle_event(self,snake1,snake2):
        global game_lock
        global stop_intro
        global block_size,block_size_decimal
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            stop_intro = True
            game_lock = False
            snake1.reset([((width-full_width)/2+float((Decimal(29)*block_size_decimal)),height/2)])
            snake2.reset([((width-full_width)/2+float((Decimal(9)*block_size_decimal)),height/2)])
            snake1.is_win = False
            snake2.is_win = False
            snake1.is_fail = False
            snake2.is_fail = False
            
# 食物类
class Food:
    def __init__(self,color=RED):
        self.position = (0, 0)
        self.color = color
        self.randomize_position()

    def randomize_position(self):
        global block_size,block_size_decimal
        width_decimal = Decimal(str((width-full_width)/2))
        x,y =  (width_decimal+
                         block_size_decimal*Decimal(random.randint(0,39)),
                         block_size_decimal*Decimal(random.randint(0, 29)))
        self.position = (float(x),float(y))
        
    def draw(self, surface):
        global block_size
        r = pygame.Rect((self.position[0], self.position[1]), (block_size, block_size))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, WHITE, r, 1)
#扣血机制
def snakes_hit(snake1,snake2):
    
    if snake1.get_head_position() == snake2.get_head_position() and snake1.is_win is False and snake2.is_win is False:
        snake1.HP_deduction()
        snake2.HP_deduction()
        
    elif snake1.get_head_position() in snake2.get_body_positions() and snake1.is_win is False and snake2.is_win is False and snake2.is_fail is False:
        snake1.HP_deduction()
        
    elif snake2.get_head_position() in snake1.get_body_positions() and snake1.is_win is False and snake2.is_win is False and snake1.is_fail is False:
        snake2.HP_deduction()
        

#胜利界面
def win_screen(snake,text,button):
    font = pygame.font.Font(None, 100)
    win_text = font.render(text+" Win", True, BLACK)
    win.blit(win_text, (width/2-175,height/2-25))
    font = pygame.font.Font(None,50)
    score_text = font.render(f"Your Final Score is {snake.score}",True,BLACK)
    win.blit(score_text,(width/2-150,height/2+50)) 
    button.draw(win)   
#失败界面
def fail_screen(snake1,snake2,button):
    font_big = pygame.font.Font(None, 100)
    font_small = pygame.font.Font(None,50)
    if snake1.is_fail and snake2.is_fail:
        fail_text = font_big.render("Draw", True, BLACK)
        win.blit(fail_text, (width/2-50, height/2-25))
        score_text = font_small.render(f"Your Final Score are {snake1.score} and {snake2.score}", True, BLACK)
        win.blit(score_text,(width/2-150,height/2+50))
        button.draw(win)
        
    elif snake1.is_fail is True:
        fail_text = font_big.render(f"{user1} Fail", True, BLACK)
        score_text = font_small.render(f"Your Final Score is {snake1.score}",True,BLACK)
        win.blit(fail_text, (width/2-175,height/2-25))
        win.blit(score_text, (width/2-150, height/2+50))
        button.draw(win)
        
    elif snake2.is_fail is True:
        fail_text = font_big.render(f"{user2} Fail", True, BLACK)
        score_text = font_small.render(f"Your Final Score is {snake2.score}",True,BLACK)
        win.blit(fail_text, (width/2-175,height/2-25))
        win.blit(score_text, (width/2-150, height/2+50))
        button.draw(win)
        
    
#操作设置
def handle_key(snake1,snake2,button,start_button):
    global snake1_win_count 
    global snake2_win_count
    global game_lock
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            #无敌
            if snake1.is_invincibe is True:
                if event.type == INVINCIBLE_TIME:
                    snake1.is_invincibe = False
                    snake1.color = color1
                    
            if snake2.is_invincibe is True:
                if event.type == INVINCIBLE_TIME:
                    snake2.is_invincibe = False
                    snake2.color = color2
                    
            #加护盾
            if snake1.is_shielded is True:    
                if event.type == ADD_SHIELD:
                    snake1.is_shielded = False
                    snake1.color = color1
            if snake2.is_shielded is True:
                if event.type == ADD_SHIELD:
                    snake2.is_shielded = False
                    snake2.color = color2
            #加血量
            if snake1.is_HP is True:        
                if event.type == ADD_HP:
                    snake1.is_HP = False
                    snake1.color = color1
            if snake2.is_HP is True:
                if event.type == ADD_HP:
                    snake2.is_HP = False
                    snake2.color = color2
            #扣血
            if snake1.is_deduct is True:
                if event.type == HP_DEDUCT:
                    snake1.is_deduct = False
                    snake1.color = color1
            if snake2.is_deduct is True:
                if event.type == HP_DEDUCT:
                    snake2.is_deduct = False
                    snake2.color = color2
            #扣护盾        
            if snake1.shield_broke is True:        
                if event.type == SHIELD_BROKEN:
                    snake1.shield_broke = False
                    snake1.color = color1
            if snake2.shield_broke is True:
                if event.type == SHIELD_BROKEN:
                    snake2.shield_broke = False
                    snake2.color = color2
            #按钮事件
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_lock:
                    if snake1.is_win is True:
                        snake1_win_count += 1
                    if snake2.is_win is True:
                        snake2_win_count += 1
                    if snake1.is_fail is True and snake2.is_fail is True:
                        snake1_win_count += 1
                        snake2_win_count += 1
                    elif snake1.is_fail is True:
                        snake2_win_count +=1
                    elif snake2.is_fail is True:
                        snake1_win_count +=1
                    button.handle_event(snake1, snake2)
                    start_button.handle_event(snake1, snake2)
            #操作设置
            if game_lock is False:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        snake1.turn((0, -1))
                    elif event.key == pygame.K_DOWN:
                        snake1.turn((0, 1))
                    elif event.key == pygame.K_LEFT:
                        snake1.turn((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        snake1.turn((1, 0))
                    if event.key == pygame.K_w:
                        snake2.turn((0, -1))
                    elif event.key == pygame.K_s:
                        snake2.turn((0, 1))
                    elif event.key == pygame.K_a:
                        snake2.turn((-1, 0))
                    elif event.key == pygame.K_d:
                        snake2.turn((1, 0))
def on_resize(snake1,snake2,food1,food2,invinc_food):
    global is_fullscreen,width,height,block_size,full_width,win,block_size_decimal
    for event in pygame.event.get(VIDEORESIZE):
        width, height = event.size
        full_width = height/3*4
        if full_width == 800:
            is_fullscreen = False 
            full_block_size = Decimal(str(block_size))
            block_size = height/3*4/40
            block_size_decimal = Decimal(str(block_size))
            snake1.modify_positions(block_size_decimal,full_block_size)
            snake2.modify_positions(block_size_decimal,full_block_size)
            food1.randomize_position()
            food2.randomize_position()
            invinc_food.randomize_position()
        else:
            is_fullscreen = True
            norm_block_size = Decimal(str(block_size))
            block_size = height/3*4/40
            block_size_decimal = Decimal(str(block_size))
            snake1.modify_positions(norm_block_size,block_size_decimal)
            snake2.modify_positions(norm_block_size,block_size_decimal)
            food1.randomize_position()
            food2.randomize_position()
            invinc_food.randomize_position()
        win = pygame.display.set_mode((width, height), RESIZABLE)
        pygame.event.post(event)
#介绍 
def intro(start_button):
    font = pygame.font.SysFont("simsun", 36,False,False)
    intro_text = font.render("Welcome to Snake Game", True, BLACK)
    win.blit(intro_text, (width/2-175, 100))
    rules_text1 = font.render("游戏规则: 每条蛇开局有五秒钟的无敌时间", True, BLACK)
    win.blit(rules_text1, (width/2-350, 150))
    rules_text2 = font.render("吃红色食物可以获得随机buff", True, BLACK)
    win.blit(rules_text2, (width/2-200, 200))
    rules_text3 = font.render("金色食物是无敌五秒，不可出界", True, BLACK)
    win.blit(rules_text3, (width/2-225, 250))
    rules_text4 = font.render("一条蛇蛇头触碰另一条蛇的身体会扣血", True, BLACK)
    win.blit(rules_text4, (width/2-250, 300))
    rules_text5 = font.render("吃到三个红色食物或将敌人血量扣光算赢", True, BLACK)
    win.blit(rules_text5, (width/2-350, 350))
    start_button.draw(win)
    
# 主函数
def main():
    
    clock = pygame.time.Clock()
    #检测是不是ikun
    kun1,kun2=False,False
    if user1 == "ikun" or user1 == "kun":
        kun1=True
    if user2 == "ikun" or user2 == "kun":
        kun2=True
    #设置游戏角色和道具
    global full_width,is_fullscreen,block_size,fps
    snake_speed = 100
    snake1 = Snake([((width-full_width)/2+(29*block_size),height/2)],color1,kun1)
    snake2 = Snake([((width-full_width)/2+(9*block_size),height/2)],color2,kun2)
    food1 = Food()
    food2 = Food()
    invinci_food = Food(GOLD)
    button = Button(width/2-50,height/2+100,100,50,(169,169,169),(105,105,105),"Try Again")
    start_button = Button(width/2-50, height/2+100, 200, 50, (169,169,169), (105,105,105), "Press to Start")
    # 设置游戏胜利条件
    win_score = 6
    #回合胜利数
    global snake1_win_count 
    global snake2_win_count
    #游戏锁定
    global game_lock
    #当前时间
    global now
    #停止介绍
    global stop_intro
    now = pygame.time.get_ticks()-101
    #添加bgm
    mixer.music.load('灰澈-森林-副本.ogg')
    mixer.music.play(-1)
    stop_intro = False
    if is_fullscreen:
        food1.randomize_position()
        food2.randomize_position()
        invinci_food.randomize_position()
    while True:
        
        on_resize(snake1,snake2,food1,food2,invinci_food)
        
        
        win.fill(WHITE)
        if stop_intro is False:
            game_lock = True
            intro(start_button)
        #控制时间
        if pygame.time.get_ticks() - now > snake_speed:
            now = pygame.time.get_ticks()
            snake1.move()
            snake2.move()
            snakes_hit(snake1, snake2)
            
        #吃食物机制
        if snake1.get_head_position() == food1.position:
            snake1.eat(food1)
        if snake1.get_head_position() == food2.position:
            snake1.eat(food2)
        if snake2.get_head_position() == food1.position:
            snake2.eat(food1)
        if snake2.get_head_position() == food2.position:
            snake2.eat(food2)
        if snake1.get_head_position() == invinci_food.position and snake2.is_invincibe is False:
            snake1.invincible_time()
            snake1.color = GOLD
            invinci_food.randomize_position()
        if snake2.get_head_position() == invinci_food.position and snake1.is_invincibe is False:
            snake2.invincible_time()
            snake2.color = GOLD
            invinci_food.randomize_position()
        
        fail_screen(snake1,snake2,button)
        #绘制图形
        snake1.draw(win)
        snake2.draw(win)
        food1.draw(win)
        food2.draw(win)
        #等待5秒显示
        if snake1.is_invincibe is False and snake2.is_invincibe is False:
            invinci_food.draw(win)
        #操作设置
        handle_key(snake1, snake2, button,start_button)
        #道具特殊文本
        font = pygame.font.SysFont("simsun", 36,True,False)
        if snake1.shield_broke is True or snake2.shield_broke is True:
            shield_text = font.render("把世界调成静音，聆听名刀破碎的声音", True, BLACK)
            win.blit(shield_text, (width/2-300, 100))
            
        if snake1.color == GOLD or snake2.color == GOLD:
            shield_text = font.render("孩子，你无敌了", True, BLACK)
            win.blit(shield_text, (width/2-125, 100))
        #UI
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"{user1} Score: {snake1.score}", True, BLACK)
        win.blit(score_text, (width/2+width/4, 10))
        score_text = font.render(f"{user2} Score: {snake2.score}", True, BLACK)
        win.blit(score_text, (10, 10))
        heart_text = font.render(f"{user1} HP: {snake1.heart}", True, BLACK)
        win.blit(heart_text, (width/2+width/4, 50))
        heart_text = font.render(f"{user2} HP: {snake2.heart}", True, BLACK)
        win.blit(heart_text, (10, 50))
        win_text = font.render(f"{snake2_win_count} VS {snake1_win_count}", True, BLACK)
        win.blit(win_text, (width/2-width/16, 10))
        shield_text = font.render(f"{user1} Shield: {snake1.shield}", True, BLACK)
        win.blit(shield_text, (width/2+width/4, 90))
        shield_text = font.render(f"{user2} Shield: {snake2.shield}", True, BLACK)
        win.blit(shield_text, (10, 90))

        #检测输赢机制    
        if snake1.score >= win_score and snake2.is_win is False:  # 假设蛇1的分数达到 10 时为胜利条件
            win_screen(snake1, user1,button)
            snake1.is_win=True
            game_lock = True
            
        if snake2.score >= win_score and snake1.is_win is False:  # 假设蛇2的分数达到 10 时为胜利条件
            win_screen(snake2,user2,button)
            snake2.is_win=True
            game_lock = True
            
        if snake1.check_position() is False and snake1.is_win is False and snake2.is_win is False and snake2.is_fail is False:
            fail_screen(snake1,snake2,button)
            snake1.is_fail = True
            game_lock = True
        
        if snake2.check_position() is False and snake1.is_win is False and snake2.is_win is False and snake1.is_fail is False:
            fail_screen(snake1,snake2,button)
            snake2.is_fail = True
            game_lock = True
        #帧数        
        pygame.display.update()
        clock.tick(fps)
        
if __name__ == '__main__':
    main()