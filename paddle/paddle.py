import pygame
pygame.init()

from fieldObject.fieldObject import FieldObject
from position.position import Position

class Paddle(FieldObject):
    def __init__(self, color, pixelsX, pixelsY, radius):
        super().__init__(color, pixelsX, pixelsY, radius)

        self.isMoving = False

    def set_is_moving(self, prevPos: Position = None, isMoving: bool = None):
        if prevPos is not None:
            currPos = self.getPosition()
            if prevPos != currPos:
                self.isMoving = True
            else:
                self.isMoving = False
        elif isMoving is not None:
            self.isMoving = isMoving

    def is_moving(self):
        return self.isMoving

    