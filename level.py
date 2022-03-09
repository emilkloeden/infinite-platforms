import os
import pygame
import random

from debug import debug
from player import Player
from platform import ExitPlatform, Platform
from settings import *
from utils import save_high_score


class Level:
    def __init__(self, score, platform_speed, bg_image, game):
        # Pygame artefacts
        self.bg_image = bg_image
        self.bg_image_pos = pygame.math.Vector2(0)
        self.bg_image_relative_y = 0
        self.font = pygame.font.Font(os.path.join("assets", "fonts", "NeonSans.otf"), 64)
        self.small_font = pygame.font.Font(os.path.join("assets", "fonts", "NeonSans.otf"), 32)
        self.score = score
        self.paused = False
        
        self.game = game

                
        # Platforms
        self.current_platform_speed = platform_speed
        self.can_increase_platform_speed = False
        self.platforms = pygame.sprite.Group()
        self.exit_platforms = pygame.sprite.Group()
        self.platform_assets = {
            2: pygame.transform.scale(pygame.image.load(os.path.join("assets", "sprites", "platform-2.png")).convert_alpha(), (2 * TILE_SIZE, TILE_SIZE)),
            3: pygame.transform.scale(pygame.image.load(os.path.join("assets", "sprites", "platform-3.png")).convert_alpha(), (3 * TILE_SIZE, TILE_SIZE)),
            4: pygame.transform.scale(pygame.image.load(os.path.join("assets", "sprites", "platform-4.png")).convert_alpha(), (4 * TILE_SIZE, TILE_SIZE)),
            5: pygame.transform.scale(pygame.image.load(os.path.join("assets", "sprites", "platform-5.png")).convert_alpha(), (5 * TILE_SIZE, TILE_SIZE)),
        }
        self.exit_platform_sprite = pygame.transform.scale(pygame.image.load(os.path.join("assets", "sprites", "exit-platform-5.png")).convert_alpha(), (5 * TILE_SIZE, TILE_SIZE))


        # spawn some initial platforms
        for i in range(3):
            self.spawn_platform(initial_w=4, initial_x=3+i, initial_y=i*3)
        

        # Player
        self.player = pygame.sprite.GroupSingle()
        Player((self.platforms.sprites()[1].rect.x, TILE_SIZE * 2), self.platforms, self.exit_platforms, self.on_player_death, self.pause, [self.player])

    def pause(self):
        self.paused = not self.paused

    def spawn_platform(self, initial_x=None, initial_y=None, initial_w=None, initial_h=None):
        valid_sizes = [2,3,4,5]
        # Choose platform width and x in tile sizes
        w = initial_w if initial_w else random.choice(valid_sizes) 
        h = initial_h if initial_h else 1
        x_pos_as_factor_of_tile_size = initial_x if initial_x else random.randint(0, WINDOW_WIDTH_IN_TILES - w)
        
        # Convert to pixels
        x = x_pos_as_factor_of_tile_size * TILE_SIZE 
        y = initial_y * TILE_SIZE if initial_y else 0 - TILE_SIZE
        
        if self.score > 0 and self.score % EXIT_AMOUNT == 0 and not self.exit_platforms:
            ExitPlatform(x, y, w, h, [self.exit_platforms], self.exit_platform_sprite)
        else:
            Platform(x, y, w, h, [self.platforms], self.platform_assets[w])

    def increment_score(self):
        self.score += 1
        if self.score > self.game.high_score:
            self.game.high_score = self.score


    def handle_input(self):
        self.player.sprite.handle_input()

    def update(self):
        self.player.update()
        
        if self.current_platform_speed >= MAX_PLATFORM_SPEED:
            self.can_increase_platform_speed = False
        elif self.score % NUM_OF_PLATFORMS_BEFORE_SPEED_INCREASE == 0:
            if self.can_increase_platform_speed:
                self.can_increase_platform_speed = False
                self.current_platform_speed += 0.5
        else:
            self.can_increase_platform_speed = True

        self.bg_image_relative_y = self.bg_image_pos.y % self.bg_image.get_rect().height
        self.bg_image_relative_y += self.current_platform_speed // 2
        self.bg_image_pos.y = self.bg_image_relative_y - self.bg_image.get_rect().height
        
        self.platforms.update(on_kill=self.spawn_platform, on_land=self.increment_score, set_speed=self.current_platform_speed)
        self.exit_platforms.update(on_land=self.increment_level, set_speed=self.current_platform_speed)
        

    def increment_level(self):
        self.increment_score()
        self.game.next_level(self.score, self.current_platform_speed -1 if self.current_platform_speed >= 2 else 1)

    def draw_score(self, surface):
        surf = self.font.render(f"{self.score}", True, DARK)
        rect = surf.get_rect(topright=(WINDOW_WIDTH - TILE_SIZE, TILE_SIZE))
        surface.blit(surf, rect)
        
    def draw_high_score(self, surface):
        surf = self.small_font.render(f"Best: {self.game.high_score}", True, DARK)
        rect = surf.get_rect(topright=(WINDOW_WIDTH - TILE_SIZE, TILE_SIZE*2))
        surface.blit(surf, rect)
        

    def draw_paused_message(self, surface):
        surf = self.font.render("PAUSED", True, DARK)
        rect = surf.get_rect(center=WINDOW_CENTER)
        surface.blit(surf, rect) 

    def draw_background(self, surface):
        debug(f"{self.bg_image.get_rect()=}")
        debug(f"{self.bg_image_pos.y=}", y=10)
        surface.blit(self.bg_image, self.bg_image_pos)
        if self.bg_image_pos.y < WINDOW_HEIGHT:
            surface.blit(self.bg_image, (0, self.bg_image_relative_y))

    def draw(self, surface):
        self.draw_background(surface)
        self.platforms.draw(surface)
        self.exit_platforms.draw(surface)
        self.player.sprite.draw(surface)
        self.draw_score(surface)
        self.draw_high_score(surface)
        if self.paused:
            self.draw_paused_message(surface)
        # self.print_debug_statements()

    def print_debug_statements(self):
        debug(f"{self.current_platform_speed=}")

    def on_player_death(self):
        self.game.next_state = "ENDGAME"
        self.game.persist["score"] = self.score
        self.game.persist["high_score"] = self.game.high_score
        self.game.persist["bg_image"] = self.bg_image
        if self.score >= self.game.high_score:
            save_high_score(self.score)
        
        self.game.done = True
    