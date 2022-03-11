import pygame 
from pygame.sprite import Sprite

class Explosion(Sprite):

    def __init__(self, center, size=1):
        """Initialize explosion coordinates."""
        super().__init__()
        self._load_assets()
        self.index = 0
        self.counter = 0
        self.image = self.explosion_images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = center

    def _load_assets(self, size):
        """Loads the necessary assets for explosions to play."""
        self.explosion_images = []
        for num in range(1, 9):
            if size == 1:
                explosion = pygame.image.load(f"assets/images/explosion_{num}.png").convert_alpha()
            elif size == 2:
                explosion = pygame.image.load(f"assets/images/explosion_mini_{num}.png").convert_alpha()
            elif size == 3:
                explosion = pygame.image.load(f"assets/images/explosion_big_{num}.png").convert_alpha()
            self.explosion_images.append(explosion)

    def update(self):
        """Update method for explosions"""
        # Playback speed at which our explosions cycle through, lower is faster
        animation_speed = 8
        self.counter += 1
        if self.counter >= animation_speed and self.index < len(self.explosion_images) - 1:
            self.counter = 0
            self.index+= 1
            self.image = self.explosion_images[self.index]
        # Reset animation index if it completes
        if self.index >= len(self.explosion_images) - 1 and self.counter >= animation_speed:
            self.kill()
