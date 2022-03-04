import os
import pygame
from level import Level
from splash import Splash
from settings import *



class Game:
    def __init__(self, first_run=False):
        # Set up
        pygame.font.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption(GAME_NAME)
        self.load_high_score()
        self.import_backgrounds()
        
        if first_run:
            # Splash screen
            splash = Splash(self.screen)
            splash.run()

        # Start Playing
        self.running = True
        self.current_level_number = 0
        self.next_level(score=0, platform_speed=1)

    def import_backgrounds(self):
        self.backgrounds = [
            pygame.image.load(os.path.join("assets", "backgrounds", png)).convert_alpha() 
            for png in os.listdir(os.path.join("assets", "backgrounds"))
            if png.lower().endswith(".png")
        ]

    def next_level(self, score, platform_speed):
        # These two lines are arranged in this order
        # so we get the backgrounds in alphabetical order
        bg_image = self.backgrounds[self.current_level_number % len(self.backgrounds)]
        self.current_level_number += 1

        self.level = Level(score, platform_speed, bg_image, self)
        self.level.run()

    def load_high_score(self):
        try:
            with open(os.path.join("data", "high_score.txt"), "r") as f:
                self.high_score = int(f.readline().strip())
        except FileNotFoundError:
            self.high_score = 0
            with open(os.path.join("data", "high_score.txt"), "w") as f:
                f.write(self.high_score)
        except ValueError:
            self.high_score = 0

    def save_high_score(self):
        with open(os.path.join("data", "high_score.txt"), "w") as f:
            f.write(f"{self.high_score}")