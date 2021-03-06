import os
import pygame
import random
import sys

from debug import debug
from main import restart
from player import Player
from platform import ExitPlatform, Platform
from settings import *
from utils import render_multi_colour_text


class Level:
    def __init__(self, score, platform_speed, bg_image, game):
        # Pygame artefacts
        self.clock  = pygame.time.Clock()
        self.bg_image = bg_image
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(os.path.join("assets", "fonts", "NeonSans.otf"), 64)
        self.small_font = pygame.font.Font(os.path.join("assets", "fonts", "NeonSans.otf"), 32)
        self.score = score
        self.game = game
        self.paused = False

                
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
        
        # Level state
        self.running = True


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

    def run(self):
        while self.running:
            self.handle_input()
            if not self.paused:
                self.update()
            self.draw()
            pygame.display.update()
            self.clock.tick(FPS)
        self.on_end_game()

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

        self.platforms.update(on_kill=self.spawn_platform, on_land=self.increment_score, set_speed=self.current_platform_speed)
        self.exit_platforms.update(on_land=self.increment_level, set_speed=self.current_platform_speed)
        

    def increment_level(self):
        self.increment_score()
        self.game.next_level(self.score, self.current_platform_speed -1 if self.current_platform_speed >= 2 else 1)

    def draw_score(self):
        display_surface = pygame.display.get_surface()
        surf = self.font.render(f"{self.score}", True, DARK)
        rect = surf.get_rect(topright=(WINDOW_WIDTH - TILE_SIZE, TILE_SIZE))
        display_surface.blit(surf, rect)
        
    def draw_high_score(self):
        display_surface = pygame.display.get_surface()
        surf = self.small_font.render(f"Best: {self.game.high_score}", True, DARK)
        rect = surf.get_rect(topright=(WINDOW_WIDTH - TILE_SIZE, TILE_SIZE*2))
        display_surface.blit(surf, rect)
        

    def draw_paused_message(self):
        display_surface = pygame.display.get_surface()
        surf = self.font.render("PAUSED", True, DARK)
        rect = surf.get_rect(center=WINDOW_CENTER)
        display_surface.blit(surf, rect) 

    def draw_background(self):
        self.display_surface.blit(self.bg_image, (0,0))
        

    def draw(self):
        self.draw_background()
        self.platforms.draw(self.display_surface)
        self.exit_platforms.draw(self.display_surface)
        self.player.sprite.draw(self.display_surface)
        self.draw_score()
        self.draw_high_score()
        if self.paused:
            self.draw_paused_message()
        self.print_debug_statements()

    def print_debug_statements(self):
        debug(f"{self.current_platform_speed=}")

    def on_player_death(self):
        self.running = False
        if self.score >= self.game.high_score:
            self.game.save_high_score()
    
    def handle_input_end_game(self):
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN :
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                else:
                    restart()

    def draw_end_game(self):
        self.draw_background()
        self.draw_score()
        self.draw_high_score()

        message = "Game Over" 
        surf = self.font.render(message, True, NEON_PINK)
        
        rect = surf.get_rect(center=(WINDOW_HORIZONTAL_CENTER, WINDOW_VERITICAL_CENTER - surf.get_height()))
        self.display_surface.blit(surf,rect)
        
        message = "Press any key to restart"
        
        surf = self.small_font.render(message, True, NEON_BLUE)
        
        rect = surf.get_rect(center=(WINDOW_HORIZONTAL_CENTER, WINDOW_VERITICAL_CENTER + surf.get_height()))
        self.display_surface.blit(surf, rect)
        

    def on_end_game(self):
        while not self.running:
            self.handle_input_end_game()
            self.draw_end_game()
            pygame.display.update()
            self.clock.tick(FPS)