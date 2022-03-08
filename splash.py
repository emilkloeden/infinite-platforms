import os
import pygame
import random
from state import _State
from settings import *

class Splash(_State):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(os.path.join("assets", "fonts", "NeonSans.otf"), 58)
        self.color = random.choice([NEON_BLUE, NEON_PINK, RED])
        self.next_state = "GAMEPLAY"
        # print("Self.splash.init")

    #TODO: reimplement this
    # def run(self):
    #     self.draw()
    #     pygame.display.update()
    #     self.clock.tick(FPS)
    #     pygame.time.delay(1000)

    def draw(self, surface):
        surface.fill(BLACK)
        surf = self.font.render(GAME_NAME, True, self.color)
        rect = surf.get_rect(center=WINDOW_CENTER)
        surface.blit(surf, rect)
        
    def get_event(self, event):
        super().get_event(event)
        if event.type == pygame.KEYDOWN:
            self.done = True
        
    