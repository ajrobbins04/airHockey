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

        quarter_width = SCREEN_WIDTH / 4
        pixels_x = quarter_width
        pixels_y = SCREEN_HEIGHT / 2
        radius = 40

        return Paddle(RED, pixels_x, pixels_y, radius)

    def _create_paddle_blue(self):

        quarter_width = SCREEN_WIDTH / 4
        pixels_x = quarter_width * 3
        pixels_y = SCREEN_HEIGHT / 2
        radius = 40
        return Paddle(BLUE, pixels_x, pixels_y, radius)

    def _create_puck(self):

        quarter_width = SCREEN_WIDTH / 4
        pixels_x = quarter_width * 2
        pixels_y = SCREEN_HEIGHT / 2
        radius = 30
        return Puck(BLACK, pixels_x, pixels_y, radius)
    
    def update_field(self, keys: pygame.key):

        self.puck.update()

        red_prev_pos = self.paddleRed.get_position()
        blue_prev_pos = self.paddleBlue.get_position()

        if keys[K_UP]:
            self.paddleBlue.update_position(0, -1)  # blue moves up
        if keys[K_DOWN]:
            self.paddleBlue.update_position(0, 1)   # blue moves down
        if keys[K_LEFT]:
            self.paddleBlue.update_position(-1, 0)  # blue moves left
        if keys[K_RIGHT]:
            self.paddleBlue.update_position(1, 0)   # blue moves right
        if keys[K_w]:
            self.paddleRed.update_position(0, -1)   # red moves up
        if keys[K_s]:
            self.paddleRed.update_position(0, 1)    # red moves down
        if keys[K_a]:
            self.paddleRed.update_position(-1, 0)   # red moves left
        if keys[K_d]:
            self.paddleRed.update_position(1, 0)    # red moves right

        self.check_paddle_boundaries()
        self.check_puck_boundaries()

        self.paddleRed.set_is_moving(red_prev_pos)
        self.paddleBlue.set_is_moving(blue_prev_pos)
        
        if pygame.sprite.collide_circle(self.paddleRed, self.puck):
            if self.paddleRed.is_moving():
                print("red is moving")
            else:
                print("red is stationary")
        
        elif pygame.sprite.collide_circle(self.paddleBlue, self.puck):      
            if self.paddleBlue.is_moving():
                print("blue is moving")
            else:
                print("blue is stationary")

    
    def draw_field(self):
        
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

        if self.puck.get_y() + self.puck.get_radius() > SCREEN_HEIGHT:   # hit bottom of field
            self.puck.bounce(360)
        elif self.puck.get_y() - self.puck.get_radius() < 0: # hit top of field
            self.puck.bounce(360)
        elif self.puck.get_x() - self.puck.get_radius() < 0:   # hit left side of field
            self.puck.bounce(180)
        elif self.puck.get_x() + self.puck.get_radius() > SCREEN_WIDTH:  # hit right side of field
            self.puck.bounce(180)

    def check_paddle_boundaries(self):
        
        # don't let self.paddleRed go too far up or down
        if self.paddleRed.get_y() + self.paddleRed.get_radius() > SCREEN_HEIGHT:
            self.paddleRed.pos.set_y(SCREEN_HEIGHT - self.paddleRed.get_radius())
        elif self.paddleRed.get_y() - self.paddleRed.get_radius() < 0:
            self.paddleRed.pos.set_y(0 + self.paddleRed.get_radius())

        # don't let self.paddleRed got too far to the left, or past the midpoint of the screen
        if self.paddleRed.get_x() - self.paddleRed.get_radius() < 0:
            self.paddleRed.pos.set_x(0 + self.paddleRed.get_radius())
        elif self.paddleRed.get_x() + self.paddleRed.get_radius() > SCREEN_WIDTH // 2:
            self.paddleRed.pos.set_x((SCREEN_WIDTH // 2) - self.paddleRed.get_radius())

        # don't let self.paddleBlue go too far up or down
        if self.paddleBlue.get_y() + self.paddleBlue.get_radius() > SCREEN_HEIGHT:
            self.paddleBlue.pos.set_y(SCREEN_HEIGHT - self.paddleBlue.get_radius())
        elif self.paddleBlue.get_y() - self.paddleBlue.get_radius() < 0:
            self.paddleBlue.pos.set_y(0 + self.paddleBlue.get_radius())

        # don't let self.paddleBlue got too far to the right, or past the midpoint of the screen
        if self.paddleBlue.get_x() + self.paddleBlue.get_radius() > SCREEN_WIDTH:
            self.paddleBlue.pos.set_x(SCREEN_WIDTH - self.paddleBlue.get_radius())
        elif self.paddleBlue.get_x() - self.paddleBlue.get_radius() < SCREEN_WIDTH // 2:
            self.paddleBlue.pos.set_x((SCREEN_WIDTH // 2) + self.paddleBlue.get_radius())
