import math
import numpy as np
positions = []
center_x = 0 
center_y = 0
radius = 1

for angle in np.linspace(0, 2*math.pi, 100):
  x = center_x + radius * math.cos(angle)
  y = center_y + radius * math.sin(angle)  
  positions.append((x, y))
  print(positions)