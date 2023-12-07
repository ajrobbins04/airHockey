import pygame
pygame.init()

from constants.constants import *
from position.position import Position

# import keys to handle events
from pygame.locals import (
    K_UP,
    K_DOWN,
    KEYDOWN,
    K_RETURN,
    K_BACKSPACE,
    K_ESCAPE,
    QUIT,     # triggered when user closes window
)

class Menu:
    def __init__(self, screen: pygame.display):
        self.screen = screen    # same screen and display dimensions in Game
        self.run_display = True
        self.move_up = False 
        self.move_down = False 
        self.select = False
        self.back = False
        self.quit = False
        self.playing = False # changes in playing get copied by Game

        # the location of the heading for every possible menu
        self.heading = Position(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        # cursor will be 200 px to the left of the menu item
        self.cursor_offset = -200
        # menu items will be spaced 100 px apart on y axis
        self.menu_item = 100
         
    def get_playing(self):
        return self.playing
    
    def check_events(self):
        # access list of active events in the queue
        for event in pygame.event.get():
            # whole program has ended
            if event.type == QUIT:
                self.quit = True
            # true whenever user hits a key
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    self.select = True
                if event.key == K_DOWN:
                    self.move_down = True
                elif event.key == K_UP:
                    self.move_up = True
                elif event.key == K_BACKSPACE:
                    self.back = True
                elif event.key == K_ESCAPE:
                    self.quit = True

    def reset_keys(self):
        self.move_up = False 
        self.move_down = False 
        self.select = False
        self.back = False
        self.quit = False

    def draw_text(self, text, size, position: Position, font, color, display: pygame.Surface):

        font = pygame.font.Font(font, size)
        text_surface = font.render(text, True, color)

        # returns the area that will hold each menu component
        text_rect = text_surface.get_rect()

        # Set the center of the text rect
        text_rect.center = (position.get_x(), position.get_y())

        # Draw the text onto the screen
        display.blit(text_surface, text_rect)

class MainMenu(Menu):
    def __init__(self, screen: pygame.display):
        Menu.__init__(self, screen)
        # starts game by default
        self.state = "start"
        self.start_game = Position(self.heading.get_x(), self.heading.get_y() + self.menu_item)
        self.select_level = Position(self.heading.get_x(), self.heading.get_y() + (self.menu_item * 2))
        self.quit_game = Position(self.heading.get_x(), self.heading.get_y() + (self.menu_item * 3))
        self.levels_menu = LevelsMenu(screen)
        self.cursor_offset = -350
        # place cursor at the first menu item under the heading by default
        self.cursor = Position(self.start_game.get_x() + self.cursor_offset, self.heading.get_y() + self.menu_item)

    def draw_main_menu(self):
        # create a new surface for the menu
        menu_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        menu_surface.fill(BLACK)

        # accepts text, size of text, its position, its font, its color, and the surface as arguments
        self.draw_text('Main Menu', MENU_SIZE, self.heading, MENU_FONT, WHITE, menu_surface)
        self.draw_text('*', MENU_SIZE, self.cursor, MENU_FONT, WHITE, menu_surface)
        self.draw_text('Start Game', MENU_SIZE, self.start_game, MENU_FONT, WHITE, menu_surface)
        self.draw_text('Select a Level', MENU_SIZE, self.select_level, MENU_FONT, WHITE, menu_surface)
        self.draw_text('End Game', MENU_SIZE, self.quit_game, MENU_FONT, WHITE, menu_surface)

        # blit the menu surface onto the main screen
        self.screen.blit(menu_surface, (0, 0))
        pygame.display.flip()

    def move_cursor(self):
        if self.move_down:
            if self.state == "start":
                self.cursor.position.x = self.select_level.get_x() + self.cursor_offset
                self.cursor.position.y = self.heading.get_y() + (self.menu_item * 2) # move to second menu item
                self.state = "select_level"
            elif self.state == "select_level":
                self.cursor.position.x = self.quit_game.get_x() + self.cursor_offset
                self.cursor.position.y = self.heading.get_y() + (self.menu_item * 3) # move to third menu item
                self.state = "quit"
            elif self.state == "quit":
                self.cursor.position.x = self.start_game.get_x() + self.cursor_offset
                self.cursor.position.y = self.heading.get_y() + (self.menu_item) # move to first menu item
                self.state = "start"
        if self.move_up:
            if self.state == "start":
                self.cursor.position.x = self.quit_game.get_x() + self.cursor_offset
                self.cursor.position.y = self.heading.get_y() + (self.menu_item * 3)
                self.state = "quit"
            elif self.state == "select_level":
                self.cursor.position.x = self.start_game.get_x() + self.cursor_offset
                self.cursor.position.y = self.heading.get_y() + self.menu_item
                self.state = "start"
            elif self.state == "quit":
                self.cursor.position.x = self.select_level.get_x() + self.cursor_offset
                self.cursor.position.y = self.heading.get_y() + (self.menu_item * 2)
                self.state = "select_level"
            

    # handles input for the main menu
    def handle_input(self):
        self.run_display = False
        if self.state == "start":
            self.playing == True
        elif self.state == "select_level":
            self.levels_menu.display_levels()
      
    # displays main menu
    def display_main(self):

        pygame.display.set_caption('Air Hockey: Main Menu')
        self.run_display = True

        while self.run_display:
            self.draw_main_menu()
            self.check_events()
            if self.quit:
                self.run_display = False
            self.move_cursor()
            # user has made their choice
            if self.select:
                self.handle_input() # will break out of loop afterwards
            self.reset_keys()

  
class LevelsMenu(Menu):
    def __init__(self, screen: pygame.display):
        Menu.__init__(self, screen)
        # selects easiest level by default
        self.state = "easy"
        
        # everything gets placed relative to the heading attribute from Menu
        self.level_easy = Position(self.heading.get_x(), self.heading.get_y() + self.menu_item)
        self.level_medium = Position(self.heading.get_x(), self.heading.get_y() + (self.menu_item * 2))
        self.level_hard = Position(self.heading.get_x(), self.heading.get_y() + (self.menu_item * 3))
        self.return_main_menu = Position(self.heading.get_x(), self.heading.get_y() + (self.menu_item * 4))

        # place cursor at the first menu item under the heading by default
        self.cursor = Position(self.level_easy.get_x() + self.cursor_offset, self.heading.get_y() + self.menu_item)

    def get_level(self):
        return self.state
        
    # displays level menu
    def display_levels(self):

        pygame.display.set_caption('Air Hockey: Select a Level')
        self.run_display = True

        while self.run_display:
            self.draw_levels_menu()
            self.check_events()
            if self.quit:
                self.run_display = False
            self.move_cursor()
            # user has made their choice
            if self.select:
                self.run_display = False
            self.reset_keys()
            
    def move_cursor(self):
        if self.move_down:
            if self.state == "easy":
                self.cursor.position.x = self.level_medium.get_x() + self.cursor_offset
                self.cursor.position.y = self.heading.get_y() + (self.menu_item * 2) # move to second menu item
                self.state = "medium"
            elif self.state == "medium":
                self.cursor.position.x = self.level_hard.get_x() + self.cursor_offset
                self.cursor.position.y = self.heading.get_y() + (self.menu_item * 3) # move to third menu item
                self.state = "hard"
            elif self.state == "hard":
                self.cursor.position.x = self.return_main_menu.get_x() + self.cursor_offset
                self.cursor.position.y = self.heading.get_y() + (self.menu_item * 4) # move to fourth menu item
                self.state = "return"
            # wraps back up to top of menu
            elif self.state == "return":
                self.cursor.position.x = self.level_easy.get_x() + self.cursor_offset
                self.cursor.position.y = self.heading.get_y() + self.menu_item # move to first menu item
                self.state = "easy"
        if self.move_up:
            # wraps down to bottom of menu
            if self.state == "easy":
                self.cursor.position.x = self.return_main_menu.get_x() + self.cursor_offset
                self.cursor.position.y = self.heading.get_y() + (self.menu_item * 4)
                self.state = "return"
            elif self.state == "medium":
                self.cursor.position.x = self.level_easy.get_x() + self.cursor_offset
                self.cursor.position.y = self.heading.get_y() + self.menu_item
                self.state = "easy"
            elif self.state == "hard":
                self.cursor.position.x = self.level_medium.get_x() + self.cursor_offset
                self.cursor.position.y = self.heading.get_y() + (self.menu_item * 2)
                self.state = "medium"
            elif self.state == "return":
                self.cursor.position.x = self.level_hard.get_x() + self.cursor_offset
                self.cursor.position.y = self.heading.get_y() + (self.menu_item * 3)
                self.state = "hard"


    def draw_levels_menu(self):
        levels_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        levels_surface.fill(BLACK)

        # accepts text, size of text, its position, its font, and its color as arguments
        self.draw_text('Select a level', MENU_SIZE, self.heading, MENU_FONT, WHITE, levels_surface)
        self.draw_text('*', MENU_SIZE, self.cursor, MENU_FONT, WHITE, levels_surface)
        self.draw_text('Easy', MENU_SIZE, self.level_easy, MENU_FONT, WHITE, levels_surface)
        self.draw_text('Medium', MENU_SIZE, self.level_medium, MENU_FONT, WHITE, levels_surface)
        self.draw_text('Hard', MENU_SIZE, self.level_hard, MENU_FONT, WHITE, levels_surface)
        self.draw_text('Return to Main Menu', MENU_SIZE, self.return_main_menu, MENU_FONT, WHITE, levels_surface)

        self.screen.blit(levels_surface, (0, 0))
        pygame.display.flip()
        