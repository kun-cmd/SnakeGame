
import pygame_gui
import sys
from pygame_gui.core import ObjectID
from accelerator_snake import Acc_snake
from setting import *
from snake import Snake
from food import Food
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


win = pygame.display.set_mode((width, height),RESIZABLE)
pygame.display.set_caption("贪吃蛇")

#之后再说
snake1_win_count = 0
snake2_win_count = 0


#按钮类
# class Button:
#     def __init__(self,x,y,width,height,normal_color,hover_color,text,text_size=30) -> None:
#         self.rect = pygame.Rect(x,y,width,height)
#         self.normal_color = normal_color
#         self.hover_color = hover_color
#         self.text=text
#         self.text_size = text_size
#     def draw(self,surface):
        
#         color = self.normal_color
#         if self.rect.collidepoint(pygame.mouse.get_pos()):
#             color = self.hover_color
#         pygame.draw.rect(surface,color,self.rect)
#         font = pygame.font.Font(None,self.text_size)
#         text = font.render(self.text,True,BLACK)
#         text_rect = text.get_rect(center = self.rect.center)
#         surface.blit(text,text_rect)
#     def handle_event(self,snake1,snake2):
#         global game_lock
#         global stop_intro
#         global block_size,block_size_decimal
#         if self.rect.collidepoint(pygame.mouse.get_pos()):
#             game_lock = False
#             snake1.reset([((width-full_width)/2+float((Decimal(29)*block_size_decimal)),height/2)])
#             snake2.reset([((width-full_width)/2+float((Decimal(9)*block_size_decimal)),height/2)])
#             snake1.is_win = False
#             snake2.is_win = False
#             snake1.is_fail = False
#             snake2.is_fail = False

#胜利界面
def win_screen(snake,text,button):
    font = pygame.font.Font(None, 100)
    win_text = font.render(text+" Win", True, BLACK)
    win.blit(win_text, (width/2-175,height/2-25))
    font = pygame.font.Font(None,50)
    score_text = font.render(f"Your Final Score is {snake.score}",True,BLACK)
    win.blit(score_text,(width/2-150,height/2+50)) 
    button.show()  
#失败界面
def fail_screen(snake1,snake2,button):
    global game_lock
    font_big = pygame.font.Font(None, 100)
    font_small = pygame.font.Font(None,50)
    if snake1.is_fail and snake2.is_fail:
        fail_text = font_big.render("Draw", True, BLACK)
        win.blit(fail_text, (width/2-50, height/2-25))
        score_text = font_small.render(f"Your Final Score are {snake1.score} and {snake2.score}", True, BLACK)
        win.blit(score_text,(width/2-150,height/2+50))
        button.show()
        game_lock = True
    elif snake1.is_fail is True:
        fail_text = font_big.render(f"{user1} Fail", True, BLACK)
        score_text = font_small.render(f"Your Final Score is {snake1.score}",True,BLACK)
        win.blit(fail_text, (width/2-175,height/2-25))
        win.blit(score_text, (width/2-150, height/2+50))
        button.show()
        game_lock = True
    elif snake2.is_fail is True:
        fail_text = font_big.render(f"{user2} Fail", True, BLACK)
        score_text = font_small.render(f"Your Final Score is {snake2.score}",True,BLACK)
        win.blit(fail_text, (width/2-175,height/2-25))
        win.blit(score_text, (width/2-150, height/2+50))
        button.show()
        game_lock = True
