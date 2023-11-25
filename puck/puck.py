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
        self.update_rect()

    def update(self):

        # use velocity to assign new position
        self.pos.add_x(self.velocity.get_dx())
        self.pos.add_y(self.velocity.get_dy())

        # reassigns rect.center to new position
        self.update_rect()

        # add friction to speed
       # self.velocity.speed *= 0.99

    # occurs when puck collides with a boundary
    def boundary_bounce(self, minuend): 
        # current angle of travel is subtracted from the minuend
        # to find new angle of travel
        self.velocity.mirror_travel_angle(minuend) 
        self.velocity.update_velocity()
        self.update()

    # occurs when puck collides with a paddle
    def paddle_bounce(self):
        self.velocity.opposite_travel_angle()
        self.velocity.update_velocity()
        self.update()