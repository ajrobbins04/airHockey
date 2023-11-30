import math
import random

class Angle:
    def __init__(self):
        # set angle for pucks in random direction
        angle = random.uniform(0, 360)

        self._angle_degrees = angle
        self._angle_radians = math.radians(angle)

        self._x_direction = math.cos(self._angle_radians)
        self._y_direction = math.sin(self._angle_radians)
    
    def get_angle_degrees(self):
        return self._angle_degrees
    
    def get_angle_radians(self):
        return self._angle_radians
    
    def get_x_direction(self):
        return self._x_direction
    
    def get_y_direction(self):
        return self._y_direction
    
    # used by puck to define its direction of travel
    """" def set_angle(self, angle_degrees = None, angle_radians = None):

        if angle_degrees is not None:
            # set angle in degrees
            self._angle_degrees = angle_degrees
            # convert and set angle in radians
            self._angle_radians = math.radians(angle_degrees)

        elif angle_radians is not None:
            # set angle in radians
            self._angle_radians = angle_radians
            # convert and set angle in radians
            self._angle_degrees = math.degrees(angle_radians)

        self._x_direction = math.cos(self._angle_radians)
        self._y_direction = math.sin(self._angle_radians)
        self._xy_direction = math.atan2(self._y_direction, self._x_direction)"""

    # calulates the angle in between two points  
    @staticmethod    
    def calc_angle(x1, y1, x2, y2):
        angle = math.atan2(y2 - y1, x2 - x1)
        return math.degrees(angle)

    def set_direction(self, angle_degrees):
      
        # set angle in degrees
        self._angle_degrees = angle_degrees
        # convert and set angle in radians
        self._angle_radians = math.radians(angle_degrees)

        self._x_direction = math.cos(self._angle_radians)
        self._y_direction = math.sin(self._angle_radians)

    def set_direction_radians(self, angle_radians):
        
        self._angle_degrees = math.degrees(angle_radians)
        self._angle_radians = angle_radians
        self._x_direction = math.cos(self._angle_radians)
        self._y_direction = math.sin(self._angle_radians)

    # returns the angle mirroring the current angle
    def get_angle_mirror(self, minuend):
        return minuend - self._angle_degrees

    # returns the angle opposite the current angle
    def get_angle_opposite(self):
        return (self._angle_degrees + 180) % 360
     