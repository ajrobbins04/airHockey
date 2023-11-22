# import and initialize PyGame
import pygame
pygame.init()

# measured in pixels
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 700

# sets up game window w/600 px height and 1200px width
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

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

    return FieldObject(RED, pixelsX, pixelsY, radius)

def createPaddleBlue():

    quarterWidth = SCREEN_WIDTH / 4
    pixelsX = quarterWidth * 3
    pixelsY = SCREEN_HEIGHT / 2
    radius = 40
    return FieldObject(BLUE, pixelsX, pixelsY, radius)

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

            # true whenever user hits a key
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_SPACE:
                    pause = True
                    
            elif event.type == QUIT:
                running = False

        # returns a dictionary of the keys that were pressed
        keys = pygame.key.get_pressed()
        updateField(keys, paddleRed, paddleBlue)
        drawField(paddleRed, paddleBlue, puck)

        # updates appearance of the entire screen
        pygame.display.flip()

    # quit once out of the game loop    
    pygame.quit()

def updateField(keys, paddleRed: FieldObject, paddleBlue: FieldObject):

    if keys[K_UP]:
        paddleBlue.pos.updatePosition(0, -1)  # blue moves up
    if keys[K_DOWN]:
        paddleBlue.pos.updatePosition(0, 1)   # blue moves down
    if keys[K_LEFT]:
        paddleBlue.pos.updatePosition(-1, 0)  # blue moves left
    if keys[K_RIGHT]:
        paddleBlue.pos.updatePosition(1, 0)   # blue moves right
    if keys[K_w]:
        paddleRed.pos.updatePosition(0, -1)   # red moves up
    if keys[K_s]:
        paddleRed.pos.updatePosition(0, 1)    # red moves down
    if keys[K_a]:
        paddleRed.pos.updatePosition(-1, 0)   # red moves left
    if keys[K_d]:
        paddleRed.pos.updatePosition(1, 0)    # red moves right
    checkBoundaries(paddleRed, paddleBlue)

def checkBoundaries(paddleRed: FieldObject, paddleBlue: FieldObject):
    
    # don't let paddleRed go too far up or down
    if paddleRed.getPosY() + paddleRed.getRadius() > SCREEN_HEIGHT:
        paddleRed.pos.setY(SCREEN_HEIGHT - paddleRed.getRadius())
    elif paddleRed.getPosY() - paddleRed.getRadius() < 0:
        paddleRed.pos.setY(0 + paddleRed.getRadius())

    # don't let paddleRed got too far to the left, or past the midpoint of the screen
    if paddleRed.getPosX() - paddleRed.getRadius() < 0:
        paddleRed.pos.setX(0 + paddleRed.getRadius())
    elif paddleRed.getPosX() + paddleRed.getRadius() > SCREEN_WIDTH // 2:
        paddleRed.pos.setX((SCREEN_WIDTH // 2) - paddleRed.getRadius())

    # don't let paddleBlue go too far up or down
    if paddleBlue.getPosY() + paddleBlue.getRadius() > SCREEN_HEIGHT:
        paddleBlue.pos.setY(SCREEN_HEIGHT - paddleBlue.getRadius())
    elif paddleBlue.getPosY() - paddleBlue.getRadius() < 0:
        paddleBlue.pos.setY(0 + paddleBlue.getRadius())

    # don't let paddleBlue got too far to the right, or past the midpoint of the screen
    if paddleBlue.getPosX() + paddleBlue.getRadius() > SCREEN_WIDTH:
        paddleBlue.pos.setX(SCREEN_WIDTH - paddleBlue.getRadius())
    elif paddleBlue.getPosX() - paddleBlue.getRadius() < SCREEN_WIDTH // 2:
        paddleBlue.pos.setX((SCREEN_WIDTH // 2) + paddleBlue.getRadius())

def drawField(paddleRed: FieldObject, paddleBlue: FieldObject, puck: FieldObject):
        
        # create a green playing field
        screen.fill(WHITE)
        
        pygame.draw.rect(screen, BLACK, (3, 3, SCREEN_WIDTH - 6, SCREEN_HEIGHT - 6), 2)                     # outer boundary
        pygame.draw.line(screen, BLACK, (SCREEN_WIDTH // 2, 5), (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 3), 2)  # center line
        pygame.draw.circle(screen, BLACK, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 100, 2)                  # center circle

        # goal boxes
        box_width = 150
        box_height = 300

        # left goal box
        pygame.draw.rect(screen, BLACK, (0, (SCREEN_HEIGHT - box_height) // 2, box_width, box_height), 2) 
        pygame.draw.line(screen, BLACK, (0, (SCREEN_HEIGHT - box_height) // 2), (0, ((SCREEN_HEIGHT - box_height) // 2)* 2.5), 4) 

        # right goal box
        pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - box_width, (SCREEN_HEIGHT - box_height) // 2, box_width, box_height), 2)  
        pygame.draw.line(screen, BLACK, (SCREEN_WIDTH - 2, (SCREEN_HEIGHT - box_height) // 2), (SCREEN_WIDTH - 2, ((SCREEN_HEIGHT - box_height) // 2) + box_height), 4) 

        pygame.draw.circle(screen, paddleRed.getColor(), paddleRed.pos.getPosition(), paddleRed.getRadius())    # red paddle
        pygame.draw.circle(screen, paddleBlue.getColor(), paddleBlue.pos.getPosition(), paddleBlue.getRadius()) # blue paddle
        pygame.draw.circle(screen, puck.getColor(), puck.pos.getPosition(), puck.getRadius())                   # hockey puck

gameLoop(paddleRed, paddleBlue, puck)
