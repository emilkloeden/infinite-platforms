import sys
import random
import pygame

from debug import debug


# Frames per second
FPS = 60

# Colours
DARK = "#43523d"
LIGHT = "#c7f0d8"

# Actor dimensions
TILE_SIZE = 64
PLAYER_WIDTH = TILE_SIZE // 2
PLAYER_HEIGHT = TILE_SIZE
PLAYER_SIZE = (PLAYER_WIDTH, PLAYER_HEIGHT)

# Window dimensions
WINDOW_WIDTH_IN_TILES = 10
WINDOW_WIDTH = WINDOW_WIDTH_IN_TILES * TILE_SIZE
WINDOW_HEIGHT_IN_TILES = 8
WINDOW_HEIGHT = WINDOW_HEIGHT_IN_TILES * TILE_SIZE
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
WINDOW_HORIZONTAL_CENTER = WINDOW_WIDTH // 2
WINDOW_VERITICAL_CENTER = WINDOW_HEIGHT // 2
WINDOW_CENTER = (WINDOW_HORIZONTAL_CENTER, WINDOW_VERITICAL_CENTER)

# Physics
NUM_OF_PLATFORMS_BEFORE_SPEED_INCREASE = 3

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, platforms, on_death, groups) -> None:
        super().__init__(groups)
        # Platforms
        self.platforms = platforms

        # Image
        self.image = pygame.Surface(PLAYER_SIZE)
        self.rect = self.image.get_rect(topleft=pos)
        self.image.fill(DARK)
        
        # Movement
        self.pos = pygame.math.Vector2(pos)
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 3
        self.jumping = False
        self.on_platform = True
        self.jump_force = -16
        self.gravity_force = 0.8

        self.current_platform = None

        self.on_death = on_death

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN :
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:
                    restart()
                elif event.key == pygame.K_UP:
                    self.jump()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.direction.x = -self.speed
        elif keys[pygame.K_RIGHT]:
            self.direction.x = self.speed
        else:
            self.direction.x = 0


    def apply_gravity(self):
        self.direction.y += self.gravity_force
        self.rect.y += self.direction.y
        


    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.direction.y = self.jump_force

    def handle_horizontal_movement(self):
        self.rect.x += self.speed * self.direction.x
        if self.rect.right < 0:
            self.rect.left = WINDOW_WIDTH
        elif self.rect.left > WINDOW_WIDTH:
            self.rect.right = 0


    def handle_vertical_movement(self):
        for platform in  self.platforms.sprites():
            if platform.rect.colliderect(self.rect):
                if self.direction.y > 0: # falling
                    self.rect.bottom = platform.rect.top
                    self.direction.y = 0
                    self.jumping = False
                    self.on_platform = True
                    self.current_platform = platform
                elif self.direction.y < 0: # rising
                    self.rect.top = platform.rect.bottom
                    self.direction.y = 0
                    self.current_platform = None
            else:
                self.current_platform = None

        if self.on_platform and self.direction.y != 0:
            self.on_platform = False

    def update(self):
        self.handle_horizontal_movement()
        if not self.current_platform:
            self.apply_gravity()
        elif not self.jumping:
            self.rect.bottom = self.current_platform.rect.top
        self.handle_vertical_movement()
        if self.rect.top > WINDOW_HEIGHT:
            self.on_death()


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, groups):
        super().__init__(groups)
        self.image = pygame.Surface((w, h))
        self.image.fill(DARK)
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, on_kill, set_speed):
        self.rect.y += set_speed
        if self.rect.top > WINDOW_HEIGHT:
            on_kill()
            self.kill()

class Level:
    def __init__(self, clock):
        # Pygame artefacts
        self.clock = clock
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 64)
        self.small_font = pygame.font.Font(None, 32)
        self.score = 0
                
        # Platforms
        self.current_platform_speed = 1
        self.can_increase_platform_speed = False
        self.platforms = pygame.sprite.Group()
        for i in range(3):
            w = TILE_SIZE * 4
            h = TILE_SIZE
            x = WINDOW_HORIZONTAL_CENTER - w // 2
            y = (i * 3) * TILE_SIZE
            Platform(x, y, w, h, [self.platforms])
        # self.visible_sprites = pygame.sprite.Group()

        # Player
        self.player = pygame.sprite.GroupSingle()
        Player(WINDOW_CENTER, self.platforms, self.on_player_death, [self.player])
        
        # Level state
        self.running = True

    def spawn_platform_and_increase_score(self):
        "Callback that spawns a new platform"
        # Calculate width and x in tile sizes
        valid_sizes = [2,3,4,5]
        platform_width = random.choice(valid_sizes) 
        platform_x = random.randint(0, WINDOW_WIDTH_IN_TILES - platform_width)
        self.score += 1
        
        # Convert to pixels
        x = TILE_SIZE * platform_x 
        y = 0 - TILE_SIZE
        w = TILE_SIZE * platform_width
        h = TILE_SIZE
        Platform(x, y, w, h, [self.platforms])

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            pygame.display.update()
            self.clock.tick(FPS)
        self.on_end_game()

    def handle_input(self):
        self.player.sprite.handle_input()

    def update(self):
        self.player.update()
        
        if self.score % NUM_OF_PLATFORMS_BEFORE_SPEED_INCREASE == 0:
            if self.can_increase_platform_speed:
                self.can_increase_platform_speed = False
                self.current_platform_speed += 0.5
        else:
            self.can_increase_platform_speed = True

        self.platforms.update(on_kill=self.spawn_platform_and_increase_score, set_speed=self.current_platform_speed)
        
    def draw_score(self):
        display_surface = pygame.display.get_surface()
        debug_surf = self.font.render(f"{self.score}", True, DARK)
        debug_rect = debug_surf.get_rect(topright = (WINDOW_WIDTH - TILE_SIZE, TILE_SIZE))
        display_surface.blit(debug_surf,debug_rect)

    def draw(self):
        self.display_surface.fill(LIGHT)
        self.platforms.draw(self.display_surface)
        # self.visible_sprites.draw(self.display_surface)
        self.player.draw(self.display_surface)
        self.draw_score()

    def on_player_death(self):
        self.running = False
    
    def handle_input_end_game(self):
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN :
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:
                    restart()

    def draw_end_game(self):
        self.display_surface.fill(LIGHT)
        self.draw_score()
        debug_surf = self.small_font.render(f"Game Over. Press 'R' to restart.", True, DARK)
        debug_rect = debug_surf.get_rect(center=WINDOW_CENTER)
        self.display_surface.blit(debug_surf,debug_rect)
        
    def on_end_game(self):
        while not self.running:
            self.handle_input_end_game()
            self.draw_end_game()
            pygame.display.update()
            self.clock.tick(FPS)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.clock  = pygame.time.Clock()
        self.running = True
        self.level = Level(self.clock)

    def run(self):
        self.level.run()


    def draw(self):
        # Keep if we need more than one screen
        self.screen.fill("black")
        pygame.display.update()
        self.clock.tick(FPS)


def restart():
    main()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()