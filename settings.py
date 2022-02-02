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
        self.backstack_multiplier = 2
        self.cqc_multiplier = 2

        #  Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullets_allowed = 4
        

        # How quickly the game speeds up.
        self.speedup_scale = 1.05
        self.score_scale = 1.1

        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 1.25
        self.alien_speed = 1.0
        self.bullet_speed = 1.2
        # Scoring 
        self.alien_points = 100


    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
