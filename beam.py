import pygame 
from pygame.sprite import Sprite 

class Beam(Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, ai_game):
        """Create a beam object at the ship's current position."""
        super().__init__()
        self.beam_images = []
        # Create a list of beam sprites to play in order whenever a super round is fired
        for num in range(1, 5):
            bolt = pygame.image.load(f"images/bolt{num}.png").convert_alpha()
            self.beam_images.append(bolt)
        self.screen = ai_game.screen
        self.settings = ai_game.settings 
        self.index = 0
        self.counter = 0
        self.image = self.beam_images[self.index]
        self.direction = 1
        self.rect = self.image.get_rect()
        self.rect.center = ai_game.ship.rect.center
               
        # Store the bullet's position as a decimal vlaue. 
        self.x = float(self.rect.x)

    def rotate_beam(self):
        """Flips the beam across the y-axis."""
        self.direction *= -1
        self.image = pygame.transform.flip(self.image, True, False)

    def draw_beam(self):
        """Draw the beam at the current position."""
        self.screen.blit(self.image, self.rect) 

    def update(self):
        """Update method for explosions"""
        # Update the decimal position of the beam. 
        self.x += self.settings.bullet_speed  * self.direction * 1.25
        # Update the rect position. 
        self.rect.x = self.x
        # Playback speed at which our explosions cycle through, lower is faster
        animation_speed = 4
        self.counter += 1

        if self.counter >= animation_speed and self.index < len(self.beam_images) - 1:
            self.counter = 0
            self.index+= 1
            self.image = self.beam_images[self.index]

        # Reset animation index if it completes
        if self.index >= len(self.beam_images) - 1 and self.counter >= animation_speed:
            self.index = 0
