import pygame
from pygame.sprite import Sprite
from math import sqrt
from random import randint


class Gunner(Sprite):
    """A class to represent an elite gunner enemy."""

    def __init__(self, ai_game):
        """Initialize the gunner and set its starting position."""
        super().__init__()

        self.image = pygame.image.load('assets/images/alien.bmp')
        self.rect = self.image.get_rect()
        self.screen = ai_game.screen
        self.ship = ai_game.ship
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.play_warning = False
        self.radius = 20
        self.audio_delay = 0
        self.hitpoints = 9
        self.fire_rate = 0
        self.rect.midright = self.screen_rect.midright

        self.y = float(self.rect.y)
        self.x = float(self.rect.x)


    def update(self):
        """Update method for mines"""
        self._move_gunner()
        self.fire_rate+=1
        # Playback speed at which our mines cycle through, lower is faster

    def _move_gunner(self):
        """Updates the position of the mines."""
        if self.y < self.ship.y:
            self.y = self.y + self.settings.gunner_speed
        if self.y > self.ship.y:
            self.y = self.y - self.settings.gunner_speed

        self.rect.y = self.y 

    def draw_gunner(self):
        """Draw the mine at the current position."""
        self.screen.blit(self.image, self.rect) 


