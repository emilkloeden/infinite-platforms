import pygame

from debug import debug
from settings import *
from utils import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, platforms, exit_platforms, on_death, pause, groups):
        super().__init__(groups)
        # Platforms
        self.platforms = platforms
        self.exit_platforms = exit_platforms

        # Image
        self.image = pygame.Surface(PLAYER_SIZE)
        self.rect = self.image.get_rect(topleft=pos)
        self.image.fill(DARK)
        

        # graphics setup
        self.import_player_assets()
        self.frame_index = 0
        self.animation_speed = 0.15

        # Movement
        self.pos = pygame.math.Vector2(pos)
        self.direction = pygame.math.Vector2(0, 0)
        self.status = "right_idle"
        self.speed = 3
        self.jumping = False
        self.on_platform = True
        self.jump_force = -20
        self.gravity_force = 0.8

        self.current_platform = None

        # Callbacks
        self.on_death = on_death
        self.pause = pause
        
    def import_player_assets(self):
        character_path = 'assets/sprites/player/'
        self.animations = {
            # Walking
            "left": [], "right": [],
            # Idling
            'left_idle':[], 'right_idle':[],
            }

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def apply_gravity(self):
        # If we're not on a platform, apply gravity
        # Our vertical positioning if on a platform is controlled by the platform class (to avoid a bounce effect)
        if not self.current_platform:
            self.direction.y += self.gravity_force
            self.rect.y += self.direction.y
        
    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.direction.y = self.jump_force

    def handle_horizontal_movement(self):
        "Allows player to exit screen on one side and reenter on the other"
        self.rect.x += self.speed * self.direction.x
        if self.rect.right < 0:
            self.rect.left = WINDOW_WIDTH
        elif self.rect.left > WINDOW_WIDTH:
            self.rect.right = 0


    def handle_vertical_movement(self):
        # Stick to top of current platform unless not jumping
        if self.current_platform and not self.jumping:
            self.rect.bottom = self.current_platform.rect.top
        elif self.current_platform:
            self.current_platform = None
        
        # If we don't have a current platform...
        # See if we collide with one
        # If we collide with one from above
        # Mark it as a current platform and stick to it
        else:
            for exit_platform in self.exit_platforms.sprites():
                if exit_platform.rect.colliderect(self.rect):
                    if self.rect.centery < exit_platform.rect.centery:
                        exit_platform.player = self

            for platform in self.platforms.sprites():
                if platform.rect.colliderect(self.rect):
                    if self.rect.centery < platform.rect.centery: # is above the platform
                        self.current_platform = platform
                        platform.player = self
                        self.direction.y = 0
                        self.rect.bottom = self.current_platform.rect.top
                        self.jumping = False
                        break
            # If we iterate through all platforms and don't collide with any, we're not on a platform
            self.current_platform = None
            
    def get_status(self):
        # If moving left, walk left
        if self.direction.x < 0:
            self.status = 'left'
        # If moving right, walk right
        elif self.direction.x > 0:
            self.status = 'right'
        # if not currently idle, be either left_idle or right_idle
        # TODO FIX:- THIS WILL BREAK WHEN NEW ANIMATIONS ADDED
        elif "_idle" not in self.status:
            self.status += "_idle"
        

    def animate(self):
        animation = self.animations[self.status]

        # loop over the frame index 
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set the image
        try:
            self.image = animation[int(self.frame_index)]
        except IndexError as e:
            print(int(self.frame_index))
            print(self.animations)
            raise
        # self.rect = self.image.get_rect(center = self.hitbox.center)

    def update(self):
        self.handle_horizontal_movement()
        self.apply_gravity()
        self.handle_vertical_movement()
        self.get_status()
        self.animate()

        if self.rect.top > WINDOW_HEIGHT:
            self.on_death()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        # self.print_debug_calls()


    def print_debug_calls(self):
        debug(self.direction.y)
