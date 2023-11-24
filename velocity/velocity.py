import math
import random

class Velocity:
    def __init__(self, speed = None):
        # set velocity movemement in random direction
        angle = random.uniform(0, 360)
        self.travelAngle = angle

        if speed == None:
            self.speed = 0.3
        else:
            self.speed = speed
        
        angle_radians = math.radians(angle)
        self.dx = self.speed * math.cos(angle_radians)
        self.dy = self.speed * math.sin(angle_radians)

    def getDX(self):
        return self.dx
    
    def getDY(self):
        return self.dy
    
    def getTravelAngle(self):
        return self.travelAngle
    
    def setDX(self, pixelsDX):
        self.dx = pixelsDX

    def setDY(self, pixelsDY):
        self.dy = pixelsDY
    
    def setTravelAngle(self, angle):
        self.travelAngle = angle

    def getVelocity(self):
        return self.dx, self.dy
    
    def switchVelocity(self, minuend):

        # reassign travel angle to the angle mirroring the current travel angle
        self.travelAngle = minuend - self.getTravelAngle()
        angle_radians = math.radians(self.travelAngle)
        dx = self.speed * math.cos(angle_radians) 
        dy = self.speed * math.sin(angle_radians) 
        self.dx = dx
        self.dy = dy 