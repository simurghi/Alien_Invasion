import pygame
from pygame.sprite import Sprite
from math import sqrt
from random import randint
from gunner_bullet import GunnerBullet

class Gunner(Sprite):
    """A class to represent an elite gunner enemy."""

    def __init__(self, ai_game):
        """Initialize the gunner and set its starting position."""
        super().__init__()
        self._set_assets()
        self.rect = self.image.get_rect()
        self.screen_rect = ai_game.screen.get_rect()
        self._make_game_objects(ai_game)
        self._set_gunner_stats()
        self._set_initial_coordinates()

    def _set_assets(self):
        """Loads the audio and images for the gunner and sets their properties."""
        self.image = pygame.image.load('assets/images/alien.bmp')
        self.fire_sfx = pygame.mixer.Sound('assets/audio/SingleShot2.wav')
        self.fire_sfx.set_volume(0.40)

    def _make_game_objects(self, ai_game):
        """Makes the objects necessary for the gunner to function."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.ship = ai_game.ship
        self.settings = ai_game.settings
        self.gunner_bullets = pygame.sprite.Group()

    def _set_gunner_stats(self):
        """Sets the combat stats for the gunner."""
        self.hitpoints = 9
        self.fire_rate = 0

    def _set_initial_coordinates(self):
        """Sets the initial coordinates for gunners and their rects."""
        self.rect.x = self.screen_rect.right 
        self.rect.y = self.screen_rect.centery
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    def update(self):
        """Update method for mines"""
        self._move_gunner()
        self.fire_rate+=1
        self._fire_bullets()
        if self.gunner_bullets:
            self.gunner_bullets.update()

    def _fire_bullets(self):
        """Creates new bullets based on a cooldown"""
        if self.fire_rate % 120 == 0:
            new_gbullet = GunnerBullet(self.ai_game, self)
            self.gunner_bullets.add(new_gbullet)
            if (self.settings.play_sfx and 
                self.ai_game.stats.state is self.ai_game.stats.GAMEPLAY):
                    self.fire_sfx.play()

    def _move_gunner(self):
        """Updates the position of the mines."""
        if self.x > self.screen_rect.right - 175:
            self.x -= 2 * self.settings.gunner_speed
        if self.rect.centery < self.ship.rect.centery:
            self.y += self.settings.gunner_speed
        if self.rect.centery > self.ship.rect.centery:
            self.y -= self.settings.gunner_speed
        self.rect.y = self.y 
        self.rect.x = self.x
