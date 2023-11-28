# import and initialize PyGame
import pygame
pygame.init()
from game.game import Game

# import keys to handle events
from pygame.locals import (
    K_SPACE,
    K_ESCAPE,
    KEYDOWN,
    KEYUP,
    QUIT,     # triggered when user closes window
)


def game_loop():

    game = Game()
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
                """elif event.key in game.redKeys:
                    game.paddleRed.begin_track_movement()
                elif event.key in game.blueKeys:
                    game.paddleBlue.begin_track_movement()"""
                    
            elif event.type == QUIT:
                running = False
           
            # releasing a key stops movement
            """elif event.type == KEYUP:
                if event.key in game.redKeys:
                    game.paddleRed.end_track_movement()
                elif event.key in game.blueKeys:
                    game.paddleBlue.end_track_movement()"""

        # returns a dictionary of the keys that were pressed
        pressed_keys = pygame.key.get_pressed()

        # update field based on keys pressed and draw the resulting field
        game.update(pressed_keys)
        game.draw_field()

        # updates appearance of the entire screen
        pygame.display.flip()

    # quit once out of the game loop    
    pygame.quit()


game_loop()
