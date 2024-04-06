from setting import *
# 食物类
class Food():
    def __init__(self,color=RED):
        self.position = (0, 0)
        self.color = color
        self.randomize_position()

    def randomize_position(self):
        
        width_decimal = Decimal(str((width-full_width)/2))
        x,y =  (width_decimal+
                         block_size_decimal*Decimal(random.randint(0,39)),
                         block_size_decimal*Decimal(random.randint(0, 29)))
        self.position = (float(x),float(y))
        
    def draw(self, surface):
        
        r = pygame.Rect((self.position[0], self.position[1]), (block_size, block_size))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, WHITE, r, 1)
