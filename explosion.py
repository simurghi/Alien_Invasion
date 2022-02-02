import pygame 
from pygame.sprite import Sprite

class Explosion(Sprite):

    def __init__(self, center):
        """Initialize explosion coordinates."""
        super().__init__()
        self.explosion_images = []
        for num in range(1, 9):
            explosion = pygame.image.load(f"images/explosion_{num}.png").convert_alpha()
            self.explosion_images.append(explosion)
        self.index = 0
        self.image = self.explosion_images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.counter = 0

    def update(self):
        """Update method for explosions"""
        animation_speed = 8
        #update explosion animation
        self.counter += 1

        if self.counter >= animation_speed and self.index < len(self.explosion_images) - 1:
            self.counter = 0
            self.index+= 1
            self.image = self.explosion_images[self.index]

        # Reset animation index if it completes
        if self.index >= len(self.explosion_images) - 1 and self.counter >= animation_speed:
            self.kill()
