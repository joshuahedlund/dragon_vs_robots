class Settings:
    def __init__(self):
        # Screen settings
        self.bg_color = (230, 230, 230)
        self.margin = 20

        # Player settings
        self.player_speed = 4
        self.player_hit_limit = 3

        # Bullet settings
        self.bullet_speed = 8
        self.bullets_allowed = 5

        # Robot settings
        self.fleet_speed = 1.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1
        self.fleet_cur_shift_cycles = 0
        self.fleet_max_shift_cycles = 0 #will track length to first direction change and keep that constant
                                        # (otherwise the length will get longer as rows are eliminated)

        # Boss settings
        self.boss_hit_limit = 3

        # Score settings
        self.hit_points = 50
        self.boss_hit_points = 200
        self.miss_points = -10

    def is_at_max_shift_cycles(self):
        if self.fleet_max_shift_cycles > 0 and self.fleet_cur_shift_cycles >= self.fleet_max_shift_cycles:
            return True

        return False

    def update_fleet_direction(self):
        self.fleet_direction *= -1
        if self.fleet_max_shift_cycles == 0:
            self.fleet_max_shift_cycles = self.fleet_cur_shift_cycles
        self.fleet_cur_shift_cycles = 0