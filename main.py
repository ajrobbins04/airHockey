# import and initialize PyGame
import pygame
pygame.init()
from game.game import Game

# import keys to handle events
from pygame.locals import (
    K_SPACE,
    K_ESCAPE,
    KEYDOWN,
    QUIT,     # triggered when user closes window
)

game = Game()

def gameLoop(game: Game):

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
                    
            elif event.type == QUIT:
                running = False
            else:
                game.paddleRed.set_is_moving(False)
                game.paddleBlue.set_is_moving(False)

        # returns a dictionary of the keys that were pressed
        keys = pygame.key.get_pressed()

        game.updateField(keys)
        game.drawField()

        # updates appearance of the entire screen
        pygame.display.flip()

    # quit once out of the game loop    
    pygame.quit()


gameLoop(game)
