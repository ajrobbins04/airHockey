import pygame
pygame.init()

from fieldObject.fieldObject import FieldObject
from paddle.paddle import Paddle

class Puck(FieldObject):
    def __init__(self, color, pixelsX, pixelsY, radius, speed):
        super().__init__(color, pixelsX, pixelsY, radius, speed)
        pygame.sprite.Sprite.__init__(self) 


    def move(self, time_passed):

        # new position = position + (velocity * time)
        self.pos.add_x(self.velocity.get_dx() * time_passed)
        self.pos.add_y(self.velocity.get_dy() * time_passed)

        # bounce if new position out of bounds
        if self.hit_top_bottom() == True:
            self.bounce_off_boundary(360, time_passed)
        elif self.hit_left_right() == True:
            self.bounce_off_boundary(180, time_passed)

        # reassigns rect.center to updated position
        self.update_rect()

        # velocity gradually decreases due to friction
        self.velocity.add_friction()

    # occurs when puck collides with a boundary
    def bounce_off_boundary(self, minuend, time_passed): 
        # current angle of travel is subtracted from the minuend
        # to find new angle of travel
        angle = self.velocity.get_direction_angle_mirror(minuend)
        self.velocity.update_direction(angle)
        self.velocity.update_velocity()
        

    # occurs when puck collides with a stationary paddle
    def bounce_off_paddle(self):
        angle = self.velocity.get_direction_angle_opposite()
        self.velocity.update_direction(angle)
        self.velocity.update_velocity()
        self.update()

    # occurs when puck collides with a moving paddle
    def bounce_off_moving_paddle(self, paddle: Paddle):
    
        # use change in paddle position to ascertain its direction
        angle = paddle.calc_motion()
        # give puck same motion as paddle upon collision
        self.velocity.update_direction(angle)
        # speeds the puck up 
        self.velocity.add_momentum()
        self.velocity.update_velocity()