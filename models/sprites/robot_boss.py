import pygame

class RobotBoss:
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        
        #load the robot and set rect
        self.image = pygame.image.load('images/robot-boss.png')
        self.rect = self.image.get_rect()

    def set_init_position(self, x):
        self.x = x
        self.x_orig = self.x
        self.rect.x = self.x

        # Set vertically to center
        self.rect.y = (self.screen_rect.height - self.rect.height) // 2

        # Store decimals
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
    def update(self):
        self.y += (self.settings.fleet_speed * self.settings.fleet_direction)
        self.rect.y = self.y

    def draw(self):
        self.screen.blit(self.image, self.rect)