import pygame 
from pygame.sprite import Sprite 

class Beam(Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, ai_game, ship):
        """Create a beam object at the ship's current position."""
        super().__init__()
        self._load_assets()
        self.screen = ai_game.screen
        self.settings = ai_game.settings 
        self._initialize_dynamic_settings()
        self.image = self.beam_images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = ship.rect.center
        self.x = float(self.rect.x)

    def _load_assets(self):
        """Loads the necessary assets for beams to play."""
        self.beam_images = []
        for num in range(1, 5):
            bolt = pygame.image.load(f"assets/images/bolt{num}.png").convert_alpha()
            self.beam_images.append(bolt)

    def _initialize_dynamic_settings(self):
        """Initializes dynamic settings for the beam like its animations and direction."""
        self.index = 0
        self.counter = 0
        self.direction = 1

    def rotate_beam(self):
        """Flips the beam across the y-axis."""
        self.direction *= -1
        self.image = pygame.transform.flip(self.image, True, False)

    def update(self, dt):
        """Update method for explosions"""
        self.x += self.settings.bullet_speed  * self.direction * 1.25 * dt
        self.rect.x = self.x
        # Playback speed at which our explosions cycle through, lower is faster
        animation_speed = 4
        self.counter += 1
        if self.counter >= animation_speed and self.index < len(self.beam_images) - 1:
            self.counter = 0
            self.index+= 1
            self.image = self.beam_images[self.index]
        # Reset animation index if it completes
        if self.index >= len(self.beam_images) - 1 and self.counter >= animation_speed:
            self.index = 0
