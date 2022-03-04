import pygame
from debug import debug
from settings import *


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, groups, image=None, color=DARK, player=None):
        super().__init__(groups)
        if image:
            self.image = image
        else:
            self.image = pygame.Surface((TILE_SIZE * w, TILE_SIZE * h))
            self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.player = player
        self.speed = 0
        self.has_player = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, on_kill, on_land, set_speed):
        self.speed = set_speed
        self.rect.y += self.speed
        if self.player:
            self.player.rect.y += self.speed
        # Do this only once
        if self.player and not self.has_player:
            self.has_player = True
            on_land()
            

        if self.rect.top > WINDOW_HEIGHT:
            on_kill()
            self.kill()

class ExitPlatform(Platform):
    def __init__(self, x, y, w, h, groups, image, color=DARK, player=None):
        super().__init__(x, y, w, h, groups=groups, image=image, color=color, player=player)
        
    def update(self, on_land, set_speed):
        self.speed = set_speed
        self.rect.y += self.speed
        if self.player:
            on_land()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        # self.print_debug_statements()

    def print_debug_statements(self):
        debug(f"{self.rect.topleft=} {self.rect.topright=}", y=200)
        