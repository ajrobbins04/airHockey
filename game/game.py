import pygame
pygame.init()

from paddle.paddle import Paddle
from puck.puck import Puck

# measured in pixels
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 700

RED = (255,0,0)
BLUE = (0,0,205)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# import keys to handle events
from pygame.locals import(
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_w,
    K_s,
    K_a,
    K_d
)

class Game:
    def __init__(self):
        self.paddleRed = self._create_paddle_red()
        self.paddleBlue = self._create_paddle_blue()
        self.puck = self._create_puck()
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

 
    def _create_paddle_red(self):

        quarterWidth = SCREEN_WIDTH / 4
        pixelsX = quarterWidth
        pixelsY = SCREEN_HEIGHT / 2
        radius = 40

        return Paddle(RED, pixelsX, pixelsY, radius)

    def _create_paddle_blue(self):

        quarterWidth = SCREEN_WIDTH / 4
        pixelsX = quarterWidth * 3
        pixelsY = SCREEN_HEIGHT / 2
        radius = 40
        return Paddle(BLUE, pixelsX, pixelsY, radius)

    def _create_puck(self):

        quarterWidth = SCREEN_WIDTH / 4
        pixelsX = quarterWidth * 2
        pixelsY = SCREEN_HEIGHT / 2
        radius = 30
        return Puck(BLACK, pixelsX, pixelsY, radius)
    
    def updateField(self, keys: pygame.key):

        self.puck.update()

        redPrevPos = self.paddleRed.getPosition()
        bluePrevPos = self.paddleBlue.getPosition()

        if keys[K_UP]:
            self.paddleBlue.updatePosition(0, -1)  # blue moves up
        if keys[K_DOWN]:
            self.paddleBlue.updatePosition(0, 1)   # blue moves down
        if keys[K_LEFT]:
            self.paddleBlue.updatePosition(-1, 0)  # blue moves left
        if keys[K_RIGHT]:
            self.paddleBlue.updatePosition(1, 0)   # blue moves right
        if keys[K_w]:
            self.paddleRed.updatePosition(0, -1)   # red moves up
        if keys[K_s]:
            self.paddleRed.updatePosition(0, 1)    # red moves down
        if keys[K_a]:
            self.paddleRed.updatePosition(-1, 0)   # red moves left
        if keys[K_d]:
            self.paddleRed.updatePosition(1, 0)    # red moves right

        self.check_paddle_boundaries()
        self.check_puck_boundaries()

        self.paddleRed.set_is_moving(redPrevPos)
        self.paddleBlue.set_is_moving(bluePrevPos)
        
        if pygame.sprite.collide_circle(self.paddleRed, self.puck):
            if self.paddleRed.is_moving():
                print("red is moving")
                self.puck.velocity.setDX(self.puck.velocity.getDX() * -1)
                self.puck.velocity.setDY(self.puck.velocity.getDY() * -1)
            else:
                print("red is stationary")
                self.puck.velocity.setDX(self.puck.velocity.getDX() * -1)
                self.puck.velocity.setDY(self.puck.velocity.getDY() * -1)
        
        if pygame.sprite.collide_circle(self.paddleBlue, self.puck):      
            if self.paddleBlue.is_moving():
                print("blue is moving")
                self.puck.velocity.setDX(self.puck.velocity.getDX() * -1)
                self.puck.velocity.setDY(self.puck.velocity.getDY() * -1)
            else:
                print("blue is stationary")
                self.puck.velocity.setDX(self.puck.velocity.getDX() * -1)
                self.puck.velocity.setDY(self.puck.velocity.getDY() * -1)

    
    def drawField(self):
        
        # create a green playing field
        self.screen.fill(WHITE)
        
        pygame.draw.rect(self.screen, BLACK, (3, 3, SCREEN_WIDTH - 6, SCREEN_HEIGHT - 6), 2)                     # outer boundary
        pygame.draw.line(self.screen, BLACK, (SCREEN_WIDTH // 2, 5), (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 3), 2)  # center line
        pygame.draw.circle(self.screen, BLACK, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 100, 2)                  # center circle

        # goal box dimensions
        box_width = 150
        box_height = 300

        # left goal box
        pygame.draw.rect(self.screen, BLACK, (0, (SCREEN_HEIGHT - box_height) // 2, box_width, box_height), 2) 
        pygame.draw.line(self.screen, BLACK, (0, (SCREEN_HEIGHT - box_height) // 2), (0, ((SCREEN_HEIGHT - box_height) // 2)* 2.5), 6) 

        # right goal box
        pygame.draw.rect(self.screen, BLACK, (SCREEN_WIDTH - box_width, (SCREEN_HEIGHT - box_height) // 2, box_width, box_height), 2)  
        pygame.draw.line(self.screen, BLACK, (SCREEN_WIDTH - 2, (SCREEN_HEIGHT - box_height) // 2), (SCREEN_WIDTH - 2, ((SCREEN_HEIGHT - box_height) // 2) + box_height), 6) 

        # a red paddle, a blue paddle, and a black self.puck
        self.paddleRed.draw_field_obj(self.screen)
        self.paddleBlue.draw_field_obj(self.screen)
        self.puck.draw_field_obj(self.screen)

    def check_puck_boundaries(self):

        if self.puck.getPosY() + self.puck.getRadius() > SCREEN_HEIGHT:   # hit bottom of field
            self.puck.bounce(360)
        elif self.puck.getPosY() - self.puck.getRadius() < 0: # hit top of field
            self.puck.bounce(360)
        elif self.puck.getPosX() - self.puck.getRadius() < 0:   # hit left side of field
            self.puck.bounce(180)
        elif self.puck.getPosX() + self.puck.getRadius() > SCREEN_WIDTH:  # hit right side of field
            self.puck.bounce(180)

    def check_paddle_boundaries(self):
        
        # don't let self.paddleRed go too far up or down
        if self.paddleRed.getPosY() + self.paddleRed.getRadius() > SCREEN_HEIGHT:
            self.paddleRed.pos.setY(SCREEN_HEIGHT - self.paddleRed.getRadius())
        elif self.paddleRed.getPosY() - self.paddleRed.getRadius() < 0:
            self.paddleRed.pos.setY(0 + self.paddleRed.getRadius())

        # don't let self.paddleRed got too far to the left, or past the midpoint of the screen
        if self.paddleRed.getPosX() - self.paddleRed.getRadius() < 0:
            self.paddleRed.pos.setX(0 + self.paddleRed.getRadius())
        elif self.paddleRed.getPosX() + self.paddleRed.getRadius() > SCREEN_WIDTH // 2:
            self.paddleRed.pos.setX((SCREEN_WIDTH // 2) - self.paddleRed.getRadius())

        # don't let self.paddleBlue go too far up or down
        if self.paddleBlue.getPosY() + self.paddleBlue.getRadius() > SCREEN_HEIGHT:
            self.paddleBlue.pos.setY(SCREEN_HEIGHT - self.paddleBlue.getRadius())
        elif self.paddleBlue.getPosY() - self.paddleBlue.getRadius() < 0:
            self.paddleBlue.pos.setY(0 + self.paddleBlue.getRadius())

        # don't let self.paddleBlue got too far to the right, or past the midpoint of the screen
        if self.paddleBlue.getPosX() + self.paddleBlue.getRadius() > SCREEN_WIDTH:
            self.paddleBlue.pos.setX(SCREEN_WIDTH - self.paddleBlue.getRadius())
        elif self.paddleBlue.getPosX() - self.paddleBlue.getRadius() < SCREEN_WIDTH // 2:
            self.paddleBlue.pos.setX((SCREEN_WIDTH // 2) + self.paddleBlue.getRadius())
