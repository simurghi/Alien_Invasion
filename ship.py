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
        self.is_flipped = False
        self.radius = 8

        # Load the ship image and get its rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at the center left of the screen. 
        self.rect.midleft = self.screen_rect.midleft
        # Store a decimal value for the ship's vertical position. 
        self.y = float(self.rect.y) 
        self.x = float(self.rect.x) 

        # Movement flags 
        self.moving_up = False
        self.moving_down = False 
        self.moving_left = False
        self.moving_right = False 


    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect) 

    def update(self):
        """Update the ship's position based on the movement flag."""
        # Update the ship's x and y values, not the rect.
        if self.moving_up and self.rect.top > 50: 
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
