import pygame
pygame.init()

from fieldObject.fieldObject import FieldObject
from position.position import Position

class Paddle(FieldObject):
    def __init__(self, color, pixels_x, pixels_y, radius):
        super().__init__(color, pixels_x, pixels_y, radius)

        # paddle is initially stationary
        self.moving = False
        self.prev_positions = []

    def track_movement(self):
        if self.moving == True:
            self.prev_positions.append(Position(self.pos.get_x(), self.pos.get_y()))
     
    def begin_track_movement(self):
        self.moving = True
        self.prev_positions.append(Position(self.pos.get_x(), self.pos.get_y()))

    def end_track_movement(self):
        pos1 = self.prev_positions[0]
        pos2 = self.prev_positions.pop()
        self.moving = False
        self.prev_positions.clear()

    def is_moving(self):
        return self.moving

    def calc_motion(self):
        return self.moving