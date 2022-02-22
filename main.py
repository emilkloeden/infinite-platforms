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



class Player(pygame.sprite.Sprite):
    def __init__(self, pos, platforms, groups) -> None:
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
        self.jump_force = -16
        self.gravity_force = 0.8

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN :
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
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

        for platform in self.platforms.sprites():
            if platform.rect.colliderect(self.rect):
                if self.direction.x < 0: # heading left
                    self.rect.left = platform.rect.right
                elif self.direction.x > 0: # heading right
                    self.rect.left = platform.rect.right

    def handle_vertical_movement(self):
        self.apply_gravity()
        for platform in  self.platforms.sprites():
            if platform.rect.colliderect(self.rect):
                if self.direction.y > 0: # falling
                    self.rect.bottom = platform.rect.top
                    self.direction.y = 0
                    self.jumping = False
                elif self.direction.y < 0: # rising
                    self.rect.top = platform.rect.bottom
                    self.direction.y = 0

    def update(self):
        self.handle_horizontal_movement()
        self.handle_vertical_movement()


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, groups):
        super().__init__(groups)
        self.image = pygame.Surface((w, h))
        self.image.fill(DARK)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 2

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, on_kill):
        self.rect.y += self.speed
        if self.rect.top > WINDOW_HEIGHT:
            on_kill()
            self.kill()

class Level:
    def __init__(self, clock):
        # Pygame artefacts
        self.clock = clock
        self.display_surface = pygame.display.get_surface()
        
        # Platforms
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
        Player(WINDOW_CENTER, self.platforms, [self.player])
        
        # Level state
        self.running = True

    def spawn_platform(self):
        "Callback that spawns a new platform"
        # Calculate width and x in tile sizes
        valid_sizes = [2,3,4,5]
        platform_width = random.choice(valid_sizes) 
        platform_x = random.randint(0, WINDOW_WIDTH_IN_TILES - platform_width)
        
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

    def handle_input(self):
        self.player.sprite.handle_input()

    def update(self):
        self.platforms.update(on_kill=self.spawn_platform)
        # self.visible_sprites.update()
        self.player.update()

    def draw(self):
        self.display_surface.fill(LIGHT)
        self.platforms.draw(self.display_surface)
        # self.visible_sprites.draw(self.display_surface)
        self.player.draw(self.display_surface)


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


def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()