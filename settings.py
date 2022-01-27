class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        self.screen_width = 960
        self.screen_height = 640
        self.bg_color = (0,0,0)
        self.play_music = True
        self.play_sfx = True

        #  Ship settings
        self.ship_speed = 1.25

        # Bullet settings
        self.bullet_speed = 1.3
        self.bullets_allowed = 4
        
        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        self.fleet_direction = -1


