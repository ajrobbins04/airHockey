import pygame
pygame.init()

from paddle.paddle import Paddle
from puck.puck import Puck
from constants.constants import *

# import pressed_keys to handle events
from pygame.locals import (
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
        self.clock = pygame.time.Clock()

 
    def _create_paddle_red(self):

        quarter_width = SCREEN_WIDTH / 4
        pixels_x = quarter_width
        pixels_y = SCREEN_HEIGHT / 2

        return Paddle(RED, pixels_x, pixels_y, PADDLE_RADIUS, PADDLE_MASS, PADDLE_SPEED, 0) # set initial angle to 0 degrees

    def _create_paddle_blue(self):

        quarter_width = SCREEN_WIDTH / 4
        pixels_x = quarter_width * 3
        pixels_y = SCREEN_HEIGHT / 2
        return Paddle(BLUE, pixels_x, pixels_y, PADDLE_RADIUS, PADDLE_MASS, PADDLE_SPEED, 0) 

    def _create_puck(self):

        quarter_width = SCREEN_WIDTH / 4
        pixels_x = quarter_width * 2
        pixels_y = SCREEN_HEIGHT / 2
        return Puck(BLACK, pixels_x, pixels_y, PUCK_RADIUS, PUCK_MASS, PUCK_START_SPEED, None) # angle is None b/c it gets assigned randomly
    
    def update(self, pressed_keys: pygame.key):
       
        frame_rate = self.clock.tick(45)
        time_passed: float = frame_rate/1000.0

        # all move methods will check for crossed boundaries internally
        self.puck.move(time_passed)
        self.paddleBlue.move(pressed_keys, time_passed)
        self.paddleRed.move(pressed_keys, time_passed)

        if pygame.sprite.collide_circle(self.paddleRed, self.puck):
            self.puck.resolve_collision(self.paddleRed)
        elif pygame.sprite.collide_circle(self.paddleBlue, self.puck):  
            self.puck.resolve_collision(self.paddleBlue)
      
    
    def check_collisions(self):
          
        if pygame.sprite.collide_circle(self.paddleRed, self.puck):
            if self.paddleRed.is_moving() == True:
                self.puck.resolve_collision(self.paddleRed)
            else:
                self.puck.bounce_off_paddle()
        
        elif pygame.sprite.collide_circle(self.paddleBlue, self.puck):      
            if self.paddleBlue.is_moving() == True:
                self.puck.resolve_collision(self.paddleBlue)
            else:
                self.puck.bounce_off_paddle()

    def draw_field(self):
        
        # create a green playing field
        self.screen.fill(WHITE)
        
        pygame.draw.rect(self.screen, BLACK, (3, 3, SCREEN_WIDTH - 6, SCREEN_HEIGHT - 6), 2)                     # outer boundary
        pygame.draw.line(self.screen, BLACK, (SCREEN_WIDTH // 2, 5), (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 3), 2)  # center line
        pygame.draw.circle(self.screen, BLACK, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 100, 2)                  # center circle

        # left goal box
        pygame.draw.rect(self.screen, BLACK, (0, (SCREEN_HEIGHT - BOX_HEIGHT) // 2, BOX_WIDTH, BOX_HEIGHT), 2) 
        pygame.draw.line(self.screen, BLACK, (0, (SCREEN_HEIGHT - BOX_HEIGHT) // 2), (0, ((SCREEN_HEIGHT - BOX_HEIGHT) // 2)* 2.5), 6) 

        # right goal box
        pygame.draw.rect(self.screen, BLACK, (SCREEN_WIDTH - BOX_WIDTH, (SCREEN_HEIGHT - BOX_HEIGHT) // 2, BOX_WIDTH, BOX_HEIGHT), 2)  
        pygame.draw.line(self.screen, BLACK, (SCREEN_WIDTH - 2, (SCREEN_HEIGHT - BOX_HEIGHT) // 2), (SCREEN_WIDTH - 2, ((SCREEN_HEIGHT - BOX_HEIGHT) // 2) + BOX_HEIGHT), 6) 

        # a red paddle, a blue paddle, and a black self.puck
        self.paddleRed.draw_field_obj(self.screen)
        self.paddleBlue.draw_field_obj(self.screen)
        self.puck.draw_field_obj(self.screen)

