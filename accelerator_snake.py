from snake import Snake
from setting import *
class Acc_snake(Snake):
    def __init__(self, positions, color,ACC_EVENT,SLOW_EVENT, is_ikun=False):
        super().__init__(positions, color, ACC_EVENT,SLOW_EVENT, is_ikun)
        
        self.max_stamina = 100.0
        self.current_stamina = 100.0
        self.stam_recharge_tick = 0.05
        self.stam_recharge_acc = 0.0
        self.acc = False
        
        self.rect = pygame.Rect(self.get_head_position(),(block_size,block_size))
    def move(self):
        
        cur = self.get_head_position()
        x, y = self.direction
        x = Decimal(str(x))
        y = Decimal(str(y))
        x = float(Decimal(str(cur[0])) +(x*block_size_decimal))
        y = float(Decimal(str(cur[1])) +(y*block_size_decimal))
        new = (x, y)
        if self.acc:
            self.current_stamina -= 1
            self.current_stamina = max(self.current_stamina, 0)
        
        # if len(self.positions) > 2 and new in self.positions[2:]:
        #if new in self.positions:
            #self.reset()
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
    def reset(self, positions):
        super().reset(positions)
        self.max_stamina = 100.0
        self.current_stamina = 100.0
        self.stam_recharge_tick = 0.05
        self.stam_recharge_acc = 0.0
    def update_stamina(self,time_delta_secs):
        if self.current_stamina < self.max_stamina:
            self.stam_recharge_acc += time_delta_secs
            if self.stam_recharge_acc >= self.stam_recharge_tick:
                self.current_stamina += 0.2
                self.stam_recharge_acc = 0.0
        self.current_stamina = min(self.current_stamina,self.max_stamina)
    
    def get_stamina_percentage(self) -> float:
        return self.current_stamina/self.max_stamina

    def skill(self,is_pressed):
        if is_pressed:
            self.acc = True
            self.speed = self.speed -30
            print(self.speed)
        else:
            self.speed = NORMAL_SPEED
            self.acc = False
