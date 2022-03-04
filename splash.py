import os
import pygame
import random
from settings import *

class Splash():
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(os.path.join("assets", "fonts", "NeonSans.otf"), 58)
        self.color = random.choice([NEON_BLUE, NEON_PINK, RED])

    def run(self):
        self.draw()
        pygame.display.update()
        self.clock.tick(FPS)
        pygame.time.delay(1000)

    def draw(self):
        
        self.screen.fill(BLACK)
        surf = self.font.render(GAME_NAME, True, self.color)
        rect = surf.get_rect(center=WINDOW_CENTER)
        self.screen.blit(surf, rect)