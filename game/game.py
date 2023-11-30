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

        return Paddle(RED, pixels_x, pixels_y, PADDLE_RADIUS, PADDLE_MASS, PADDLE_SPEED, PADDLE_BOUNCE) 

    def _create_paddle_blue(self):

        quarter_width = SCREEN_WIDTH / 4
        pixels_x = quarter_width * 3
        pixels_y = SCREEN_HEIGHT / 2
        return Paddle(BLUE, pixels_x, pixels_y, PADDLE_RADIUS, PADDLE_MASS, PADDLE_SPEED, PADDLE_BOUNCE) 

    def _create_puck(self):

        quarter_width = SCREEN_WIDTH / 4
        pixels_x = quarter_width * 2
        pixels_y = SCREEN_HEIGHT / 2
        return Puck(BLACK, pixels_x, pixels_y, PUCK_RADIUS, PUCK_MASS, PUCK_START_SPEED, PUCK_BOUNCE) 
    
    def update(self, pressed_keys: pygame.key):
       
        frame_rate = self.clock.tick(60)
        time_passed: float = frame_rate/1000.0

        self.puck.move(time_passed)

        self.check_paddle_boundaries()

        self.paddleBlue.move(pressed_keys, time_passed)
        self.paddleRed.move(pressed_keys, time_passed)

        if pygame.sprite.collide_circle(self.paddleRed, self.puck):
            self.puck.resolve_collision(self.paddleRed)
        elif pygame.sprite.collide_circle(self.paddleBlue, self.puck):  
            self.puck.resolve_collision(self.paddleBlue)
      
    
    def check_collisions(self):
          
        if pygame.sprite.collide_circle(self.paddleRed, self.puck):
            if self.paddleRed.is_moving() == True:
                self.puck.bounce_off_moving_paddle(self.paddleRed)
            else:
                self.puck.bounce_off_paddle()
        
        elif pygame.sprite.collide_circle(self.paddleBlue, self.puck):      
            if self.paddleBlue.is_moving() == True:
                self.puck.bounce_off_moving_paddle(self.paddleBlue)
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


    def check_paddle_boundaries(self):
        
        # Check if paddleRed has hit the bottom boundary. If so, assign it that position.
        if self.paddleRed.get_y() + self.paddleRed.get_radius() >= SCREEN_HEIGHT:
            self.paddleRed.pos.set_y(SCREEN_HEIGHT - self.paddleRed.get_radius())

        # Check if paddleRed has hit the top boundary. If so, assign it that position.
        elif self.paddleRed.get_y() - self.paddleRed.get_radius() <= 0:
            self.paddleRed.pos.set_y(0 + self.paddleRed.get_radius())

        # Check if paddleRed has hit the far left boundary. If so, assign it that position.
        if self.paddleRed.get_x() - self.paddleRed.get_radius() <= 0:
            self.paddleRed.pos.set_x(0 + self.paddleRed.get_radius())

        # Check if paddleRed has hit the midpoint of the field. If so, assign it that position.
        elif self.paddleRed.get_x() + self.paddleRed.get_radius() >= SCREEN_WIDTH // 2:
            self.paddleRed.pos.set_x((SCREEN_WIDTH // 2) - self.paddleRed.get_radius())

        # Check if paddleBlue has hit the bottom boundary. If so, assign it that position.
        if self.paddleBlue.get_y() + self.paddleBlue.get_radius() >= SCREEN_HEIGHT:
            self.paddleBlue.pos.set_y(SCREEN_HEIGHT - self.paddleBlue.get_radius())

        # Check if paddleBlue has hit the top boundary. If so, assign it that position.
        elif self.paddleBlue.get_y() - self.paddleBlue.get_radius() <= 0:
            self.paddleBlue.pos.set_y(0 + self.paddleBlue.get_radius())

        # Check if paddleBlue has hit the far right boundary. If so, assign it that position.
        if self.paddleBlue.get_x() + self.paddleBlue.get_radius() >= SCREEN_WIDTH:
            self.paddleBlue.pos.set_x(SCREEN_WIDTH - self.paddleBlue.get_radius())

        # Check if paddleBlue has hit the midpoint of the field. If so, assign it that position.
        elif self.paddleBlue.get_x() - self.paddleBlue.get_radius() <= SCREEN_WIDTH // 2:
            self.paddleBlue.pos.set_x((SCREEN_WIDTH // 2) + self.paddleBlue.get_radius())
