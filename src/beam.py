import pygame
from pygame.sprite import Sprite


class Beam(Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, ai_game, ship):
        """Create a beam object at the ship's current position."""
        super().__init__()
        self._load_assets()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self._initialize_dynamic_settings()
        self.image = self.beam_images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = ship.rect.center
        self.x = float(self.rect.x)
        self.direction = 1

    def _load_assets(self):
        """Load the necessary assets for beams to play."""
        self.beam_images = []
        self.rev_beam_images = []
        for num in range(1, 5):
            bolt = pygame.image.load(f"assets/images/bolt{num}.png").convert_alpha()
            self.beam_images.append(bolt)
        for num in range(1, 5):
            bolt = pygame.image.load(f"assets/images/bolt{num}.png").convert_alpha()
            bolt = pygame.transform.flip(bolt, True, False)
            self.rev_beam_images.append(bolt)

    def _initialize_dynamic_settings(self):
        """Initialize dynamic settings for the beam like its animations and direction."""
        self.index = 0
        self.counter = 0
        self.direction = 1

    def rotate_beam(self):
        """Flip the beam across the y-axis."""
        self.direction *= -1

    def update(self, dt):
        """Update method for beam's position and animation loop."""
        self.x += self.settings.bullet_speed * self.direction * 1.50 * dt
        self.rect.x = self.x
        animation_speed = 0.0375
        self.counter += 1 * dt
        if self.counter >= animation_speed and self.index < len(self.beam_images) - 1:
            self.counter = 0
            self.index += 1
            if self.direction > 0:
                self.image = self.beam_images[self.index]
            else:
                self.image = self.rev_beam_images[self.index]
        if self.index >= len(self.beam_images) - 1 and self.counter >= animation_speed:
            self.index = 0
