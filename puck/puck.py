import pygame
pygame.init()

import math
import numpy as np
from fieldObject.fieldObject import FieldObject
from paddle.paddle import Paddle
from constants.constants import *

class Puck(FieldObject):
    def __init__(self, color, pixelsX, pixelsY, radius, mass, speed, angle):
        super().__init__(color, pixelsX, pixelsY, radius, mass, speed, angle)
        pygame.sprite.Sprite.__init__(self) 


    def move(self, time_passed):

        # new position = position + (velocity * time)
        x = (self.get_x_velocity() * time_passed)
        y = (self.get_y_velocity() * time_passed)
        self.add_x_y(x, y)

        if self.crossed_boundaries() == True:
            # reassigns rect.center to corrected position
            self.update_rect()
      
        # velocity gradually decreases due to friction
        self.velocity.add_friction(PUCK_MIN_SPEED, PUCK_MAX_SPEED)

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
        x = math.sin(v1.x) * v1.y + math.sin(v2.x) * v2.y
        y = math.cos(v1.x) * v1.y + math.cos(v2.x) * v2.y

        # applies pythagorean theorem to get final magnitude
        magnitude = math.hypot(x, y)
        angle = math.pi / 2 - math.atan2(y, x)
        return (angle, magnitude)

   
    def resolve_collision(self, paddle: Paddle):

        self.separate(paddle)

        # must find normal of collision to determine the direction of puck's movement
       
        # distance between the center of both circles
        distance = pygame.Vector2(self.rect.center).distance_to(pygame.Vector2(paddle.rect.center))

        delta_x = self.get_x() - paddle.get_x()
        delta_y = self.get_y() - paddle.get_y()

        collision_angle = math.atan2(delta_y, delta_x)

        # angle perpendicular to collision angle is the direction
        # in which the objects move post-collision
        post_collision_angle = collision_angle + math.pi/2
        total_mass = self.mass + paddle.get_mass()

        # conservation of momentum stipulates that the puck's velocity is determined
        # by its initial velocity and its difference in weight from the paddle (it 
        # gains momentum b/c paddle is heavier) divided by the sum of weights
        pre_collision_puck = pygame.Vector2(self.get_direction(), self.get_speed() * (paddle.get_mass() - self.mass) / total_mass)
        post_collision_puck = pygame.Vector2(post_collision_angle, 2 * paddle.get_speed() * paddle.get_mass() / total_mass)

        puck_direction_speed = pygame.Vector2(pre_collision_puck, post_collision_puck)
        self.speed = puck_direction_speed.y
        self.update_velocity(puck_direction_speed.x)

        # use collision angle, initial velocity, and initial direction to derive each sprite's new velocity
        """puck_dx = self.get_x_velocity() * math.cos(self.get_direction() - collision_angle)
        puck_dy = self.get_y_velocity() * math.sin(self.get_direction() - collision_angle)

        paddle_dx = paddle.get_x_velocity() * math.cos(paddle.get_direction() - collision_angle)
        paddle_dy = paddle.get_y_velocity() * math.sin(paddle.get_direction() - collision_angle)

        # final velocity = initial velocity * (mass - paddle's mass) + (2 * paddle's mass * paddle's initial velocity * total mass
        puck_dx_final = puck_dx * (self.mass - paddle.get_mass()) + (2 * paddle.get_mass() * paddle_dx) * total_mass
        paddle_dx_final = paddle_dx * (self.mass - paddle.get_mass()) + (2 * paddle.get_mass() * puck_dx) * total_mass

        self.update_velocity(math.atan2(puck_dy, puck_dx_final) + collision_angle)
        paddle.update_velocity(math.atan2(paddle_dy, paddle_dx_final) + collision_angle)"""

        # ensure puck and paddle arent out of bounds
        if self.crossed_boundaries() == True:
            self.update_rect()
        if paddle.crossed_boundaries() == True:
            self.update_rect() 


    def separate(self, paddle: Paddle):
        # the distance between the centers of the puck and paddle
        distance = pygame.Vector2(self.rect.center).distance_to(pygame.Vector2(paddle.rect.center))

        # amount of displacement determined by amount of overlap
        overlap = 0.5 * (distance - self.radius - paddle.get_radius())

        puck_x = (- (overlap * (self.get_x() - paddle.get_x()) / distance))
        puck_y = (- (overlap * (self.get_y() - paddle.get_y()) / distance))
        self.add_x_y(puck_x, puck_y)

        paddle_x = overlap * (self.get_x() - paddle.get_x()) / distance
        paddle_y = overlap * (self.get_y() - paddle.get_y()) / distance
        paddle.add_x_y(paddle_x, paddle_y)

        # ensure puck and paddle aren't out of bounds
        if self.crossed_boundaries() == True:
            self.update_rect()
        if paddle.crossed_boundaries() == True:
            self.update_rect()

    # occurs when puck collides with a boundary
    def bounce_off_boundary(self, minuend): 
        # current direction is subtracted from the minuend
        # to find new direction in radians
        angle = self.calc_mirror_angle(minuend)
        self.velocity.update_velocity(angle)


    # occurs when puck collides with a stationary paddle
    """  def bounce_off_paddle(self, paddle: Paddle):
       
        self.separate()
        
        distance = pygame.Vector2(self.rect.center).distance_to(pygame.Vector2(paddle.rect.center))

        # normal
        normal_x = (self.get_x() - paddle.get_x()) / distance
        normal_y = (self.get_y() - paddle.get_y()) / distance

        # tangent
        tangent_x = -normal_y
        tangent_y = normal_x

        # dot product tangent
        dot_product_tan_1 = self.get_x_velocity() * tangent_x + self.get_y_velocity() * tangent_y
        dot_product_tan_2 = paddle.get_x_velocity() * tangent_x + paddle.get_y_velocity() * tangent_y

        puck_dx = tangent_x * dot_product_tan_1
        puck_dy = tangent_y * dot_product_tan_1
        self.set_velocity(puck_dx, puck_dy)

        paddle_dx = tangent_x * dot_product_tan_2
        paddle_dy = tangent_y * dot_product_tan_2
        paddle.set_velocity(puck_dx, puck_dy)
        """
        # occurs when puck collides with a stationary paddle
    def bounce_off_paddle(self, paddle: Paddle):
       
        self.separate()
        distance = pygame.Vector2(self.rect.center).distance_to(pygame.Vector2(paddle.rect.center))

        # normal
        normal_x = (self.get_x() - paddle.get_x()) / distance
        normal_y = (self.get_y() - paddle.get_y()) / distance

        # tangent
        tangent_x = -normal_y
        tangent_y = normal_x

        # dot product tangent
        dot_product_tan_1 = self.get_x_velocity() * tangent_x + self.get_y_velocity() * tangent_y
        dot_product_tan_2 = paddle.get_x_velocity() * tangent_x + paddle.get_y_velocity() * tangent_y

        puck_dx = tangent_x * dot_product_tan_1
        puck_dy = tangent_y * dot_product_tan_1
        self.set_velocity(puck_dx, puck_dy)

        paddle_dx = tangent_x * dot_product_tan_2
        paddle_dy = tangent_y * dot_product_tan_2
        paddle.set_velocity(paddle_dx, paddle_dy)

        # ensure puck and paddle aren't out of bounds
        if self.crossed_boundaries() == True:
            self.update_rect()
        if paddle.crossed_boundaries() == True:
            self.update_rect()
        
