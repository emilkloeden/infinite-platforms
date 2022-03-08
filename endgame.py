import os

import pygame

from settings import *
from state import _State

class EndGame(_State):
    def __init__(self) -> None:
        super().__init__()
        self.font = pygame.font.Font(os.path.join("assets", "fonts", "NeonSans.otf"), 64)
        self.small_font = pygame.font.Font(os.path.join("assets", "fonts", "NeonSans.otf"), 32)
        

    def startup(self, persistent):
        self.persist = persistent
        self.score = self.persist["score"]
        self.high_score = self.persist["high_score"]
        self.bg_image = self.persist['bg_image']
        
    def draw_score(self):
        display_surface = pygame.display.get_surface()
        surf = self.font.render(f"{self.score}", True, DARK)
        rect = surf.get_rect(topright=(WINDOW_WIDTH - TILE_SIZE, TILE_SIZE))
        display_surface.blit(surf, rect)
        
    def draw_high_score(self):
        display_surface = pygame.display.get_surface()
        surf = self.small_font.render(f"Best: {self.high_score}", True, DARK)
        rect = surf.get_rect(topright=(WINDOW_WIDTH - TILE_SIZE, TILE_SIZE*2))
        display_surface.blit(surf, rect)

    def draw_background(self):
        display_surface = pygame.display.get_surface()
        display_surface.blit(self.bg_image, (0,0))

    def draw(self, surface):
        self.draw_background()
        self.draw_score()
        self.draw_high_score()

        message = "Game Over" 
        surf = self.font.render(message, True, NEON_PINK)
        
        rect = surf.get_rect(center=(WINDOW_HORIZONTAL_CENTER, WINDOW_VERITICAL_CENTER - surf.get_height()))
        surface.blit(surf,rect)
        
        message = "Press any key to restart"
        
        surf = self.small_font.render(message, True, NEON_BLUE)
        
        rect = surf.get_rect(center=(WINDOW_HORIZONTAL_CENTER, WINDOW_VERITICAL_CENTER + surf.get_height()))
        surface.blit(surf, rect)
        
    def get_event(self, event):
        super().get_event(event)
        if event.type == pygame.KEYDOWN and not event.key == pygame.K_ESCAPE:
            self.next_state = "GAMEPLAY"
            self.done = True
