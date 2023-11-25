import math
import random

class Velocity:
    def __init__(self, speed = None):
        # set velocity movemement in random direction
        angle = random.uniform(0, 360)
        self.travel_angle = angle

        if speed == None:
            self.speed = 0.3
        else:
            self.speed = speed
        
        angle_radians = math.radians(angle)
        self.dx = self.speed * math.cos(angle_radians)
        self.dy = self.speed * math.sin(angle_radians)

    def get_dx(self):
        return self.dx
    
    def get_dy(self):
        return self.dy
    
    def get_travel_angle(self):
        return self.travel_angle
    
    def set_dx(self, pixelsDX):
        self.dx = pixelsDX

    def set_dy(self, pixelsDY):
        self.dy = pixelsDY
    
    def set_travel_angle(self, angle):
        self.travel_angle = angle

    def increase_velocity(self, speedIncrease):
        self.speed += speedIncrease

    def get_velocity(self):
        return self.dx, self.dy
    
    def update_velocity(self):
        angle_radians = math.radians(self.travel_angle)
        # calculate new velocity
        self.dx = self.speed * math.cos(angle_radians) 
        self.dy = self.speed * math.sin(angle_radians) 

    # reassign travel angle to the angle mirroring the current travel angle
    def mirror_travel_angle(self, minuend):
        self.travel_angle = minuend - self.get_travel_angle()

    # reassign travel angle to the angle opposite the current travel angle
    def opposite_travel_angle(self):
        self.travel_angle = (self.travel_angle+ 180) % 360

    


    