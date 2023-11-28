import pygame
pygame.init()

from paddle.paddle import Paddle
from puck.puck import Puck
from constants.constants import *

# import pressed_keys to handle events
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
        self.blueKeys = {K_UP, K_DOWN, K_LEFT, K_RIGHT}
        self.redKeys = {K_w, K_s, K_a, K_d}
        self.clock = pygame.time.Clock()

 
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
    
    def update(self, pressed_keys: pygame.key):
       
        frame_rate = self.clock.tick(60)
        time_passed = frame_rate/1000

        self.puck.move(time_passed)

        if pressed_keys[K_UP]:
            self.paddleBlue.update_position(0, -1)  # blue moves up
        if pressed_keys[K_DOWN]:
            self.paddleBlue.update_position(0, 1)   # blue moves down
        if pressed_keys[K_LEFT]:
            self.paddleBlue.update_position(-1, 0)  # blue moves left
        if pressed_keys[K_RIGHT]:
            self.paddleBlue.update_position(1, 0)   # blue moves right
        if pressed_keys[K_w]:
            self.paddleRed.update_position(0, -1)   # red moves up
        if pressed_keys[K_s]:
            self.paddleRed.update_position(0, 1)    # red moves down
        if pressed_keys[K_a]:
            self.paddleRed.update_position(-1, 0)   # red moves left
        if pressed_keys[K_d]:
            self.paddleRed.update_position(1, 0)    # red moves right

        self.check_paddle_boundaries()
        self.check_puck_boundaries()

        self.paddleRed.track_movement()
        self.paddleBlue.track_movement()

        self.check_collisions()
      
    
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

    def check_puck_boundaries(self):

        if self.puck.get_y() + self.puck.get_radius() > SCREEN_HEIGHT:   # hit bottom of field
            self.puck.bounce_off_boundary(360)
        elif self.puck.get_y() - self.puck.get_radius() < 0: # hit top of field
            self.puck.bounce_off_boundary(360)
        elif self.puck.get_x() - self.puck.get_radius() < 0:   # hit left side of field
            self.puck.bounce_off_boundary(180)
        elif self.puck.get_x() + self.puck.get_radius() > SCREEN_WIDTH:  # hit right side of field
            self.puck.bounce_off_boundary(180)

    def check_paddle_boundaries(self):
        
        # Check if paddleRed has hit the bottom boundary. If so, assign it that position.
        if self.paddleRed.get_y() + self.paddleRed.get_radius() > SCREEN_HEIGHT:
            self.paddleRed.pos.set_y(SCREEN_HEIGHT - self.paddleRed.get_radius())
            self.paddleRed.end_track_movement() # the paddle has stopped

        # Check if paddleRed has hit the top boundary. If so, assign it that position.
        elif self.paddleRed.get_y() - self.paddleRed.get_radius() < 0:
            self.paddleRed.pos.set_y(0 + self.paddleRed.get_radius())
            self.paddleRed.end_track_movement()

        # Check if paddleRed has hit the far left boundary. If so, assign it that position.
        if self.paddleRed.get_x() - self.paddleRed.get_radius() < 0:
            self.paddleRed.pos.set_x(0 + self.paddleRed.get_radius())
            self.paddleRed.end_track_movement()

        # Check if paddleRed has hit the midpoint of the field. If so, assign it that position.
        elif self.paddleRed.get_x() + self.paddleRed.get_radius() > SCREEN_WIDTH // 2:
            self.paddleRed.pos.set_x((SCREEN_WIDTH // 2) - self.paddleRed.get_radius())
            self.paddleRed.end_track_movement()

        # Check if paddleBlue has hit the bottom boundary. If so, assign it that position.
        if self.paddleBlue.get_y() + self.paddleBlue.get_radius() > SCREEN_HEIGHT:
            self.paddleBlue.pos.set_y(SCREEN_HEIGHT - self.paddleBlue.get_radius())
            self.paddleBlue.end_track_movement()

        # Check if paddleBlue has hit the top boundary. If so, assign it that position.
        elif self.paddleBlue.get_y() - self.paddleBlue.get_radius() < 0:
            self.paddleBlue.pos.set_y(0 + self.paddleBlue.get_radius())
            self.paddleBlue.end_track_movement()

        # Check if paddleBlue has hit the far right boundary. If so, assign it that position.
        if self.paddleBlue.get_x() + self.paddleBlue.get_radius() > SCREEN_WIDTH:
            self.paddleBlue.pos.set_x(SCREEN_WIDTH - self.paddleBlue.get_radius())
            self.paddleBlue.end_track_movement()

        # Check if paddleBlue has hit the midpoint of the field. If so, assign it that position.
        elif self.paddleBlue.get_x() - self.paddleBlue.get_radius() < SCREEN_WIDTH // 2:
            self.paddleBlue.pos.set_x((SCREEN_WIDTH // 2) + self.paddleBlue.get_radius())
            self.paddleBlue.end_track_movement()
