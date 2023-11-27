import pygame
pygame.init()

from fieldObject.fieldObject import FieldObject
from position.position import Position
from angle.angle import Angle

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
        self.moving = False
        self.prev_positions.clear()

    def is_moving(self):
        return self.moving

    # calculates the angle in which the paddle is moving
    def calc_motion(self):
        
        angle_degrees = 0

        if self.prev_positions:
            pos_start: Position = self.prev_positions[0]
            pos_end: Position = self.prev_positions[-1]

            x1 = pos_start.get_x()
            y1 = pos_start.get_y()
            x2 = pos_end.get_x()
            y2 = pos_end.get_y()

            # Calculate the angle of the path
            angle_degrees = Angle.calc_angle(x1, y1, x2, y2)

        # returns direction 
        return angle_degrees