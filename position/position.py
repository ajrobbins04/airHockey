import pygame
pygame.init()

class Position:
    def __init__(self, pixels_x, pixels_y):
        self.position = pygame.math.Vector2(pixels_x, pixels_y)

    def get_x(self):
        return self.position.x
    
    def get_y(self):
        return self.position.y
    
    def add_x(self, pixels_x):
        self.position.x += pixels_x

    def add_y(self, pixels_y):
        self.position.y += pixels_y

    def set_x(self, pixels_x):
        self.position.x = pixels_x

    def set_y(self, pixels_y):
        self.position.y = pixels_y

    def update_pos(self, pixels_x, pixels_y):
        self.add_x(pixels_x)
        self.add_y(pixels_y)

    def get_position(self):
        return self.position
     