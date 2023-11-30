from angle.angle import Angle
from constants.constants import *

class Velocity:
    def __init__(self, speed):

        # velocity direction is set at a random angle
        self._direction = Angle()

        self._speed = speed

        self._dx = self._speed * self._direction.get_x_direction()
        self._dy = self._speed * self._direction.get_y_direction()

    def set_dx(self, dx):
        self._dx = dx

    def set_dy(self, dy):
        self._dy = dy

    def set_velocity(self, dx, dy):
        self._dx = dx
        self._dy = dy

    def get_dx(self):
        return self._dx
    
    def get_dy(self):
        return self._dy
    
    def get_direction(self):
        return self._direction.get_angle_radians()
    
    def get_speed(self):
        return self._speed
    
    def increase_velocity(self, speedIncrease):
        self._speed += speedIncrease

    def get_velocity(self):
        return (self._dx, self._dy)
    
    def get_direction_angle_opposite(self):
        return self._direction.get_angle_opposite()
    
    def get_direction_angle_mirror(self, minuend):
        return self._direction.get_angle_mirror(minuend)
    
    def speed_up(self):
        self._speed = PUCK_MAX_SPEED

    def add_friction(self):
        self._speed *= FRICTION

        # never let puck be stationary
        if self._speed < PUCK_MIN_SPEED:
            self._speed = PUCK_MIN_SPEED

    def update_direction(self, angle_degrees):
        self._direction.set_direction(angle_degrees)

    def update_direction_radians(self, angle_radians):
        self._direction.set_direction_radians(angle_radians)
    
    # calculate new velocity
    def update_velocity(self):
       
        # dx = speed * cos(direction in radians)
        self._dx = self._speed * self._direction.get_x_direction()
        # dy = speed * sin(direction in radians)
        self._dy = self._speed * self._direction.get_y_direction()





    