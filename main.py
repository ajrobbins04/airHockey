# import and initialize PyGame
import pygame
pygame.init()
from game.game import Game
from constants.constants import *

def run_game():
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    display = pygame.Surface([SCREEN_WIDTH, SCREEN_HEIGHT])

    game = Game(screen, display)
    game.run_game()

    # quit once game has run
    pygame.quit() 

run_game()

