import pygame
pygame.init()

import math
import numpy as np
from fieldObject.fieldObject import FieldObject
from paddle.paddle import Paddle
from constants.constants import *

class Puck(FieldObject):
    def __init__(self, color, pixelsX, pixelsY, radius, mass, speed, angle, max_speed):
        super().__init__(color, pixelsX, pixelsY, radius, mass, speed, angle)
        pygame.sprite.Sprite.__init__(self) 

        self.max_speed = max_speed

    def move(self, time_passed):

        # new position = position + (velocity * time)
        x = (self.get_x_velocity() * time_passed)
        y = (self.get_y_velocity() * time_passed)
     
        self.add_x_y(x, y)

        if self.crossed_boundaries() == True:
            # reassigns rect.center to corrected position
            self.update_rect()
      
        # velocity gradually decreases due to friction
        self.velocity.add_friction(PUCK_MIN_SPEED, self.max_speed)

    def crossed_boundaries(self):
        # bounce if new position out of bounds
        if self.hit_top_bottom() == True:
            self.bounce_off_boundary(360)
            return True
        elif self.hit_left_right() == True:
            self.bounce_off_boundary(180)
            return True
        
        return False
    
    def add_vectors(self, v1, v2):
        x = math.cos(v1.x) * v1.y + math.cos(v2.x) * v2.y
        y = math.sin(v1.x) * v1.y + math.sin(v2.x) * v2.y

        # applies pythagorean theorem to get final magnitude
        magnitude = math.hypot(x, y)
        angle = math.pi / 2 - math.atan2(y, x)
        return (angle, magnitude)


    def resolve_collision(self, paddle: Paddle):
       
        # distance between the center of both circles
        distance = pygame.Vector2(self.rect.center).distance_to(pygame.Vector2(paddle.rect.center))

        delta_x = self.get_x() - paddle.get_x()
        delta_y = self.get_y() - paddle.get_y()

        collision_angle = math.atan2(delta_y, delta_x)

        # angle perpendicular to collision angle is the direction
        # in which the objects move post-collision
        projection_angle = collision_angle + math.pi/2
        total_mass = self.mass + paddle.get_mass()

        # conservation of momentum stipulates that the puck's velocity is determined
        # by its initial velocity and its difference in weight from the paddle (it 
        # gains momentum b/c paddle is heavier) divided by the sum of weights
        pre_collision_puck = pygame.Vector2(self.get_direction(), self.get_speed() * (self.mass - paddle.get_mass()) / total_mass)
        post_collision_puck = pygame.Vector2(projection_angle, 2 * paddle.get_speed() * paddle.get_mass() / total_mass)

        self.update_velocity(projection_angle)
        puck_direction_speed = pygame.Vector2(self.add_vectors(pre_collision_puck, post_collision_puck))
        self.set_speed(puck_direction_speed.y)
        self.update_velocity(puck_direction_speed.x)
        
        self.separate(paddle)

        # ensure puck and paddle arent out of bounds
        if self.crossed_boundaries() == True:
            self.update_rect()
        if paddle.crossed_boundaries() == True:
            self.update_rect() 
  
    def separate(self, paddle: Paddle):
        # applies distance formula for distance between the centers of the puck and paddle
        distance = pygame.Vector2(self.rect.center).distance_to(pygame.Vector2(paddle.rect.center))

        # amount of displacement determined by amount of overlap
        overlap = 0.5 * (distance - self.radius - paddle.get_radius())
        puck_x = (- (overlap * (self.get_x() - paddle.get_x()) / distance))
        puck_y = (- (overlap * (self.get_y() - paddle.get_y()) / distance))
        self.add_x_y(puck_x, puck_y)

        paddle_x = overlap * (self.get_x() - paddle.get_x()) / distance
        paddle_y = overlap * (self.get_y() - paddle.get_y()) / distance
        paddle.add_x_y(paddle_x, paddle_y)


    # occurs when puck collides with a boundary
    def bounce_off_boundary(self, minuend): 
        # current direction is subtracted from the minuend
        # to find new direction in radians
        angle = self.calc_mirror_angle(minuend) # angle returned in radians

        angle_degrees = math.degrees(angle)

        # keep angle w/in 0 - 360 degree range
        if angle_degrees < 0 or angle_degrees > 360:
            angle_degrees = angle_degrees % 360
            self.velocity.update_velocity_degrees(angle_degrees)
        else:
            self.velocity.update_velocity(angle)


