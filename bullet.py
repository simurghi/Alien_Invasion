import pygame 
from pygame.sprite import Sprite 

class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, ai_game):
        """Create a bullet object a the ship's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings 
        self.direction = ai_game.bullet_direction
        self.image = pygame.image.load('images/missile.bmp')
        self.rect = self.image.get_rect()
        self.rect.center = ai_game.ship.rect.center
        
        # Store the bullet's position as a decimal vlaue. 
        self.x = float(self.rect.x)


    def update(self):
        """Move the bullet to the right of the screen."""
        # Update the decimal position of the bullet. 
        self.x += self.settings.bullet_speed  * self.direction
        # Update the rect position. 
        self.rect.x = self.x


    def draw_bullet(self):
        """Draw the bullet at the current position."""
        self.screen.blit(self.image, self.rect) 


