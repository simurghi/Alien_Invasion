import pygame

class AspectRatio:
    """Displays black bars on the top/bottom of the screen."""

    def __init__(self,ai_game, y_offset = 0, x_offset = 0):
        """Initialize attributes of bar."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.width, self.height = 960, 50
        self.color = (0, 0, 0)

        self.rect = pygame.Rect(x_offset, 0 + y_offset, self.width, self.height)

    def draw_bar(self):
        """ Draw a blank black bar."""
        pygame.draw.rect(self.screen, self.color, self.rect)

