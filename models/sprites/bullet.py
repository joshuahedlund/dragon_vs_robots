import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.settings = ai_game.settings

        self._load_image()

    def update(self):
        """Move the bullet across the screen"""
        self.x += self.settings.bullet_speed
        self.rect.x = self.x

    def set_pos_from_player(self, player_rect):
        """ Position the bullet as firing from the player """
        self.rect.midright = player_rect.midright

        # Store the bullet's position as a decimal value
        self.x = float(self.rect.x)

        self.is_moving = True

    def _load_image(self):
        self.image = pygame.image.load('images/flame-ball.png')
        self.rect = self.image.get_rect()