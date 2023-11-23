import pygame
pygame.init()

from fieldObject.fieldObject import FieldObject

class Paddle(FieldObject):
    def __init__(self, color, pixelsX, pixelsY, radius):
        super().__init__(color, pixelsX, pixelsY, radius)