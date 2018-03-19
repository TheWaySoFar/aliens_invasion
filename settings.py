class Settings():
    def __init__(self):
        self.screen_width=1000
        self.screen_height=600
        self.bg_color=(230,230,230)

        """ship factor"""

        self.ship_limit = 3

        """bullet factor"""
        self.bullet_width = 3
        self.bullet_height = 10
        self.bullet_color = (60,60,60)
        self.bullet_allowed = 3
        """alien factor"""

        self.speedup_scale = 1.5
        self.init_dynamic_settings()
        self.alien_points = 50

    def init_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 5
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        self.fleet_direction = 1

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.speedup_scale)



