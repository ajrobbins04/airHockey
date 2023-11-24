import pygame
pygame.init()

from fieldObject.fieldObject import FieldObject
from position.position import Position

class Paddle(FieldObject):
    def __init__(self, color, pixelsX, pixelsY, radius):
        super().__init__(color, pixelsX, pixelsY, radius)

        # paddle is initially stationary
        self.isMoving = False

    def set_is_moving(self, prevPos: Position = None, isMoving: bool = None):

        # value of isMoving is determined by paddle's 
        # current and previous positions
        if prevPos is not None:
            currPos = self.getPosition()
            if prevPos != currPos:
                self.isMoving = True
            else:
                self.isMoving = False
        # or, the specified value is assigned to isMoving
        elif isMoving is not None:
            self.isMoving = isMoving

    def is_moving(self):
        return self.isMoving

    def calc_motion(self):
        return self.isMoving