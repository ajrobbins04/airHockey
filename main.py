# import and initialize PyGame
import pygame
pygame.init()

# measured in pixels
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

# sets up game window w/600 px height and 1200px width
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

GREEN = (199, 214, 146)
RED = (255,0,0)
BLUE = (0,0,205)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

from fieldObject.fieldObject import FieldObject

def createPaddleRed():

    quarterWidth = SCREEN_WIDTH / 4
    pixelsX = quarterWidth
    pixelsY = SCREEN_HEIGHT / 2
    radius = 40

    return FieldObject("red", pixelsX, pixelsY, radius)

def createPaddleBlue():

    quarterWidth = SCREEN_WIDTH / 4
    pixelsX = quarterWidth * 3
    pixelsY = SCREEN_HEIGHT / 2
    radius = 40
    return FieldObject("blue", pixelsX, pixelsY, radius)

def createPuck():

    quarterWidth = SCREEN_WIDTH / 4
    pixelsX = quarterWidth * 2
    pixelsY = SCREEN_HEIGHT / 2
    radius = 30
    return FieldObject(BLACK, pixelsX, pixelsY, radius)

paddleRed = createPaddleRed()
paddleBlue = createPaddleBlue()
puck = createPuck()

# import keys to handle events
from pygame.locals import(
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_w,
    K_s,
    K_a,
    K_d,
    K_SPACE,
    K_ESCAPE,
    KEYDOWN,
    QUIT,     # triggered when user closes window
)

def gameLoop(paddleRed: FieldObject, paddleBlue: FieldObject, puck: FieldObject):

    running = True

    while running:

        # access list of active events in the queue
        for event in pygame.event.get():

            # returns a dictionary of the keys that were pressed
            keys = pygame.key.get_pressed()

            # true whenever user hits a key
            if event.type == KEYDOWN:
                if keys[K_ESCAPE]:
                    running = False
                elif keys[K_SPACE]:
                    pause = True
                else:
                    updateField(keys)
            elif event.type == QUIT:
                running = False

        drawField(paddleRed, paddleBlue, puck)

        # updates appearance of the entire screen
        pygame.display.flip()

    # quit once out of the game loop    
    pygame.quit()

def updateField(keys):
    moveUp_1 = False 
    moveDown_1 = False
    moveLeft_1 = False
    moveRight_1 = False
    moveUp_2 = False
    moveDown_2 = False
    moveLeft_2 = False
    moveRight_2 = False
    pause = False
    if keys[K_UP]:
        moveUp_1 = True
    if keys[K_DOWN]:
        moveDown_1 = True
    if keys[K_LEFT]:
        moveLeft_1 = True
    if keys[K_RIGHT]:
        moveRight_1 = True
    if keys[K_w]:
        moveUp_2 = True
    if keys[K_s]:
        moveDown_2 = True
    if keys[K_a]:
        moveLeft_2 = True
    if keys[K_d]:
        moveRight_2 = True

def drawField(paddleRed: FieldObject, paddleBlue: FieldObject, puck: FieldObject):
        
        # create a green playing field
        screen.fill(GREEN)
        
        pygame.draw.rect(screen, WHITE, (15, 15, SCREEN_WIDTH - 30, SCREEN_HEIGHT - 30), 2)  # outer boundary
        pygame.draw.line(screen, WHITE, (SCREEN_WIDTH // 2, 15), (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 15), 2)  # center line
        pygame.draw.circle(screen, WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 100, 2)  # center circle

        pygame.draw.circle(screen, paddleRed.getColor(), paddleRed.pos.getPosition(), paddleRed.getRadius())    # red paddle
        pygame.draw.circle(screen, paddleBlue.getColor(), paddleBlue.pos.getPosition(), paddleBlue.getRadius()) # blue paddle
        pygame.draw.circle(screen, puck.getColor(), puck.pos.getPosition(), puck.getRadius())                   # hockey puck

gameLoop(paddleRed, paddleBlue, puck)
