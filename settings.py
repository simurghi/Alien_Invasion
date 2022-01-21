class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's settings."""
        self.screen_width = 1280
        self.screen_height = 720
        self.bg_color = (0,0,0)

        #  Ship settings
        self.ship_speed = 1.5 

        # Bullet settings
        self.bullet_speed = 1.0
        self.bullets_allowed = 5

