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


        #  Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullets_allowed = 4
        

        # How quickly the game speeds up.
        self.speedup_scale = 1.00
        self.score_scale = 25

        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        if self.turbo_speed:
            self.speed_mult = 1.5
        else: 
            self.speed_mult = 1
        self.ship_speed = 4.00 * self.speed_mult
        self.alien_speed = 4.00 * self.speed_mult
        self.bullet_speed = 4.00 * self.speed_mult
        # Scoring 
        self.alien_points = 100


    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed += self.speedup_scale 
        self.bullet_speed += self.speedup_scale 
        self.alien_speed += self.speedup_scale 
        self.alien_points += self.score_scale

