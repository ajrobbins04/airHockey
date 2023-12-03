import pygame
pygame.init()

from constants.constants import *

# import keys to handle events
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_ESCAPE,
    KEYDOWN,
    K_RETURN,
    K_KP_ENTER,
    QUIT,     # triggered when user closes window
)

class Menu:
    def __init__(self):
        self.state = "easy"
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

        # every component shown on the menu screen
        self.heading = pygame.Vector2((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        self.cursor = pygame.Vector2(self.heading.x - 200, self.heading.y + 100)
        self.level_easy = pygame.Vector2(self.heading.x, self.heading.y + 100)
        self.level_medium = pygame.Vector2(self.heading.x, self.heading.y + 200)
        self.level_hard = pygame.Vector2(self.heading.x, self.heading.y + 300)
        self.exit = pygame.Vector2(self.heading.x, self.heading.y + 400)

    def get_state(self):
        return self.state
    
    def draw_menu(self):
        self.screen.fill(BLACK)

        # use default font w/a font size of 45
        font = pygame.font.Font('fonts/8bit_wonder/8-BITWONDER.TTF', 45)
        heading = font.render('Select a level', True, WHITE)
        cursor = font.render('X', True, WHITE)
        easy = font.render('Easy', True, WHITE)
        medium = font.render('Medium', True, WHITE)
        hard = font.render('Hard', True, WHITE)
        exit = font.render('Exit Game', True, WHITE)

        heading_pos = heading.get_rect()
        cursor_pos = cursor.get_rect()
        easy_pos = easy.get_rect()
        medium_pos = medium.get_rect()
        hard_pos = hard.get_rect()
        exit_pos = exit.get_rect()

        # Set the center of the text rect
        heading_pos.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        cursor_pos.center = self.cursor
        easy_pos.center = self.level_easy
        medium_pos.center = self.level_medium
        hard_pos.center = self.level_hard
        exit_pos.center = self.exit

        # Draw the text onto the screen
        self.screen.blit(heading, heading_pos)
        self.screen.blit(cursor, cursor_pos)
        self.screen.blit(easy, easy_pos)
        self.screen.blit(medium, medium_pos)
        self.screen.blit(hard, hard_pos)

        # Update the display
        pygame.display.flip()

    def run_menu_loop(self):

        pygame.display.set_caption('Air Hockey: Select a Level')
        moving = True

        while moving:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    # moving down menu options 
                    if event.key == K_DOWN:
                        if self.state == "easy":
                            self.cursor.y = self.level_medium.y
                            self.state = "medium"
                        elif self.state == "medium":
                            self.cursor.y = self.level_hard.y
                            self.state = "hard"
                        elif self.state == "hard":
                            self.cursor.y = self.exit.y
                            self.state = "exit"
                        # wraps back up to top of menu
                        elif self.state == "exit":
                            self.cursor.y = self.level_easy.y
                            self.state = "easy"
                    # moving up menu options
                    elif event.key == K_UP:
                        # wraps back down to bottom of menu
                        if self.state == "easy":
                            self.cursor.y = self.exit.y
                            self.state = "exit"
                        elif self.state == "medium":
                            self.cursor.y = self.level_easy.y
                            self.state = "easy"
                        elif self.state == "hard":
                            self.cursor.y = self.level_medium.y
                            self.state = "medium"
                        elif self.state == "exit":
                            self.cursor.y = self.level_hard.y
                            self.state = "hard"
                    elif event.key == K_RETURN:
                        moving = False

                elif event.type == QUIT:
                    moving = False
                    self.state = "exit"
                
            self.draw_menu() 