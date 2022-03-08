import pygame


class _State:
    def __init__(self) -> None:
        self.done = False
        self.quit = False
        self.next_state = None
        self.persist = {}

    def startup(self, persistent):
        self.persist = persistent

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYUP and event.key ==pygame.K_ESCAPE:
            self.quit = True

    def update(self, dt):
        "Called once per frame"
        pass

    def draw(self, surface):
        pass

    