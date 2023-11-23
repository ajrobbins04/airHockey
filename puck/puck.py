import pygame
pygame.init()

from fieldObject.fieldObject import FieldObject
from velocity.velocity import Velocity

class Puck(FieldObject):
    def __init__(self, color, pixelsX, pixelsY, radius):
        super().__init__(color, pixelsX, pixelsY, radius)
        self.velocity = Velocity()
        pygame.sprite.Sprite.__init__(self) 
        self.updateRect()

    def move(self):
        self.pos.addX(self.velocity.getDX())
        self.pos.addY(self.velocity.getDY())
        self.updateRect()

    def bounce(self):
        self.velocity.reverseVelocity()
        self.move()
