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
        self.EASY_SPEED = 2
        self.NORMAL_SPEED = 3
        self.TURBO_SPEED = 4
        self.LUDICROUS_SPEED = 5
        self.NATIVE_GFX = 1
        self.SCALED_GFX = 2
        self.FULLSCREEN_GFX = 3
        self.HUD_A = 1
        self.HUD_A_SMOLL = 2
        self.HUD_B = 3
        self.HUD_B_SMOLL = 4

    def _set_window_properties(self):
        """Sets the properties for the game window and background."""
        self.screen_width = 960
        self.screen_height = 640
        self.bg_color = (0,0,0)

    def _initialize_user_preferences(self):
        """Sets default preferences for user options."""
        self.music_volume = 1.0
        self.sound_volume = 1.0
        self.speed = self.NORMAL_SPEED
        self.gfx_mode = 1 
        self.FPS = 120.0
        self.show_score = True
        self.show_arrow = True
        self.HUD = self.HUD_A

    def _initialize_static_settings(self):
        """Initialize settings that do not change throughout the game."""
        self.ship_limit = 3
        self.bullets_allowed = 5
        self.beam_limit = 3
        self.speedup_scale = 120.00

    def _initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.bandaid = 2
        if self.speed is self.EASY_SPEED:
            self.speed_mult = 0.80
            self.alien_points = 75
        elif self.speed is self.NORMAL_SPEED: 
            self.speed_mult = 1
            self.alien_points = 100
        elif self.speed is self.TURBO_SPEED:
            self.speed_mult = 1.2
            self.alien_points = 125
        elif self.speed is self.LUDICROUS_SPEED:
            self.speed_mult = 2.5
            self.alien_points = 300
        self.ship_speed = 210 * self.speed_mult * self.bandaid
        self.alien_speed = 200.00 * self.speed_mult * self.bandaid
        self.bullet_speed = 200.00 * self.speed_mult * self.bandaid
        self.gunner_bullet_speed = 175 * self.speed_mult * self.bandaid
        self.mine_speed = 90 * self.speed_mult * self.bandaid
        self.gunner_speed = 50 * self.speed_mult * self.bandaid
        self.scroll_speed = -1.0
        self.background_x = 0
        self.difficulty_counter = 0
        self.respawn_timer = -0.5
        self.adjust_beams = False

    def increase_speed(self):
        """Increase speed and bonus point settings."""
        if self.speed is self.EASY_SPEED:
            self.speed_add = 0.08
            self.score_scale = 4
        elif self.speed is self.NORMAL_SPEED:
            self.speed_add = 0.1
            self.score_scale = 5
        elif self.speed is self.TURBO_SPEED:
            self.speed_add = 0.12
            self.score_scale = 6
        elif self.speed is self.LUDICROUS_SPEED:
            self.speed_add = 0.25
            self.score_scale = 15
        self.ship_speed += self.speedup_scale * self.speed_add
        self.bullet_speed += self.speedup_scale * self.speed_add
        self.gunner_bullet_speed += self.speedup_scale * self.speed_add / 3
        self.alien_speed += self.speedup_scale * self.speed_add
        self.mine_speed += self.speedup_scale * self.speed_add / 3
        self.alien_points += self.score_scale 
        self.scroll_speed += -0.2
