import pygame
pygame.init()

from paddle.paddle import Paddle
from puck.puck import Puck
from menu.menu import MainMenu
from constants.constants import *

# import pressed_keys to handle events
from pygame.locals import (
    K_ESCAPE,
    K_BACKSPACE,
    KEYDOWN,
    KEYUP,
    QUIT,   
)

class Game:
    def __init__(self, screen: pygame.display, display: pygame.Surface):
        
        # program is running, but game isn't being played yet
        self.running = True
        self.playing = False
        self.main_menu = MainMenu(screen)
     
        self.screen = screen
        self.display = display

        # no need to instantiate until user opts to start game
        self.puck = None
        self.paddleRed = None
        self.paddleBlue = None
        self.clock = None

    def start_game(self):
        # user either selected a level or easy is used by default
        level = self.main_menu.levels_menu.get_level()
        self.puck = self.create_puck(level)
        self.paddleRed = self.create_paddle_red()
        self.paddleBlue = self.create_paddle_blue()
        self.clock = pygame.time.Clock()

    def create_paddle_red(self):

        quarter_width = SCREEN_WIDTH / 4
        pixels_x = quarter_width
        pixels_y = SCREEN_HEIGHT / 2

        return Paddle(RED, pixels_x, pixels_y, PADDLE_RADIUS, PADDLE_MASS, PADDLE_SPEED, 0) # set initial angle to 0 degrees

    def create_paddle_blue(self):

        quarter_width = SCREEN_WIDTH / 4
        pixels_x = quarter_width * 3
        pixels_y = SCREEN_HEIGHT / 2
        return Paddle(BLUE, pixels_x, pixels_y, PADDLE_RADIUS, PADDLE_MASS, PADDLE_SPEED, 0) 

    def create_puck(self, level):

        quarter_width = SCREEN_WIDTH / 4
        pixels_x = quarter_width * 2
        pixels_y = SCREEN_HEIGHT / 2

        if level == "easy":
            # angle is None b/c it gets assigned randomly
            return Puck(BLACK, pixels_x, pixels_y, PUCK_RADIUS, PUCK_MASS, PUCK_START_SPEED, None, PUCK_MAX_SPEED_EASY) 
        elif level == "medium":
            return Puck(BLACK, pixels_x, pixels_y, PUCK_RADIUS, PUCK_MASS, PUCK_START_SPEED, None, PUCK_MAX_SPEED_MEDIUM) 
        elif level == "hard":
            return Puck(BLACK, pixels_x, pixels_y, PUCK_RADIUS, PUCK_MASS, PUCK_START_SPEED, None, PUCK_MAX_SPEED_HARD) 


    def check_events(self):

        # access list of active events in the queue
        for event in pygame.event.get():
            # whole program has ended
            if event.type == QUIT:
                self.running = False
                self.playing = False

            # true whenever user hits a key
            if event.type == KEYDOWN:
                # go back to main menu
                if event.key == K_BACKSPACE:
                    self.playing = False
                    self.main_menu.run_display = True
             
                # whole program has ended
                elif event.key == K_ESCAPE:
                    self.running = False
                    self.playing = False
                # either one or both paddles have begun moving
                elif event.key in self.paddleBlue.moves.values():
                    self.paddleBlue.start_moving()
                elif event.key in self.paddleRed.moves.values():
                    self.paddleRed.start_moving()

            # either one or both paddles have stopped moving
            elif event.type == KEYUP:
                if event.key in self.paddleBlue.moves.values():
                    self.paddleBlue.stop_moving()
                elif event.key in self.paddleRed.moves.values():
                    self.paddleRed.stop_moving()

        # returns a dictionary of the keys that were pressed
        pressed_keys = pygame.key.get_pressed()
        return pressed_keys

    def run_game(self):

        self.running = True

        while self.running:
            self.main_menu.display_main()
            self.playing = self.main_menu.get_playing()
            self.running = self.main_menu.get_running()
            if self.playing:
                self.start_game()
                self.play_game()

    def play_game(self):

        self.playing = True

        while self.playing:

            pygame.display.set_caption('Air Hockey')

            # returns a dictionary of the keys that were pressed
            pressed_keys = self.check_events()

            # update field based on keys pressed and draw the resulting field
            self.update(pressed_keys)
            self.draw_field()

            # updates appearance of the entire screen
            pygame.display.flip()


    def update(self, pressed_keys: pygame.key):
       
        frame_rate = self.clock.tick(40)
        time_passed: float = frame_rate/1000.0

        # all move methods will check for crossed boundaries internally
        self.puck.move(time_passed)
        self.paddleBlue.move(pressed_keys, time_passed)
        self.paddleRed.move(pressed_keys, time_passed)

        self.check_collisions()
    
    def check_collisions(self):

        if pygame.sprite.collide_circle(self.paddleRed, self.puck):
            self.puck.resolve_collision(self.paddleRed)

            # crossed_boundaries corrects position internally.
            # only rect.center needs to be updated afterwards.
            if self.puck.crossed_boundaries() == True:
                self.puck.update_rect()
            if self.paddleRed.crossed_boundaries() == True:
                self.paddleRed.update_rect() 

        elif pygame.sprite.collide_circle(self.paddleBlue, self.puck):  
            self.puck.resolve_collision(self.paddleBlue)
            if self.puck.crossed_boundaries() == True:
                self.puck.update_rect()
            if self.paddleBlue.crossed_boundaries() == True:
                self.paddleBlue.update_rect() 
           

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

    
