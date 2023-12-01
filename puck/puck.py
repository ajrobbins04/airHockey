import pygame
pygame.init()

import math
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

        if self.crossed_boundaries(time_passed) == True:
            # reassigns rect.center to corrected position
            self.update_rect()
      
        # velocity gradually decreases due to friction
        self.velocity.add_friction(PUCK_MAX_SPEED)

    def crossed_boundaries(self, time_passed):
        # bounce if new position out of bounds
        if self.hit_top_bottom() == True:
            self.bounce_off_boundary(360)
            return True
        elif self.hit_left_right() == True:
            self.bounce_off_boundary(180)
            return True
        
        return False

    def resolve_collision(self, paddle: Paddle):
        self.separate(paddle)

        # must find normal of collision to determine the direction of puck's movement
       
        # distance between the center of both circles
        distance = pygame.Vector2(self.rect.center).distance_to(pygame.Vector2(paddle.rect.center))

        delta_x = self.get_x() - paddle.get_x()
        delta_y = self.get_y() - paddle.get_y()

        collision_angle = math.atan2(delta_y, delta_x)
        total_mass = self.mass + paddle.get_mass()

        # use collision angle, initial velocity, and initial direction to derive each sprite's new velocity
        puck_dx = self.get_x_velocity() * math.cos(self.get_direction() - collision_angle)
        puck_dy = self.get_y_velocity() * math.sin(self.get_direction() - collision_angle)

        paddle_dx = paddle.get_x_velocity() * math.cos(paddle.get_direction() - collision_angle)
        paddle_dy = paddle.get_y_velocity() * math.sin(paddle.get_direction() - collision_angle)

        # final velocity = initial velocity * (mass - paddle's mass) + (2 * paddle's mass * paddle's initial velocity * total mass
        puck_dx_final = puck_dx * (self.mass - paddle.get_mass()) + (2 * paddle.get_mass() * paddle_dx) * total_mass
        paddle_dx_final = paddle_dx * (self.mass - paddle.get_mass()) + (2 * paddle.get_mass() * puck_dx) * total_mass

        self.update_velocity(math.atan2(puck_dy, puck_dx_final) + collision_angle)
        paddle.update_velocity(math.atan2(paddle_dy, paddle_dx_final) + collision_angle)


        # normal
        """ normal_x = (self.pos.get_x() - paddle.pos.get_x()) / distance
        normal_y = (self.pos.get_y() - paddle.pos.get_y()) / distance

        # dot product normal 
        dp_normal_1 = self.velocity.get_dx() * normal_x + self.velocity.get_dy() * normal_y
        dp_normal_2 = paddle.velocity.get_dx() * normal_x + paddle.velocity.get_dy() * normal_y

        momentum_1 = (dp_normal_1 * (self.mass - paddle.get_mass())  * paddle.get_mass() * dp_normal_2) / (self.mass + paddle.get_mass())
        momentum_2 = (dp_normal_2 * (paddle.get_mass() - self.mass)  * self.mass * dp_normal_1) / (self.mass + paddle.get_mass())

        # tangent
        tangent_x = -normal_y
        tangent_y = normal_x

        # dot product tangent
        dot_product_tan_1 = self.velocity.get_dx() * tangent_x + self.velocity.get_dy() * tangent_y
        dot_product_tan_2 = paddle.velocity.get_dx() * tangent_x + paddle.velocity.get_dy() * tangent_y

        self.velocity.set_dx(tangent_x * dot_product_tan_1 + normal_x * momentum_1)
        self.velocity.set_dy(tangent_y * dot_product_tan_1 + normal_y * momentum_1)

        paddle.velocity.set_dx(tangent_x * dot_product_tan_2 + normal_x * momentum_2)
        paddle.velocity.set_dy(tangent_y * dot_product_tan_2 + normal_y * momentum_2)

    
    def resolve_collision(self, paddle: Paddle):
       
        relative_velocity = (
            self.velocity.get_dx() - paddle.velocity.get_dx(),
            self.velocity.get_dy() - paddle.velocity.get_dy()
        )
        direction_vector = pygame.Vector2(self.rect.center) - pygame.Vector2(paddle.rect.center)
        normal = direction_vector.normalize()
     
        vel_along_normal = relative_velocity[0] * normal[0] + relative_velocity[1] * normal[1]

        # find minimum level of energy to retain after collision
        restitution = min(paddle.get_restitution(), self.restitution)
        
        if vel_along_normal <= 0:
            j = -(1 + restitution) * vel_along_normal
            j /= 1 / self.mass + 1 / paddle.get_mass()

            # Apply impulse
            impulse = (j * normal[0], j * normal[1])

            # Update velocities based on impulse
            self.velocity.set_dx(-1 / self.mass * impulse[0])
            self.velocity.set_dy(-1 / self.mass * impulse[1])

            paddle.velocity.set_dx(1 / paddle.get_mass() * impulse[0])
            paddle.velocity.set_dy(1 / paddle.get_mass() * impulse[1])"""

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

    # occurs when puck collides with a boundary
    def bounce_off_boundary(self, minuend): 
        # current direction is subtracted from the minuend
        # to find new direction in radians
        angle = self.calc_mirror_angle(minuend)
        self.velocity.update_velocity(angle)

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
        paddle.set_velocity(puck_dx, puck_dy)

