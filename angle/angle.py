import math
import random

class Angle:
    def __init__(self, speed = None):
        # set angle in random direction
        angle = random.uniform(0, 360)

        self.angle_degrees = angle
        self.angle_radians = math.radians(angle)

        self.x_direction = math.cos(self.angle_radians)
        self.y_direction = math.sin(self.angle_radians)
    
    def get_angle_degrees(self):
        return self.angle_degrees
    
    def get_angle_radians(self):
        return self.angle_radians
    
    def get_x_direction(self):
        return self.x_direction
    
    def get_y_direction(self):
        return self.y_direction

    def set_angle(self, angle_degrees):
        self.angle_degrees = angle_degrees
        self.angle_radians = math.radians(angle_degrees)

        self.x_direction = math.cos(self.angle_radians)
        self.y_direction = math.sin(self.angle_radians)

    # returns the angle mirroring the current angle
    def get_angle_mirror(self, minuend):
        return minuend - self.angle_degrees

    # returns the angle opposite the current angle
    def get_angle_opposite(self):
        return (self.angle_degrees + 180) % 360
     