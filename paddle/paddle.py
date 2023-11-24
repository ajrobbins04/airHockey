import pygame
pygame.init()

from fieldObject.fieldObject import FieldObject
from position.position import Position

class Paddle(FieldObject):
    def __init__(self, color, pixels_x, pixels_y, radius):
        super().__init__(color, pixels_x, pixels_y, radius)

        # paddle is initially stationary
        self.is_moving = False

    def set_is_moving(self, prev_pos: Position = None, is_moving: bool = None):

        # value of is_moving is determined by paddle's 
        # current and previous positions
        if prev_pos is not None:
            currPos = self.get_position()
            if prev_pos != currPos:
                self.is_moving = True
            else:
                self.is_moving = False
        # or, the specified value is assigned to is_moving
        elif is_moving is not None:
            self.is_moving = is_moving

    def is_moving(self):
        return self.is_moving

    def calc_motion(self):
        return self.is_moving