import pygame

class Player():
    def __init__(self, ai_game):
        """ Initialize the player and set starting position """
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        self.inv_super_bullets = 0

        # Load image and get rect
        self.image = pygame.image.load('images/baby-dragon-small.png')
        self.rect = self.image.get_rect()

        self.center()

        self.moving_x = 0
        self.moving_y = 0

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def center(self):
        # Start each spawned player at the left center
        self.rect.x = 10
        self.rect.y = (self.screen_rect.height - self.rect.height) // 2

        # Store a decimal value for positions
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        self.x += self.moving_x
        self.y += self.moving_y

        # wrap around if player goes off screen
        if self.x <= 0:
            self.x = self.screen_rect.width
        elif self.x >= self.screen_rect.width:
            self.x = 0

        if self.y <= 0:
            self.y = self.screen_rect.height
        elif self.y >= self.screen_rect.height:
            self.y = 0

        # Update rect object with int values from self decimal
        self.rect.x = self.x
        self.rect.y = self.y