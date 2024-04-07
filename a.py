import pygame
import pygame_gui
from pygame_gui.core import ObjectID

pygame.init()
class HappySprite:
    def __init__(self) -> None:
        self.position = pygame.Vector2(200.0, 300.0)
        self.rect = pygame.Rect((0, 200), (50,6))
        self.image = pygame.Surface((50, 100))
        self.image.fill((255, 0, 0))
        self.max_health = 100
        self.current_health = 90
        self.speed = 100.0
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False

    def get_health_percentage(self) -> float:
        return self.current_health/self.max_health
    def update(self, time_delta_secs: float) -> None:
        self.rect.move_ip(0,5)
        
        
        
pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((800, 600))

background = pygame.Surface((800, 600))
background.fill((225,225,225))

manager = pygame_gui.UIManager((800, 600),'theme.json')

hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 275), (100, 50)),
                                            text='Say Hello',
                                            manager=manager)

clock = pygame.time.Clock()
is_running = True
happy_sprite = HappySprite()
health_bar = pygame_gui.elements.UIStatusBar(pygame.Rect((0, 30), (50, 6)),
                                             manager,
                                             sprite=happy_sprite,
                                             percent_method=happy_sprite.get_health_percentage,object_id=ObjectID(
                                                 '#health_bar', '@player_status_bars'))
while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == hello_button:
                print("Hello")
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pygame.time.set_timer(pygame.USEREVENT, 1000)
                
        if event.type == pygame.USEREVENT:
            print(1)
            pygame.event.clear(pygame.USEREVENT)
        manager.process_events(event)
    happy_sprite.update(time_delta)
    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    
    manager.draw_ui(window_surface)

    pygame.display.update()