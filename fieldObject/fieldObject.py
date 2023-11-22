import pygame
pygame.init()


from position.position import Position

RED = (255,0,0)
BLUE = (0,0,205)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Define a Player object by extending pygame's Sprite
# The surface drawn on the screen is now an attribute of 'player'
class FieldObject(pygame.sprite.Sprite):
    def __init__(self, color, pixelsX, pixelsY, radius):

        # inherits from Sprite 
        super().__init__()

        # include radius b/c all field objects are circles
        self.radius = radius

        # surface size is twice the size of the radius
        surfaceSize = radius * 2
        self.surface = pygame.Surface((surfaceSize, surfaceSize))

        if color == "red":     # first paddle
            self.color = RED
        elif color == "blue":  # second paddle
            self.color = BLUE
        else:
            self.color = BLACK # hockey puck

        # the position is the circles center
        self.pos = Position(pixelsX, pixelsY)
        
    def getSurface(self):
        return self.surface

    def getColor(self):
        return self.color
    
    def getRadius(self):
        return self.radius

    def getPosition(self):
        return self.pos.getPosition()