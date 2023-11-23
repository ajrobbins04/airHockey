import math
import random

class Velocity:
    def __init__(self):
        angle = random.uniform(0, 360)
        angle_radians = math.radians(angle)
        self.speed = 0.5

        self.dx = self.speed * math.cos(angle_radians)
        self.dy = self.speed * math.sin(angle_radians)

    def getDX(self):
        return self.dx
    
    def getDY(self):
        return self.dy
    
    def setDX(self, pixelsDX):
        self.dx = pixelsDX

    def setDY(self, pixelsDY):
        self.dy = pixelsDY

    def getVelocity(self):
        return self.dx, self.dy