#窗口改变大小
def on_resize(snake1,snake2,food1,food2,invinc_food):
    global is_fullscreen,width,height,block_size,full_width,win,block_size_decimal,draw_edge
    for event in pygame.event.get(VIDEORESIZE):
        width, height = event.size
        full_width = height/3*4
        if full_width == 800:
            # 设置游戏界面尺寸
            is_fullscreen = False 
            full_block_size = Decimal(str(block_size))
            block_size = height/3*4/40
            block_size_decimal = Decimal(str(block_size))
            snake1.modify_positions(block_size_decimal,full_block_size,is_fullscreen)
            snake2.modify_positions(block_size_decimal,full_block_size,is_fullscreen)
            food1.randomize_position()
            food2.randomize_position()
            invinc_food.randomize_position()
            draw_edge = False
        else:
            # 设置游戏界面尺寸
            is_fullscreen = True
            norm_block_size = Decimal(str(block_size))
            block_size = height/3*4/40
            block_size_decimal = Decimal(str(block_size))
            snake1.modify_positions(norm_block_size,block_size_decimal,is_fullscreen)
            snake2.modify_positions(norm_block_size,block_size_decimal,is_fullscreen)
            food1.randomize_position()
            food2.randomize_position()
            invinc_food.randomize_position()
            draw_edge = True
        win = pygame.display.set_mode((width, height), RESIZABLE)
        pygame.event.post(event)
#介绍 
def intro():
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
    
