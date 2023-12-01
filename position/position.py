import pygame
pygame.init()

class Position:
    def __init__(self, pixels_x, pixels_y):
        self.position = pygame.math.Vector2(pixels_x, pixels_y)

    def get_x(self):
        return self.position.x
    
    def get_y(self):
        return self.position.y
    
    # returns whole position vector
    def get_position(self):
        return self.position
    
    def set_x(self, pixels_x):
        self.position.x = pixels_x

    def set_y(self, pixels_y):
        self.position.y = pixels_y
    
    # update position by re-setting it
    def set_x_y(self, pixels_x, pixels_y):
        self.set_x(pixels_x)
        self.set_y(pixels_y)

    def add_x(self, pixels_x):
        self.position.x += pixels_x
    
    def add_y(self, pixels_y):
        self.position.y += pixels_y
        
    # update position by adding to it
    def add_x_y(self, pixels_x, pixels_y):
        self.position.x += pixels_x
        self.position.y += pixels_y
     