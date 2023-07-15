import pygame.font
from pygame.sprite import Group

class Scoreboard:
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.player_super_bullets = 0

        # Font settings for scoring
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        self.font_large = pygame.font.SysFont(None, 72)

        self.render_lives()
        self.render_super_bullets()
        self.render_score()

    def draw(self):
        self.screen.blit(self.lives_image, self.lives_rect)
        self.screen.blit(self.bullets_image, self.bullets_rect)
        self.screen.blit(self.score_image, self.score_rect)

    def render_lives(self):
        lives_str = ''
        for i in range(self.stats.player_life_left):
            lives_str += '*'
        self.lives_image = self.font_large.render(lives_str, True, self.text_color, self.settings.bg_color)

        # Display lives at top left of screen
        self.lives_rect = self.lives_image.get_rect()
        self.lives_rect.left = self.lives_rect.left + self.settings.margin
        self.lives_rect.top = self.settings.margin

    def render_super_bullets(self):
        bullets_str = ''
        for i in range(self.player_super_bullets):
            bullets_str += 'o'
        self.bullets_image = self.font_large.render(bullets_str, True, self.text_color, self.settings.bg_color)

        # Display lives at top left of screen
        self.bullets_rect = self.bullets_image.get_rect()
        self.bullets_rect.left = self.bullets_rect.left + self.settings.margin
        self.bullets_rect.top = self.settings.margin + 25

    def render_score(self):
        """ Turn score into rendered image """
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # Display score at top right of screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - self.settings.margin
        self.score_rect.top = self.settings.margin

    def reset_score(self):
        self.stats.score = 0
        self.render_score()

    def update_score(self, score_adjust):
        self.stats.score += score_adjust
        self.render_score()