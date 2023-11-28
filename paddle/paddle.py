import pygame
pygame.init()

from fieldObject.fieldObject import FieldObject
from position.position import Position
from angle.angle import Angle
from constants.constants import *
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_w,
    K_s,
    K_a,
    K_d
)

class Paddle(FieldObject):
    def __init__(self, color, pixels_x, pixels_y, radius):
        super().__init__(color, pixels_x, pixels_y, radius)

        # paddle is initially stationary
        self.moving = False
        self.prev_positions = []

        self.setup_moves()


    def setup_moves(self):
        directions = ["up", "down", "left", "right"]
        if self.color == BLUE:
            input_keys = [K_UP, K_DOWN, K_LEFT, K_RIGHT]
        else:
            input_keys = [K_w, K_s, K_a, K_d]
        
        # assigns each direction to the key that 
        # triggers it when pressed
        self.moves = dict(zip(directions, input_keys))

    # move according to the pressed keys that
    # are also found in the paddle's set of keys
    def move(self, pressed_keys):
       
        if pressed_keys[self.moves["up"]]:
            if pressed_keys[self.moves["left"]]:
                angle = 135
                print("135")
            elif pressed_keys[self.moves["right"]]:
                angle = 45
                print("45")
            else:
                angle = 90
                print("90")
        elif pressed_keys[self.moves["down"]]:
            if pressed_keys[self.moves["left"]]:
                angle = 225
                print("225")
            elif pressed_keys[self.moves["right"]]:
                angle = 315
                print("315")
            else:
                angle = 270
                print("270")
        elif pressed_keys[self.moves["left"]]:
            angle = 180
            print("180")
        elif pressed_keys[self.moves["right"]]:
            angle = 0
            print("0")
    

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