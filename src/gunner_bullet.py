import pygame
from pygame.sprite import Sprite


class GunnerBullet(Sprite):
    """A class to manage bullets fired from the gunner."""

    def __init__(self, ai_game, gunner):
        """Create a bullet object a the ship's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image = pygame.image.load('assets/images/thiccmissile.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = gunner.rect.center
        self.x = float(self.rect.x)

    def update(self, dt):
        """Move the bullet to the right of the screen and delete it if it goes offscreen."""
        self.x -= self.settings.gunner_bullet_speed * dt
        self.rect.x = self.x
        if self.x < -100:
            self.kill()

    def draw_bullet(self):
        """Draw the bullet at the current position."""
        self.screen.blit(self.image, self.rect)
        
    def draw_hitbox(self):
        pygame.draw.rect(self.screen, (255,0,0), self.rect)
