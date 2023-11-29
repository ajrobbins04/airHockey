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
    def __init__(self, color, pixels_x, pixels_y, radius, speed):
        super().__init__(color, pixels_x, pixels_y, radius, speed)

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
    def move(self, pressed_keys, time_passed):
        
        if self.moving == True:
            self.calc_direction(pressed_keys)
            # new position = position + (velocity * time)
            self.pos.add_x(self.velocity.get_dx() * time_passed)
            self.pos.add_y(self.velocity.get_dy() * time_passed)

            # check if new position out of bounds
            

            # reassigns rect.center to updated position
            self.update_rect()

        
    # checks if the event key is one of the
    # possible inputs to move the paddle
    def in_keys(self, key):
        for possible_key in self.moves.values():
            if key == possible_key:
                return True
        return False
    
    def track_movement(self):
        if self.moving == True:
            self.prev_positions.append(Position(self.pos.get_x(), self.pos.get_y()))
     
    def begin_track_movement(self):
        self.moving = True
        self.prev_positions.append(Position(self.pos.get_x(), self.pos.get_y()))

    def end_track_movement(self):
        self.moving = False
        self.prev_positions.clear()

    def set_moving(self, moving):
        self.moving = moving

    def is_moving(self):
        return self.moving
    
    def stop_moving(self):
        self.moving = False
        self.angle = 0

    # determines the angle in which the paddle is moving
    def calc_direction(self, pressed_keys):

        up = pressed_keys[self.moves["up"]]
        down = pressed_keys[self.moves["down"]]
        left = pressed_keys[self.moves["left"]]
        right = pressed_keys[self.moves["right"]]
     
        if up == True:
            if left == True:
                self.velocity.update_direction(135)
            elif right == True:
                self.velocity.update_direction(45)
            else:
                self.velocity.update_direction(90)
                
        elif down == True:
            if left == True:
                self.velocity.update_direction(225)
            elif right == True:
                self.velocity.update_direction(315)
            else:
                self.velocity.update_direction(270)

        elif left == True:
            self.velocity.update_direction(180)

        elif right == True:
             self.velocity.update_direction(0)

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