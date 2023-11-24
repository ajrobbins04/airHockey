import pygame
pygame.init()


from position.position import Position

# Define a Player object by extending pygame's Sprite
# The surface drawn on the screen is now an attribute of 'player'
class FieldObject(pygame.sprite.Sprite):
    def __init__(self, color, pixels_x, pixels_y, radius):

        # inherits from Sprite 
        super(FieldObject, self).__init__()
        
        # include radius b/c all field objects are circles
        self.radius = radius

        # surface size is twice the size of the radius
        surface_size = radius * 2
        self.surface = pygame.Surface((surface_size, surface_size))

        # include rect to use its collision detection methods
        self.rect = self.surface.get_rect(center=(pixels_x, pixels_y))

        # red or blue for paddles, and black for puck
        self.color = color

        # the position is the circles center
        self.pos = Position(pixels_x, pixels_y)
        
    def get_surface(self):
        return self.surface

    def get_color(self):
        return self.color
    
    def get_radius(self):
        return self.radius
    
    def get_x(self):
        return self.pos.get_x()
    
    def get_y(self):
        return self.pos.get_y()
    
    def get_position(self):
        return self.pos.get_position()
    
    def update_position(self, pixels_x, pixels_y):
        self.pos.update_pos(pixels_x, pixels_y)
        self.update_rect()
    
    # rect.center must contain current position of
    # sprite for collision detection
    def update_rect(self):
        self.rect.center = self.get_position()

    def draw_field_obj(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.get_color(), self.get_position(), self.get_radius())  