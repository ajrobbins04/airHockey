import pygame
pygame.init()

from fieldObject.fieldObject import FieldObject
from position.position import Position
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
    def __init__(self, color, pixels_x, pixels_y, radius, mass, speed, angle):
        super().__init__(color, pixels_x, pixels_y, radius, mass, speed, angle)

        # paddle is initially stationary
        self.moving = False

        # set initial velocity to 0
        self.velocity.set_velocity_stationary()

        # assign input keys to corresponding moves
        self.setup_moves()


    def setup_moves(self):
        directions = ["up", "down", "left", "right"]

        # lhs paddle corresponds to keys on far left of keyboard
        if self.position.get_x() <= SCREEN_WIDTH // 2:
            input_keys = [K_w, K_s, K_a, K_d]
        # rhs paddle corresponds to keys on far right of keyboard
        else:
            input_keys = [K_UP, K_DOWN, K_LEFT, K_RIGHT]

        # assigns each movemment direction to the 
        # key that triggers it when pressed
        self.moves = dict(zip(directions, input_keys))

    # move according to the pressed keys that
    # are also found in the paddle's set of keys
    def move(self, pressed_keys, time_passed):
        
        if self.moving == True:
            self.update_direction(pressed_keys)

            # new position = position + (velocity * time)
            x = self.get_x_velocity() * time_passed
            y = self.get_y_velocity() * time_passed

            self.add_x_y(x, y)

            if self.crossed_boundaries() == True:
                # reassigns rect.center to corrected position
                self.update_rect()

  
    # checks if the event key is one of the
    # possible inputs to move the paddle
    def in_keys(self, key):
        for possible_key in self.moves.values():
            if key == possible_key:
                return True
        return False
 
    def start_moving(self):
        self.moving = True
        self.set_speed(PADDLE_SPEED)

    def is_moving(self):
        return self.moving
    
    # collisions w/a non-moving puck will
    # have less momentum w/o speed
    def stop_moving(self):
        self.moving = False
        self.set_speed(0)

    # determines the angle in which the paddle is moving
    def update_direction(self, pressed_keys):

        up = pressed_keys[self.moves["up"]]
        down = pressed_keys[self.moves["down"]]
        left = pressed_keys[self.moves["left"]]
        right = pressed_keys[self.moves["right"]]
     
        # updates velocity based on new direction given
        if up == True:
            if left == True:
                self.update_velocity_degrees(225)
            elif right == True:
                self.update_velocity_degrees(315)
            else:
                self.update_velocity_degrees(270)
                
        elif down == True:
            if left == True:
                self.update_velocity_degrees(135)
            elif right == True:
                self.update_velocity_degrees(45)
            else:
                self.update_velocity_degrees(90)

        elif left == True:
            self.update_velocity_degrees(180)

        elif right == True:
             self.update_velocity_degrees(0)

    def crossed_boundaries(self):

        if self.hit_top() == True:
            self.position.set_y(0 + self.get_radius())
            return True
        elif self.hit_bottom() == True:
            self.position.set_y(SCREEN_HEIGHT - self.get_radius())
            return True
        
        # check paddle on lhs of field
        if self.color == RED:
            if self.hit_left():
                self.position.set_x(0 + self.get_radius())
                return True
            elif self.hit_midfield():
                self.position.set_x((SCREEN_WIDTH // 2) - self.get_radius())
                return True
            
        # check paddle on rhs of field
        else:
            if self.hit_right():
                self.position.set_x(SCREEN_WIDTH - self.get_radius())
                return True
            elif self.hit_midfield():
                self.position.set_x((SCREEN_WIDTH // 2) + self.get_radius())
                return True
            
        return False
