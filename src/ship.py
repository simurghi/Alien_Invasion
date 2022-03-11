import pygame 
from pygame.sprite import Sprite

class Ship(Sprite):
    """A class to manage the ship."""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        self.image = pygame.image.load('assets/images/ship.bmp')
        self.rect = self.image.get_rect()
        self.rect.midleft = self.screen_rect.midleft
        self.is_flipped = False
        self.y = float(self.rect.y) 
        self.x = float(self.rect.x) 
        self._create_movement_flags()

    def _create_movement_flags(self):
        """Creates the movement flags for the ship for smooth movement."""
        self.moving_up = False
        self.moving_down = False 
        self.moving_left = False
        self.moving_right = False 

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect) 

    def update(self):
        """Update the ship's position based on the movement flag."""
        if self.moving_up and self.rect.top > 60: 
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom - 60:
            self.y += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed 
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        self.rect.y = self.y 
        self.rect.x = self.x 

    def position_ship(self):
        """Position the ship on the midleft portion of the screen."""
        self.rect.midleft = self.screen_rect.midleft
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    def rotate_ship(self):
        """Flips the ship across the y-axis."""
        self.image = pygame.transform.flip(self.image, True, False)
        self.is_flipped = not self.is_flipped

    def reset_ship_flip(self):
        """Resets the orientation of the ship on each new game."""
        self.image = pygame.image.load('assets/images/ship.bmp')
        self.is_flipped = False
