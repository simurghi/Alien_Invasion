import pygame, os

class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        self._set_window_properties()
        self._init_option_states()
        self._initialize_user_preferences()
        self._initialize_static_settings()
        self._initialize_dynamic_settings()

    def _init_option_states(self):
        """For options in the menu with multiple states."""
        self.GAME_SPEEDS = ("SPD: Slow", "SPD: Normal", "SPD: Fast",
                "SPD: Very Fast", "SPD: Ludicrous")
        self.GFX_SETTINGS = ("REZ: Native", "REZ: Scaled", "REZ: Full Scaled")
        self.HUD_SETTINGS = ("HUD: Classic", "HUD: Alt", "HUD: OFF")
        self.ARROW_SETTINGS = ("Arrows: ALL", "Arrows: Mine", "Arrows: Ship", "Arrows: OFF")
        self.SCORE_SETTINGS = ("SCORE: ALL", "SCORE: Game", "Score: Menu", "Score: OFF")

    def _set_window_properties(self):
        """Sets the properties for the game window and background."""
        self.screen_width = 960
        self.screen_height = 640
        self.FPS = 120.0
        self.bg_color = (0,0,0)

    def _initialize_user_preferences(self):
        """Sets default preferences for user options."""
        self.music_volume = 1.0
        self.sound_volume = 1.0
        self.speed = self.GAME_SPEEDS[1]
        self.speed_counter = 1
        self.gfx_mode = self.GFX_SETTINGS[0]
        self.gfx_counter = 0
        self.HUD = self.HUD_SETTINGS[0]
        self.HUD_counter = 0
        self.arrow_mode = self.ARROW_SETTINGS[0]
        self.arrow_counter = 0
        self.score_mode = self.SCORE_SETTINGS[0]
        self.score_counter = 0


    def _initialize_static_settings(self):
        """Initialize settings that do not change throughout the game."""
        self.ship_limit = 3
        self.bullets_allowed = 5
        self.beam_limit = 3
        self.speedup_scale = 100.00

    def _initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.bandaid = 2
        if self.speed == self.GAME_SPEEDS[0]:
            self.speed_mult = 0.80
            self.alien_points = 75
        elif self.speed == self.GAME_SPEEDS[1]:
            self.speed_mult = 1
            self.alien_points = 100
        elif self.speed == self.GAME_SPEEDS[2]:
            self.speed_mult = 1.2
            self.alien_points = 125
        elif self.speed == self.GAME_SPEEDS[3]:
            self.speed_mult = 1.5
            self.alien_points = 175
        elif self.speed == self.GAME_SPEEDS[4]:
            self.speed_mult = 2.5
            self.alien_points = 300
        self.ship_speed = 210 * self.speed_mult * self.bandaid
        self.alien_speed = 200.00 * self.speed_mult * self.bandaid
        self.bullet_speed = 200.00 * self.speed_mult * self.bandaid
        self.gunner_bullet_speed = 175 * self.speed_mult * self.bandaid
        self.mine_speed = 90 * self.speed_mult * self.bandaid
        self.gunner_speed = 50 * self.speed_mult * self.bandaid
        self.scroll_speed = -120.0
        self.background_x = 0
        self.difficulty_counter = 0
        self.respawn_timer = 0.0
        self.adjust_beams = False

    def increase_speed(self):
        """Increase speed and bonus point settings."""
        if self.speed == self.GAME_SPEEDS[0]:
            self.speed_add = 0.08
            self.score_scale = 4
        elif self.speed == self.GAME_SPEEDS[1]:
            self.speed_add = 0.1
            self.score_scale = 5
        elif self.speed == self.GAME_SPEEDS[2]:
            self.speed_add = 0.12
            self.score_scale = 6
        elif self.speed == self.GAME_SPEEDS[3]:
            self.speed_add = 0.15
            self.score_scale = 10
        elif self.speed == self.GAME_SPEEDS[4]:
            self.speed_add = 0.25
            self.score_scale = 20
        self.ship_speed += self.speedup_scale * self.speed_add
        self.bullet_speed += self.speedup_scale * self.speed_add
        self.gunner_bullet_speed += self.speedup_scale * self.speed_add / 3
        self.alien_speed += self.speedup_scale * self.speed_add
        self.mine_speed += self.speedup_scale * self.speed_add / 3
        self.alien_points += self.score_scale 
        self.scroll_speed += -20
