import pygame
pygame.init()

from position.position import Position
from velocity.velocity import Velocity
from constants.constants import *

# Define a Player object by extending pygame's Sprite
# The surface drawn on the screen is now an attribute of 'player'
class FieldObject(pygame.sprite.Sprite):
    def __init__(self, color, pixels_x, pixels_y, radius, mass, speed, angle):

        # inherits from Sprite 
        super(FieldObject, self).__init__()

        self.radius = radius
        self.mass = mass

        # both attributes are vectors
        self.position = Position(pixels_x, pixels_y)
        self.velocity = Velocity(speed, angle)

        # surface size is twice the size of the radius
        surface = pygame.Surface((radius * 2, radius * 2))
  
        # include rect to use its collision detection methods
        self.rect = surface.get_rect(center=(pixels_x, pixels_y))

        # will be red or blue for paddles and black for puck
        self.color = color

    
    def get_radius(self):
        return self.radius
    
    def get_mass(self):
        return self.mass
    
    def get_color(self):
        return self.color
    
    """ all the wrapper methods for position and velocity attributes """
    def get_x(self):
        return self.position.get_x()
    
    def get_y(self):
        return self.position.get_y()
    
    def get_position(self):
        return self.position.get_position()
    
    def get_speed(self):
        return self.velocity.get_speed()
    
    def get_x_velocity(self):
        return self.velocity.get_x_velocity()
    
    def get_y_velocity(self):
        return self.velocity.get_y_velocity()
    
    def get_velocity(self):
        return self.velocity.get_velocity()
    def get_speed(self):
        return self.velocity.get_speed()

    # returns direction in radians
    def get_direction(self):
        return self.velocity.get_direction()
    
    def add_x_y(self, pixels_x, pixels_y):
        self.position.add_x_y(pixels_x, pixels_y)
        self.update_rect()

    # returns mirrored angle in radians
    def calc_mirror_angle(self, minuend):
        return self.velocity.calc_mirror_angle(minuend)
    
    def set_velocity(self, dx, dy):
        self.velocity.set_velocity(dx, dy)

    def set_velocity_direction(self, speed, direction):
        self.velocity.set_velocity_direction(speed, direction)

    def set_speed(self, speed):
        self.velocity.set_speed(speed)

    # updates velocity based on new direction given in radians
    def update_velocity(self, angle_radians):
        self.velocity.update_velocity(angle_radians)
    
    def update_velocity_degrees(self, angle_degrees):
        self.velocity.update_velocity_degrees(angle_degrees)

    # rect.center must contain current position for collision detection
    def update_rect(self):
        self.rect.center = self.get_position()

    def draw_field_obj(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.color, self.get_position(), self.radius) 

    """ boundary-checking methods """

    def hit_top(self):
        return self.get_y() - self.radius <= 0
    
    def hit_bottom(self):
        return self.get_y() + self.radius >= SCREEN_HEIGHT
    
    def hit_left(self):
        return self.get_x() - self.radius <= 0

    def hit_right(self):
        return self.get_x() + self.radius >= SCREEN_WIDTH
    
    def hit_midfield(self):
        # check from left side of field
        if self.get_color() == RED:
            return self.get_x() + self.get_radius() >= SCREEN_WIDTH // 2
        # check from right side of field
        else:
            return self.get_x() + self.get_radius() <= SCREEN_WIDTH // 2
    
    def hit_top_bottom(self):
        if self.hit_top() or self.hit_bottom():
            return True
        return False
        
    def hit_left_right(self):
        if self.hit_left() or self.hit_right():
            return True
        return False