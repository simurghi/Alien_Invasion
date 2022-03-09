import pygame
from pygame.sprite import Sprite
from math import sqrt
from random import randint


class Mine(Sprite):
    """A class to represent an elite mine enemy."""

    def __init__(self, ai_game):
        """Initialize the mine and set its starting position."""
        super().__init__()
        # Load the mine images 
        self.mine_images = []
        for num in range(1, 5):
            drone = pygame.image.load(f"assets/images/mine{num}.png").convert_alpha()
            self.mine_images.append(drone)
        self.detect_sound = pygame.mixer.Sound('assets/audio/MineDetected.wav')

        self.screen = ai_game.screen
        self.ship = ai_game.ship
        self.random_pos = randint(1, 10)
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.play_warning = False
        self.radius = 20
        self.audio_delay = 0

        self.index = 0
        self.counter = 0
        self.image = self.mine_images[self.index]
        self.rect = self.image.get_rect()
        self.set_random_position()

        # Store the mine's exact position as a float
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    def update(self):
        """Update method for mines"""
        self._move_mine()
        # Playback speed at which our mines cycle through, lower is faster
        animation_speed = self.cqc_warning()
        self.counter += 1

        if self.counter >= animation_speed and self.index < len(self.mine_images) - 1:
            self.counter = 0
            self.index+= 1
            self.image = self.mine_images[self.index]

        # Reset animation index if it completes
        if self.index >= len(self.mine_images) - 1 and self.counter >= animation_speed:
            self.index = 0

    def _move_mine(self):
        """Updates the position of the mines."""
        if self.x < self.ship.x:
            self.x = self.x + self.settings.mine_speed
        if self.x > self.ship.x:
            self.x = self.x - self.settings.mine_speed
        if self.y < self.ship.y:
            self.y = self.y + self.settings.mine_speed
        if self.y > self.ship.y:
            self.y = self.y - self.settings.mine_speed

        self.rect.y = self.y 
        self.rect.x = self.x 

    def set_random_position(self):
        """Sets a random position on spawn."""
        if self.random_pos == 1:
            self.rect.topleft = self.screen_rect.topleft
        elif self.random_pos == 2:
            self.rect.bottomleft = self.screen_rect.bottomleft
        elif self.random_pos == 3:
            self.rect.midtop = self.screen_rect.midtop
        elif self.random_pos == 4:
            self.rect.midbottom = self.screen_rect.midtop
        elif self.random_pos == 5:
            self.rect.centerx = self.screen_rect.centerx / 2
            self.rect.y = self.screen_rect.top
        elif self.random_pos == 6:
            self.rect.centerx = self.screen_rect.centerx / 2
            self.rect.y = self.screen_rect.bottom
        elif self.random_pos == 7:
            self.rect.bottomright = self.screen_rect.bottomright
        elif self.random_pos == 8:
            self.rect.topright = self.screen_rect.topright
        elif self.random_pos == 9:
            self.rect.centerx = self.screen_rect.centerx * 3 / 2
            self.rect.y = self.screen_rect.top
        elif self.random_pos == 10:
            self.rect.centerx = self.screen_rect.centerx * 3 / 2
            self.rect.y = self.screen_rect.bottom




    def draw_mine(self):
        """Draw the mine at the current position."""
        self.screen.blit(self.image, self.rect) 

    def cqc_warning(self):
        """If a mine is close to the player ship, they will receive a warning."""
        formula_x = sqrt((self.ship.rect.centerx - self.rect.centerx)**2 + 
                (self.ship.rect.centerx - self.rect.centerx)**2)
        formula_y = sqrt((self.ship.rect.centery - self.rect.centery)**2 + 
                (self.ship.rect.centery - self.rect.centery)**2)
        if formula_x < 151 and formula_y < 151:
            if (self.settings.play_sfx and self.stats.state is self.stats.GAMEPLAY
                    and not self.play_warning and self.audio_delay % 120 == 0):
                self.detect_sound.play()
                self.audio_delay += 1
                self.play_warning = True
            return 8
        else: 
            self.play_warning = False
            return 16



