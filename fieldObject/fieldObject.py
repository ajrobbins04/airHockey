import pygame
pygame.init()


from position.position import Position

# Define a Player object by extending pygame's Sprite
# The surface drawn on the screen is now an attribute of 'player'
class FieldObject(pygame.sprite.Sprite):
    def __init__(self, color, pixelsX, pixelsY, radius):

        # inherits from Sprite 
        super(FieldObject, self).__init__()
        
        # include radius b/c all field objects are circles
        self.radius = radius

        # surface size is twice the size of the radius
        surfaceSize = radius * 2
        self.surface = pygame.Surface((surfaceSize, surfaceSize))

        # include rect to use its collision detection methods
        self.rect = self.surface.get_rect(center=(pixelsX, pixelsY))

        # red or blue for paddles, and black for puck
        self.color = color

        # the position is the circles center
        self.pos = Position(pixelsX, pixelsY)
        
    def getSurface(self):
        return self.surface

    def getColor(self):
        return self.color
    
    def getRadius(self):
        return self.radius
    
    def getPosX(self):
        return self.pos.getX()
    
    def getPosY(self):
        return self.pos.getY()
    
    def getPosition(self):
        return self.pos.getPosition()
    
    def updatePosition(self, pixelsX, pixelsY):
        self.pos.updatePos(pixelsX, pixelsY)
        self.updateRect()
    
    # rect.center must contain current position of
    # sprite for collision detection
    def updateRect(self):
        self.rect.center = self.getPosition()

    def draw_field_obj(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.getColor(), self.pos.getPosition(), self.getRadius())  