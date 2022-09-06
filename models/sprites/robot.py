import pygame
from pygame.sprite import Sprite

class Robot(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        #load img and set rect
        self.image = pygame.image.load('images/angry-robot-small.png')
        self.rect = self.image.get_rect()

    def update(self):
        self.y += (self.settings.fleet_speed * self.settings.fleet_direction)
        self.rect.y = self.y

    def is_at_edge(self):
        """ Return True if sprite is at edge of screen """
        screen_rect = self.screen.get_rect()
        if self.rect.bottom >= screen_rect.bottom or self.rect.top <= 0:
            return True