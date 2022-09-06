import pygame
import random

from models.sprites.bullet import Bullet

class SuperBullet(Bullet):
    def __init__(self, ai_game):
        super().__init__(ai_game)
        self.screen_rect = ai_game.screen.get_rect()


    def set_pos_random(self, player_x):
        """ Position the bullet randomly, for player to pick up """
        self.x = player_x + 75
        self.y = random.randrange(10, self.screen_rect.height - self.settings.margin)

        self.rect.x = self.x
        self.rect.y = self.y

        self.is_moving = False

    def update(self):
        """Move the bullet across the screen"""
        if not self.is_moving:
            return

        self.x += self.settings.bullet_speed
        self.rect.x = self.x

    def _load_image(self):
        self.image = pygame.image.load('images/flame-ball-super.bmp')
        self.rect = self.image.get_rect()
