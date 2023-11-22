import pygame
pygame.init()


from position.position import Position

RED = (255,0,0)
BLUE = (0,0,205)
GREEN = (199, 214, 146)


# Define a Player object by extending pygame's Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, pixelsX, pixelsY):

        # inherits from Sprite 
        super().__init__()
        self.surface = pygame.Surface((80, 80))
        
        self.radius = 40

        if color == "red":
            self.color = RED
        elif color == "blue":
            self.color = BLUE
        else:
            self.color = BLUE

        self.pos = Position(pixelsX, pixelsY)
        
    def getSurface(self):
        return self.surface

    def getColor(self):
        return self.color
    
    def getRadius(self):
        return self.radius

    def getPosition(self):
        return self.pos.getPosition()