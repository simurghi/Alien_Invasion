import pygame, random
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.random_y = random.randint(-5, 5)*5
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        self.image = pygame.image.load('assets/images/alien_med.bmp')
        self.rect = self.image.get_rect()
        self.x = float(self.rect.x) 
        self.y = float(self.rect.y)
        self.radius = 23

    def update(self):
        """Move the alien to the left."""
        self.x -= (self.settings.alien_speed)
        self.rect.x = self.x
