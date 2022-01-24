import pygame, random
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.random_y = random.randint(-4, 4)*5

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()


        # Start each new alien alined to the right of the screen at a random height
        self.rect.x = ai_game.settings.screen_width - 70
        self.rect.y = ai_game.settings.screen_height

        # Store the alien's exact vertical position
        self.y = float(self.rect.y)
