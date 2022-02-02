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
        self.is_colliding = False
        self.radius = 20

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load('images/alien_med.bmp')
        self.rect = self.image.get_rect()


        # Start each new alien alined to the right of the screen at a random height
        self.rect.x = 0 #ai_game.settings.screen_width + 50
        self.rect.y = 0 #ai_game.settings.screen_height

        # Store the alien's exact vertical position
        #self.y = float(self.rect.y)
        #self.x = float(self.rect.x)

    def update(self):
        """Move the alien to the left."""
        if not self.is_colliding:
            self.rect.x -= (self.settings.alien_speed)
            #self.rect.x = self.x


    def draw_hitbox(self):
        pygame.draw.circle(self.image, (0, 255, 0), self.rect.center, self.radius)
