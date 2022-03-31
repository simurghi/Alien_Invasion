import pygame

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
        self.BABY_SPEED = 1
        self.NORMAL_SPEED = 2
        self.TURBO_SPEED = 3

    def _set_window_properties(self):
        """Sets the properties for the game window and background."""
        self.screen_width = 960
        self.screen_height = 640
        self.bg_color = (0,0,0)

    def _initialize_user_preferences(self):
        """Sets default preferences for user options."""
        self.play_music = True
        self.play_sfx = True
        self.cinematic_bars = True
        self.speed = self.NORMAL_SPEED
        self.scaled_gfx = True 
        self.high_FPS = False
        self.FPS = 60.0

    def _initialize_static_settings(self):
        """Initialize settings that do not change throughout the game."""
        self.ship_limit = 3
        self.bullets_allowed = 5
        self.beam_limit = 3
        self.speedup_scale = 120.00

    def _initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.bandaid = 2
        if self.speed is self.BABY_SPEED:
            self.speed_mult = 0.75
            self.alien_points = 75
        elif self.speed is self.NORMAL_SPEED: 
            self.speed_mult = 1
            self.alien_points = 100
        elif self.speed is self.TURBO_SPEED:
            self.speed_mult = 1.5
            self.alien_points = 150
        self.ship_speed = 210 * self.speed_mult * self.bandaid
        self.alien_speed = 200.00 * self.speed_mult * self.bandaid
        self.bullet_speed = 200.00 * self.speed_mult * self.bandaid
        self.gunner_bullet_speed = 175 * self.speed_mult * self.bandaid
        self.mine_speed = 96 * self.speed_mult * self.bandaid
        self.gunner_speed = 50 * self.speed_mult * self.bandaid
        self.scroll_speed = -1.0
        self.background_x = 0
        self.difficulty_counter = 0
        self.adjust_beams = False

    def increase_speed(self):
        """Increase speed and bonus point settings."""
        if self.speed is self.BABY_SPEED:
            self.speed_add = 0.04
            self.score_scale = 2
        elif self.speed is self.NORMAL_SPEED:
            self.speed_add = 0.1
            self.score_scale = 5
        elif self.speed is self.TURBO_SPEED:
            self.speed_add = 0.2
            self.score_scale = 10
        self.ship_speed += self.speedup_scale * self.speed_add
        self.bullet_speed += self.speedup_scale * self.speed_add
        self.gunner_bullet_speed += self.speedup_scale * self.speed_add / 3
        self.alien_speed += self.speedup_scale * self.speed_add
        self.mine_speed += self.speedup_scale * self.speed_add / 3
        self.alien_points += self.score_scale 
        self.scroll_speed += -0.2

    def toggle_fps(self):
        """Toggles between high and low FPS based on settings."""
        if self.high_FPS:
            self.FPS = 120.0
        else:
            self.FPS = 60.0

