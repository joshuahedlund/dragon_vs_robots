import pygame
import random

from models.sprites.bullet import Bullet

class BossBullet(Bullet):
    def __init__(self, ai_game):
        super().__init__(ai_game)
        self.screen_rect = ai_game.screen.get_rect()


    def set_pos(self, boss_rect):
        """ Fire the bullet from boss position """
        self.x = boss_rect.left - 10
        self.y = boss_rect.top + 60

        self.rect.x = self.x
        self.rect.y = self.y

        self.is_moving = True

    def update(self):
        """Move the bullet across the screen"""
        if not self.is_moving:
            return

        self.x -= self.settings.bullet_speed
        self.rect.x = self.x

    def _load_image(self):
        self.image = pygame.image.load('images/flame-ball-boss.bmp')
        self.rect = self.image.get_rect()