# 主函数
def main():
    
    clock = pygame.time.Clock()
    manager = pygame_gui.UIManager((width,height),'theme.json')
    #检测是不是ikun
    kun1,kun2=False,False
    if user1 == "ikun" or user1 == "kun":
        kun1=True
    if user2 == "ikun" or user2 == "kun":
        kun2=True
    #设置游戏角色和道具
    global block_size
    block_size = height/3*4/40
    snake1 = Snake([((width-full_width)/2+(29*block_size),height/2)],color1,kun1)
    snake2 = Acc_snake([((width-full_width)/2+(9*block_size),height/2)],color2,kun2)
    food1 = Food()
    food2 = Food()
    invinci_food = Food(GOLD)
    # button = Button(width/2-50,height/2+100,100,50,(169,169,169),(105,105,105),"Try Again")
    # start_button = Button(width/2-50, height/2+100, 200, 50, (169,169,169), (105,105,105), "Press to Start")
    # 设置游戏胜利条件
    win_score = 6
    #回合胜利数
    global snake1_win_count 
    global snake2_win_count
    
    #当前时间
    now1 = pygame.time.get_ticks()-101
    now2 = pygame.time.get_ticks()-101
    now3 = pygame.time.get_ticks()-101
    
    normal_speed = 100
    #停止介绍
    
    global draw_edge
    draw_edge = False
    #添加bgm
    mixer.music.load('灰澈-森林-副本.mp3')
    mixer.music.play(-1)
    stop_intro = False
    hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((width/2-50,height/2+100), (100, 50)),
                                            text='Say Hello',
                                            manager=manager#anchors={'center':'center'}
                                            )
    health_bar1 = pygame_gui.elements.UIStatusBar(pygame.Rect((80,47),(200,30)),
                                                  manager,
                                                  percent_method=snake2.get_health_percentage,
                                                  object_id=ObjectID('#health_bar', '@player_status_bars')
                                                  )
    health_bar2 = pygame_gui.elements.UIStatusBar(pygame.Rect((-200,47),(200,30)),
                                                  manager,
                                                  percent_method=snake1.get_health_percentage,
                                                  object_id=ObjectID('#health_bar', '@player_status_bars'),
                                                  anchors={'right': 'right'})
    stamina_bar2 = pygame_gui.elements.UIStatusBar(pygame.Rect((0,0),(50,6)),
                                                   manager,
                                                   sprite=snake2,
                                                   percent_method=snake2.get_stamina_percentage,
                                                   object_id=ObjectID('#stamina_bar', '@player_status_bars'))
    
    while True:
        time_delta = clock.tick(FPS)/1000.0
        on_resize(snake1,snake2,food1,food2,invinci_food)
        
        win.fill(WHITE)
        if draw_edge:
            pygame.draw.rect(win,BLACK,((width-full_width)/2,0,full_width,height),1)
        if stop_intro is False:
            game_lock = True
            intro()
        #控制时间
        if pygame.time.get_ticks() - now1 > snake1.get_speed():
            now1 = pygame.time.get_ticks()
            snake1.move()
            
        if pygame.time.get_ticks() - now2 > snake2.get_speed():
            now2 = pygame.time.get_ticks()
            snake2.move()
            snake2.update_stamina(time_delta)

        if pygame.time.get_ticks() - now3 > normal_speed:
            now3 = pygame.time.get_ticks()
            #碰撞检测
            snake1.check_hit(snake2)
            snake2.check_hit(snake1)
        #吃食物机制
        snake1.check_eat(food1)
        snake1.check_eat(food2)
        snake2.check_eat(food1)
        snake2.check_eat(food2)
        if snake1.get_head_position() == invinci_food.position and snake2.is_invincibe is False:
            snake1.invincible_time()
            snake1.color = GOLD
            invinci_food.randomize_position()
        if snake2.get_head_position() == invinci_food.position and snake1.is_invincibe is False:
            snake2.invincible_time()
            snake2.color = GOLD
            invinci_food.randomize_position()
        
        fail_screen(snake1,snake2,hello_button)
        #绘制图形
        snake1.draw(win)
        snake2.draw(win)
        food1.draw(win)
        food2.draw(win)
        #等待5秒显示
        if snake1.is_invincibe is False and snake2.is_invincibe is False:
            invinci_food.draw(win)
        #操作设置
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
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
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     if game_lock:
            #         if snake1.is_win is True:
            #             snake1_win_count += 1
            #         if snake2.is_win is True:
            #             snake2_win_count += 1
            #         if snake1.is_fail is True and snake2.is_fail is True:
            #             snake1_win_count += 1
            #             snake2_win_count += 1
            #         elif snake1.is_fail is True:
            #             snake2_win_count +=1
            #         elif snake2.is_fail is True:
            #             snake1_win_count +=1
            #         button.handle_event(snake1, snake2)
            #         start_button.handle_event(snake1, snake2)
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
                    if event.key == pygame.K_SPACE:
                        snake2.skill(True)
                        
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        snake2.skill(False)
                        
            #按钮事件
            if game_lock:
                
                if (event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == hello_button):
                    stop_intro = True
                    game_lock = False
                    snake1.reset([((width-full_width)/2+float((Decimal(29)*block_size_decimal)),height/2)])
                    snake2.reset([((width-full_width)/2+float((Decimal(9)*block_size_decimal)),height/2)])
                    snake1.is_win = False
                    snake2.is_win = False
                    snake1.is_fail = False
                    snake2.is_fail = False
                    hello_button.hide()
                    
            manager.process_events(event)
        stamina_bar2.update(time_delta)
        manager.update(time_delta)
        manager.draw_ui(win)
        #道具特殊文本
        pygame.font.init()
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
        heart_text = font.render(f"HP: {snake1.heart}", True, BLACK)
        win.blit(heart_text, (width/2+width/4-70, 50))
        heart_text = font.render(f"HP: {snake2.heart}", True, BLACK)
        win.blit(heart_text, (10, 50))
        win_text = font.render(f"{snake2_win_count} VS {snake1_win_count}", True, BLACK)
        win.blit(win_text, (width/2-width/16, 10))
        shield_text = font.render(f"Shield: {snake1.shield}", True, BLACK)
        win.blit(shield_text, (width/2+width/4, 90))
        shield_text = font.render(f"Shield: {snake2.shield}", True, BLACK)
        win.blit(shield_text, (10, 90))

        #检测输赢机制    
        if snake1.score >= win_score and snake2.is_win is False:  # 假设蛇1的分数达到 10 时为胜利条件
            snake1.is_win=True
            win_screen(snake1, user1,hello_button)
            
            
            
        if snake2.score >= win_score and snake1.is_win is False:  # 假设蛇2的分数达到 10 时为胜利条件
            snake2.is_win=True
            win_screen(snake2,user2,hello_button)
            
            
            
        if snake1.check_position() is False and snake1.is_win is False and snake2.is_win is False and snake2.is_fail is False:
            snake1.is_fail = True
            fail_screen(snake1,snake2,hello_button)
            
            
        
        if snake2.check_position() is False and snake1.is_win is False and snake2.is_win is False and snake1.is_fail is False:
            snake2.is_fail = True
            fail_screen(snake1,snake2,hello_button)
            
            
        #帧数        
        pygame.display.update()
        clock.tick(FPS)
        
if __name__ == '__main__':
    main()