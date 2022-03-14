import os
import random
import sys
from platform import ExitPlatform, Platform

import pygame

from debug import debug
from level import Level
from player import Player
from settings import *
from splash import Splash
from state import _State
from utils import load_background_images, load_high_score



        



class Game(_State):
    def __init__(self):
        # Set up
        super().__init__()
        self.high_score = load_high_score()
        self.backgrounds = load_background_images()

        self.persist = {
            "score": "0",
            "high_score": self.high_score,
        }

        # Start Playing
        self.current_level_number = 0
        self.next_level(score=0, platform_speed=1)
        
    def next_level(self, score, platform_speed):
        # These two lines are arranged in this order
        # so we get the backgrounds in alphabetical order
        bg_image = self.backgrounds[self.current_level_number % len(self.backgrounds)]
        self.current_level_number += 1

        self.level = Level(score, platform_speed, bg_image, self)
        # self.level.run()

    def startup(self, persistent):
        self.persist = persistent
        self.current_level_number = 0
        self.next_level(score=0, platform_speed=3)


    def get_event(self, event):
        super().get_event(event)
        
        player = self.level.player.sprites()[0]
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                self.level.pause()
            # elif event.key == pygame.K_r:
            #     restart()
            elif event.key in [pygame.K_UP, pygame.K_w, pygame.K_SPACE]:
                player.jump()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.direction.x = -player.speed
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.direction.x = player.speed
        else:
            player.direction.x = 0

    def update(self, dt):
        if not self.level.paused:
            self.level.update()

    def draw(self, surface):
        self.level.draw(surface)

    def save_high_score(self):
        with open(os.path.join("data", "high_score.txt"), "w") as f:
            f.write(f"{self.high_score}")


# Old way
# class Game:
#     def __init__(self, first_run=False):
#         # Set up
#         pygame.font.init()
#         self.screen = pygame.display.set_mode(WINDOW_SIZE)
#         pygame.display.set_caption(GAME_NAME)
#         self.load_high_score()
#         self.import_backgrounds()
        
#         if first_run:
#             # Splash screen
#             splash = Splash(self.screen)
#             splash.run()

#         # Start Playing
#         self.running = True
#         self.current_level_number = 0
#         self.next_level(score=0, platform_speed=1)

#     def import_backgrounds(self):
#         self.backgrounds = [
#             pygame.image.load(os.path.join("assets", "backgrounds", png)).convert_alpha() 
#             for png in os.listdir(os.path.join("assets", "backgrounds"))
#             if png.lower().endswith(".png")
#         ]

#     def next_level(self, score, platform_speed):
#         # These two lines are arranged in this order
#         # so we get the backgrounds in alphabetical order
#         bg_image = self.backgrounds[self.current_level_number % len(self.backgrounds)]
#         self.current_level_number += 1

#         self.level = Level(score, platform_speed, bg_image, self)
#         self.level.run()

#     def load_high_score(self):
#         try:
#             with open(os.path.join("data", "high_score.txt"), "r") as f:
#                 self.high_score = int(f.readline().strip())
#         except FileNotFoundError:
#             self.high_score = 0
#             with open(os.path.join("data", "high_score.txt"), "w") as f:
#                 f.write(self.high_score)
#         except ValueError:
#             self.high_score = 0

#     def save_high_score(self):
#         with open(os.path.join("data", "high_score.txt"), "w") as f:
#             f.write(f"{self.high_score}")
