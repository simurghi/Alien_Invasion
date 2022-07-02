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
        """Track the arrow with the ship's current position on the screen."""
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
        """Flips the arrow across the y-axis."""
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()

    def reset_arrow(self):
        """Resets the position of the arrow on game reset."""
        self.image = pygame.image.load('assets/images/dir_arrow_black_smol_2.bmp')
        self.rect.midleft = self.ship.rect.midright
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def blitme(self):
        """Draw the arrow at its current location."""
        if (
            self.settings.arrow_mode == self.settings.ARROW_SETTINGS[0]
            or self.settings.arrow_mode == self.settings.ARROW_SETTINGS[2]
        ):
            self.screen.blit(self.image, self.rect)


class WarningArrow(Sprite):
    """A class to manage the warning arrows."""

    def __init__(self, ai_game, mine):
        super().__init__()
        self.mine = mine
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        if mine.y < 50:
            self.image = pygame.image.load('assets/images/warning_arrow_top.bmp')
        elif mine.y > 590:
            self.image = pygame.image.load('assets/images/warning_arrow_bot.bmp')
        self.rect = self.image.get_rect()
        self.rect.x = mine.rect.x
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        if self.mine.y < 50:
            self.rect.y = self.screen_rect.top + 100
        elif self.mine.y > 590:
            self.rect.y = self.screen_rect.bottom - 100

    def blitme(self):
        """Draws the warning arrows at their current position."""
        if (
            self.settings.arrow_mode == self.settings.ARROW_SETTINGS[0]
            or self.settings.arrow_mode == self.settings.ARROW_SETTINGS[1]
        ) and (self.mine.y < 50 or self.mine.y > 590):
            self.screen.blit(self.image, self.rect)
