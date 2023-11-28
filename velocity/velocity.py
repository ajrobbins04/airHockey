from angle.angle import Angle
from constants.constants import *

class Velocity:
    def __init__(self):

        # velocity direction is set at a random angle
        self._direction = Angle()

        self._speed = PUCK_START_SPEED

        self._dx = self._speed * self._direction.get_x_direction()
        self._dy = self._speed * self._direction.get_y_direction()

    def get_dx(self):
        return self._dx
    
    def get_dy(self):
        return self._dy
    
    def get_direction(self):
        return self._direction
    
    def increase_velocity(self, speedIncrease):
        self._speed += speedIncrease

    def get_velocity(self):
        return self._dx, self._dy
    
    def get_direction_angle_opposite(self):
        return self._direction.get_angle_opposite()
    
    def get_direction_angle_mirror(self, minuend):
        return self._direction.get_angle_mirror(minuend)
    
    def add_momentum(self):
        self._speed = PUCK_MAX_SPEED

    def add_friction(self):
        self._speed *= FRICTION

    def update_direction(self, angle_degrees):
        self._direction.set_direction(angle_degrees)
    
    # calculate new velocity
    def update_velocity(self):
        # dx = speed * cos(direction in radians)
        self.dx = self._speed * self._direction.get_x_direction()
        # dy = speed * sin(direction in radians)
        self.dy = self._speed * self._direction.get_y_direction()





    