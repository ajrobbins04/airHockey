import pygame
pygame.init()

import random
import math

from constants.constants import *


class Velocity:
    def __init__(self, speed, angle):

        # occurs when object is a puck
        if angle is None:
            # set angle initially at a random value from 0 - 360
            angle = random.uniform(0, 360)
        else:
            angle = angle

        angle_radians = math.radians(angle)
        self.speed = speed

        velocity = self.calc_velocity(angle_radians)

        # velocity made up of magnitude (speed) and direction
        self.velocity = pygame.math.Vector2(velocity, angle_radians)

    # calculates velocity using speed and direction
    def calc_velocity(self, angle_radians):

        dx = self.calc_x_velocity(angle_radians)
        dy = self.calc_y_velocity(angle_radians)
        velocity = math.sqrt((dx * dx) + (dy * dy))

        return velocity

    # returns velocity traveling in x direction
    def calc_x_velocity(self, angle_radians):
        return self.speed * math.cos(angle_radians)

    # returns velocity traveling in y direction
    def calc_y_velocity(self, angle_radians):
        return self.speed * math.sin(angle_radians)
    
    def calc_mirror_angle(self, minuend):
        angle_radians = self.get_direction()
        angle_degrees = math.degrees(angle_radians)
        mirror_degrees = minuend - angle_degrees
        print(mirror_degrees)
        return math.radians(mirror_degrees)
    
    def get_x_velocity(self):
        # second vector attribute corresponds to direction (an angle)
        angle_radians = self.velocity.y
        return self.speed * math.cos(angle_radians)

    def get_y_velocity(self):
        angle_radians = self.velocity.y
        return self.speed * math.sin(angle_radians)
    
    def get_velocity(self):
        return self.velocity
    
    def get_speed(self):
        return self.speed
    
    # returns the angle in radians
    def get_direction(self):
        return self.velocity.y
    
    def set_speed(self, speed):
        self.speed = speed
    
    def set_velocity(self, dx, dy):
        velocity = math.sqrt((dx * dx) + (dy * dy))
        self.velocity.x = velocity

    def set_velocity_direction(self, direction):
        self.velocity.y = direction
        self.velocity.x = self.calc_velocity(direction)
    
    def set_velocity_stationary(self):
        self.velocity.x = 0
        self.velocity.y = 0
    
    # calculate new velocity
    def update_velocity(self, angle_radians):
        velocity = self.calc_velocity(angle_radians)
 
        self.velocity.x = velocity 
        self.velocity.y = angle_radians

    def update_velocity_degrees(self, angle_degrees):
        angle_radians = math.radians(angle_degrees)
        velocity = self.calc_velocity(angle_radians)
 
        self.velocity.x = velocity 
        self.velocity.y = angle_radians

    def increase_speed(self, speedIncrease):
        self.speed += speedIncrease

    # used for the puck, which continues to slow 
    # down until a collision adds momentum
    def add_friction(self, min_speed, max_speed):
        self.speed *= FRICTION

        # but never let puck be stationary
        if self.speed <= min_speed:
            self.speed = min_speed
        elif self.speed >= max_speed:
            self.speed = max_speed




    