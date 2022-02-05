class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        self.screen_width = 960
        self.screen_height = 640
        self.bg_color = (0,0,0)
        self.play_music = True
        self.play_sfx = True
        self.cinematic_bars = True
        self.turbo_speed = False
        self.speed_mult = 1.0
        self.speed_add = 1.0


        #  Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullets_allowed = 5
        

        # How quickly the game speeds up.
        self.speedup_scale = 1.00
        self.score_scale = 25

        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        if self.turbo_speed:
            self.speed_mult = 1.5
            self.alien_points = 150
        else: 
            self.speed_mult = 1
            self.alien_points = 100
        self.ship_speed = 4.00 * self.speed_mult
        self.alien_speed = 4.00 * self.speed_mult
        self.bullet_speed = 4.00 * self.speed_mult
        # Scoring 


    def increase_speed(self):
        """Increase speed settings."""
        if self.turbo_speed:
            self.speed_add = 2
            self.score_scale = 50
        else:
            self.speed_add = 1
            self.score_scale = 25
        self.ship_speed += self.speedup_scale * self.speed_add
        self.bullet_speed += self.speedup_scale * self.speed_add
        self.alien_speed += self.speedup_scale * self.speed_add
        self.alien_points += self.score_scale * self.speed_add

