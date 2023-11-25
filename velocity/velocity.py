import math
import random

from angle.angle import Angle

class Velocity:
    def __init__(self, speed = None):

        # velocity direction is set at a random angle
        self.direction = Angle()

        if speed == None:
            self.speed = 0.3
        else:
            self.speed = speed

        self.dx = self.speed * self.direction.get_x_direction()
        self.dy = self.speed * self.direction.get_y_direction()

    def get_dx(self):
        return self.dx
    
    def get_dy(self):
        return self.dy
    
    def get_direction(self):
        return self.direction
    
    def set_dx(self, pixelsDX):
        self.dx = pixelsDX

    def set_dy(self, pixelsDY):
        self.dy = pixelsDY

    def increase_velocity(self, speedIncrease):
        self.speed += speedIncrease

    def get_velocity(self):
        return self.dx, self.dy
    
    def update_direction(self, angle_degrees):
        self.direction.set_angle(angle_degrees)
    
    # calculate new velocity
    def update_velocity(self):
        self.dx = self.speed * self.direction.get_x_direction()
        self.dy = self.speed * self.direction.get_y_direction()


    


    