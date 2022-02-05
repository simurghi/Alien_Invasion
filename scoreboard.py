import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings for scoring information
        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font("fonts/m5x7.ttf", 48)

        # Prepare the initial score image
        self.prep_score()
        self.prep_high_score()
        self.prep_ships()

    def prep_score(self):
        """Turn the score into a rendered image. For non-cinematic mode."""
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True,
                self.text_color)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 0

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        self.high_score_image = self.font.render(str(self.stats.high_score),
            True, self.text_color)

        # Center the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def show_score(self):
        """Draw score and lives to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.ships.draw(self.screen)

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score: 
            self.stats.high_score = self.stats.score
            self.prep_high_score()
    
    def prep_ships(self):
        """Show how many lives the player has left."""
        self.ships = Group()
        for life in range (self.stats.ships_remaining):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + life * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score_game_over(self):
        """Draw score on the game over screen."""
        end_font = pygame.font.Font("fonts/m5x7.ttf", 64)
        max_score = str(self.stats.high_score)
        high_score_image_go = end_font.render(f"BEST: {max_score}", True, self.text_color)

        # Center the high score at the top of the screen
        high_score_rect_go = high_score_image_go.get_rect()
        high_score_rect_go.centerx = self.screen_rect.centerx
        high_score_rect_go.bottom = self.screen_rect.bottom - 100

        self.screen.blit(high_score_image_go, high_score_rect_go)

