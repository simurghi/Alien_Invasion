import pygame 
from pygame.sprite import Sprite 

class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, ai_game, ship, direction=1):
        """Create a bullet object a the ship's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings 
        self.direction = direction
        self.ai_game = ai_game
        self.image = pygame.image.load('assets/images/missile.bmp')
        self.rect = self.image.get_rect()
        self.rect.midright = ship.rect.midright
        self.x = float(self.rect.x)

    def update(self):
        """Move the bullet to the right of the screen."""
        self.x += self.settings.bullet_speed  * self.direction
        self.rect.x = self.x

    def rotate_bullet(self):
        """Flips the bullet across the y-axis."""
        self.direction *= -1
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        if self.direction > 0:
            self.rect.midright = self.ai_game.ship.rect.midright
        else:
            self.rect.midleft = self.ai_game.ship.rect.midleft
