import pygame
pygame.init()

from fieldObject.fieldObject import FieldObject
from velocity.velocity import Velocity

class Puck(FieldObject):
    def __init__(self, color, pixelsX, pixelsY, radius):
        super().__init__(color, pixelsX, pixelsY, radius)
        pygame.sprite.Sprite.__init__(self) 

        self.velocity = Velocity()

        # assign current position to rect.center
        self.updateRect()

    def update(self):

        # use velocity to assign new position
        self.pos.addX(self.velocity.getDX())
        self.pos.addY(self.velocity.getDY())

        # reassigns rect.center to new position
        self.updateRect()

        # add friction to speed
        self.velocity.speed *= 0.99

    # current angle of travel is subtracted from the minuend
    # to find new angle of travel
    def bounce(self, minuend): 
        self.velocity.switchVelocity(minuend) 
        self.update()
