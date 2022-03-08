import sys

import pygame

import game
from endgame import EndGame
from settings import *
from splash import Splash
from statemachine import StateMachine


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    states = {"SPLASH": Splash(),
                   "GAMEPLAY": game.Game(),
                   "ENDGAME": EndGame(),
                   }
    # game = Game(screen, states, "SPLASH")
    # game.run()
    control = StateMachine(screen, states, "SPLASH")
    control.run()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

# Old ways
# def restart():
#     main(first_run=False)

# def main(first_run=False):
#     game.Game(first_run)

# if __name__ == "__main__":
#     main(first_run=True)
