import pygame
from pygame.sprite import Sprite

class Arrow(Sprite):
    """A class to manage the direction arrow."""
    def __init__(self, ai_game, ship):
        super().__init__()
        self.ship = ship
        self.screen = ai_game.screen
        self.settings = ai_game.settings 
        self.image = pygame.image.load('assets/images/dir_arrow_black_smol_2.bmp')
        self.rect = self.image.get_rect()
        self.rect.midleft = ship.rect.midright
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet to the right of the screen."""
        self.y = self.ship.y
        self.x = self.ship.x
        self.rect.y = self.y 
        self.rect.x = self.x 
        if self.ship.is_flipped:
            self.rect.right = self.ship.rect.left - 32
            self.rect.centery = self.ship.rect.centery
        else:
            self.rect.left = self.ship.rect.right + 32
            self.rect.centery = self.ship.rect.centery

    def flip_arrow(self):
        """Flips the bullet across the y-axis."""
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()

    def blitme(self):
        """Draw the ship at its current location."""
        if self.settings.show_arrow:
            self.screen.blit(self.image, self.rect) 

