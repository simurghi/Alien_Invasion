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
        self.radius = 17

    def update(self, dt):
        """Move the alien to the left."""
        self.x -= self.settings.alien_speed * dt
        self.rect.x = self.x

class ChonkyAlien(Alien): 
    """A class to represent the champion alien."""
    def __init__(self, ai_game):
        super().__init__(ai_game)
        self.image = pygame.image.load('assets/images/bigboi.bmp')
        self.rect = self.image.get_rect()
        self.radius = 17
        self.hitpoints = 4

    def update(self, dt):
        """Move the alien to the left."""
        self.x -= self.settings.alien_speed * dt
        self.rect.x = self.x
        pygame.draw.circle(self.image, (255,0,0), self.rect.center, self.radius)


