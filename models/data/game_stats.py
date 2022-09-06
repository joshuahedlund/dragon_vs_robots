class GameStats:
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.game_started = False
        self.game_active = False
        self.score = 0
        self.set_game()

    def set_game(self):
        """ Init stats that can change during the game """
        self.player_life_left = self.settings.player_hit_limit
        self.boss_life_left = self.settings.boss_hit_limit